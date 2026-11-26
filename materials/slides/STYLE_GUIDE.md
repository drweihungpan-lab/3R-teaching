# Slide Style Guide

The standard for every course deck (Sessions 1–5 and any later deck). The reference
is the Session 1 deck, `Session 1_ From Jupyter to Production.pdf`. Session 2
(`session-2.md` → `session-2.pptx` → `session-2.pdf`) is the first deck built to this
guide by `scripts/build_slides.py`.

Audience: graduate students in a Statistics Master's program, in a lecture hall.
Slides are visual cues. The explanation lives in the speaker notes.

How to build and export a deck is in [README.md](README.md). This guide covers what a
slide should look like and how to write one.

---

## 1. Principles

- **One concept per slide.** Each `##` heading is its own slide. Never put two ideas
  on one slide. Split them, e.g. "Why Branches? (1/2)" and "(2/2)".
- **Scannable, not prose.** At most 29 words on a slide face (the build enforces this).
  Turn paragraphs into cards, callouts, code panels or short lines.
- **Narration goes in the notes.** Anything you would *say* belongs in a ` ```notes `
  fence, never on the slide.
- **Whitespace.** Leave at least a quarter of every slide empty. A sparse slide is
  fine: the body is centred vertically under the title.
- **Colour has meaning.** Teal means a solution or takeaway. Amber means an example or
  a warning. Red means a failure mode or a critical rule. Do not use colour for
  decoration.

---

## 2. Slide anatomy

Every slide has, top to bottom:

1. **Eyebrow:** a small uppercase category label in a monospace font.
2. **Title:** short, in title case, one line where possible (two at most).
3. **Body:** one block of components (see §4), centred vertically.

There is no footer, no page number, no rule under the title and no progress bar.

~~~markdown
---

### FAILURE MODES · STAGE 3
## Stage 3: Dependencies Declared

Stage 2 crashed on a newer pandas. Stage 3 adds `requirements.txt`.

> [!WARNING] **The answer depends on which cells ran.**

```notes
What you say out loud goes here.
```
~~~

### Slide types

| Slide | Source | Look |
|---|---|---|
| Cover | the first slide, `# Session N: Title` | Dark navy, amber eyebrow, large white title, short subtitle, short teal rule |
| Content | `## Title` | Off-white canvas, coloured eyebrow, dark slate title |
| Closing | the last slide in the deck | Dark navy like the cover: wrap-up, exercise, what comes next |

---

## 3. Eyebrows

Write the eyebrow on a `### ` line directly above every title. It is required: the
build fails without one. Write it in UPPERCASE; use ` · ` to add a sub-category.

The colour follows from the words, first match wins:

| Colour | Trigger words | Use for |
|---|---|---|
| **Red** `DC2626` | `FAILURE`, `PITFALL`, `SECURITY`, `RULE`, `NEVER` | What goes wrong; rules students must not break |
| **Amber** `D97706` | `STAGE`, `EXAMPLE`, `EXPERIMENT`, `HANDS-ON`, `OPTIONAL`, `ACCOUNTABILITY`, `GRADING`, `WHY WE BUILT` | The running device example, activities, optional material |
| **Teal** `0D9488` | anything else | Concepts, solutions, tools |

On the dark cover and closing slides the eyebrow is always amber.

Recommended vocabulary, so decks read as one course:

- `3R COURSE · SESSION N` for the cover
- `COURSE FORMAT`, `COURSE ROADMAP`, `SESSION TIMELINE`, `WARM-UP`, `ANALOGY`,
  `DISCUSSION PROMPT`
- `FAILURE MODES`, `FAILURE MODES · STAGE N`, `PITFALL`, `SECURITY & PRIVACY RULE`
- `SOLUTION N · <PRINCIPLE>` (e.g. `SOLUTION 1 · REPEATABILITY`), `TECH DECISIONS`,
  `WHY WE BUILT IT THIS WAY`
- `TEMPLATE ANATOMY`, `TEMPLATE ANATOMY · 1 OF 3`
- Topic families: `ENVIRONMENTS · …`, `GIT · …`, `BRANCHES · …`, `COMMAND LINE · …`,
  `PULL REQUESTS`, `CONTINUOUS INTEGRATION`
- `HANDS-ON`, `NEXT SESSION`

---

## 4. Components

Use these building blocks. Anything else in the Markdown dialect is rejected by the
build (tables, other block quotes, nested lists, images, HTML).

### Short lines

One sentence per line, each a separate paragraph. Use **bold** for the phrase that
carries the idea. Bold text is slate, not coloured.

```markdown
**Fix the template once.**

Every repo generated **afterwards** gets the fix.
```

### Takeaway (teal, no box)

The one thing to remember. Bold teal text, no card. Use at most one per slide.

```markdown
> [!TIP] **Same input, same output, every time.**
```

### Callout cards

A white card with a small monospace tag. Bold words take the tag's colour. Write one
line and lead with a bold phrase.

