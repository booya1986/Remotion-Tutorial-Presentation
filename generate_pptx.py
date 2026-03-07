#!/usr/bin/env python3
"""Generate a PowerPoint (.pptx) version of the Remotion + Claude Code presentation."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Constants ──
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

BG_COLOR = RGBColor(0x1B, 0x1B, 0x1B)
GREEN = RGBColor(0x22, 0xC5, 0x5E)
GREEN_DIM = RGBColor(0x1A, 0x80, 0x3E)
WHITE = RGBColor(0xDC, 0xDA, 0xD5)
GRAY = RGBColor(0xA0, 0x9D, 0x96)
DARK_PANEL = RGBColor(0x0D, 0x11, 0x17)
DARK_PANEL2 = RGBColor(0x14, 0x17, 0x1F)
CODE_BG = RGBColor(0x0A, 0x0E, 0x14)

FONT_NAME = "Arial"  # Fallback; Heebo if available


def set_slide_bg(slide, color=BG_COLOR):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, left, top, width, height, text, font_size=18,
                color=WHITE, bold=False, alignment=PP_ALIGN.RIGHT,
                font_name=FONT_NAME, anchor=MSO_ANCHOR.TOP):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    try:
        tf.paragraphs[0].alignment = alignment
    except Exception:
        pass
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = font_name
    return txBox


def add_multiline_textbox(slide, left, top, width, height, lines,
                          font_size=14, color=WHITE, alignment=PP_ALIGN.LEFT,
                          font_name="Consolas", line_spacing=1.2):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    for i, line_text in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = alignment
        p.space_after = Pt(2)
        run = p.add_run()
        run.text = line_text
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
        run.font.name = font_name
    return txBox


def add_rect(slide, left, top, width, height, fill_color, border_color=None,
             corner_radius=None):
    if corner_radius:
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                       left, top, width, height)
        # Adjust corner rounding (0-1 scale internally, but we set via EMU)
    else:
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                       left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape


def add_slide_number_label(slide, text, top=Inches(0.8)):
    add_textbox(slide, Inches(0.5), top, Inches(12.3), Inches(0.5),
                text, font_size=12, color=GREEN, bold=True,
                alignment=PP_ALIGN.CENTER)


def add_slide_title(slide, text, top=Inches(1.3), font_size=36):
    add_textbox(slide, Inches(0.5), top, Inches(12.3), Inches(1.0),
                text, font_size=font_size, color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)


def add_slide_subtitle(slide, text, top=Inches(2.3), font_size=18):
    add_textbox(slide, Inches(1.5), top, Inches(10.3), Inches(0.8),
                text, font_size=font_size, color=GRAY, bold=False,
                alignment=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════
#  SLIDE BUILDERS
# ══════════════════════════════════════════════════════════════

def slide_1_title(prs):
    """Opening — Remotion + Claude Code"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    set_slide_bg(slide)

    # Green tag
    add_textbox(slide, Inches(3), Inches(2.2), Inches(7.3), Inches(0.5),
                "From Code to Video", font_size=14, color=GREEN, bold=True,
                alignment=PP_ALIGN.CENTER)

    # Main title
    add_textbox(slide, Inches(1.5), Inches(2.8), Inches(10.3), Inches(1.5),
                "מהפכת יצירת הווידאו עם Remotion ו-Claude Code",
                font_size=40, color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)

    # Subtitle
    add_textbox(slide, Inches(2.5), Inches(4.5), Inches(8.3), Inches(1.0),
                "אנימציה. גרפיקה. סאונד. קריינות.\nהכל נבנה בקוד.",
                font_size=20, color=GRAY, alignment=PP_ALIGN.CENTER)


