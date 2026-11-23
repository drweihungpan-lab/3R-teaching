#!/usr/bin/env python3
"""Build and check editable course slides. See materials/slides/README.md."""

import argparse
from dataclasses import dataclass, field
import os
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt


WIDTH, HEIGHT = 13.333333, 7.5
LEFT = 0.92
BODY_WIDTH = WIDTH - 2 * LEFT
TITLE_SIZE, BODY_SIZE, CODE_SIZE = 40, 22, 17
TITLE_TOP, TITLE_LINE = 0.82, 50
RULE_WIDTH, RULE_HEIGHT, RULE_GAP = 1.1, 0.05, 0.3
BODY_GAP, BODY_BOTTOM, SPACE_AFTER = 0.42, 6.62, 0.14
# The shallowest body region, used as the validator's bound: a one-line title.
BODY_TOP = TITLE_TOP + TITLE_LINE / 72 + RULE_GAP + RULE_HEIGHT + BODY_GAP
FOOTER_TOP, TRACK_TOP, TRACK_HEIGHT = 6.92, 7.33, 0.055
PROSE_LIMIT = 30
PAPER, INK, MUTED, ACCENT = "FBFBF9", "1B2733", "6E7F8D", "007F82"
CODE_FILL, TRACK = "EDF3F6", "E2E7EA"
CODE_EDGE = 0.045
INLINE = re.compile(r"`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|\*([^*]+)\*")


@dataclass(frozen=True)
class Span:
    text: str
    code: bool = False
    bold: bool = False
    italic: bool = False
    link: str | None = None


@dataclass
class Element:
    key: str
    spans: list[Span]
    code: bool = False
    bullet: bool = False

    @property
    def text(self):
        return "".join(span.text for span in self.spans)

    @property
    def size(self):
        return CODE_SIZE if self.code else BODY_SIZE

    @property
    def leading(self):
        """Body text is airy; code stays tight so a block reads as one unit."""
        return self.size * (1.32 if self.code else 1.5)


@dataclass
class Section:
    title: Element
    elements: list[Element]
    notes: list[str] = field(default_factory=list)

    @property
    def prose_words(self):
        """Words on the slide face. Titles, code and speaker notes are exempt."""
        return sum(len(element.text.split()) for element in self.elements
                   if not element.code)


def inline(text):
    """Convert Markdown inline syntax to editable runs, retaining link targets."""
    spans, start = [], 0
    for match in INLINE.finditer(text):
        if match.start() > start:
            spans.append(Span(text[start:match.start()]))
        code, label, target, bold, italic = match.groups()
        spans.append(Span(code or label or bold or italic or "", code=code is not None,
                          bold=bold is not None, italic=italic is not None, link=target))
        start = match.end()
    if start < len(text):
        spans.append(Span(text[start:]))
    return spans or [Span("")]


def parse_source(source):
    """Read the course slide dialect; do not treat --- inside a fence as a slide."""
    sections, current, fence, notes = [], None, None, False
    expect_title = True
    for number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        key = f"line-{number}"
        if fence is not None:
            if line.strip() == fence:
                fence, notes = None, False
            elif notes:
                current.notes.append(line)
            else:
                current.elements.append(Element(key, [Span(line, code=True)], code=True))
            continue
        if line.startswith("```"):
            if current is None or expect_title:
                raise ValueError(f"Line {number}: code before a slide title")
            fence, notes = "```", line[3:].strip() == "notes"
            if notes and current.notes:
                raise ValueError(f"Line {number}: a second notes block on one slide")
            continue
        if line.strip() == "---":
            if current is None or expect_title:
                raise ValueError(f"Line {number}: empty slide")
            expect_title = True
            continue
        if not line.strip():
            continue
        heading = re.fullmatch(r"(#{1,2}) (.+)", line)
        if expect_title:
            if not heading:
                raise ValueError(f"Line {number}: expected # or ## slide title")
            current = Section(Element(key, inline(heading[2])), [])
            sections.append(current)
            expect_title = False
        elif heading:
            raise ValueError(f"Line {number}: add --- before the next slide title")
        else:
            if re.match(r"\s*(?:[>#]|\||[-*+]\s*\[[ xX]\])", line):
                raise ValueError(f"Line {number}: unsupported block syntax; see slide README")
            bullet = line.startswith(("- ", "* ", "+ "))
            current.elements.append(Element(key, inline(line[2:] if bullet else line),
                                            bullet=bullet))
    if fence is not None:
        raise ValueError("Unclosed code fence")
    if not sections or expect_title:
        raise ValueError("Source is empty or ends with an empty slide")
    if any(not section.elements or not any(e.text.strip() for e in section.elements)
           for section in sections):
        raise ValueError("Every source slide needs a title and nonempty body")
    check_prose(sections)
    return sections


