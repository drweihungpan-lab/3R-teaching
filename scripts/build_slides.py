#!/usr/bin/env python3
"""Build and check editable course slides. See materials/slides/README.md."""

import argparse
from dataclasses import dataclass, field
import math
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
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt


# --- Geometry (inches, 16:9) -------------------------------------------------
WIDTH, HEIGHT = 13.333333, 7.5
LEFT = 0.7
BODY_WIDTH = WIDTH - 2 * LEFT
EYEBROW_TOP, EYEBROW_SIZE = 0.52, 10.5
TITLE_TOP, TITLE_SIZE, TITLE_LINE = 0.76, 30, 37
COVER_EYEBROW_TOP, COVER_TITLE_TOP, COVER_TITLE_SIZE, COVER_TITLE_LINE = 2.05, 2.36, 46, 54
BODY_GAP = 0.5
BODY_BOTTOM = 6.95
BLOCK_GAP, SPLIT_GAP = 0.2, 0.45
PROSE_LIMIT = 30

# --- Type -------------------------------------------------------------------
HEAD_FONT, BODY_FONT, MONO_FONT = "DM Sans", "DM Sans", "JetBrains Mono"
BODY_SIZE, CODE_SIZE, CALLOUT_SIZE, STEP_SIZE = 18, 14, 18, 16

# --- Palette: the Session 1 look ---------------------------------------------
TEAL = "0D9488"         # eyebrows, takeaways, solutions
TEAL_DARK = "0F766E"    # inline code and links on light slides
AMBER = "D97706"        # examples, warnings
RED = "DC2626"          # failure modes, critical rules
TERMINAL = "1E293B"     # code block fill
LIGHT = {"bg": "F8FAFC", "ink": "0F172A", "title": "0F172A", "muted": "64748B",
         "card": "FFFFFF", "border": "E2E8F0", "accent": TEAL_DARK, "code": TEAL_DARK}
DARK = {"bg": "0F172A", "ink": "E2E8F0", "title": "FFFFFF", "muted": "94A3B8",
        "card": "1E293B", "border": "334155", "accent": "5EEAD4", "code": "5EEAD4"}
THEME = dict(LIGHT)     # the palette of the slide being drawn
SYNTAX = {              # tints on the terminal fill
    None: "E2E8F0", "command": "7DD3FC", "flag": "93C5FD", "string": "FCD34D",
    "comment": "94A3B8", "error": "FCA5A5", "arrow": "5EEAD4",
}
# GitHub alert keyword -> (accent colour, tag text). TIP is bare teal text, no card.
CALLOUTS = {
    "TIP": (TEAL, ""),
    "NOTE": (TEAL, "NOTE:"),
    "IMPORTANT": (TEAL, "IMPORTANT:"),
    "WARNING": (AMBER, "WATCH OUT:"),
    "CAUTION": (RED, "CRITICAL RULE:"),
}
# Eyebrow colour by keyword, first match wins; teal otherwise.
EYEBROW_TONES = [
    (RED, ("FAILURE", "PITFALL", "SECURITY", "RULE", "NEVER")),
    (AMBER, ("STAGE", "EXAMPLE", "EXPERIMENT", "HANDS-ON", "OPTIONAL", "ACCOUNTABILITY",
             "GRADING", "WHY WE BUILT")),
]

# --- Component geometry -----------------------------------------------------
CODE_PAD, CODE_INSET = 0.22, 0.28
CARD_PAD, CARD_TAG = 0.2, 0.3
STEP_GAP, STEP_ROW_GAP = 0.25, 0.25

INLINE = re.compile(r"`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|\*([^*]+)\*")
SHELL = {"bash", "sh", "shell", "console", "zsh"}


@dataclass(frozen=True)
class Span:
    text: str
    code: bool = False
    bold: bool = False
    italic: bool = False
    link: str | None = None
    tint: str | None = None