def slide_2_code_to_video(prs):
    """Code → Video visual"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)

    # Left panel: Code editor
    add_rect(slide, Inches(0.8), Inches(0.6), Inches(5.5), Inches(6.3),
             CODE_BG, border_color=RGBColor(0x30, 0x30, 0x30))

    # Terminal bar dots
    for i, c in enumerate([RGBColor(0xFF, 0x5F, 0x57),
                           RGBColor(0xFE, 0xBC, 0x2E),
                           RGBColor(0x28, 0xC8, 0x40)]):
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                     Inches(1.0 + i * 0.25), Inches(0.75),
                                     Inches(0.15), Inches(0.15))
        dot.fill.solid()
        dot.fill.fore_color.rgb = c
        dot.line.fill.background()

    code_lines = [
        "import { Composition } from 'remotion'",
        "import { useCurrentFrame } from 'remotion'",
        "import { interpolate } from 'remotion'",
        "",
        "export const MyVideo = () => {",
        "  const frame = useCurrentFrame()",
        "  const opacity = interpolate(",
        "    frame, [0, 30], [0, 1]",
        "  )",
        "  return <AbsoluteFill style={{opacity}} />",
        "}",
    ]
    add_multiline_textbox(slide, Inches(1.1), Inches(1.2), Inches(5.0), Inches(5.5),
                          code_lines, font_size=11, color=RGBColor(0xC5, 0xC1, 0xB9),
                          font_name="Consolas")

    # Connector arrow
    add_textbox(slide, Inches(6.1), Inches(3.2), Inches(1.2), Inches(0.6),
                "→", font_size=32, color=GREEN, bold=True,
                alignment=PP_ALIGN.CENTER)

    # Right panel: Video preview grid
    add_rect(slide, Inches(7.0), Inches(0.6), Inches(5.5), Inches(6.3),
             DARK_PANEL, border_color=RGBColor(0x30, 0x30, 0x30))

    # Title for preview
    add_textbox(slide, Inches(7.2), Inches(0.7), Inches(2.0), Inches(0.4),
                "Preview", font_size=10, color=RGBColor(0x22, 0xC5, 0x5E),
                alignment=PP_ALIGN.LEFT, font_name="Consolas")

    # Color grid cells
    colors = [
        [(Inches(7.3), Inches(1.3), Inches(1.5), Inches(1.5)), RGBColor(0x63, 0x66, 0xF1)],
        [(Inches(9.0), Inches(1.3), Inches(1.5), Inches(1.5)), GREEN],
        [(Inches(10.7), Inches(1.3), Inches(1.5), Inches(1.5)), RGBColor(0xF5, 0x9E, 0x0B)],
        [(Inches(7.3), Inches(3.0), Inches(3.0), Inches(1.5)), RGBColor(0x0E, 0xA5, 0xE9)],
        [(Inches(10.5), Inches(3.0), Inches(1.5), Inches(1.5)), RGBColor(0xEC, 0x48, 0x99)],
        [(Inches(7.3), Inches(4.7), Inches(1.5), Inches(1.5)), RGBColor(0xF9, 0x73, 0x16)],
        [(Inches(9.0), Inches(4.7), Inches(3.0), Inches(1.5)), RGBColor(0x22, 0xC5, 0x5E)],
    ]
    for (l, t, w, h), clr in colors:
        r = add_rect(slide, l, t, w, h, clr, corner_radius=True)
        r.fill.fore_color.rgb = clr


def slide_3_problem(prs):
    """The Problem — timeline visual"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)

    # Text side (right in RTL, but we place visually)
    add_slide_number_label(slide, "THE PROBLEM", top=Inches(1.0))
    add_textbox(slide, Inches(6.5), Inches(1.5), Inches(6.0), Inches(1.0),
                "לערוך וידאו זה... קשה",
                font_size=36, color=WHITE, bold=True, alignment=PP_ALIGN.RIGHT)
    add_textbox(slide, Inches(6.5), Inches(2.5), Inches(6.0), Inches(0.6),
                "טיימליין. ליירים. אפקטים. אינסוף קליקים.",
                font_size=18, color=GREEN, alignment=PP_ALIGN.RIGHT)
    add_textbox(slide, Inches(6.5), Inches(3.2), Inches(6.0), Inches(0.8),
                "עריכת וידאו קלאסית היא ידנית. חוזרת על עצמה. ולא סקיילבילית.",
                font_size=16, color=GRAY, alignment=PP_ALIGN.RIGHT)

    # Timeline visual (left side)
    tracks = [
        ("VIDEO", RGBColor(0x63, 0x66, 0xF1), [0.22, 0.03, 0.27, 0.02, 0.18, 0.04, 0.20]),
        ("AUDIO", RGBColor(0x0E, 0xA5, 0xE9), [1.0]),
        ("TEXT", RGBColor(0xF5, 0x9E, 0x0B), [0.0, 0.18, 0.08, 0.14, 0.09, 0.22]),
        ("FX", RGBColor(0xEC, 0x48, 0x99), [0.0, 0.11, 0.14, 0.09, 0.11, 0.13]),
        ("MUSIC", RGBColor(0x22, 0xC5, 0x5E), [0.42, 0.05, 0.30]),
        ("B-ROLL", RGBColor(0xF9, 0x73, 0x16), [0.0, 0.16, 0.11, 0.20, 0.07, 0.13]),
    ]

    track_left = Inches(0.8)
    track_width = Inches(5.5)
    track_top_start = Inches(1.2)
    track_height = Inches(0.6)
    track_gap = Inches(0.15)

    for i, (label, color, segments) in enumerate(tracks):
        y = track_top_start + (track_height + track_gap) * i

        # Label
        add_textbox(slide, track_left - Inches(0.1), y, Inches(0.8), track_height,
                    label, font_size=8, color=GRAY, alignment=PP_ALIGN.LEFT,
                    font_name="Consolas")

        # Clips
        x = track_left + Inches(0.85)
        clip_total_w = track_width - Inches(0.9)
        is_gap = False  # For TEXT/FX/B-ROLL, first segment is a gap
        if label in ("TEXT", "FX", "B-ROLL"):
            is_gap = True

        cx = x
        for seg in segments:
            seg_w = int(clip_total_w * seg)
            if seg_w < Emu(10000):
                cx += seg_w
                is_gap = not is_gap
                continue
            if not is_gap and seg > 0:
                r = add_rect(slide, cx, y + Inches(0.05), seg_w,
                             track_height - Inches(0.1), color)
                # Make slightly transparent
            cx += seg_w
            is_gap = not is_gap


