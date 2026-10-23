# Session 1 PowerPoint maintenance

[session-1.md](session-1.md) is the approved content source;
[session-1.pptx](session-1.pptx) contains editable native text and shapes.
Edit the Markdown and regenerate: PowerPoint-only edits are overwritten.
The architecture and Git workflow diagrams remain editable monospace text.

From the repository root, use Python 3.12 with the dependencies in
`requirements-slides.txt` (see the [authoring setup](README.md)):

```bash
python scripts/build_slides.py \
  --source materials/slides/session-1.md \
  --output materials/slides/session-1.pptx
python scripts/build_slides.py \
  --source materials/slides/session-1.md \
  --output materials/slides/session-1.pptx --check-only
```

Both commands passed: 22 source slides become 31 editable 16:9 slides,
with nine continuation slides, 136 source elements, 142 body text boxes,
and 10 distinct clickable link targets. All source text and ordering are
preserved, including the agenda, demonstrations, conflict rehearsal, and
final-presentation requirements. Continuations repeat their source title
and identify the source slide and continuation number.

Checks covered exact text and sequence, local link existence and rebased
hyperlink targets, nonempty slides, native editable content without raster
pictures, shape bounds, body overlap and text-height budgets, XML and
relationship parsing, slide-part counts, and ZIP integrity. Keep the deck
with the repository so its relative links continue to work.

These checks do not render the slides. PowerPoint, LibreOffice, and Docker
were unavailable; no rendered preview or container execution was performed.
Before teaching, open the deck in PowerPoint with Arial and Courier New
available. Inspect long titles, wrapped commands, continuation boundaries
(especially the conflict walkthrough), architecture/workflow arrows, and
links in presentation mode. Font substitution and viewer-specific clipping
remain unverified. Copy runnable commands from Markdown, since display
wrapping in PowerPoint may need joining. Backend tests were not rerun for
this presentation-only change.
