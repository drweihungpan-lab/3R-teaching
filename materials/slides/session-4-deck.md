# Session 4 PowerPoint maintenance

[session-4.md](session-4.md) is the approved content source;
[session-4.pptx](session-4.pptx) contains editable native text and shapes,
including the request-flow and Compose diagrams. Edit Markdown and regenerate;
PowerPoint-only edits are overwritten. Keep the repository alongside the deck
so relative links remain usable.

From the repository root, use Python 3.12 with
[requirements-slides.txt](../../requirements-slides.txt) installed as described
in the [slide authoring guide](README.md):

```bash
python scripts/build_slides.py \
  --source materials/slides/session-4.md \
  --output materials/slides/session-4.pptx
python scripts/build_slides.py \
  --source materials/slides/session-4.md \
  --output materials/slides/session-4.pptx --check-only
```

## Verification results

Generation and the saved-artifact check preserve 22 source slides across 34
PowerPoint slides (12 continuations): 154 source elements, 158 body text boxes,
and 21 distinct clickable link targets. Exact source text and order, including
code whitespace, are checked after removing inserted soft line breaks. Local
link existence, shape bounds, body overlap and line-height budgets, slide XML,
relationships, and ZIP integrity pass. No raster pictures replace editable
content. The deck uses 16:9 slides, 32 pt titles, 21 pt prose, and 18 pt code.

These are structural checks, not a rendered preview. PowerPoint and LibreOffice
are unavailable here; font substitution, visible clipping, and viewer-specific
layout remain unverified. Before teaching, open the deck in PowerPoint with
Arial and Courier New installed, inspect long titles, wrapped commands,
diagram alignment and continuation boundaries, and try links in presentation
mode. Copy runnable commands from Markdown to avoid inserted display wraps.
Docker is also unavailable on this authoring host; deck checks do not execute
the classroom demonstrations or establish new container evidence.
