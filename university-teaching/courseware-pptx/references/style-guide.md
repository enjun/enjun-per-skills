# Courseware PPTX — Style Guide

Design system reference for the Python-themed courseware PPTX skill. All numbers are inches unless noted.

## 1. Page Setup

| Property | Value |
|----------|-------|
| Slide size | 13.333 × 7.5 in (16:9) |
| Layout | blank (no master) |
| Background | white `#FFFFFF` for content; section color for dividers/cover |

```python
from pptx import Presentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SLIDE_W, SLIDE_H = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]
```

## 2. Color Tokens

| Token | RGB | Usage |
|-------|-----|-------|
| `PY_BLUE` | `#306998` | Primary brand color, headers, divider blocks |
| `PY_BLUE_LIGHT` | `#4B8BC8` | Secondary accent, AI prompts, lower-emphasis titles |
| `PY_YELLOW` | `#FFD43B` | Accent bars, badges, highlights |
| `PY_DARK` | `#1E2A38` | Primary text |
| `PY_GRAY` | `#5A6673` | Secondary text, captions |
| `PY_BG_LIGHT` | `#F5F7FA` | Alternating row backgrounds, code block page bg |
| `PY_WHITE` | `#FFFFFF` | Card backgrounds |
| `PY_CODE_BG` | `#2B3A45` | Code block background |
| `PY_CODE_FG` | `#E8E8E8` | Code block text |
| `PY_ACCENT_GREEN` | `#37B24D` | Success, positive (Python) |
| `PY_ACCENT_RED` | `#E64A4A` | Errors, warnings |
| `PY_ACCENT_ORANGE` | `#F59E42` | AI prompt sections, call-outs |

Section accent assignments:
- PART 01 → `PY_BLUE`
- PART 02 → `PY_BLUE_LIGHT`
- PART 03 → `PY_YELLOW`
- PART 04 → `PY_ACCENT_GREEN`
- PART 05 → `PY_ACCENT_ORANGE`

## 3. Typography

| Role | Font | Size | Color | Weight |
|------|------|------|-------|--------|
| Page title | Microsoft YaHei | 32 pt | `PY_BLUE` | bold |
| Subtitle | Microsoft YaHei | 14 pt | `PY_GRAY` | regular |
| Section title | Microsoft YaHei | 36 pt | `PY_DARK` | bold |
| Section giant number | Microsoft YaHei | 160 pt | `PY_WHITE` | bold |
| Card title | Microsoft YaHei | 16–18 pt | `PY_DARK` | bold |
| Body bullet | Microsoft YaHei | 13–15 pt | `PY_DARK` | regular |
| Code | Consolas | 10–13 pt | `PY_CODE_FG` | regular |
| Cover main | Microsoft YaHei | 54 pt | `PY_WHITE` | bold |
| Q&A quote | Microsoft YaHei | 30 pt | `PY_BLUE` | bold |
| Page meta | Microsoft YaHei | 10 pt | `PY_GRAY` | regular |

**Chinese rendering:** always set both `font.name` and the `a:ea` (East Asian) typeface via XML:

```python
from lxml import etree
from pptx.oxml.ns import qn
rPr = run._r.get_or_add_rPr()
ea = rPr.find(qn('a:ea'))
if ea is None:
    ea = etree.SubElement(rPr, qn('a:ea'))
ea.set('typeface', 'Microsoft YaHei')
```

## 4. Spacing & Layout Grid

- **Safe area:** left `0.6 in`, right `0.6 in`, top `1.85 in`, bottom `0.04 in`
- **Page header band:** `0 – 0.5 in` (course name + section + page number)
- **Section title row:** `0.7 – 1.65 in` (yellow bar + title + subtitle)
- **Content area:** `1.85 – 6.95 in`
- **Footer:** `7.46 – 7.5 in` (4 pt blue strip)

## 5. Page Header Spec

Every content slide calls `add_page_header(slide, page_no, total, section)`:

```
┌─────────────────────────────────────────────────────┐
│█  Python 语言程序设计 · 第 1 周    [小节]    NN/TOTAL│
│                                                     │
│  ← 0.25 in blue bar runs full height               │
│                                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 6. Section Title Spec

```
0.6 in → [█ 12pt 70pt] ← yellow accent
0.85 in → "32 pt bold blue title" 
         "14 pt gray subtitle"