def check_prose(sections):
    """A slide face carries one idea; the narration belongs in a notes block."""
    for index, section in enumerate(sections, 1):
        words = section.prose_words
        if words >= PROSE_LIMIT:
            raise ValueError(
                f"Slide {index} ({section.title.text!r}) has {words} prose words; "
                f"the limit is {PROSE_LIMIT - 1}. Move narration into a ```notes block")


def link_address(target, source, output):
    parts = urlsplit(target)
    if parts.scheme or parts.netloc or target.startswith("#"):
        return target
    local = source.parent / unquote(parts.path)
    if not local.exists():
        raise ValueError(f"Missing source link: {target}")
    relative = Path(os.path.relpath(local.resolve(), output.parent.resolve())).as_posix()
    return relative + (f"#{parts.fragment}" if parts.fragment else "")


def character_width(char, size, code=False):
    """Conservative point estimates; these are layout guards, not font rendering."""
    if unicodedata.east_asian_width(char) in ("W", "F"):
        return size * 1.1
    if code:
        return size * 0.64
    if char in "MW@%mw":
        return size * 1.04
    if char in " il.,:;!|'`":
        return size * 0.36
    return size * (0.8 if char.isupper() else 0.65)


def wrapped_ranges(element, size, width):
    """Return exact source substrings; soft breaks never remove whitespace/tokens."""
    text = element.text
    if not text:
        return [(0, 0)]
    widths = [character_width(c, size, element.code or span.code)
              for span in element.spans for c in span.text]
    ranges, start = [], 0
    while start < len(text):
        end, used, last_space = start, 0, None
        while end < len(text) and used + widths[end] <= width:
            used += widths[end]
            if text[end].isspace():
                last_space = end + 1
            end += 1
        if end == start:
            raise ValueError("A character is wider than the available text area")
        if end < len(text) and last_space is not None and last_space > start:
            end = last_space
        ranges.append((start, end))
        start = end
    return ranges


def color(value):
    return RGBColor.from_string(value)


def title_ranges(section):
    lines = wrapped_ranges(section.title, TITLE_SIZE, (BODY_WIDTH * 72 - 14) * 0.94)
    if len(lines) > 2:
        raise ValueError(f"Title needs more than two lines: {section.title.text}")
    return lines


def body_top(title_lines):
    return TITLE_TOP + title_lines * TITLE_LINE / 72 + RULE_GAP + RULE_HEIGHT + BODY_GAP


def textbox(slide, name, x, y, width, height, size, fill=None):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(width), Inches(height))
    shape.name = name
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = color(fill)
    frame = shape.text_frame
    frame.clear()
    frame.auto_size = MSO_AUTO_SIZE.NONE
    frame.word_wrap = False  # All wrapping is explicit and included in the height budget.
    frame.vertical_anchor = MSO_ANCHOR.TOP
    frame.margin_left = frame.margin_right = Pt(7)
    frame.margin_top = frame.margin_bottom = Pt(3)
    paragraph = frame.paragraphs[0]
    paragraph.font.name = "Arial"
    paragraph.font.size = Pt(size)
    paragraph.font.color.rgb = color(INK)
    paragraph.line_spacing = Pt(size * 1.32)
    paragraph.space_before = paragraph.space_after = Pt(0)
    return shape, paragraph


def block(slide, name, x, y, width, height, fill):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                   Inches(width), Inches(height))
    shape.name = name
    shape.fill.solid()
    shape.fill.fore_color.rgb = color(fill)
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def add_runs(paragraph, element, ranges, size, source, output):
    for row, (start, end) in enumerate(ranges):
        if row:
            paragraph.add_line_break()  # Soft breaks can be removed to recover exact text.
        offset = 0
        for span in element.spans:
            left, right = max(start, offset), min(end, offset + len(span.text))
            if right > left:
                run = paragraph.add_run()
                run.text = span.text[left - offset:right - offset]
                run.font.name = "Courier New" if element.code or span.code else "Arial"
                run.font.size = Pt(size)
                run.font.bold = span.bold
                run.font.italic = span.italic
                run.font.color.rgb = color(ACCENT if span.link else INK)
                if span.link:
                    run.hyperlink.address = link_address(span.link, source, output)
            offset += len(span.text)


