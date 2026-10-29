---
name: pdf2obsidian
description: 把 Zotero 中的 PDF 文献解析为 Markdown 并摄入 Obsidian 知识库。链路：Zotero 取 PDF → ocr-parse 技能解析 → 存入 raw/papers 分类目录 → 按知识库 CLAUDE.md 的 Ingest 工作流建 wiki 页面并记账。当用户要求"把论文入库/摄入知识库/解析后存入Obsidian"并给出 Zotero 条目时手动调用。
disable-model-invocation: true
argument-hint: [论文标题/作者/DOI/Zotero集合名，可多篇]
---

> **本技能仅限用户手动调用**（`disable-model-invocation: true` 已使其对模型不可见）：单篇涉及 GPU OCR（IEEE 双栏约 150~230 秒/页）与知识库深度摄入，耗时约 1 小时/篇、token 消耗大。

# PDF → Obsidian 知识库入库

把 Zotero 中的论文 PDF 解析为 Markdown，存入 Obsidian 知识库 `raw/papers/`，随后执行知识库定义的摄入（Ingest）流程。

流程总览：**取 PDF（Zotero）→ 解析（ocr-parse 技能）→ 归档（raw/papers）→ 摄入（Ingest）**。

## 第 0 步：确定知识库路径

- 从当前工作目录开始逐层向上查找：若某层目录**自身**同时包含 `raw/papers/`、`wiki/` 与定义知识库 Schema 的 `CLAUDE.md`，该目录即知识库根目录。
  - **找到** → 直接使用，**不要**询问路径。
  - **未找到** → 用 AskUserQuestion 询问用户知识库的绝对路径，确认后验证该目录下存在 `raw/papers/`、`wiki/`、`CLAUDE.md`。

## 第 1 步：收集论文清单

用户可提供：论文标题（全称或部分）、作者、DOI、Zotero 分类集合名，或其组合，一次任意多篇。给出集合名时，用 `zotero_get_collection_items` 展开为该集合下的全部论文。逐篇在 Zotero 中检索确认元数据（标题、第一作者、年份），组成处理队列并展示——**展示后直接开始处理，不等待确认**；检索不到的条目记录原因后从队列剔除。

**队列查重（逐篇，开工前必做）**：检查知识库中是否已有该文献的解析文件，两路并查——

```
1. 文件名匹配（按命名规则找候选目录）:
   find <知识库>/raw/papers -type d -iname "<第一作者姓氏>*<年份>"

2. 内容匹配（标题特征词检索正文）:
   grep -ril "<标题特征词>" <知识库>/raw/papers --include="paper_context.md"
```

- 内容匹配取标题中**若干特征词的连续片段**（避开冠词与常见介词；OCR 可能引入断行或大小写差异，片段宜短、配合 `-i`）；`paper_context.md` 的"标题"字段与 `paper.md` 首行 `# 标题` 均含全文标题。
- 两路均无命中 → 正常处理。
- 任一路有命中 → 读取候选目录的 `paper_context.md`，比对标题/DOI 确认是否同一篇（特征词也可能出现在其他论文的引述中，**必须二次确认**）：
  - **同一篇 → 跳过该篇**，不重复解析与摄入，记入"已存在"清单；
  - 非同一篇 → 视为不同文献，正常处理（命名冲突按第 4.2 步加 `_2` 后缀）。

## 第 2 步：从 Zotero 获取 PDF

```
1. 检索: zotero_search_items(query="<标题或作者>")
   → 得到父条目 key（如 "P9KCJ6HN"）

2. 取附件: zotero_get_item_children(item_key="<父条目key>")
   → 得到 PDF 附件 key（如 "MVXCKSAX"）

3. 取本地路径:
   curl -s http://localhost:23119/api/users/0/items/<附件key> | grep -oP '"href"\s*:\s*"\K[^"]+' | grep -i pdf

4. 复制到临时目录: cp "<取到的路径>" <临时目录>/paper.pdf
```

- 有多个 PDF 附件时，默认取最近修改的一个；无法判断时 AskUserQuestion 请用户定。
- 第 3 步取不到本地路径（本地 API 未开启、链接附件无本地文件等）→ 报告用户，请其确认 Zotero 附件状态后重试或跳过该篇。

临时目录自建自清（如 `./pdf2obsidian-tmp/<目录名>/`），全部处理完成后删除。

## 第 3 步：调用 ocr-parse 技能解析

- 用 Skill 工具调用 `ocr-parse` 技能，向其传入：PDF 绝对路径、输出位置（临时目录下 `<ASCII短名>.md`）。
- ocr-parse 技能全权负责：部署检查、GPU 服务启停（用完必须关）、逐页 OCR、整理交付。不要跳过或代做其内部步骤。
- **解析交付的 md 即最终版本：排版、公式均已正确，不再做任何清洗、修公式或结构调整。**
- **交付核对（防串稿，必做）**：拿到交付 md 后，检查首个 `#` 标题行与目标论文标题（以 Zotero 元数据为准）是否一致。服务器端脚本写死旧论文输出名时会出现"日志报 ALL_DONE、交付的却是旧论文"的假完成——标题不符则**不归档**，按解析失败处理并向用户报告。此为身份核对，不属于内容清洗，与上一条不冲突。

