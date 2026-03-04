# Remotion + Claude Code — Presentation

A Hebrew RTL slideshow presenting how to build programmatic videos using [Remotion](https://remotion.dev) and [Claude Code](https://claude.ai/code).

## Quick Start

Open `index.html` in any modern browser — no build step or server required.

```bash
open index.html
```

Navigate with arrow keys (← →), click the side arrows, or use the dot nav at the bottom.

## What's Inside

| File | Description |
|------|-------------|
| `index.html` | The entire presentation — HTML, CSS, and JS in a single file |
| `matrix-clip.mp4` | 15-second Matrix clip used in the skills slide animation |
| `CLAUDE.md` | Development context for Claude Code |

## Slides

1. **Title** — Opening slide with Remotion + Claude Code branding
2. **Code to Video** — Visual showing the code → video concept
3. **The Problem** — Why traditional video editing doesn't scale
4. **What is Remotion** — Interactive code panel with hover animations
5. **Showcase** — 5 use-case cards (data-driven video, prompts, API, etc.)
6. **Pipeline** — Prompt → Agent → Code → Video flow diagram
7. **Claude Terminal** — Typewriter animation of Claude Code in action
8. **Skills** — Progress bar install + Matrix "I Know Remotion" moment
9. **Checklist** — Animated learning objectives
10. **Live Demo** — Transition slide with Remotion & Anthropic logos

## Tech

- Vanilla HTML/CSS/JS — no frameworks or dependencies
- Hebrew RTL (`dir="rtl"`) with LTR overrides for code panels
- CSS animations + JS `MutationObserver` loops for per-slide effects
- Canvas-based Matrix digital rain effect
- Local `<video>` playback for the Matrix clip

## License

This presentation is for educational purposes.
