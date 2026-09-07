---
name: courseware-pptx
description: This skill should be used when generating classroom-ready PowerPoint (PPTX) courseware from structured lesson content. Trigger phrases include "把课件做成 PPT", "制作上课用的 PPT", "把这份讲义转成幻灯片", "generate slides from lesson markdown", "make a PPT for teaching". It is JSON-driven: author a content JSON (17 layout types), run the bundled engine, and get a 16:9 PPTX with a consistent Python-themed visual system (blue/yellow) supporting covers, agenda, section dividers, knowledge-point pages, macOS-style code blocks, comparison tables, workflow diagrams, AI prompt pages, exercises, summary, and Q&A.
agent_created: true
---

# Courseware Pptx

## Overview

Convert structured lesson notes into classroom-ready PPTX via a JSON-driven engine. The skill separates **content** (a JSON file you author) from **layout** (`scripts/build_pptx.py`, a generic python-pptx engine with 17 slide types and a Python-themed visual system: blue `#306998` + yellow `#FFD43B`). New lessons = new JSON, no code changes.

## 内容保真规则（必须遵守）

1. **不允许修改原内容**：源笔记里的代码、表格、提示、blockquote、AI Prompt 一律原样搬运——不改写、不缩写、不"概括"、不删注释。只允许调整**呈现位置和分页**。
2. **完整展现所有原内容**：源笔记的每一个知识点、每一段代码、每一条提示都必须出现在 PPT 里。放不下就**加页**，不是删内容。
3. 允许的"胶水"仅限：页面标题、`section` 标识、卡片标题、agenda/sidebar、导航性短语（如"接下页"）、以及 code_compare 页对代码结论的中性复述。不得借胶水引入源笔记没有的知识性断言。

## 长代码分页规则

一页代码容量参考（可用高度 ≈ 4.2“，行距 1.15，行高 ≈ size×1.38/72 英寸）：

| 容器 | 代码区宽×高 | 11pt 最多行数 | 10pt 最多行数 |
|---|---|---|---|
| `code_full`（整页） | 12.15"×~5.3" | 23 行 | 26 行 |
| `code_demo`（右侧代码块） | 7.65"×4.7" | 17 行 | 20 行 |
| `two_cards` 卡片（6.0" 宽） | 5.4" 宽 | 16 行 | 18 行 |
| `code_compare` 卡片 | 3.7"×3.75"（11pt 固定） | 15 行 | – |

代码超过容器容量时：
1. 在**逻辑边界**（空行、注释分组、函数边界）拆成连续多页/多卡；
2. 文件名标签标注 `xxx.py（1/2）`、`xxx.py（2/2）`，页面标题加「（上）」「（下）」或「（续）」；
3. **绝不为塞进一页而删代码行或缩短注释**。

实战示例：`examples/week2_python_core_syntax.json` 中 31 行的 `demo_control_flow()` 拆成（上）（下）两页连续展示。

## When to Use

Trigger when the user asks to turn teaching notes into slides:
- "制作上课的 PPT / 把讲义转成 PPT / 生成幻灯片"
- Source is structured Markdown or any lesson notes with knowledge points, code examples, exercises
- Output must be `.pptx` (not Markdown preview, not PDF)

Do NOT use for: free-form brainstorms, single-page posters, data dashboards.

## Workflow

### Step 1 — Verify environment

```bash
uv run --with python-pptx python -c "import pptx; print(pptx.__version__)"
```

### Step 2 — Read source lesson notes

Use `Read` to load the source Markdown/notes. Map its structure to slide types: goals → `two_cards`, 知识点 sections → dividers + concept/table/code pages, AI 提示 → `ai_prompts`, 实验/练习 → `exercise_grid`, 小结 → `summary`. 遵守上方内容保真规则：先盘点源内容清单（每个代码块、提示、表格），确保 JSON 里一样不少。

### Step 3 — Author the content JSON

Write a content JSON following `references/schema.md`:

- Top level: `course`, `week`, `output`, `slides[]`
- Pick types from the 17-type catalog; colors as palette names only (`blue`, `yellow`, `green`, `red`, `orange`, `purple`, `gray`, …) — never hex
- Give `code` blocks and long `bullets` blocks explicit `height` (inches) to avoid overflow
- Reference implementations: `examples/week1_python.json` (28 slides, 16 of 17 types) and `examples/week2_python_core_syntax.json` (46-slide real lesson, 内容保真 + `code_full` 长代码分页) — copy and adapt