## 第 4 步：归档到 raw/papers

### 4.1 选分类目录

- `ls <知识库>/raw/papers/` 查看现有分类（一级目录，如 `BD-RIS`、`codebook-design`、`beamforming`；部分分类下还有二级子目录，如 `BD-RIS/optimization-problem`）。
- 根据论文主题**自主选择最合适的现有分类**（含子目录层级）；分类含义不明时先浏览该分类下已有论文的标题再定。
- 无合适分类时**自主创建新分类**（英文小写连字符风格，与现有分类一致）。

### 4.2 命名与输出结构

目录命名规则（同 pdf-parser-paper 技能）：
**`<FirstAuthorLastName><TitleWord1><TitleWord2><TitleWord3><Year>`**

- 第一作者姓氏 PascalCase（`de Almeida` → `Dealmeida`）
- 标题前 3 个实词各首字母大写（跳过开头的冠词 A/An/The）
- 4 位年份；各段直接拼接，无空格无分隔符
- 示例："Global Optimal Closed-Form Solutions..." by Nerini, 2026 → `NeriniGlobalOptimalClosedForm2026`
- 目录名冲突时追加后缀 `_2`

最终结构（目录内只放这两个文件）：

```
raw/papers/<分类>/[<子分类>/]<目录名>/
├── paper.md          # ocr-parse 交付的 md 原样归档（raw 层不可变，此后只读）
└── paper_context.md  # 阅读解析稿后提取的上下文（术语、记号、问题/方法/结果概要）
```

- `paper_context.md` 按 pdf-parser-paper 技能 Step 5 的模板与深度要求撰写，篇幅以"不读原文也能掌握核心贡献"为准。
- 归档后 `ls -la` 验证目录内只有这两个文件，清理临时目录。

## 第 5 步：摄入（Ingest）

打开知识库根目录的 `CLAUDE.md`，找到 **Ingest（摄入新资料）** 工作流，严格逐步执行。要点（细节以 CLAUDE.md 为准）：

1. **深度阅读** `raw/papers/` 中刚归档的 `paper.md`，提取研究问题的数学本质、方法推导、定量结果。
2. **检索强相关论文**：通过 tags 匹配找出知识库中所有强相关论文（共享 ≥2 个 tags），阅读其 wiki 页面。
3. **创建论文页面** `wiki/papers/{topic}-{lastname}-{year}-{journal缩写}.md`：含 `## 原始资料` 节（用标准 Markdown 链接指向 raw 文件，不用 frontmatter 双链）、定位差异、系统模型、方法推导（标注原文公式编号）、定量结果、相关链接。
4. **双向关联**：所有强相关论文页面的 `## 相关链接` 节中添加反向链接（一句话说明关联性质）；同步修正发现的 tags 缺失/不准。
5. **作者登记**：维护 `wiki/authors/author-registry.md`；仅当论文数 > 1 时创建作者页面。
6. **记账**：每个新建页面执行 `python <知识库>/scripts/update_dashboard.py --touch "<page>=create,ingest"`；每个被修改的既有页面执行 `--touch "<page>=update,ingest"`。**不可省略。**
7. **更新 `wiki/index.md`**；在 `wiki/log.md` 追加 `## [YYYY-MM-DD] ingest | 资料标题`。

## 多篇论文

一次可处理任意多篇（含整个 Zotero 集合），全程无需逐篇确认：

1. 展示完整处理队列（每篇含元数据与目标分类）后直接开工
2. 串行逐篇走完"取 PDF → 解析 → 归档 → 摄入"全流程，再开始下一篇
3. 每篇结束报告"第 N/M 篇完成：<目录名> + <wiki页面名>"
4. 单篇失败记录原因后跳过，继续下一篇
5. 全部完成后汇总：成功清单（目录名 + wiki 页面名）、已存在跳过清单、失败清单（原因）

## 错误处理

| 问题 | 处理 |
|:---|:---|
| Zotero 中找不到论文 | 报告用户，跳过该篇 |
| 无 PDF 附件 | 报告用户，跳过该篇 |
| OCR 解析失败 | 交由 ocr-parse 技能处理重试；仍失败则报告并跳过（确认 GPU 服务已关闭） |
| 知识库目录校验失败（缺 raw/papers 等） | 报告用户确认路径是否正确 |

## 收尾清单（每篇）

- [ ] raw 目录：`<命名规则>` 目录下只有 `paper.md` + `paper_context.md`，临时文件已清理
- [ ] wiki：论文页面已创建，含原始资料链接、定位差异、推导与定量结果、相关链接
- [ ] 关联：所有强相关论文已加反向链接，tags 已审定
- [ ] 作者：author-registry.md 已登记（必要时建作者页面）
- [ ] 记账：--touch 已执行（新建 create,ingest / 修改 update,ingest）
- [ ] index.md 与 log.md 已更新
- [ ] GPU OCR 服务已确认关闭（按 ocr-parse 技能规定的方式确认显存回落）