def add_page(prs, section, index, total, part, source, output):
    """One page of a source slide: title, accent rule, progress track, page number."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color(PAPER)
    lines = title_ranges(section)
    _, paragraph = textbox(slide, f"title:{section.title.key}", LEFT, TITLE_TOP,
                           BODY_WIDTH, len(lines) * TITLE_LINE / 72 + 0.12, TITLE_SIZE)
    paragraph.line_spacing = Pt(TITLE_LINE)
    add_runs(paragraph, section.title, lines, TITLE_SIZE, source, output)
    block(slide, "rule", LEFT, TITLE_TOP + len(lines) * TITLE_LINE / 72 + RULE_GAP,
          RULE_WIDTH, RULE_HEIGHT, ACCENT)
    block(slide, "track", 0, TRACK_TOP, WIDTH, TRACK_HEIGHT, TRACK)
    block(slide, "progress", 0, TRACK_TOP, WIDTH * index / total, TRACK_HEIGHT, ACCENT)
    _, footer = textbox(slide, "footer", LEFT, FOOTER_TOP, BODY_WIDTH, 0.26, 10)
    footer.text = ("CONTINUED   ·   " if part > 1 else "") + str(len(prs.slides))
    footer.font.color.rgb = color(MUTED)
    return slide


def paginate(section):
    """Split a source slide's body into pages that fit under the title."""
    top = body_top(len(title_ranges(section)))
    pages, page, y = [], [], top
    for element in section.elements:
        inset = 26 if element.bullet else 0
        rows = wrapped_ranges(element, element.size,
                              (BODY_WIDTH * 72 - 14 - inset) * 0.94)
        cursor = 0
        while cursor < len(rows):
            capacity = int(((BODY_BOTTOM - y) * 72 - 6) // element.leading)
            if capacity < 1:
                if not page:
                    raise ValueError(f"No room for body text under {section.title.text!r}")
                pages.append(page)
                page, y = [], top
                continue
            chunk = rows[cursor:cursor + capacity]
            height = (len(chunk) * element.leading + 6) / 72
            page.append((element, chunk, height))
            y += height + (0 if element.code else SPACE_AFTER)
            cursor += len(chunk)
    pages.append(page)
    return top, pages


def page_height(page):
    total = 0
    for position, (element, _, height) in enumerate(page):
        total += height
        if position < len(page) - 1 and not element.code:
            total += SPACE_AFTER
    return total


def build(sections, source, output):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(WIDTH), Inches(HEIGHT)
    prs.core_properties.title = sections[0].title.text
    prs.core_properties.subject = f"Editable slides generated from {source.name}"
    prs.core_properties.author = "Three-R course"
    prs.core_properties.keywords = "editable, Markdown, course"
    for index, section in enumerate(sections, 1):
        top, pages = paginate(section)
        for part, page in enumerate(pages, 1):
            slide = add_page(prs, section, index, len(sections), part, source, output)
            if part == 1 and section.notes:
                slide.notes_slide.notes_text_frame.text = "\n".join(section.notes)
            # Centre the block vertically so a sparse slide reads as composed.
            y = top + max(0.0, (BODY_BOTTOM - top - page_height(page)) / 2)
            for element, chunk, height in page:
                _, paragraph = textbox(slide, f"content:{element.key}:{chunk[0][0]}", LEFT, y,
                                       BODY_WIDTH, height, element.size,
                                       CODE_FILL if element.code else None)
                if element.code:
                    # Drawn after the box so the edge sits on top of the code fill.
                    block(slide, f"edge:{element.key}", LEFT, y, CODE_EDGE, height, ACCENT)
                if element.bullet:
                    properties = paragraph._p.get_or_add_pPr()
                    properties.set("marL", str(Pt(26)))
                    properties.set("indent", str(Pt(-20)))
                    bullet = OxmlElement("a:buChar")
                    bullet.set("char", "–" if chunk[0][0] == 0 else " ")
                    properties.append(bullet)
                paragraph.line_spacing = Pt(element.leading)
                add_runs(paragraph, element, chunk, element.size, source, output)
                y += height + (0 if element.code else SPACE_AFTER)
    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(output)


def validate(sections, source, output):
    """Check the saved artifact, including coverage/order, native text and slide bounds."""
    prs = Presentation(output)
    if abs(prs.slide_width / prs.slide_height - 16 / 9) > 0.0001:
        raise ValueError("Expected 16:9 slide dimensions")
    check_prose(sections)
    expected = [element for section in sections for element in section.elements]
    by_key = {element.key: element for element in expected}
    expected_titles = [section.title for section in sections]
    expected_notes = {section.title.key: "\n".join(section.notes)
                      for section in sections if section.notes}
    actual, order, titles, links, notes = {}, [], [], set(), {}
    body_shapes = 0
    for number, slide in enumerate(prs.slides, 1):
        has_body, title_count, title_key = False, 0, None
        previous_bottom = Inches(BODY_TOP)
        for shape in slide.shapes:
            if (shape.left < 0 or shape.top < 0 or shape.width <= 0 or shape.height <= 0
                    or shape.left + shape.width > prs.slide_width + 2
                    or shape.top + shape.height > prs.slide_height + 2):
                raise ValueError(f"Slide {number}: out-of-bounds shape {shape.name}")
            if shape.shape_type == 13:  # MSO_SHAPE_TYPE.PICTURE
                raise ValueError(f"Slide {number}: raster image found instead of editable content")
            if not shape.has_text_frame:
                continue
            text = shape.text.replace("\v", "")
            if shape.name.startswith("title:"):
                title_key = shape.name.split(":")[1]
                if not titles or titles[-1][0] != title_key:
                    titles.append((title_key, text))
                elif titles[-1][1] != text:
                    raise ValueError(f"Slide {number}: changed continuation title")
                title_count += 1
            if shape.name.startswith("content:"):
                key = shape.name.split(":")[1]
                if shape.top < previous_bottom - 2:
                    raise ValueError(f"Slide {number}: overlapping body shapes")
                if shape.top + shape.height > Inches(BODY_BOTTOM) + 2:
                    raise ValueError(f"Slide {number}: body exceeds content region")
                previous_bottom = shape.top + shape.height
                if not order or order[-1] != key:
                    order.append(key)
                actual[key] = actual.get(key, "") + text
                has_body = has_body or bool(text.strip())
                body_shapes += 1
                # Explicit row heights and width estimates guard against internal clipping.
                for paragraph in shape.text_frame.paragraphs:
                    if paragraph.font.size is None:
                        raise ValueError(f"Slide {number}: missing explicit body font size")
                    rows = paragraph.text.split("\v")
                    if len(rows) * by_key[key].leading + 6 > shape.height / 12700 + 0.01:
                        raise ValueError(f"Slide {number}: text height exceeds its box")
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    if run.hyperlink.address:
                        links.add(run.hyperlink.address)
        if not has_body or title_count != 1:
            raise ValueError(f"Slide {number}: empty/missing body or title")
        if title_key not in notes:
            notes[title_key] = (slide.notes_slide.notes_text_frame.text
                                if slide.has_notes_slide else None)
    if titles != [(element.key, element.text) for element in expected_titles]:
        raise ValueError("Source titles are missing, changed, or out of sequence")
    if order != [element.key for element in expected]:
        raise ValueError("Source body elements are missing, duplicated, or out of sequence")
    for element in expected:
        if actual.get(element.key) != element.text:
            raise ValueError(f"Source text mismatch at {element.key}")
    for key, text in expected_notes.items():
        if notes.get(key) != text:
            raise ValueError(f"Speaker notes missing or changed for title {key}")
    if {key for key, text in notes.items() if text} - set(expected_notes):
        raise ValueError("A deck slide carries speaker notes the source does not declare")
    expected_links = {link_address(span.link, source, output)
                      for section in sections for element in [section.title, *section.elements]
                      for span in element.spans if span.link}
    if links != expected_links:
        raise ValueError("Hyperlink targets differ from the source")
    with ZipFile(output) as archive:
        if archive.testzip():
            raise ValueError("Corrupt PPTX ZIP member")
        for name in archive.namelist():
            if name.endswith((".xml", ".rels")):
                etree.fromstring(archive.read(name))
        slide_parts = [name for name in archive.namelist()
                       if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)]
        if len(slide_parts) != len(prs.slides):
            raise ValueError("Missing or orphaned slide XML")
    widest = max(sections, key=lambda section: section.prose_words)
    return (f"PASS: {len(sections)} source slides -> {len(prs.slides)} editable slides; "
            f"{len(expected)} source elements, {body_shapes} text boxes, "
            f"{len(expected_notes)} notes pages, {len(links)} links; "
            f"wordiest face {widest.prose_words}/{PROSE_LIMIT - 1} words "
            f"({widest.title.text!r}). "
            "Exact text/order, notes text, shape bounds, body overlap/height budgets, "
            "XML/ZIP checked. No rendered inspection; font substitution and visual "
            "clipping need PowerPoint review.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Markdown slide source")
    parser.add_argument("--output", required=True, type=Path, help="PowerPoint destination")
    parser.add_argument("--check-only", action="store_true", help="Validate an existing deck without writing")
    args = parser.parse_args()
    try:
        if args.source.resolve() == args.output.resolve():
            raise ValueError("Source and output must be different files")
        if args.output.suffix.lower() != ".pptx":
            raise ValueError("Output must have a .pptx extension")
        sections = parse_source(args.source)
        if not args.check_only:
            build(sections, args.source, args.output)
        print(validate(sections, args.source, args.output))
    except (OSError, ValueError, etree.XMLSyntaxError) as error:
        parser.exit(1, f"Slide build/check failed: {error}\n")


if __name__ == "__main__":
    main()