@dataclass
class Element:
    key: str
    spans: list[Span]
    kind: str = "para"          # para | bullet | code | callout | step
    lang: str = ""              # code fences
    tone: str = ""              # callouts
    number: str = ""            # steps

    @property
    def code(self):
        return self.kind == "code"

    @property
    def bullet(self):
        return self.kind == "bullet"

    @property
    def text(self):
        return "".join(span.text for span in self.spans)

    @property
    def size(self):
        return {"code": CODE_SIZE, "callout": CALLOUT_SIZE, "step": STEP_SIZE}.get(
            self.kind, BODY_SIZE)

    @property
    def leading(self):
        """Body text is airy; code stays tight so a block reads as one unit."""
        return self.size * (1.32 if self.code else 1.45)

    @property
    def pad(self):
        """Vertical points a text box needs beyond its rows."""
        return 2 if self.code else 6


@dataclass
class Section:
    eyebrow: str
    title: Element
    elements: list[Element]
    cover: bool = False
    notes: list[str] = field(default_factory=list)

    @property
    def prose_words(self):
        """Words on the slide face. Eyebrow, title, code and notes are exempt."""
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


def highlight(line, lang):
    """Light syntax tints for terminal blocks. Text is unchanged, only coloured."""
    if lang in SHELL:
        body, comment = line, ""
        match = re.search(r"(^|\s)#", line)
        if match:
            cut = match.start() + len(match.group(1))
            body, comment = line[:cut], line[cut:]
        spans, first = [], True
        for token in re.finditer(r"\s+|'[^']*'|\"[^\"]*\"|\S+", body):
            word = token.group()
            if word.isspace():
                tint = None
            elif first:
                tint, first = "command", False
            elif word[0] in "'\"":
                tint = "string"
            elif word.startswith("-"):
                tint = "flag"
            else:
                tint = None
            spans.append(Span(word, code=True, tint=tint))
        if comment:
            spans.append(Span(comment, code=True, tint="comment"))
        return spans or [Span("", code=True)]
    spans, start = [], 0
    for match in re.finditer(r"\b\w*Error\b|→", line):
        if match.start() > start:
            spans.append(Span(line[start:match.start()], code=True))
        spans.append(Span(match.group(), code=True,
                          tint="error" if match.group().endswith("Error") else "arrow"))
        start = match.end()
    if start < len(line):
        spans.append(Span(line[start:], code=True))
    return spans or [Span("", code=True)]