def slide_4_solution(prs):
    """What is Remotion — code + preview"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)

    add_slide_number_label(slide, "THE SOLUTION", top=Inches(0.4))
    add_slide_title(slide, "?מה זה Remotion", top=Inches(0.8), font_size=32)
    add_slide_subtitle(slide, "בונים וידאו עם React", top=Inches(1.5), font_size=16)
    add_textbox(slide, Inches(1.5), Inches(2.0), Inches(10.3), Inches(0.6),
                "Remotion מאפשר לבנות וידאו באמצעות קוד. קומפוננטות. אנימציות. דינמיות מלאה.",
                font_size=14, color=GRAY, alignment=PP_ALIGN.CENTER)

    # Code panel (left)
    add_rect(slide, Inches(0.5), Inches(2.8), Inches(6.8), Inches(4.3),
             CODE_BG, border_color=RGBColor(0x30, 0x30, 0x30))
    add_textbox(slide, Inches(0.7), Inches(2.85), Inches(2.0), Inches(0.3),
                "MyComp.tsx", font_size=9, color=GREEN_DIM,
                alignment=PP_ALIGN.LEFT, font_name="Consolas")

    code_lines = [
        "import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion'",
        "export const MyComp = () => {",
        "  const frame = useCurrentFrame()",
        "  return (<AbsoluteFill style={{ background: '#0d1117' }}>",
        "    <div style={{ transform: `translateX(${frame*3}px)` }} />",
        "    <h1 style={{ opacity: interpolate(frame,[0,30],[0,1]) }}>",
        "      Hello, Remotion</h1>",
        "    <div style={{ transform: `scale(${...})` }} />",
        "  </AbsoluteFill>)",
        "}",
    ]
    add_multiline_textbox(slide, Inches(0.7), Inches(3.3), Inches(6.4), Inches(3.5),
                          code_lines, font_size=10, color=RGBColor(0xC5, 0xC1, 0xB9),
                          font_name="Consolas")

    # Preview panel (right)
    add_rect(slide, Inches(7.6), Inches(2.8), Inches(5.2), Inches(4.3),
             DARK_PANEL, border_color=RGBColor(0x30, 0x30, 0x30))
    add_textbox(slide, Inches(7.8), Inches(2.85), Inches(3.0), Inches(0.3),
                "Preview · frame 24", font_size=9, color=GREEN_DIM,
                alignment=PP_ALIGN.LEFT, font_name="Consolas")

    # Box element
    add_rect(slide, Inches(8.2), Inches(3.8), Inches(0.8), Inches(0.8),
             GREEN)

    # Text element
    add_textbox(slide, Inches(8.0), Inches(4.8), Inches(4.0), Inches(0.6),
                "Hello, Remotion", font_size=20, color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)

    # Circle element
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                    Inches(9.8), Inches(5.6), Inches(0.9), Inches(0.9))
    circle.fill.solid()
    circle.fill.fore_color.rgb = RGBColor(0x63, 0x66, 0xF1)
    circle.line.fill.background()


def slide_5_showcase(prs):
    """5 use-case cards"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)

    add_slide_number_label(slide, "מה אפשר לבנות", top=Inches(0.5))
    add_slide_title(slide, "לא רק אנימציה. Remotion היא מערכת לייצור וידאו.",
                    top=Inches(1.0), font_size=28)

    cards = [
        ("סרטוני\nSHORTS", "📱"),
        ("הדמיות\nנתונים", "📊"),
        ("סרטוני\nPromotion", "🎬"),
        ("הוספת\nכתוביות", "💬"),
        ("אינטראקציות\nבממשק", "🖱"),
    ]

    card_w = Inches(2.2)
    card_h = Inches(3.2)
    total_w = card_w * 5 + Inches(0.3) * 4
    start_x = (SLIDE_WIDTH - total_w) // 2
    card_y = Inches(2.2)

    for i, (label, icon) in enumerate(cards):
        x = start_x + (card_w + Inches(0.3)) * i

        # Card background
        card = add_rect(slide, x, card_y, card_w, card_h,
                        DARK_PANEL2, border_color=RGBColor(0x2A, 0x2A, 0x2A),
                        corner_radius=True)

        # Icon
        add_textbox(slide, x, card_y + Inches(0.4), card_w, Inches(0.8),
                    icon, font_size=36, color=WHITE, alignment=PP_ALIGN.CENTER)

        # Label
        add_textbox(slide, x, card_y + Inches(1.5), card_w, Inches(1.2),
                    label, font_size=16, color=WHITE, bold=False,
                    alignment=PP_ALIGN.CENTER)

    # Bottom text
    add_textbox(slide, Inches(2), Inches(5.8), Inches(9.3), Inches(0.5),
                "וידאו שמבוסס על דאטה, פרומפט או API.",
                font_size=16, color=GRAY, alignment=PP_ALIGN.CENTER)


