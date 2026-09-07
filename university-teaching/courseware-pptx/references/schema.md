# courseware-pptx JSON Schema 参考

引擎 `scripts/build_pptx.py` 从 JSON 课件数据生成 16:9 教学 PPT。完整可运行的示例见 `examples/week1_python.json`（28 页，覆盖 16/17 种版式）与 `examples/week2_python_core_syntax.json`（46 页真实课程：内容保真 + `code_full` 长代码分页）。

## 内容保真与长代码分页

- **原样搬运**：源笔记的代码、表格、blockquote、AI Prompt 不改写、不缩写、不删注释；只调整呈现位置与分页。
- **放不下就加页**：代码超过容器容量时，在逻辑边界（空行/注释分组/函数边界）拆成连续多页，文件名标注 `xxx.py（1/2）`、`（2/2）`，标题可加「（上）」「（下）」「（续）」。
- 容量参考（代码行高 ≈ size×1.38/72 英寸，代码块头部 +0.47"）：

| 容器 | 代码区 | 11pt 最多行数 | 10pt 最多行数 |
|---|---|---|---|
| `code_full` | 12.15"×~5.3" | 23 | 26 |
| `code_demo` 右侧代码 | 7.65"×4.7" | 17 | 20 |
| `two_cards` 卡片（默认 6.0" 宽） | 5.4" 宽 | 16 | 18 |
| `code_compare` 卡片 | 3.7"×3.75"（11pt 固定） | 15 | – |

## 顶层结构

```json
{
  "course": "Python 语言程序设计",
  "week": "第 1 周",
  "output": "第1周_Python导论与环境搭建.pptx",
  "palette": { "blue": "#306998" },
  "slides": [ { "type": "...", "...": "..." } ]
}
```

| 字段 | 必填 | 说明 |
|---|---|---|
| `course` | ✓ | 页眉课程名（左上） |
| `week` | ✓ | 页眉周次；页眉课程行渲染为 `course  ·  week` |
| `output` | – | 默认输出文件名（相对 JSON 所在目录）；也可用 CLI 第二参数覆盖 |
| `palette` | – | 覆盖主题色，`色名 → #RRGGBB`；一般不用 |
| `slides` | ✓ | 幻灯片列表，顺序即页序；页码 = 数组位置（cover 和 qa 占位但不显示页码） |

## 内容页公共字段

除 `cover` / `divider` / `qa` 外，所有 type 都支持：

| 字段 | 说明 |
|---|---|
| `section` | 页眉右上小节标识（如 `"知识点 1  ·  Python 发展史"`） |
| `title` | 大标题（32pt 蓝色粗体 + 左侧黄色竖条） |
| `subtitle` | 大标题下灰色副标题 |

## 颜色约定

JSON 中**只允许 palette 名字符串**，禁止 hex：

`blue` `blue_light` `yellow` `dark` `gray` `bg_light` `white` `code_bg` `code_fg` `green` `red` `orange` `purple`

## 富文本约定

| 场景 | 写法 | 效果 |
|---|---|---|
| 普通文本/单元格 | `"纯文本"` | 默认样式 |
| 富单元格 | `{"text": "...", "color": "blue", "bold": true}` | 自定义样式 |
| 列表项（含局部加粗） | `"a **加粗** b"` | `**` 内加粗 |
| 列表项（主 + 副文本） | `{"main": "粗体引导", "sub": "灰色小字"}` | main 粗体 + sub 灰色小一号 |
| 多行文本 | `"line1\nline2"` | 按行分段 |

注意：JSON 内的反斜杠需转义（`".venv\\Scripts\\activate"`）；中文内容里的英文双引号建议改用「」避免转义。

## 卡片（Card）规格

`two_cards` 的 `cards`、`code_demo` 的 `scenario`、`cards_flow` 的 `top_cards` 共用 Card 结构：

```json
{
  "style": "header",
  "accent": "blue",
  "title": "📘 知识目标",
  "title_size": 18,
  "title_color": "white",
  "header_h": 0.7,
  "badge": { "text": "5", "bg": "yellow", "fg": "blue" },
  "height": 4.7,
  "bg": "bg_light",
  "blocks": [ ... ]
}
```

| 字段 | 适用 style | 说明 |
|---|---|---|
| `style` | 全部 | `header`（彩色顶栏）/ `strip`（左侧细色条）/ `plain`（纯底色） |
| `accent` | header / strip | 强调色（顶栏或色条） |
| `title` | 全部 | 卡片标题 |
| `title_size` | 全部 | 标题字号；header 默认 17（header_h≥0.7 时）或 15，strip 默认 15，plain 默认 14 |
| `title_color` | 全部 | 标题颜色；header 默认 white，strip/plain 默认 accent 蓝 |
| `header_h` | header | 顶栏高度，默认 0.7（紧凑卡用 0.5） |
| `badge` | header | 圆形徽章 `{text, bg, fg}`（如数量角标 "5"、"AI"） |
| `height` | cards_flow 卡片 | 卡片高度；two_cards 用 slide 级 `height`（默认 4.7） |
| `bg` | plain | 底色，默认 `bg_light` |
| `blocks` | 全部 | 内容块列表，自上而下排流 |

## 内容块（blocks）规格

