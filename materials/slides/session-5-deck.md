# Session 5 PowerPoint maintenance

[session-5.md](session-5.md) is the approved source for
[session-5.pptx](session-5.pptx). The deck contains editable native text and
shapes, including the application workflow diagram. Edit the Markdown and
regenerate; PowerPoint-only changes are overwritten. Distribute the repository
alongside the deck to preserve relative links.

From the repository root, use Python 3.12 with
[requirements-slides.txt](../../requirements-slides.txt) installed following the
[slide authoring guide](README.md):

```bash
python scripts/build_slides.py \
  --source materials/slides/session-5.md \
  --output materials/slides/session-5.pptx
python scripts/build_slides.py \
  --source materials/slides/session-5.md \
  --output materials/slides/session-5.pptx --check-only
```

Generation and the saved-artifact check preserve all 17 source slides across
19 PowerPoint slides (two continuations), with 68 source elements, 70 body text
boxes, and 14 distinct clickable link targets. Checks cover exact content and
order, code whitespace, local link existence, shape bounds, body overlap and
line-height budgets, slide XML, relationships, and ZIP integrity. No raster
pictures replace editable content. The deck uses 16:9 slides, 32 pt titles,
21 pt prose, and 18 pt code, retaining the showcase timing, engineering evidence,
individual participation, and final-only pass/fail policy.

These are structural checks, not a rendered preview. PowerPoint and LibreOffice
are unavailable here, so visible clipping, font substitution, and viewer-specific
layout remain unverified. Before teaching, open the deck in PowerPoint with
Arial and Courier New installed; inspect long titles, wrapped text/code, workflow
alignment, continuation boundaries, and links in presentation mode. Copy runnable
commands from Markdown to avoid inserted display wraps. Docker is also unavailable;
deck validation does not execute classroom demonstrations or provide container
evidence.