def parse_source(source):
    """Read the course slide dialect; do not treat --- inside a fence as a slide."""
    sections, current, fence, notes, lang = [], None, None, False, ""
    expect_title, eyebrow = True, None
    for number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        key = f"line-{number}"
        if fence is not None:
            if line.strip() == fence:
                fence, notes = None, False
            elif notes:
                current.notes.append(line)
            else:
                current.elements.append(Element(key, highlight(line, lang), kind="code",
                                                lang=lang))
            continue
        if line.startswith("```"):
            if current is None or expect_title:
                raise ValueError(f"Line {number}: code before a slide title")
            lang = line[3:].strip()
            fence, notes = "```", lang == "notes"
            if notes and current.notes:
                raise ValueError(f"Line {number}: a second notes block on one slide")
            continue
        if line.strip() == "---":
            if current is None or expect_title:
                raise ValueError(f"Line {number}: empty slide")
            expect_title, eyebrow = True, None
            continue
        if not line.strip():
            continue
        if expect_title:
            label = re.fullmatch(r"### (.+)", line)
            if label:
                if eyebrow is not None:
                    raise ValueError(f"Line {number}: a second ### eyebrow on one slide")
                eyebrow = label[1].strip()
                continue
            heading = re.fullmatch(r"(#{1,2}) (.+)", line)
            if not heading:
                raise ValueError(f"Line {number}: expected ### eyebrow, then # or ## title")
            if eyebrow is None:
                raise ValueError(f"Line {number}: add a ### EYEBROW line above the title")
            current = Section(eyebrow, Element(key, inline(heading[2])), [],
                              cover=heading[1] == "#")
            sections.append(current)
            expect_title = False
            continue
        if re.fullmatch(r"#{1,3} .+", line):
            raise ValueError(f"Line {number}: add --- before the next slide title")
        callout = re.fullmatch(r"> \[!(\w+)\] (.+)", line)
        if callout:
            if callout[1] not in CALLOUTS:
                raise ValueError(f"Line {number}: unknown callout [!{callout[1]}]; "
                                 f"use one of {', '.join(CALLOUTS)}")
            current.elements.append(Element(key, inline(callout[2]), kind="callout",
                                            tone=callout[1]))
            continue
        step = re.fullmatch(r"(\d+)\. (.+)", line)
        if step:
            current.elements.append(Element(key, inline(step[2]), kind="step",
                                            number=step[1]))
            continue
        if re.match(r"\s*(?:[>#]|\||[-*+]\s*\[[ xX]\])", line):
            raise ValueError(f"Line {number}: unsupported block syntax; see slide README")
        bullet = line.startswith(("- ", "* ", "+ "))
        current.elements.append(Element(key, inline(line[2:] if bullet else line),
                                        kind="bullet" if bullet else "para"))
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
        return size * 0.92
    if char in " il.,:;!|'`":
        return size * 0.3
    return size * (0.72 if char.isupper() else 0.58)


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


def text_width(inches, inset=0):
    """Usable points inside a text box of this width, with a safety margin."""
    return (inches * 72 - 16 - inset) * 0.97


def color(value):
    return RGBColor.from_string(value)


def title_metrics(section):
    if section.cover:
        return COVER_EYEBROW_TOP, COVER_TITLE_TOP, COVER_TITLE_SIZE, COVER_TITLE_LINE
    return EYEBROW_TOP, TITLE_TOP, TITLE_SIZE, TITLE_LINE


def title_ranges(section):
    _, _, size, _ = title_metrics(section)
    lines = wrapped_ranges(section.title, size, text_width(BODY_WIDTH * 0.8))
    if len(lines) > 2:
        raise ValueError(f"Title needs more than two lines: {section.title.text}")
    return lines


def body_top(section, lines):
    _, top, _, line = title_metrics(section)
    return top + lines * line / 72 + 0.1 + (0.3 if section.cover else BODY_GAP)


# The shallowest body region, used as the validator's bound: a one-line title.
BODY_TOP = TITLE_TOP + TITLE_LINE / 72 + 0.1 + BODY_GAP


def eyebrow_color(section, dark):
    if dark:
        return AMBER
    text = section.eyebrow.upper()
    for tone, words in EYEBROW_TONES:
        if any(word in text for word in words):
            return tone
    return TEAL


def textbox(slide, name, x, y, width, height, size, text_color=None, font=BODY_FONT,
            margin_y=4):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(width), Inches(height))
    shape.name = name
    shape.fill.background()
    frame = shape.text_frame
    frame.clear()
    frame.auto_size = MSO_AUTO_SIZE.NONE
    frame.word_wrap = False  # All wrapping is explicit and included in the height budget.
    frame.vertical_anchor = MSO_ANCHOR.TOP
    frame.margin_left = frame.margin_right = Pt(8)
    frame.margin_top = frame.margin_bottom = Pt(margin_y)
    paragraph = frame.paragraphs[0]
    paragraph.font.name = font
    paragraph.font.size = Pt(size)
    paragraph.font.color.rgb = color(text_color or THEME["ink"])
    paragraph.line_spacing = Pt(size * 1.32)
    paragraph.space_before = paragraph.space_after = Pt(0)
    return shape, paragraph


