# Brand Kit

---

## Canvas

- **Dimensions:** 1080 × 1350px (LinkedIn portrait — non-negotiable)
- **Format output:** PNG per slide + one combined PDF
- **Slide numbering:** Top-right corner, format `X / N` (e.g. `3 / 10`)
- **Handle watermark:** Bottom-left of every slide — `@dhyan2815` — small, muted, never bold

---

## Colours

### Core Palette

| Role             | Hex       | Usage                                              |
|------------------|-----------|----------------------------------------------------|
| Background       | `#0A192F` | Slide background — deep navy, used on every slide  |
| Primary Text     | `#FFFFFF` | Headlines, body text                               |
| Accent           | `#00D9C0` | Highlighted words, pill badges, key callouts       |
| Warm Accent      | `#FFB347` | Secondary highlights, step numbers, CTA badges     |
| Muted Text       | `#8892A4` | Subtitles, watermarks, small labels                |
| CTA Slide BG     | `#00A896` | Final CTA/follow slide — solid teal, full bleed    |

### Accent Highlight Rule
When a key word in a headline needs emphasis, wrap it in a solid **accent-coloured box** (`#00D9C0` background, `#0A192F` text). Do not use underlines or italics for emphasis — use the box.

### Rainbow Left Strip (Required on content slides)
A 6px vertical strip on the left edge of every content slide (not cover, not CTA), using this exact gradient top-to-bottom:

```
#E74C3C → #F39C12 → #F1C40F → #2ECC71 → #3498DB → #9B59B6
```

---

## Typography

### Fonts (load via Google Fonts)

| Role          | Font                      | Weight    | Style     |
|---------------|---------------------------|-----------|-----------|
| Cover title   | Barlow Condensed          | 900 Black | ALL CAPS  |
| Section title | Barlow Condensed          | 700 Bold  | ALL CAPS  |
| Step label    | Barlow Condensed          | 600       | ALL CAPS  |
| Body          | Inter                     | 400/500   | Sentence case |
| Brand label   | Inter                     | 600       | ALL CAPS, tracked wide (`letter-spacing: 0.15em`) |

### Font Size Floor
- **Never below 15px** for any visible text element
- Body text minimum: **18px**
- Headlines: **64–120px** depending on length (fewer words = bigger type)
- Step badge labels: **12–14px** ALL CAPS

---

## Slide Structure

### Every Content Slide Must Include

1. **Rainbow left strip** — 6px, full height, gradient (see above)
2. **Step badge** — top-left, pill shape, accent colour background, e.g. `STEP 01`
3. **Slide counter** — top-right, muted text, e.g. `2 / 10`
4. **Headline** — ALL CAPS, Barlow Condensed Black, at least one key word in accent highlight box
5. **Body text** — max 2–3 lines under the headline, Inter, 18–20px
6. **Visual zone** — bottom half of slide: code screenshot, diagram, file tree, comparison table, or illustration. Never leave it empty.
7. **Watermark** — bottom-left, `@dhyan2815`, muted, 13px

### Cover Slide (Slide 1)
- No step badge, no rainbow strip
- Full-bleed navy background
- Brand name top-left in small tracked caps
- Massive ALL CAPS headline — primary keyword in accent highlight box
- Subline: slide count + descriptor (e.g. `10 SLIDES · FULL SYSTEM`) in muted small caps
- Optional: mascot or brand icon top-right

### CTA / Final Slide
- Background: solid `#00A896` (teal), full bleed — no navy
- No rainbow strip, no step badge
- Brand name + avatar top-center
- Large ALL CAPS CTA headline, key word in white box with teal text
- Subtext: newsletter/social CTA, muted white, centered
- Watermark bottom-left

---

## Visual Elements (Bottom-Half Zone)

Use exactly one of these per slide. No blank lower halves.

- **Code screenshot** — dark code editor mockup, syntax-highlighted, realistic chrome
- **File tree** — annotated directory structure, monospace, with `←` comment annotations
- **Terminal/CLI block** — dark terminal with realistic prompt, coloured output text
- **Comparison table** — column headers in accent colour, alternating row shading
- **Flow diagram** — CSS-only, numbered steps connected by arrows, accent-coloured nodes
- **Annotated screenshot** — UI screenshot with labelled callouts

No emoji icons in visual elements. No stock illustrations.

---

## Aesthetic Rules

1. **Dark-first** — every slide starts from `#0A192F`, never white or light backgrounds (except CTA slide)
2. **High contrast** — white text on navy must always pass WCAG AA
3. **Structured density** — content slides feel full but never cluttered. One idea per slide.
4. **No decorative gradients** — background stays flat navy. Gradient lives only in the left strip.
5. **No emoji** — use CSS shapes, icons, or illustrated PNGs from `assets/` only
6. **Consistent spacing** — 48px padding on all edges of slide content area

---

## Asset Paths

```
assets/
  headshot.jpeg           ← Used on CTA slide only
  logos/                 ← Brand logos for use in content if needed
  icons/                 ← Any approved icon PNGs
```

Claude reads `assets/` before building. Never hardcode image paths outside this folder.

---

## Tone

- **Voice:** Direct, instructional, zero fluff
- **Headlines:** Imperative verbs or noun phrases. ALL CAPS. ("BUILD YOUR QA AGENT", "CREATE YOUR SKILL FILE")
- **Body:** One punchy sentence. Bold the payoff phrase.
- **No exclamation marks.** No motivational filler. Say what it is, say why it matters, stop.

---

## Usage

This file is read automatically by the carousel skill before every build.  
It is the single source of truth for colours, fonts, layout, and tone.  
Do not override values inline — edit here and rebuild.