def slide_6_pipeline(prs):
    """PROMPT → AI AGENT → CODE → VIDEO flow"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)

    add_slide_number_label(slide, "למה עכשיו", top=Inches(0.5))
    add_slide_title(slide, "כי בינה מלאכותית כותבת קוד", top=Inches(1.0), font_size=32)

    steps = [
        ("PROMPT", "💬", "תאר מה אתה רוצה"),
        ("AI AGENT", "🤖", "Claude Code מנתח ומתכנן"),
        ("CODE", "< >", "קומפוננטות React + Remotion"),
        ("VIDEO", "▶", "MP4 מוכן לפרסום"),
    ]

    box_w = Inches(2.3)
    box_h = Inches(2.8)
    arrow_w = Inches(0.6)
    total = box_w * 4 + arrow_w * 3
    start_x = (SLIDE_WIDTH - total) // 2
    box_y = Inches(2.2)

    for i, (name, icon, desc) in enumerate(steps):
        x = start_x + (box_w + arrow_w) * i

        # Box
        add_rect(slide, x, box_y, box_w, box_h,
                 DARK_PANEL2, border_color=GREEN_DIM, corner_radius=True)

        # Icon
        add_textbox(slide, x, box_y + Inches(0.3), box_w, Inches(0.8),
                    icon, font_size=36, color=GREEN, alignment=PP_ALIGN.CENTER)

        # Name
        add_textbox(slide, x, box_y + Inches(1.2), box_w, Inches(0.5),
                    name, font_size=16, color=WHITE, bold=True,
                    alignment=PP_ALIGN.CENTER, font_name="Consolas")

        # Description
        add_textbox(slide, x, box_y + Inches(1.8), box_w, Inches(0.8),
                    desc, font_size=13, color=GRAY, alignment=PP_ALIGN.CENTER)

        # Arrow (except after last)
        if i < 3:
            ax = x + box_w
            add_textbox(slide, ax, box_y + Inches(1.0), arrow_w, Inches(0.6),
                        "→", font_size=28, color=GREEN, bold=True,
                        alignment=PP_ALIGN.CENTER)

    # Bottom note
    add_textbox(slide, Inches(1.5), Inches(5.5), Inches(10.3), Inches(0.8),
                "כל הצינור הזה רץ אוטומטית — אתה רק מתאר את הוידאו שאתה רוצה",
                font_size=16, color=GRAY, alignment=PP_ALIGN.CENTER)


def slide_7_terminal(prs):
    """Claude Code terminal demo"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)

    add_slide_number_label(slide, "מה זה Claude Code", top=Inches(0.3))
    add_slide_title(slide, "סוכן AI שכותב, מריץ ומרנדר קוד", top=Inches(0.7), font_size=28)

    # Terminal window (left)
    add_rect(slide, Inches(0.5), Inches(1.5), Inches(7.5), Inches(5.5),
             CODE_BG, border_color=RGBColor(0x30, 0x30, 0x30))

    # Terminal bar
    add_rect(slide, Inches(0.5), Inches(1.5), Inches(7.5), Inches(0.45),
             RGBColor(0x1E, 0x1E, 0x1E))
    for i, c in enumerate([RGBColor(0xFF, 0x5F, 0x57),
                           RGBColor(0xFE, 0xBC, 0x2E),
                           RGBColor(0x28, 0xC8, 0x40)]):
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                     Inches(0.7 + i * 0.25), Inches(1.6),
                                     Inches(0.13), Inches(0.13))
        dot.fill.solid()
        dot.fill.fore_color.rgb = c
        dot.line.fill.background()

    add_textbox(slide, Inches(2.0), Inches(1.53), Inches(4.0), Inches(0.35),
                "claude — terminal", font_size=10, color=GRAY,
                alignment=PP_ALIGN.CENTER, font_name="Consolas")

    # Terminal content
    terminal_lines = [
        "$ claude",
        "",
        "> Create a Remotion video with animated title,",
        "  background music, and smooth transitions",
        "",
        "⠋ Analyzing project structure...",
        "✓ Created Root.tsx",
        "✓ Created Composition.tsx",
        "✓ Created AudioTrack.tsx",
        "✓ Installing dependencies...",
        "✓ npm install remotion @remotion/cli",
        "",
        "✨ Project ready! Run: npx remotion preview",
    ]
    add_multiline_textbox(slide, Inches(0.8), Inches(2.1), Inches(7.0), Inches(4.5),
                          terminal_lines, font_size=12, color=RGBColor(0xC5, 0xC1, 0xB9),
                          font_name="Consolas")

    # Files panel (right)
    add_rect(slide, Inches(8.3), Inches(1.5), Inches(4.5), Inches(5.5),
             DARK_PANEL2, border_color=RGBColor(0x30, 0x30, 0x30))

    add_textbox(slide, Inches(8.5), Inches(1.7), Inches(4.0), Inches(0.4),
                "PROJECT FILES", font_size=11, color=GREEN, bold=True,
                alignment=PP_ALIGN.LEFT, font_name="Consolas")

    files = [
        ("Root.tsx", "entry point", "{ }"),
        ("Composition.tsx", "animated title", "▶"),
        ("AudioTrack.tsx", "sound effects", "♪"),
        ("package.json", "dependencies", "◆"),
    ]

    for i, (name, desc, icon) in enumerate(files):
        fy = Inches(2.4 + i * 0.95)

        # File icon background
        icon_bg = add_rect(slide, Inches(8.6), fy, Inches(0.5), Inches(0.5),
                           RGBColor(0x1A, 0x2A, 0x1A), corner_radius=True)

        add_textbox(slide, Inches(8.6), fy, Inches(0.5), Inches(0.5),
                    icon, font_size=14, color=GREEN, alignment=PP_ALIGN.CENTER)

        add_textbox(slide, Inches(9.3), fy, Inches(3.0), Inches(0.3),
                    name, font_size=14, color=WHITE, bold=True,
                    alignment=PP_ALIGN.LEFT, font_name="Consolas")
        add_textbox(slide, Inches(9.3), fy + Inches(0.3), Inches(3.0), Inches(0.25),
                    desc, font_size=10, color=GRAY,
                    alignment=PP_ALIGN.LEFT, font_name="Consolas")