def label(slide, name, x, y, width, text, size, text_color, bold=False, spacing=60,
          font=MONO_FONT, align=None):
    """A single-line furniture label (eyebrow, tag, number). Tracking in 1/100 pt."""
    _, paragraph = textbox(slide, name, x, y, width, size * 1.6 / 72, size, text_color,
                           font, margin_y=0)
    if align:
        paragraph.alignment = align
    run = paragraph.add_run()
    run.text = text
    run.font.name, run.font.size, run.font.bold = font, Pt(size), bold
    run.font.color.rgb = color(text_color)
    run.font._rPr.set("spc", str(spacing))
    return paragraph


def block(slide, name, x, y, width, height, fill, shape=MSO_SHAPE.RECTANGLE,
          line=None, radius=None):
    item = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(width), Inches(height))
    item.name = name
    item.fill.solid()
    item.fill.fore_color.rgb = color(fill)
    if line:
        item.line.color.rgb = color(line)
        item.line.width = Pt(0.75)
    else:
        item.line.fill.background()
    if radius is not None:
        item.adjustments[0] = radius
    item.shadow.inherit = False
    style = item._element.find("{http://schemas.openxmlformats.org/presentationml/2006/main}style")
    if style is not None:  # Drop theme effects (shadows) so the canvas stays flat.
        item._element.remove(style)
    return item


def run_color(element, span):
    if element.code:
        return SYNTAX[span.tint]
    if element.kind == "callout" and element.tone == "TIP":
        return THEME["accent"]
    if span.link or span.code:
        return THEME["code"]
    if element.kind == "callout" and span.bold:
        return CALLOUTS[element.tone][0]
    return THEME["ink"]


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
                run.font.name = MONO_FONT if element.code or span.code else BODY_FONT
                run.font.size = Pt(size)
                run.font.bold = (span.bold or (element.code and span.tint == "command")
                                 or (element.kind == "callout" and element.tone == "TIP"))
                run.font.italic = span.italic or span.tint == "comment"
                run.font.color.rgb = color(run_color(element, span))
                if span.link:
                    run.font.underline = True
                    run.hyperlink.address = link_address(span.link, source, output)
            offset += len(span.text)


def add_page(prs, section, dark, source, output):
    """One page of a source slide: background, mono eyebrow and title. No footer."""
    THEME.clear()
    THEME.update(DARK if dark else LIGHT)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color(THEME["bg"])
    eyebrow_top, title_top, size, line = title_metrics(section)
    label(slide, f"eyebrow:{section.title.key}", LEFT - 0.11, eyebrow_top, BODY_WIDTH,
          section.eyebrow.upper(), EYEBROW_SIZE, eyebrow_color(section, dark))
    lines = title_ranges(section)
    _, paragraph = textbox(slide, f"title:{section.title.key}", LEFT - 0.11, title_top,
                           BODY_WIDTH, len(lines) * line / 72 + 0.1, size, THEME["title"],
                           HEAD_FONT, margin_y=0)
    paragraph.line_spacing = Pt(line)
    paragraph.font.bold = True
    add_runs(paragraph, section.title, lines, size, source, output)
    for run in paragraph.runs:  # Code spans keep the mono face, as on Session 1.
        run.font.bold = run.font.name != MONO_FONT
        run.font.color.rgb = color(THEME["title"])
        run.font._rPr.set("spc", "-20")
    return slide


# --- Blocks: what a slide body is made of -----------------------------------

def group_blocks(elements):
    """Consecutive code lines form one terminal; consecutive steps form one row."""
    blocks = []
    for element in elements:
        kind = element.kind if element.kind in ("code", "step") else None
        if kind and blocks and blocks[-1][0] == kind and blocks[-1][1][-1].lang == element.lang:
            blocks[-1][1].append(element)
        else:
            blocks.append((element.kind, [element]))
    return blocks


