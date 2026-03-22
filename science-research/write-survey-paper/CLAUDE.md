# CLAUDE.md

## 项目概述
通信领域综述论文写作。以`.claude/Near-Field Communications A Comprehensive Survey.pdf`为范本，撰写关于"RIS Near-Field Beam Management"（RIS近场波束管理）的综述文章。

## 要求

### 语言：英语

### 撰写方法

* 文献综述不仅仅是对先前研究的总结；它是一个批判性评估、重新组织和综合的过程。
* 从多个角度分析问题，展示对支持和反对观点的理解。
* 需要考虑论点是否合理，是否同意结论，是否存在矛盾或局限性，以及研究结果是否普遍适用。
* 需要综合多篇文献的研究结果，从更高的视角进行审视。

* 每一篇文献的分析内容简洁表述，但不要丢掉核心内容。
* 每一篇文献不要单独写成一段，需要把属于一类方法的文献放在一段进行讨论，如何将这部分进行分类需要深入思考，即如何提取不同方法的共同特征作为一类。

### 禁止事项
- 不要向 `myref.bib` 添加任何参考文献条目。
- 在主会话中，不要读入Zotero文献库中pdf文件占用太大的token。

### 流程
1. 根据 `myref.bib`，先使用 `search_library` 搜索文献标题，找到正确的 Zotero item keys，将"title"、"bibtex_key"、"zotero_key"写入到文件 `docs/references-index.json` 中。
2. 根据 `docs/references-index.md` 中的对应关系，使用 zotero-mcp 搜索每篇参考文献的笔记和标签，使用子智能体，提炼笔记中的研究问题、内容、方法，局限性，将"title"、“tags”、"problem","method","limitation"，写入到文件 `docs/references-summary.json` 中。标签中包含一个一颗 ⭐ 或多颗 ⭐的文献标记为重要文献，使用字段'isImportant' : true表示。
3. 对于 `docs/references-summary.json` 中的重要参考文献，使用子智能体从zotero文献库获取全文信息，分析提出的方法的原理、优势，包含的假设条件、适用的场景、局限性以及导致局限性的原因，将分析结果写入到文件 `docs/references-summary.json` 中'methodAnalysis'字段。
4. 使用/clear 命令清空会话，开始新的会话。
5. 读入`docs/references-summary.json`，先进行整体框架构思，围绕主题展开，再撰写各个章节，每个章节先介绍该章节的背景和相关工作，再介绍该章节的主要贡献和创新点，最后总结该章节的贡献。一定要参考`.claude/survey-example.md`中的例子。
6. 对文章进行细节改进：(1) 类似 O(log₂ N) 的内容应使用公式表示。(2)单栏表格放不下的内容，应考虑使用双栏表格或其他布局。（3）重要的小节需要有一个总结段落。（4）结构逻辑性强，每个小节之间有明确的过渡。（5）表格、公式等使用标签加引用的方式，不要硬编码（例如：Table 1）。（6）检查所有参考文献是否被正确引用。（7）检查是否有中文符号（例如括号，逗号等）。
7. 根据 `.claude/rate-survey-paper.md` 中的规则对综述文章进行评分。
8. 如果综述文章得分低于 90 分，回到步骤 (5) 改进文章。
9. 编译LaTeX文档并清理构建文件。

## zotero-mcp搜索技巧
在 Zotero 文献库中搜索独立笔记时，优先搜索 H1 标题结构：明确查找以 <h1>标题</h1> 格式的内容。

## 使用的主要LaTeX宏包

- `amsmath, amsfonts` - 高级数学排版
- `algorithmic, algorithm` - 伪代码/算法环境
- `graphicx` - 图片插入
- `cite` - 引用管理

## 添加内容

### 图片
将图片放在 `figures/` 目录中。图片路径已预配置：
```latex
\graphicspath{{figures/}}
```

### 引用
使用标准 BibTeX 条目类型（`@article`、`@inproceedings` 等）向 `myref.bib` 添加参考文献条目。IEEE 缩写可通过 `IEEEabrv.bib` 使用。`myref.bib` 中的每个条目都是 BibTeX 格式，使用 Zotero-MCP 从我的 Zotero 库中导出。在 `main.tex` 中使用 `\cite{}` 引用参考文献。

### 摘要和关键词
编辑 `\begin{abstract}...\end{abstract}` 和 `\begin{IEEEkeywords}...\end{IEEEkeywords}` 部分。

## 模板说明

文档使用 `\documentclass[journal]{IEEEtran}`，提供：
- 双栏期刊格式
- IEEE 标准标题、字体和间距
- `\IEEEPARstart` 用于章节开头的大首字母
- `\IEEEkeywords` 环境用于索引关键词

## 常用命令

### 编译LaTeX文档并清理构建文件

```bash
cd "latex"
latexmk -xelatex main.tex
latexmk -c
```

