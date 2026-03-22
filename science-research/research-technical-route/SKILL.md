---
name: research-technical-route
description: 围绕科学/工程问题，使用zotero-mcp查询文献，分析技术路线，生成LaTeX报告
context: fork
agent: general-purpose
disable-model-invocation: true
---

# Research Technical Route

## Overview

针对科学或工程问题，系统性地调研和分析相关技术路线。通过Zotero文献库查询参考文献，提炼和批判性审视技术方法，最终生成结构化的LaTeX技术报告。

## Usage

使用参数传递问题和文献集合：

```
/research-technical-route <问题> <文献集合文件>
```

- `$ARGUMENTS[0]`: 要研究的科学/工程问题（必填）
- `$ARGUMENTS[1]`: bib格式的文献集合文件（必填）

## Workflow

### 1. 深入研究 $ARGUMENTS[0]

使用zotero-mcp工具搜索 `$ARGUMENTS[1]` 文件中列出的每一条文献：

- **语义搜索**: `mcp__zotero-mcp__zotero_semantic_search` - AI驱动的语义搜索
- **标签搜索**: `mcp__zotero-mcp__zotero_search_by_tag` - 按标签筛选
- **高级搜索**: `mcp__zotero-mcp__zotero_advanced_search` - 多条件组合搜索

搜索后获取文献的详细信息：
- 使用 `mcp__zotero-mcp__zotero_get_item_metadata` 获取元数据
- 使用 `mcp__zotero-mcp__zotero_get_notes` 获取笔记内容

### 2. 提炼技术路线

分析参考文献，提取相关技术路线和方法（保证数据、观点的准确性，避免错误或误导性信息）：

- **优先使用笔记**: 如果文献的笔记中包含技术路线描述，直接提炼采用
- **从内容总结**: 如果笔记不包含，根据文献正文总结技术路线
- **分类**: 根据技术路线的特征和方法原理，将文献分类。

### 3. 批判性审视

对每个技术路线进行多维度评估：

| 评估维度 | 说明 |
|---------|------|
| 假设条件 | 方法成立的前提条件是否合理 |
| 局限性 | 方法的不足和约束 |
| 优势 | 方法的核心优势和创新点 |
| 适用范围 | 方法适用的场景和边界 |
| 关联性 | 与目标问题的相关程度 |
| 实际挑战 | 应用中的问题和难点 |

### 4. 性能排序

总结相关性能指标，按重要性对技术路线进行加权排序。

### 5. 生成报告

#### 创建目录和文件
- 在当前目录创建 `latex` 目录
- 将 `assets`目录中的所有文件复制到 `.\latex` 目录
- 将 `$ARGUMENTS[1]` 文件复制到 `.\latex` 目录，重命名为 `myref.bib`。
- 在 `latex/main.tex`文件中，写入以下内容：
    - **标题**: `$ARGUMENTS[0]的技术路线`
    - **背景**: 阐述 `$ARGUMENTS[0]` 的背景和技术背景
    - **技术路线分析**: 每一篇文献不要单独罗列，需要把属于一类方法的文献放在一起进行讨论（每种方法必须引用参考文献），不同文献的方法之间既有联系又有区别，一类方法指的是具有某种共同的典型特征的方法集合。如果某种方法对于解决 ARGUMENTS[0] 有重要贡献，则必须深入分析其方法原理，前提假设，优势和局限性。论述必须逻辑清晰，语句连贯。
    - **对比表格**: 使用\begin{table*}[htbp]（双栏文档中的跨栏表格），展示所有技术路线的综合比较（每种技术路线需要引用参考文献），需要包括关键性能指标（数据必须保证真实可靠，来源必须引用文献）。
    - **总结**: `$ARGUMENTS[0]` 是否被完全解决，如果未解决，提出建设性、有启发意义、具体的改进方向。
- 编译tex文件，生成pdf文件
    ```bash
    # 编译文档
    latexmk -xelatex "main.tex"

    # 清理构建文件
    latexmk -c
    ```
- 在 `latex` 目录下，生成与 `main.tex` 文件内容相同的 `main.md` 文件，markdown文件中需要引用参考文献。

## 输出

向用户输出：

1. 阐述 `$ARGUMENTS[0]`（问题）
2. 介绍相关的技术路线和方法
3. 总结 `$ARGUMENTS[0]` 是否被完全解决，以及未解决的改进方向

## Resources

### assets/

LaTeX模板文件，用于生成技术路线报告：

- `main.tex`: LaTeX文档模板，包含标准结构和中文字体支持
- `IEEEabrv.bib`: 包含IEEE标准的缩写文献引用
- `IEEEtran.bst`: IEEE论文LaTeX样式文件
- `IEEEtran.cls`: IEEE论文LaTeX类文件
- `myref.bib`: 参考文献文件

### references/

无额外参考文档。工作流程已在本SKILL.md中完整描述。

### scripts/

无脚本文件。所有操作通过标准工具（zotero-mcp、latexmk）完成。