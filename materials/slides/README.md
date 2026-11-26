# Editable PowerPoint slides

The `session-N.md` files are the content source. Their `session-N.pptx` companions
contain editable native PowerPoint text and shapes, including monospace workflow
diagrams and code. Make content changes in Markdown, then regenerate the deck.
Changes made only in PowerPoint are overwritten on regeneration. The
`session-N.pdf` handout is exported from the PPTX (see below).

A slide face carries one idea in at most 29 words. The narration belongs in the
slide's speaker notes, written as a fence tagged `notes` in the source, so present
from Presenter View or the notes pane.

Every course deck follows the format of the Session 1 deck
(`Session 1_ From Jupyter to Production.pdf`). The full guide for authors is
[STYLE_GUIDE.md](STYLE_GUIDE.md); *Visual standard* below summarises the tokens.

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
  One `##` heading is one slide and one concept.
- Every title needs an **eyebrow**: a `### CATEGORY` line directly above it, such as
  `### FAILURE MODES`, `### SOLUTION 1 · REPEATABILITY`, `### TEMPLATE ANATOMY`. The
  build fails without one. Eyebrows and titles do not count toward the word limit.
- The eyebrow colour comes from its words: red for `FAILURE`, `PITFALL`, `SECURITY`,
  `RULE`, `NEVER`; amber for `STAGE`, `EXAMPLE`, `EXPERIMENT`, `HANDS-ON`, `OPTIONAL`,
  `ACCOUNTABILITY`, `GRADING`, `WHY WE BUILT`; teal otherwise.
- `1. text`, `2. text` ... become **white cards** with a mono number: up to four in
  one row, five or six in a 3×2 grid. Use them for agendas, roadmaps and reasons.
- `> [!TIP] text` is a bold teal takeaway line with no box. `> [!WARNING]`,
  `> [!CAUTION]`, `> [!NOTE]` and `> [!IMPORTANT]` become a white card with a mono tag
  (`WATCH OUT:` amber, `CRITICAL RULE:` red, `NOTE:`/`IMPORTANT:` teal); bold words
  take the tag colour. One line each; lead with a bold phrase.
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
- Tables, other block quotes, nested lists, checkboxes, images, HTML, and advanced
  Markdown are outside this small converter's dialect. Use editable text for
  simple diagrams. Do not add unsupported syntax expecting a rendered image.
- Markdown markers become text styling or native bullets. Link labels remain
  visible, with clickable targets. Local links are checked and rebased relative
  to the output file; distribute the repository with the deck to keep them usable.
- Code fences become plain dark panels with rounded corners. `bash` fences get light
  syntax tints (command, flags, strings, comments); `text` fences tint `→` and
  `...Error` names.
- **Split layout:** when a slide has exactly one code block, followed by more content,
  and every code line fits in half the width, the code (with anything above it) sits
  on the left and the rest on the right, as on Session 1. Otherwise everything is
  stacked full width.

## Visual standard

- **Canvas:** 16:9. Content slides are off-white `F8FAFC`. The `#` cover slide and
  the last slide are dark navy `0F172A` with white titles and amber eyebrows. No
  footer, page numbers, rules or progress bar. Each column of the body is centred
  vertically under the title; on the cover it follows the title, with a short teal
  rule underneath.
- **Palette:** slate `0F172A` for titles and text; teal `0D9488` for eyebrows,
  takeaways and inline code; amber `D97706` and red `DC2626` for examples, warnings
  and failure modes. Cards are white with `E2E8F0` borders; code panels `1E293B`.
- **Type:** DM Sans bold for titles (30 pt; 46 pt on the cover), DM Sans for body
  (18 pt, 1.45 line height); JetBrains Mono for code (14 pt), inline code, card
  numbers, tags and the small uppercase eyebrows (10.5 pt).
- DM Sans and JetBrains Mono are free (SIL OFL) fonts. Install both before building
  or exporting, or PowerPoint and LibreOffice substitute other fonts and wrapping
  changes.
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

## Export the PDF

With LibreOffice installed and both fonts available:

```bash
soffice --headless --convert-to pdf --outdir materials/slides \
  materials/slides/session-2.pptx
```

## Checks and presentation review

Every build, and `--check-only`, reopens the PPTX and checks:

- The 29-word limit on every slide face.
- An eyebrow on every slide, matching the source.
- Every parsed source title and body element, in order, with exact text after
  removing only inserted soft breaks. Code whitespace is retained.
- Speaker notes text, per slide, against the source's `notes` fences, and that no
  slide carries notes the source does not declare.
- Clickable link targets and local source-link existence.
- Nonempty slides with one title and a body; expected slide XML parts; well-formed
  XML/relationships and ZIP integrity; absence of raster pictures.
- All shapes stay inside the slide; body text boxes (including those inside cards
  and callouts) do not overlap, stay inside the content region, and have enough
  height for their explicit display lines.

These are structural checks, not a PowerPoint render. A shape inside the slide
can still clip text if a viewer substitutes a wider font. Open the deck in
PowerPoint before teaching and review long titles, wrapped code, continuation
boundaries, and links in presentation mode. Do not claim visual inspection from
the XML checks alone.
