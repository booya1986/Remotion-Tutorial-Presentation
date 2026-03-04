# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a single-file Hebrew RTL presentation (`index.html`) about building video with Remotion and Claude Code. It is a standalone HTML file — no build system, no dependencies, no package manager.

Open in browser: `open index.html`

## Architecture

Everything lives in `index.html` with one external asset:

- **`matrix-clip.mp4`** — 15s clip from The Matrix ("I know Kung Fu" → "Show me"), played in slide 8's overlay via `<video>` element

- **CSS** — all styles in a single `<style>` block in `<head>`
- **HTML** — slides inside `.slideshow > .slide[data-layout="..."]`
- **JS** — all logic in a single `<script>` block at the bottom of `<body>`

### Slide system

- Each slide is a `<div class="slide" data-layout="...">` — the `data-layout` value drives all CSS targeting
- Active slide has class `active`; exiting slides get `exit-left` or `exit-right`
- Navigation: `goTo(index)`, `next()`, `prev()` in the JS IIFE at the bottom
- Dot nav, progress bar, and keyboard/swipe/click are all wired up in that same IIFE

### RTL / Hebrew

- `<html lang="he" dir="rtl">` — flex row order is naturally reversed throughout
- Arrow keys: `ArrowLeft` → `next()`, `ArrowRight` → `prev()`
- Progress bar anchored to `right: 0`; gradient direction `270deg`
- Individual slides that contain LTR content (code panels, pipeline flow) override with `direction: ltr` on the container

### CSS conventions

- Global: `.slide h1 { font-size: clamp(2rem, 4vw, 3rem) }`, `.slide p { font-size: clamp(1rem, 2vw, 1.25rem) }`, `.slide-number { font-size: 0.85rem }`
- Slide-specific overrides use `.slide[data-layout="X"] .classname` — always use the data-layout selector for specificity to avoid fighting `.slide p { text-align: center }`
- Accent color: `#22C55E` (green)
- Font: Heebo (Hebrew + Latin)

### Slide background

Every slide shares the same two-layer background defined on the global `.slide` rule — do not add per-slide `background` overrides:

1. **Green radial blob** — `background: radial-gradient(ellipse at center, rgba(34,197,94,0.12) 0%, rgba(34,197,94,0.03) 40%, transparent 70%)` on `.slide`
2. **Animated grid** — `.slide::before` renders faint square grid lines (`rgba(255,255,255,0.025)`, `40px` cells) with `@keyframes gridDrift` drifting diagonally over `8s linear infinite`

Slide content sits above the grid via `.slide > * { position: relative; z-index: 1 }` (grid is `z-index: 0`).

### Looping JS animations

Several slides use JS loops tied to slide visibility via `MutationObserver` on the slide's `class` attribute — start when `active` is added, cancel when removed. Pattern used in:
- **Slide 4** (solution): auto-cycles hover highlight across 3 code lines every 1.8s
- **Slide 6** (pipeline): lights up steps sequentially every 0.9s
- **Slide 7** (terminal): typewriter loop — types lines char-by-char, shows files, resets after pause
- **Slide 8** (skills): progress bar fills 0→100% → Matrix moment (local `matrix-clip.mp4` plays 15s, then canvas rain + "I Know Remotion" text) → pills appear, loops
- **Slide 9** (checklist): checks items one by one every 700ms, shows bottom line, resets

### Current slides

| # | data-layout | Content |
|---|-------------|---------|
| 1 | `title` | Opening — Remotion + Claude Code |
| 2 | `code-to-video` | Code → Video visual (LTR) |
| 3 | `problem` | The Problem — timeline visual |
| 4 | `solution` | What is Remotion — interactive code |
| 5 | `showcase` | 5 use-case cards with mini animations |
| 6 | `pipeline` | Prompt→Agent→Code→Video flow |
| 7 | `claude-terminal` | Typewriter terminal demo |
| 8 | `skills-install` | Progress bar + Matrix "I Know Remotion" moment |
| 9 | `checklist-anim` | Animated checklist loop |
| 10 | `demo-transition` | Live demo transition slide |