def step_layout(items, width):
    count = len(items)
    columns = count if count <= 4 else math.ceil(count / 2)
    rows = math.ceil(count / columns)
    card_width = (width - (columns - 1) * STEP_GAP) / columns
    inner = card_width - 2 * CARD_PAD + 0.16
    wraps = [wrapped_ranges(item, item.size, text_width(inner)) for item in items]
    text_height = max((len(r) * items[0].leading + items[0].pad) / 72 for r in wraps)
    card = CARD_PAD + CARD_TAG + text_height + CARD_PAD
    return columns, card_width, wraps, card, rows * card + (rows - 1) * STEP_ROW_GAP


def code_lines(items, width):
    inner = text_width(width - 2 * CODE_INSET + 0.16)
    return [(item, wrapped_ranges(item, item.size, inner),
             None) for item in items]


def measure(kind, items, width):
    """Return (height, payload) of a block drawn at this width."""
    element = items[0]
    if kind == "code":
        chunk = []
        for item, rows, _ in code_lines(items, width):
            chunk.append((item, rows, (len(rows) * item.leading + item.pad) / 72))
        return 2 * CODE_PAD + sum(h for _, _, h in chunk), chunk
    if kind in ("para", "bullet"):
        rows = wrapped_ranges(element, element.size,
                              text_width(width, 26 if element.bullet else 0))
        return (len(rows) * element.leading + element.pad) / 72, rows
    if kind == "callout":
        if element.tone == "TIP":
            rows = wrapped_ranges(element, element.size, text_width(width))
            return (len(rows) * element.leading + element.pad) / 72, rows
        rows = wrapped_ranges(element, element.size, text_width(width - 2 * CARD_PAD + 0.16))
        text = (len(rows) * element.leading + element.pad) / 72
        return CARD_PAD + CARD_TAG + text + CARD_PAD, rows
    if kind == "step":
        layout = step_layout(items, width)
        return layout[-1], layout
    raise AssertionError(kind)


def column_height(column):
    return sum(h for _, _, _, h in column) + BLOCK_GAP * max(0, len(column) - 1)


def try_split(blocks, top):
    """Code on the left, its explanation on the right, when the code fits unwrapped."""
    codes = [i for i, (kind, _) in enumerate(blocks) if kind == "code"]
    if len(codes) != 1 or codes[0] == len(blocks) - 1:
        return None
    width = (BODY_WIDTH - SPLIT_GAP) / 2
    columns = []
    for part in (blocks[:codes[0] + 1], blocks[codes[0] + 1:]):
        column = []
        for kind, items in part:
            if kind == "step":
                return None
            height, payload = measure(kind, items, width)
            if kind == "code" and any(len(rows) > 1 for _, rows, _ in payload):
                return None
            column.append((kind, items, payload, height))
        if column_height(column) > BODY_BOTTOM - top:
            return None
        columns.append(column)
    return columns


def paginate(section):
    """Pages of columns: [[full-width column]] or [[left], [right]] per page."""
    top = body_top(section, len(title_ranges(section)))
    blocks = group_blocks(section.elements)
    split = try_split(blocks, top)
    if split:
        return top, [split]
    pages, page, y = [], [], top

    def room():
        return BODY_BOTTOM - y - (BLOCK_GAP if page else 0)

    for kind, items in blocks:
        if kind == "code":
            _, lines = measure(kind, items, BODY_WIDTH)
            cursor = 0
            while cursor < len(lines):
                available, chunk, used = room() - 2 * CODE_PAD, [], 0.0
                for line in lines[cursor:]:
                    if used + line[2] > available:
                        break
                    chunk.append(line)
                    used += line[2]
                if not chunk:
                    if not page:
                        raise ValueError(f"No room for code under {section.title.text!r}")
                    pages.append(page)
                    page, y = [], top
                    continue
                height = 2 * CODE_PAD + used
                y += height + (BLOCK_GAP if page else 0)
                page.append(("code", [line[0] for line in chunk], chunk, height))
                cursor += len(chunk)
            continue
        height, payload = measure(kind, items, BODY_WIDTH)
        if height > room():
            if not page:
                raise ValueError(f"No room for body under {section.title.text!r}")
            pages.append(page)
            page, y = [], top
        y += height + (BLOCK_GAP if page else 0)
        page.append((kind, items, payload, height))
    pages.append(page)
    return top, [[page] for page in pages]


