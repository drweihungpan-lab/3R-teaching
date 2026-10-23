# Session 3 PowerPoint maintenance

[session-3.md](session-3.md) is the content source for the editable
[session-3.pptx](session-3.pptx). Edit Markdown and regenerate; PowerPoint-only
edits are overwritten. See the [converter guide](README.md) for dependencies,
supported Markdown, fonts, and distribution of repository-relative links.

From the repository root, with Python 3.12 and `requirements-slides.txt` installed:

```bash
python scripts/build_slides.py \
  --source materials/slides/session-3.md \
  --output materials/slides/session-3.pptx
python scripts/build_slides.py \
  --source materials/slides/session-3.md \
  --output materials/slides/session-3.pptx --check-only
```

## Generation and checks

The approved 23 source slides produce 23 editable PowerPoint slides, with no
continuation slides: 140 source body elements, 140 body text boxes, and 15 unique
clickable link targets. The request workflow remains editable monospace text.
The deck uses the shared 16:9 layout, 32 pt Arial titles, 21 pt Arial body text,
and 18 pt Courier New code.

Generation and the separate `--check-only` command both passed: exact title and
body content and sequence (including code whitespace), hyperlink targets and
local link existence, native text without raster pictures, shape bounds,
nonoverlapping body boxes and text-height budgets, slide XML counts, XML and
relationship parsing, and ZIP integrity.

## Preview limits

PowerPoint and LibreOffice are unavailable in the authoring environment; no
rendered visual inspection was performed. Structural checks cannot establish
viewer-specific clipping or font appearance. Before teaching, open the deck in
PowerPoint with Arial and Courier New installed; inspect long titles, wrapped
commands and the request workflow, text clipping, and links in presentation
mode. Copy runnable commands from Markdown because PowerPoint soft wraps may
need joining. Distribute the repository with the deck to retain local links.