| Source | Tag | Colour | Use for |
|---|---|---|---|
| `> [!WARNING]` | `WATCH OUT:` | amber | Common mistakes, surprising behaviour |
| `> [!CAUTION]` | `CRITICAL RULE:` | red | Never-do rules: never commit `.venv/`, secrets, real data |
| `> [!NOTE]` | `NOTE:` | teal | Neutral side information |
| `> [!IMPORTANT]` | `IMPORTANT:` | teal | Must-know facts that are not warnings |

```markdown
> [!CAUTION] **Never commit** `.venv/`. It is listed in `.gitignore`.
```

### Cards (numbered)

A numbered list becomes white bordered cards with a monospace number. Up to four sit
in one row; five or six form a 3×2 grid. Use them for agendas, roadmaps, steps and
lists of reasons. Keep each card to about 12 words.

```markdown
1. **One venv** in your Backend repo. Install. Run the template command.
2. Branch, small change, commit, push.
3. PR, review, merge, `git pull`.
```

Numbering continues across slides when a list is split ("Why Branches? (2/2)" starts
at `3.`).

### Code panels

Fenced code becomes a plain dark panel (`1E293B`) with rounded corners.

- ` ```bash ` for commands the students type. Commands, flags, strings and comments
  get light syntax colours.
- ` ```text ` for output, errors, diagrams and folder trees. `→` arrows are tinted teal
  and `…Error` names red.
- Show only what students must type or read. Keep lines under about 60 characters so
  the panel can sit beside its explanation.
- Use plain-text diagrams with `→`, `-->` and `<--` for flows (e.g. "Git: three places").

### Split layout (automatic)

When a slide has exactly **one** code panel, followed by more content, and every code
line fits in half the width, the converter puts the code (and anything above it) on
the left and the rest on the right. This is the default Session 1 pattern: code on the
left, its meaning on the right. To get it, write:

~~~markdown
```bash
git pull
```

Brings a teammate's commits **from GitHub to your computer**.

> [!TIP] **Pull before you start working.**
~~~

If a code line is too long, or there are two code panels, everything stacks full width.

### Links

`[label](target)` keeps a clickable teal link. Local links are checked at build time.
Prefer one link per slide.

---

## 5. Visual tokens

### Palette

| Token | Hex | Use |
|---|---|---|
| Canvas | `F8FAFC` | Content slide background |
| Dark canvas | `0F172A` | Cover and closing slides |
| Ink | `0F172A` | Titles and body text on light slides |
| Ink on dark | `E2E8F0` / `FFFFFF` | Body / titles on dark slides |
| Muted | `64748B` | Secondary text |
| Teal | `0D9488` | Eyebrows, takeaways, solutions |
| Teal dark | `0F766E` | Inline code and links on light slides |
| Amber | `D97706` | Examples, activities, warnings |
| Red | `DC2626` | Failure modes, critical rules |
| Card | `FFFFFF` + `E2E8F0` border | Cards and callouts |
| Terminal | `1E293B` | Code panels |

### Typography

| Element | Font | Size |
|---|---|---|
| Cover title | DM Sans Bold | 46 pt |
| Slide title | DM Sans Bold, slightly tight tracking | 30 pt |
| Body, callouts | DM Sans | 18 pt, 1.45 line height |
| Card text | DM Sans | 16 pt |
| Eyebrow | JetBrains Mono, uppercase | 10.5 pt |
| Code panels, inline code | JetBrains Mono | 14 pt (panels) |
| Card numbers, callout tags | JetBrains Mono | 10–10.5 pt |

Code spans in a title (e.g. `git push`) stay in the monospace font.

DM Sans and JetBrains Mono are free (SIL Open Font License). Install both before you
build or export, or the viewer substitutes other fonts and the text wraps differently.

### Geometry

- 16:9 (13.33 × 7.5 in), 0.7 in side margins.
- Rounded corners on cards and code panels; flat, with no shadows.
- Two-column split: two equal columns with a 0.45 in gap.

---

## 6. Writing rules

- **Titles:** state the idea, not the topic, where possible ("Logs Tell You What Ran",
  not "Logging"). Title case. Use `Pitfall:` and `Stage N:` prefixes for failure-mode slides.
- **Questions as hooks:** a slide may be just one or two bold questions (e.g.
  "Can someone else still make your tea?"). Put the answer in the notes.
- **Running example:** reuse the course's device example (`device_limit`,
  `DEV-A/B/C`, the dates) rather than inventing new data.
- **Analogy:** the bubble tea shop is the course analogy. Come back to it rather than
  adding new metaphors.
- **No timings on the face**, except on a dedicated timeline slide.
- **Speaker notes** carry the explanation, demos, common mistakes (`COMMON PROBLEMS:`),
  and instructor prep. Write bare URLs there.

---

## 7. Checklist before publishing a deck

- [ ] Every slide has a `###` eyebrow from the vocabulary above.
- [ ] One concept per slide; no slide face over 29 words.
- [ ] Every slide has a `notes` fence with the narration.
- [ ] Red appears only on failure modes and critical rules; at most one teal takeaway per slide.
- [ ] Commands are in ` ```bash `, output in ` ```text `.
- [ ] The first slide is the cover (`#`); the last slide is the wrap-up / next steps.
- [ ] `python scripts/build_slides.py …` passes.
- [ ] Exported PDF reviewed page by page with DM Sans and JetBrains Mono installed.