def body_text(slide, element, rows, x, y, width, source, output, inset=0):
    height = (len(rows) * element.leading + element.pad) / 72
    _, paragraph = textbox(slide, f"content:{element.key}:{rows[0][0]}", x, y, width,
                           height, element.size, font=MONO_FONT if element.code else BODY_FONT,
                           margin_y=0 if element.code else 4)
    if inset:
        properties = paragraph._p.get_or_add_pPr()
        properties.set("marL", str(Pt(inset)))
        properties.set("indent", str(Pt(-20)))
        marker = OxmlElement("a:buClr")
        marker_color = OxmlElement("a:srgbClr")
        marker_color.set("val", TEAL)
        marker.append(marker_color)
        properties.append(marker)
        bullet = OxmlElement("a:buChar")
        bullet.set("char", "–")
        properties.append(bullet)
    paragraph.line_spacing = Pt(element.leading)
    add_runs(paragraph, element, rows, element.size, source, output)
    return height


def card(slide, name, x, y, width, height):
    return block(slide, name, x, y, width, height, THEME["card"], MSO_SHAPE.ROUNDED_RECTANGLE,
                 line=THEME["border"], radius=0.05)


def draw(slide, kind, items, payload, x, y, width, height, source, output):
    if kind == "code":
        block(slide, f"terminal:{items[0].key}", x, y, width, height, TERMINAL,
              MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
        line_y = y + CODE_PAD
        for element, rows, line_height in payload:
            body_text(slide, element, rows, x + CODE_INSET - 0.08, line_y,
                      width - 2 * CODE_INSET + 0.16, source, output)
            line_y += line_height
    elif kind == "callout" and items[0].tone != "TIP":
        element = items[0]
        tone, tag = CALLOUTS[element.tone]
        card(slide, f"callout:{element.key}", x, y, width, height)
        label(slide, f"callout-tag:{element.key}", x + CARD_PAD - 0.08, y + CARD_PAD,
              width - 2 * CARD_PAD, tag, 10, tone)
        body_text(slide, element, payload, x + CARD_PAD - 0.08, y + CARD_PAD + CARD_TAG,
                  width - 2 * CARD_PAD + 0.16, source, output)
    elif kind == "step":
        columns, card_width, wraps, card_height, _ = payload
        for position, (item, rows) in enumerate(zip(items, wraps)):
            row, column = divmod(position, columns)
            cx = x + column * (card_width + STEP_GAP)
            cy = y + row * (card_height + STEP_ROW_GAP)
            card(slide, f"card:{item.key}", cx, cy, card_width, card_height)
            label(slide, f"step-number:{item.key}", cx + CARD_PAD - 0.08, cy + CARD_PAD,
                  card_width - 2 * CARD_PAD, item.number.zfill(2), 10.5, TEAL, bold=True)
            body_text(slide, item, rows, cx + CARD_PAD - 0.08, cy + CARD_PAD + CARD_TAG,
                      card_width - 2 * CARD_PAD + 0.16, source, output)
    else:
        body_text(slide, items[0], payload, x - 0.11, y, width + 0.11, source, output,
                  inset=26 if kind == "bullet" else 0)


def recolor_links(prs):
    """Viewers paint hyperlinks with the theme colour, so set it to the palette."""
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    theme = prs.slide_masters[0].part.part_related_by(RT.THEME)
    for name in ("hlink", "folHlink"):
        theme._blob = re.sub(
            rf"(<a:{name}>\s*<a:srgbClr val=\")[0-9A-Fa-f]{{6}}".encode(),
            rf"\g<1>{TEAL_DARK}".encode(), theme.blob)


def build(sections, source, output):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(WIDTH), Inches(HEIGHT)
    prs.core_properties.title = sections[0].title.text
    prs.core_properties.subject = f"Editable slides generated from {source.name}"
    prs.core_properties.author = "Three-R course"
    prs.core_properties.keywords = "editable, Markdown, course"
    for index, section in enumerate(sections, 1):
        # The cover and the closing slide are dark, as on Session 1.
        dark = section.cover or index == len(sections)
        top, pages = paginate(section)
        for part, columns in enumerate(pages, 1):
            slide = add_page(prs, section, dark, source, output)
            if part == 1 and section.notes:
                slide.notes_slide.notes_text_frame.text = "\n".join(section.notes)
            width = BODY_WIDTH if len(columns) == 1 else (BODY_WIDTH - SPLIT_GAP) / 2
            bottom = top
            for number, column in enumerate(columns):
                x = LEFT + number * (width + SPLIT_GAP)
                # Centre each column vertically; the cover reads top-down instead.
                y = top if section.cover else top + max(
                    0.0, (BODY_BOTTOM - top - column_height(column)) / 2)
                for kind, items, payload, height in column:
                    draw(slide, kind, items, payload, x, y, width, height, source, output)
                    y += height + BLOCK_GAP
                bottom = max(bottom, y)
            if section.cover:
                block(slide, "cover-rule", LEFT, bottom + 0.15, 0.55, 0.035, TEAL)
    recolor_links(prs)
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
    expected_eyebrows = {section.title.key: section.eyebrow.upper() for section in sections}
    expected_notes = {section.title.key: "\n".join(section.notes)
                      for section in sections if section.notes}
    actual, order, titles, links, notes = {}, [], [], set(), {}
    body_shapes = 0
    for number, slide in enumerate(prs.slides, 1):
        has_body, title_count, title_key, eyebrow = False, 0, None, None
        boxes = []
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
            if shape.name.startswith("eyebrow:"):
                eyebrow = (shape.name.split(":")[1], text)
            if shape.name.startswith("title:"):
                title_key = shape.name.split(":")[1]
                if not titles or titles[-1][0] != title_key:
                    titles.append((title_key, text))
                elif titles[-1][1] != text:
                    raise ValueError(f"Slide {number}: changed continuation title")
                title_count += 1
            if shape.name.startswith("content:"):
                key = shape.name.split(":")[1]
                if shape.top < Inches(BODY_TOP) - 2:
                    raise ValueError(f"Slide {number}: body starts above the content region")
                if shape.top + shape.height > Inches(BODY_BOTTOM) + 2:
                    raise ValueError(f"Slide {number}: body exceeds content region")
                box = (shape.left, shape.top, shape.left + shape.width, shape.top + shape.height)
                for other in boxes:
                    if (box[0] < other[2] - 2 and other[0] < box[2] - 2
                            and box[1] < other[3] - 2 and other[1] < box[3] - 2):
                        raise ValueError(f"Slide {number}: overlapping body shapes")
                boxes.append(box)
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
                    element = by_key[key]
                    if len(rows) * element.leading + element.pad > shape.height / 12700 + 0.01:
                        raise ValueError(f"Slide {number}: text height exceeds its box")
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    if run.hyperlink.address:
                        links.add(run.hyperlink.address)
        if not has_body or title_count != 1:
            raise ValueError(f"Slide {number}: empty/missing body or title")
        if eyebrow != (title_key, expected_eyebrows.get(title_key)):
            raise ValueError(f"Slide {number}: eyebrow missing or changed")
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
            "Exact text/order, eyebrows, notes text, shape bounds, body overlap/height "
            "budgets, XML/ZIP checked. No rendered inspection; font substitution and "
            "visual clipping need a render review.")


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
