# Editable PowerPoint slides

The `session-N.md` files are the content source. Their `session-N.pptx` companions
contain editable native PowerPoint text and shapes, including monospace workflow
diagrams and code. Make content changes in Markdown, then regenerate the deck.
Changes made only in PowerPoint are overwritten on regeneration.

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
- Tables, block quotes, nested lists, checkboxes, images, HTML, and advanced
  Markdown are outside this small converter's dialect. Use editable text for
  simple diagrams. Do not add unsupported syntax expecting a rendered image.
- Markdown markers become text styling or native bullets. Link labels remain
  visible, with clickable targets. Local links are checked and rebased relative
  to the output file; distribute the repository with the deck to keep them usable.
- Slides use 16:9 dimensions, Arial 32 pt titles, Arial 21 pt body text, and
  Courier New 18 pt code. Install those fonts for consistent presentation.
- Text wraps explicitly using conservative character-width estimates. Long tokens
  and code lines split across display lines; no characters, spaces, indentation,
  or source lines are discarded. Visual wraps use PowerPoint soft line breaks.
  Copy runnable commands from Markdown, since joining wrapped lines may be needed
  when copying from PowerPoint.
- Overflow creates continuation slides with the same title and a source-slide /
  continuation marker. Body order is unchanged. Code may continue on the next
  slide; retain the full block in Markdown. Titles longer than two lines fail
  instead of shrinking to unreadable text.

## Checks and presentation review

Every build, and `--check-only`, reopens the PPTX and checks:

- Every parsed source title and body element, in order, with exact text after
  removing only inserted soft breaks. Code whitespace is retained.
- Clickable link targets and local source-link existence.
- Nonempty slides with one title and a body; expected slide XML parts; well-formed
  XML/relationships and ZIP integrity; absence of raster pictures.
- All shapes stay inside the slide; body text boxes do not overlap, stay inside
  the content region, and have enough height for their explicit display lines.

These are structural checks, not a PowerPoint render. A shape inside the slide
can still clip text if a viewer substitutes a wider font. Open the deck in
PowerPoint before teaching and review long titles, wrapped code, continuation
boundaries, and links in presentation mode. Do not claim visual inspection from
the XML checks alone. PowerPoint and LibreOffice are unavailable in the build
environment, so rendered clipping and viewer-specific layout remain unverified.

Session 2 keeps the approved 25 source slides across 33 PowerPoint slides,
including eight continuation slides. The Markdown agenda and
all explanation, demonstration, break, and practice content remain unchanged.
