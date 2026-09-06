---
name: courseware-pptx
description: This skill should be used when generating classroom-ready PowerPoint (PPTX) courseware from structured Markdown lesson notes. Trigger phrases include "把 Markdown 课件做成 PPT", "制作上课用的 PPT", "把这份讲义转成幻灯片", "generate slides from lesson markdown", "make a PPT for teaching". It produces 16:9 PPTX files with a consistent Python-themed visual system (blue/yellow), supporting cover slides, agenda, section dividers, knowledge-point pages, code blocks (macOS terminal style), comparison tables, workflow diagrams, AI prompt pages, classroom exercises, summary, and Q&A.
agent_created: true
---

# Courseware Pptx

## Overview

Convert structured Markdown lesson notes into classroom-ready PPTX files using a consistent visual system. The skill wraps `python-pptx` with a Python-themed design language (blue `#306998` + yellow `#FFD43B`), standard page layouts, and reusable layout primitives.

## When to Use

Trigger when the user asks to turn Markdown teaching notes into slides:
- "制作上课的 PPT / 把 Markdown 转成 PPT / 生成幻灯片"
- Markdown contains structured sections like `### 知识点N`, `#### 🤖 AI辅助`, `## 课堂练习`
- Output must be `.pptx` (not Markdown preview, not PDF)

Do NOT use for: free-form brainstorms, single-page posters, data dashboards.

## Workflow

### Step 1 — Verify environment

Confirm python-pptx is available (use `uv run --with` so nothing is installed into the global environment):

```bash
uv run --with python-pptx python -c "import pptx; print(pptx.__version__)"
```

### Step 2 — Read source Markdown

Use `Read` tool to load the source `.md` file. Identify structural markers:
- `## 本周目标` → knowledge goals + AI-assisted goals (2-column card)
- `### 知识点N` → knowledge point group (multiple content slides + AI prompt slide)
- `#### 🤖 AI辅助` → AI prompt listing page
- `## 环境搭建实践` → experiment cards
- `## 课堂练习` → exercise grid

### Step 3 — Run the build script

The skill bundles `scripts/build_pptx.py` — a self-contained script whose slide content is written inline (the bundled version builds the Week 1 Python lesson). Either:

**Option A — Execute directly (preferred, no context cost):**

```bash
uv run --with python-pptx python <skill-dir>/courseware-pptx/scripts/build_pptx.py [output.pptx]
```

The output path defaults to the current working directory (`第1周_Python导论与环境搭建.pptx`); pass a path as the first argument to override.

**Option B — Read & adapt:** copy `scripts/build_pptx.py` into a scratch folder inside the current workspace and edit the `slide_*()` functions to match the new lesson's content structure. Re-run the script.

### Step 4 — Validate output

```bash
uv run --with python-pptx python -c "
from pptx import Presentation
p = Presentation(r'<output_path>')
print(f'Slides: {len(p.slides)}, size: {p.slide_width/914400:.2f}x{p.slide_height/914400:.2f} in')
"
```

Expected: 20–30 slides, 13.33 x 7.5 inches (16:9).

### Step 5 — Present to user

Report the output PPTX path to the user. Do not write to locations outside the user's designated output folder unless they ask.

## Visual System (reference: `references/style-guide.md`)

Hard rules for any new slide function:

1. **Page size:** 13.333 x 7.5 inches (`Inches(13.333)`, `Inches(7.5)`), blank layout.
2. **Page header on every content slide:** left blue bar (`Inches(0.25)` wide, `PY_BLUE`), course name top-left, section label top-right, page number `XX / NN` top-right corner, footer blue strip at bottom.
3. **Section title:** yellow accent bar (12pt wide, 70pt tall) + 32pt bold blue title + 14pt gray subtitle.
4. **Section dividers:** left half filled with section color, giant 160pt white number on left, yellow accent + 36pt title on right.
5. **Cards:** white fill, `#DDE3EA` border, corner radius 0.04–0.08.
6. **Code blocks:** macOS terminal style — dark `#2B3A45` background, red/yellow/green dots, filename tab, `Consolas` 11–13pt.
7. **Bullets:** blue dot for content lists, orange dot for AI-prompt sections.
8. **Colors:** `PY_BLUE #306998`, `PY_BLUE_LIGHT #4B8BC8`, `PY_YELLOW #FFD43B`, `PY_DARK #1E2A38`, `PY_GRAY #5A6673`, `PY_BG_LIGHT #F5F7FA`, `PY_CODE_BG #2B3A45`.
9. **Fonts:** `Microsoft YaHei` for Chinese, `Consolas` for code, always set `a:ea` typeface in XML for Chinese rendering.
10. **Total slide count:** aim for 25–30 slides per lecture; one knowledge point ≈ 3–5 slides + 1 AI prompt slide.

## Slide Type Catalog

| Type | Function | Use For |
|------|----------|---------|
| Cover | `slide_cover()` | First slide: course title, week number |
| Goals | `slide_goals()` | Knowledge + AI-assisted learning objectives |
| Agenda | `slide_agenda()` | Timeline preview of all knowledge points |
| Divider | `slide_section_divider(no, title, subtitle, color)` | Between major sections |
| Concept | `slide_concept()` | Single-topic explanation with sidebar |
| Compare Table | `slide_compare_table()` | Multi-row × multi-column comparison |
| Code Blocks | `slide_code_compare()` / `slide_code_example()` | Side-by-side language comparison or single demo |
| Applications | `slide_applications()` | 3×3 grid of application areas with icons |
| Workflow Steps | `slide_workflow_steps()` | Horizontal numbered steps |
| Comparison Pair | `slide_pip_vs_uv()` etc. | Two cards side-by-side with table |
| Cheatsheet | `slide_cheatsheet()` | Two-column reference list |
| Exercises | `slide_exercises()` | 2×2 or 1×4 task grid |
| Summary | `slide_summary()` | Recap of all knowledge points |
| Q&A | `slide_qa()` | Closing slide with quote |

## Common Pitfalls (learned from Week 1 build)

1. **Chinese quotation marks in Python strings:** `"…"` inside a `"…"` delimited string terminates the string. Replace with corner brackets `「…」` or single quotes `''`.
2. **`add_text()` does not accept `line_spacing`** unless extended — the bundled script extends it; if you write a new helper, mirror the signature.
3. **Console stdout encoding on Windows:** emoji/Chinese in `print()` triggers `UnicodeEncodeError`. Call `sys.stdout.reconfigure(encoding='utf-8')` before printing, or restrict terminal output to ASCII.
4. **Page counter must be a list** (`[0]`) — ints are immutable in closures; using a list lets `add_page_header()` and `add_footer()` increment correctly.
5. **Empty bullet labels:** when a knowledge point has no native marker, use emoji + space prefix (`🎯  `).
6. **Section divider page counter:** `slide_section_divider()` does NOT call `add_page_header()`, so increment `page_counter[0]` manually inside it.

## Resources

### scripts/
- `build_pptx.py` — Full build script for Week 1 (Python course). Execute directly or copy to scratch folder and adapt `slide_*()` functions for new lessons.

### references/
- `style-guide.md` — Detailed visual system specs: color tokens, typography, spacing, layout grid, code block spec, bullet conventions.

### assets/
- Empty by default. Drop in template `.pptx` files here if you build reusable section/cover templates later.