def slide_8_skills(prs):
    """Skills / Progress bar + capability pills"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)

    add_slide_number_label(slide, "מה זה Skills", top=Inches(0.5))
    add_slide_title(slide, "חבילות יכולות מובנות לסוכן", top=Inches(1.0), font_size=32)

    # Progress bar section
    bar_left = Inches(2.5)
    bar_width = Inches(8.3)
    bar_y = Inches(2.2)

    add_textbox(slide, bar_left, bar_y, Inches(5), Inches(0.4),
                "Installing remotion-skill...", font_size=14, color=WHITE,
                alignment=PP_ALIGN.LEFT, font_name="Consolas")
    add_textbox(slide, bar_left + Inches(6.5), bar_y, Inches(1.5), Inches(0.4),
                "100%", font_size=14, color=GREEN, bold=True,
                alignment=PP_ALIGN.RIGHT, font_name="Consolas")

    # Track background
    add_rect(slide, bar_left, bar_y + Inches(0.5), bar_width, Inches(0.3),
             RGBColor(0x2A, 0x2A, 0x2A))
    # Fill
    add_rect(slide, bar_left, bar_y + Inches(0.5), bar_width, Inches(0.3),
             GREEN)

    # Status
    add_textbox(slide, bar_left, bar_y + Inches(1.0), bar_width, Inches(0.4),
                "✔ Loaded 847 tools · ✔ Ready to render videos",
                font_size=12, color=GRAY, alignment=PP_ALIGN.LEFT,
                font_name="Consolas")

    # Capability pills
    pills = ["⟨/⟩  React", "⏱  Animation", "▶  Render", "♪  Audio"]
    pill_w = Inches(1.8)
    pill_h = Inches(0.55)
    total_pills_w = pill_w * 4 + Inches(0.3) * 3
    pills_start_x = (SLIDE_WIDTH - total_pills_w) // 2
    pill_y = Inches(4.0)

    for i, label in enumerate(pills):
        px = pills_start_x + (pill_w + Inches(0.3)) * i
        pill = add_rect(slide, px, pill_y, pill_w, pill_h,
                        DARK_PANEL2, border_color=GREEN_DIM, corner_radius=True)
        add_textbox(slide, px, pill_y + Inches(0.05), pill_w, pill_h,
                    label, font_size=13, color=GREEN,
                    alignment=PP_ALIGN.CENTER, font_name="Consolas")

    # GitHub link
    add_textbox(slide, Inches(3), Inches(5.0), Inches(7.3), Inches(0.4),
                "github.com/remotion-dev/skills",
                font_size=12, color=GRAY, alignment=PP_ALIGN.CENTER,
                font_name="Consolas")

    # Note
    add_textbox(slide, Inches(2), Inches(5.6), Inches(9.3), Inches(0.5),
                "Skill = מאות כלים שמאפשרים לסוכן לעבוד עם Remotion",
                font_size=14, color=GRAY, alignment=PP_ALIGN.CENTER)


def slide_9_checklist(prs):
    """Animated checklist (static version)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)

    add_slide_number_label(slide, "איך זה הולך לעבוד", top=Inches(0.8))
    add_slide_title(slide, "מה תדעו לעשות עד סוף הסרטון", top=Inches(1.3), font_size=32)

    items = [
        "התקנת Remotion",
        "יצירת פרויקט",
        "בניית אנימציה",
        "הוספת סאונד",
        "רינדור ויצוא MP4",
    ]

    list_x = Inches(4.0)
    list_w = Inches(5.5)
    item_h = Inches(0.65)
    start_y = Inches(2.5)

    for i, item in enumerate(items):
        y = start_y + item_h * i

        # Checkmark
        add_textbox(slide, list_x + Inches(4.2), y, Inches(0.5), item_h,
                    "✓", font_size=18, color=GREEN, bold=True,
                    alignment=PP_ALIGN.CENTER)

        # Item text
        add_textbox(slide, list_x, y, Inches(4.0), item_h,
                    item, font_size=20, color=WHITE,
                    alignment=PP_ALIGN.RIGHT)

    # Bottom line
    add_textbox(slide, Inches(3), Inches(5.8), Inches(7.3), Inches(0.5),
                "לא תיאוריה. בנייה אמיתית.",
                font_size=18, color=GREEN, bold=True,
                alignment=PP_ALIGN.CENTER)