| kind | 字段 | 说明 |
|---|---|---|
| `bullets` | `items[]`、`size?`=15、`line_spacing?`=1.45、`bullet_color?`="blue_light"、`height?` | 圆点列表，items 用富文本约定 |
| `code` | `code`、`label?`="python"、`size?`=12、`height` | macOS 终端风格代码块，label 是标签页文件名；**强烈建议给 height** |
| `text` | `text`、`size?`=12、`bold?`、`color?`="dark" | 小段文字，支持 `**bold**` |
| `table` | `rows[][]`、`widths[]`(英寸)、`row_h?`=0.34、`size?`=11、`col_styles?[]` | 卡片内简易表格；col_styles 逐列默认样式 |
| `callout` | `text`、`height?`=0.85 | 黄底圆角提示条，居中蓝色粗体 |
| `kv_code` | `rows[]` `[label, command]`、`row_h?`=0.42 | 速查表：斑马行 + 深色等宽代码药丸 |
| `tagged_items` | `items[]` `{tag, title, text}`、`tag_color?`="green"、`item_h?`=1.25 | 标签条目列表（如实验列表） |

排流：块从标题区下方开始依次向下排，块间距 0.15"；显式 `height` 优先于估算。**code 和多行 bullets 务必给显式 height**，否则可能溢出卡片。

## 16 种版式类型（+ code_full 共 17 种）

### 1. `cover` 封面
`kicker`✓（如 "WEEK 01"）、`title_lines`✓（1–2 行主标题）、`subtitle`✓（英文副题）、`course_line`?（默认 `course · week`）、`credit`✓（底部信息行）。

### 2. `divider` 章节分隔
`no`✓（"01" 大字）、`title`✓、`subtitle`✓、`color`✓（左半屏色块）。

### 3. `agenda` 时间线导览
`items`✓：4–6 个 `{no, title, desc, color}`；`sidebar`✓：`{heading, steps[]}`（步骤自动用 ↓ 连接）。

### 4. `two_cards` 双卡片
`cards`✓：恰好 2 个 Card；`widths?`=[6.0, 5.9]（英寸，如 [7.5, 4.45] 可做宽窄卡）；`height?`=4.7。

### 5. `story_person` 故事 + 人物卡
`story`✓：`{headline, lead, bullets[], bullet_color?}`；`person`✓：`{avatar, name, role, quote}`（蓝色人物卡 + 黄色头像圈 + 白色引言框）。

### 6. `table` 数据表
`headers`✓（富单元格）、`rows`✓、`widths`✓（英寸，**总和应为 12.15**）、`aligns?`（"left"/"center" 逐列）、`first_col_bold?`、`col_styles?`（逐列默认样式）、`row_h?`=0.55、`header_h?`=0.5、`note?`（底部黄边提示条）。

### 7. `stats` 数据卡 + 横幅
`cards`✓：3 个 `{icon, title, desc, color}`；`banner`✓：`{heading, items[]}`，items 为 3–5 个 `{icon, title, desc}`。

### 8. `ai_prompts` Prompt 列表
`box_title?`（默认 "💬  推荐 Prompt"）、`prompts`✓：3–6 个 `{label, text}`（橙色标签药丸 + 分隔线）。

### 9. `code_compare` 多语言代码对比
`cards`✓：2–3 个 `{lang, filename, color, code}`；`notes`✓：底部说明 `{icon, text, color?}`。

### 10. `code_demo` 场景 + 大代码块
`scenario`✓：一个 Card（窄左卡）；`code`✓：`{code, filename, size?=10}`（宽右块，7.65"×4.7"，10pt 约 20 行、11pt 约 17 行）。

### 10b. `code_full` 整页代码块
`code`✓：`{code, filename?, size?=11, height?}`（默认高度按行数自动估算，12.15" 全宽）。超长代码拆成连续多页（见页首「长代码分页」），不要删行。

### 11. `icon_grid` 图标网格
`items`✓：N 个 `{icon, title, desc, color}`（desc 可含 `\n`）；`cols?`=3。

### 12. `steps` 横向步骤
`steps`✓：3–5 个 `{no, title, desc, color, url?}`（编号圆 + 顶部色块 + 可选底部 URL）。

### 13. `cards_flow` 双卡 + 步骤流
`top_cards`✓：2 个 Card（常为 strip 风格，`height`=2.0）；`flow`✓：`{title, steps[6]}`，steps 为 `{title, code}`（Step N 小卡 + 箭头连接）。

### 14. `exercise_grid` 练习网格
`items`✓：4 个 `{label, title, desc, time, color}`（2×2 卡片 + 时间药丸）。

### 15. `summary` 总结 + 预告
`items`✓：4–5 个 `{no, title, desc, color}`（编号圆卡片）；`banner`✓：`{label, lines[]}`（蓝色预告横幅）。

### 16. `qa` 结束页
`headline`✓、`sub_cn`✓、`sub_en`✓、`thanks`✓；`quote`✓：`{label, en, cn, attribution}`；`resources`✓：`{label, text}`。

## 运行

```bash
uv run --with python-pptx python <skill>/scripts/build_pptx.py <content.json> [output.pptx]
```

输出解析顺序：CLI 参数 → JSON `output` 字段（相对 JSON 目录）→ 与 JSON 同名 `.pptx`。

校验错误会以 `[ERROR] slide N (type X): ...` 形式指出页序号和字段名，按提示修 JSON 即可。
