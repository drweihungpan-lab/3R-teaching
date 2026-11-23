# Editable PowerPoint slides

The `session-N.md` files are the content source. Their `session-N.pptx` companions
contain editable native PowerPoint text and shapes, including monospace workflow
diagrams and code. Make content changes in Markdown, then regenerate the deck.
Changes made only in PowerPoint are overwritten on regeneration.

A slide face carries one idea in at most 29 words. The narration belongs in the
slide's speaker notes, written as a fence tagged `notes` in the source, so present
from Presenter View or the notes pane.

The design is modern and premium: a dark navy background with electric cyan and purple
accents, contemporary typography, generous whitespace, and a clean visual hierarchy
inspired by leading technology companies.

## Regenerate from the repository root

Use Python 3.12 in an authoring environment (the backend is not required).
In a fresh checkout, the ignored `.venv/` directory is a convenient location;
if it already contains a backend environment, choose a separate path instead:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-slides.txt
python scripts/build_slides.py \
  --source materials/slides/session-2.md \
  --output materials/slides/session-2.pptx
```

The CLI takes explicit paths and can be reused for later decks by changing both
filenames. It creates output parent directories and checks the saved artifact.
To inspect an existing deck without regenerating it:

```bash
python scripts/build_slides.py \
  --source materials/slides/session-2.md \
  --output materials/slides/session-2.pptx --check-only
```

## Source format and layout

- Start with `# Session N: ...`; use `---` between slides and `## Title` thereafter.
- Use plain paragraphs, `-`/`*`/`+` bullets, fenced triple-backtick code blocks,
  inline backticks, bold/italic text, and `[label](target)` links. Each prose line
  is one paragraph; put blank lines inside code fences where they matter.
- A fence tagged `notes` becomes that slide's PowerPoint speaker notes instead of a
  code box: one per slide, anywhere in the slide, any length, blank lines retained.
  Notes are plain text, so write bare URLs rather than `[label](target)` in them.
- Every slide face is limited to 29 words. Paragraphs, bullets and link labels count;
  the title, code fences and speaker notes do not. The build fails and names the
  slide and its count, so move narration into a notes fence rather than trimming
  words to squeeze under the limit.
- Tables, block quotes, nested lists, checkboxes, images, HTML, and advanced
  Markdown are outside this small converter's dialect. Use editable text for
  simple diagrams. Do not add unsupported syntax expecting a rendered image.
- Markdown markers become text styling or native bullets. Link labels remain
  visible, with clickable targets. Local links are checked and rebased relative
  to the output file; distribute the repository with the deck to keep them usable.
- Slides use 16:9 dimensions, Segoe UI 54 pt titles (bold), Segoe UI 20 pt body text,
  and Courier New 15 pt code. These fonts are available on most systems; consider
  substituting Inter, Geist, or IBM Plex Sans if designing for a specific brand.
- Page furniture: dark navy background (0F172A), electric cyan (00D9FF) and purple (7C3AED)
  accents, near-white text (F5F5F5) with muted secondary text (A0A8B8). The title is bold
  with an accent line and decorative dot. Code blocks have a dark slate background (1E293B)
  with cyan text and a left edge. A progress bar runs across the bottom. The body block is
  centred vertically, so a sparse slide reads as composed rather than unfinished.
- Text wraps explicitly using conservative character-width estimates. Long tokens
  and code lines split across display lines; no characters, spaces, indentation,
  or source lines are discarded. Visual wraps use PowerPoint soft line breaks.
  Copy runnable commands from Markdown, since joining wrapped lines may be needed
  when copying from PowerPoint.
- Overflow creates continuation slides with the same title, marked `CONTINUED` beside
  the slide number. The 29-word limit makes this unlikely for prose, but a long code
  block can still continue onto the next slide; retain the full block in Markdown.
  Body order is unchanged. Titles longer than two lines fail instead of shrinking to
  unreadable text.

## Checks and presentation review

Every build, and `--check-only`, reopens the PPTX and checks:

- The 29-word limit on every slide face.
- Every parsed source title and body element, in order, with exact text after
  removing only inserted soft breaks. Code whitespace is retained.
- Speaker notes text, per slide, against the source's `notes` fences, and that no
  slide carries notes the source does not declare.
- Clickable link targets and local source-link existence.
- Nonempty slides with one title and a body; expected slide XML parts; well-formed
  XML/relationships and ZIP integrity; absence of raster pictures.
- All shapes stay inside the slide; body text boxes do not overlap, stay inside
  the content region, and have enough height for their explicit display lines.

These are structural checks, not a PowerPoint render. A shape inside the slide
can still clip text if a viewer substitutes a wider font. Open the deck in
PowerPoint before teaching and review long titles, wrapped code, continuation
boundaries, and links in presentation mode. Do not claim visual inspection from
the XML checks alone.