### Step 4 — Run the engine

```bash
uv run --with python-pptx python <skill-dir>/courseware-pptx/scripts/build_pptx.py content.json [output.pptx]
```

Output defaults to the JSON's `output` field (relative to the JSON's folder), else `<json-stem>.pptx` beside it.

### Step 5 — Validate

```bash
uv run --with python-pptx python -c "
from pptx import Presentation
p = Presentation(r'<output_path>')
print(f'Slides: {len(p.slides)}, size: {p.slide_width/914400:.2f}x{p.slide_height/914400:.2f} in')
"
```

Expected: slide count equals `len(slides)` in the JSON; 13.33 x 7.5 inches (16:9). Engine errors are printed as `[ERROR] slide N (type X): ...` — fix the JSON per the message and re-run.

### Step 6 — Present to user

Report the output PPTX path to the user. Do not write to locations outside the user's designated output folder unless they ask.

## Slide Type Catalog

| Type | Use For |
|------|---------|
| `cover` | First slide: kicker, title, EN subtitle, credit |
| `divider` | Section divider: giant number + title |
| `agenda` | Vertical timeline + 学习节奏 sidebar |
| `two_cards` | Any two side-by-side cards (goals, comparisons, cheatsheets) — composable content blocks |
| `story_person` | History story card + person/profile card |
| `table` | Full-width data table with header row + optional note bar |
| `stats` | Stat card row + blue banner with icon columns |
| `ai_prompts` | Copy-paste AI prompt list with orange tag pills |
| `code_compare` | 2–3 language cards side-by-side + bottom notes |
| `code_demo` | Narrow scenario card + big code block |
| `code_full` | Full-width single code block for long listings; split long code across consecutive `code_full` pages instead of trimming it |
| `icon_grid` | 3×N icon application/feature grid |
| `steps` | Horizontal numbered workflow cards (optional URLs) |
| `cards_flow` | Two half-cards + 6-step mini flow with arrows |
| `exercise_grid` | 2×2 exercise cards with time pills |
| `summary` | Numbered recap cards + preview banner |
| `qa` | Closing Q&A + quote of the day |

Content-block kinds inside cards: `bullets`, `code`, `text`, `table`, `callout`, `kv_code`, `tagged_items`.

## Common Pitfalls

1. **JSON escaping:** Windows backslash paths need `\\` (e.g. `".venv\\Scripts\\activate"`); prefer corner brackets `「…」` over English double quotes in Chinese content to avoid escape noise.
2. **Console encoding:** the engine self-configures UTF-8 stdout, but your own ad-hoc validation one-liners printing Chinese/emoji on Windows need `sys.stdout.reconfigure(encoding='utf-8')` first.
3. **No hex in slide data:** use palette names; re-theme only via top-level `palette` override.
4. **Explicit heights:** `code` blocks and bullets blocks with many/wrapping items should declare `height` (inches) — the auto-estimate can overflow the card.
5. **Empty bullet emphasis:** items with no natural bold lead can use an emoji + space prefix (`"🎯  …"`).
6. **Emoji width:** emojis render at font size; oversized icons (44pt) need generous box heights — copy geometry from the week1 example when unsure.
7. **Code fidelity under page limits:** when a code block exceeds its container (see 长代码分页规则), split across consecutive pages with `（1/2）` filename labels — never delete lines, shorten comments, or "simplify" the sample to make it fit.
8. **Content block kinds in card tables:** `table` blocks inside cards and `table` slides render cell text literally — `**bold**` and backticks are NOT parsed there; use `{"text": ..., "bold": true}` dict cells instead.

## Resources

### scripts/
- `build_pptx.py` — Generic JSON-driven engine (17 slide types, palette system, block renderer). Zero lesson content inside; never edit it to change a lesson.

### references/
- `schema.md` — Full JSON schema: top-level fields, Card spec, 7 content-block kinds, all 17 slide types with field tables.
- `style-guide.md` — Visual system specs: color tokens, typography, spacing, layout grid, code block spec.

### examples/
- `week1_python.json` — Complete 28-slide reference deck (Python 导论与环境搭建) covering 16 of the 17 slide types; the layout-catalog template.
- `week2_python_core_syntax.json` — 46-slide real lesson (Python 核心语法) demonstrating 内容保真规则 and long-code splitting via `code_full`（1/2）（2/2）pages.