```

## 7. Card Spec

- Fill: `PY_WHITE`
- Border: `RGBColor(0xDD, 0xE3, 0xEA)`, 0.75 pt
- Corner radius: 0.04–0.08 (rounded rectangle)
- Optional: 0.12 in wide colored left bar for visual category
- Optional: 0.7 in top color block as title strip

## 8. Code Block Spec (macOS Terminal)

```
┌────────────────────────────────────────────────┐
│ ●●●  filename.py                                │  ← title bar 0.32 in
├────────────────────────────────────────────────┤
│ # comment in gray                               │
│ def function():                                 │  ← body PY_CODE_BG
│     return result                               │     Consolas 11–13 pt
└────────────────────────────────────────────────┘
```

- Title bar: `PY_CODE_BG`, red `#FF5F56` / yellow `#FFBD2E` / green `#27C93F` dots (0.13 in diameter, gap 0.18 in)
- Filename label: `RGBColor(0xB8, 0xC2, 0xCC)`, 11 pt
- Body: `PY_CODE_BG` bg, `PY_CODE_FG` fg, Consolas 11–13 pt, line_spacing 1.15

## 9. Bullet Convention

- Default content lists: `●` blue dot (`PY_BLUE_LIGHT`)
- AI prompt sections: `●` orange dot (`PY_ACCENT_ORANGE`)
- Line spacing: 1.25 (single-level), 1.4–1.5 (multi-paragraph cards)
- Bold inline: wrap text in `**…**` in source list; the helper splits and bolds alternating segments

## 10. Table Spec

- Header row: `PY_BLUE` fill, white text 14–15 pt bold
- Body rows: alternating `PY_WHITE` / `PY_BG_LIGHT`
- Row height: 0.45–0.62 in
- Border: `RGBColor(0xE5, 0xE9, 0xEF)`, 0.75 pt
- Cell padding: left/right `0.1 in`, vertical centered (`MSO_ANCHOR.MIDDLE`)

## 11. Helper Function Reference

| Function | Purpose |
|----------|---------|
| `add_rect(x,y,w,h,fill,line=None,shadow=False)` | Plain rectangle |
| `add_round_rect(x,y,w,h,fill,line=None,corner=0.08)` | Rounded card; `corner` 0.04–0.1 |
| `add_text(x,y,w,h,text,size,bold,color,align,anchor,font,line_spacing=1.2)` | Textbox with East Asian font setup |
| `add_bullets(x,y,w,h,items,size,color,line_spacing,bullet,bullet_color)` | Bulleted list; items may be `tuple(main, sub)` or `str` with `**bold**` markers |
| `add_code_block(x,y,w,h,code,size,lang)` | macOS terminal-style code block |

## 12. Section Divider Page Spec

```
┌──────────────────┬────────────────────────────┐
│ ████             │                            │
│ ████  PART       │   [█ 12pt] 36 pt title     │
│ ████             │   16 pt gray subtitle      │
│ ████             │                            │
│ ████ 160 pt      │                            │
│ ████  white      │                            │
│ ████  number     │                            │
│ ████             │                            │
└──────────────────┴────────────────────────────┘
   left half = section color     right = white bg
```

## 13. Cover Page Spec

- Full bleed `PY_BLUE`
- Two decorative right triangles in `PY_BLUE_LIGHT` and `PY_YELLOW`
- "WEEK 01" small caps 20 pt yellow
- Main title 54 pt white, 2-line
- Yellow 1.2 in × 0.06 in separator
- English subtitle 18 pt yellow, course tag 16 pt light gray
- Bottom: teacher credit 12 pt yellow

## 14. Do / Don't

✅ DO: Use cards with consistent corner radius and border color across one deck.
✅ DO: Keep one accent color per section divider for visual hierarchy.
✅ DO: Set `a:ea` typeface for every Chinese text run.
❌ DON'T: Mix two corner radii in the same row of cards.
❌ DON'T: Use emoji inside table cells (alignment breaks).
❌ DON'T: Use Chinese double quotes `"…"` inside Python string literals — use `「…」`.