def slide_10_demo(prs):
    """Live demo transition"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)

    add_textbox(slide, Inches(3), Inches(1.2), Inches(7.3), Inches(0.5),
                "LIVE DEMO", font_size=14, color=GREEN, bold=True,
                alignment=PP_ALIGN.CENTER)

    # Logos area
    # Remotion logo placeholder
    r_logo = add_rect(slide, Inches(4.0), Inches(2.0), Inches(1.5), Inches(1.5),
                      DARK_PANEL2, border_color=GREEN_DIM, corner_radius=True)
    add_textbox(slide, Inches(4.0), Inches(2.2), Inches(1.5), Inches(1.0),
                "R", font_size=36, color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(3.5), Inches(3.5), Inches(2.5), Inches(0.4),
                "Remotion", font_size=14, color=GRAY,
                alignment=PP_ALIGN.CENTER)

    # × separator
    add_textbox(slide, Inches(6.0), Inches(2.3), Inches(1.3), Inches(0.8),
                "×", font_size=28, color=GRAY, alignment=PP_ALIGN.CENTER)

    # Claude Code logo placeholder
    c_logo = add_rect(slide, Inches(7.8), Inches(2.0), Inches(1.5), Inches(1.5),
                      DARK_PANEL2, border_color=GREEN_DIM, corner_radius=True)
    add_textbox(slide, Inches(7.8), Inches(2.2), Inches(1.5), Inches(1.0),
                "A", font_size=36, color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(7.3), Inches(3.5), Inches(2.5), Inches(0.4),
                "Claude Code", font_size=14, color=GRAY,
                alignment=PP_ALIGN.CENTER)

    # Title
    add_textbox(slide, Inches(1.5), Inches(4.3), Inches(10.3), Inches(0.8),
                "עכשיו בונים את זה ביחד",
                font_size=36, color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)

    # Subtitle
    add_textbox(slide, Inches(2), Inches(5.2), Inches(9.3), Inches(0.6),
                "מפתחים את הסרטון הראשון שלכם — מפרומפט עד MP4",
                font_size=18, color=GRAY, alignment=PP_ALIGN.CENTER)

    # Arrow
    add_textbox(slide, Inches(6.0), Inches(6.0), Inches(1.3), Inches(0.6),
                "↓", font_size=32, color=GREEN, bold=True,
                alignment=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════

def main():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    slide_1_title(prs)
    slide_2_code_to_video(prs)
    slide_3_problem(prs)
    slide_4_solution(prs)
    slide_5_showcase(prs)
    slide_6_pipeline(prs)
    slide_7_terminal(prs)
    slide_8_skills(prs)
    slide_9_checklist(prs)
    slide_10_demo(prs)

    output_path = "presentation.pptx"
    prs.save(output_path)
    print(f"✓ Saved {output_path} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
