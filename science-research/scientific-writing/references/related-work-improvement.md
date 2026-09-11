# Related Work Improvement

Systematic approach to improving a paper's Related Work section using Zotero.

---

## Core Principles（描述他人工作的核心原则）

These principles apply to **any writing that describes prior work** — Related Work sections, Introduction literature paragraphs, survey body sections, and technical route comparisons. Read this section before drafting; the rest of this file covers the search/assessment workflow.

### A. 查证——每条陈述经得起对照原文

1. **描述他人工作前读原文正文**，不能只看摘要——摘要常掩盖甚至美化真实方法，仅凭摘要归类他人方法容易出错。
2. **逐篇核准目标函数与约束结构**（maximize 还是 minimize、约束是什么），标题与关键词推不出来。
3. **共性陈述的量词要确定**：逐篇核实后写 all/none；确实无法核实才用限定表述并向用户说明依据。不用 mostly/some——显得没做功课。
4. **不写无法论证的断言**：首创性（seminal / takes the first step）、历史起源（originated in）、演进方向（has followed the evolution into）——难以辩护，审稿人可举反例。用中性动词 investigates / studies / considers / maximizes。

### B. 结构——逻辑靠分层，不靠修辞

5. **分类框架先行**：段首给分类轴（按误差模型/场景/方法），每篇文献的出场位置因此有依据；分类轴的末级应正对本文贡献所在的位置。
6. **重点分层**：与本文最接近的文献单独成句、给"做了什么"级细节（目标函数+场景）；同类型合并一句、各带辨识标签；非重点一句带过。
7. **详略的双约束**：读者既要看到具体研究进展，又不能是平铺列举。不要逐句列举。有效粒度 = 分类句 + 分层句，每篇有可辨识内容。
8. **总结已有研究存在的局限性和问题，阐明本文研究动机**，直接衔接贡献段，形成问题→方案钩子。
9. **与最近前作的对比写假设/模型差异**——具体到哪个假设不同、模型不同、方法不同，不写泛泛的"场景不同"。

### C. 措辞——术语与动词都有技术含义

10. **不确定的动词/术语查源头文献的正式命名**，不用转手叫法。
11. **动词精确、不越界**：技术行话各有所指，同一术语在不同子领域含义不同，不确定时以源头用法为准；不夸大单一技术作用。

### D. 流程——证据可复核、引用同步

12. **归类结论留原文证据句**：每条归类/共性结论附原文证据句，写入持久化文件，保证 grep 可复核。
13. **参考文献键与正文引用同步增删改**：删文献必须清空其所有引用点，改键名必须全局替换（检查命令见 [writing-requirements.md](writing-requirements.md) §3.3 Citation Verification）。

---

## Assessment Framework

| Dimension | What to Check |
|-----------|---------------|
| Coverage | Are key papers cited? Is recent work included? |
| Accuracy | Are prior works correctly represented? |
| Balance | Are multiple perspectives shown? |
| Gap | Is the research gap clearly identified? |
| Positioning | Is the contribution well differentiated? |

---

## Discovery Workflow

### Step 1: Search by Theme

```bash
# For each main theme in the paper
mcp__zotero-mcp__zotero_semantic_search
query: "[Theme 1] in [domain]"
limit: 20

mcp__zotero-mcp__zotero_semantic_search
query: "[Theme 2] in [domain]"
limit: 20
```

### Step 2: Find Recent Work

```bash
mcp__zotero-mcp__zotero_advanced_search
conditions: [
    {"field": "title", "condition": "contains", "value": "[keyword]"},
    {"field": "year", "condition": "isInLast", "value": "3Years"}
]
```

### Step 3: Find Alternative Approaches

```bash
mcp__zotero-mcp__zotero_semantic_search
query: "[Alternative methodology] for [problem]"
limit: 15
```

### Step 4: Extract Limitations

```bash
# For key papers, find limitations
mcp__zotero-mcp__zotero_get_item_fulltext
item_key: [key]

# Look for sections: "Limitations", "Future Work", "Discussion"
```

---

## Gap Identification

For each major cited work, identify:
1. **What problem does it solve?**
2. **What are its limitations?**
3. **What remains unaddressed?**

**Synthesize the gap**:
```markdown
## Research Gap

### What is Known
- [Established result 1]
- [Established result 2]

### What is Not Well Understood
- [Open question 1] - limited by [constraint]
- [Open question 2] - contradictory findings

### Limitations of Existing Approaches
1. [Approach A]: Limited by [specific issue]
2. [Approach B]: Does not address [condition]

### The Gap
[Clear statement of what remains to be done]

### How Current Work Addresses It
[Specific contribution that fills the gap]
```

---

## Positioning Templates

### Incremental Improvement
```
Previous work [citations] established [foundation].
However, these are limited by [specific limitation].
We extend this by [contribution], overcoming [limitation].
```

### New Problem/Context
```
While [existing approaches] work for [established context],
they are unsuitable for [new context] due to [challenge].
We propose [new approach] that addresses this.
```

### Unifying Framework
```
Existing work addresses [aspect A] [citations] and
[aspect B] [citations] separately. We propose a unified
framework that addresses both simultaneously.
```

---

## Writing Improved Related Work

### Structure Options

**Option 1: Thematic** (Recommended)
```latex
\section{Related Work}
\subsection{Foundational Approaches}
\subsection{Recent Advances}
\subsection{Alternative Approaches}
\subsection{Positioning}
```

**Option 2: Chronological**
```latex
\section{Related Work}
\subsection{Early Work}
\subsection{Intermediate Developments}
\subsection{Recent Advances}
\subsection{Our Contribution}
```

### Writing Guidelines

1. **Group thematically, not chronologically**
   - Bad: "Smith (2015) proposed X. Jones (2016) extended X."
   - Good: "Two approaches exist: approach A [Smith; Jones] and approach B [Williams]."

2. **Identify the gap clearly**
   ```latex
   While existing approaches [cite] address [aspect],
   they do not consider [missing aspect].
   Our work addresses this gap by [contribution].
   ```

3. **Position your contribution**
   ```latex
   We propose [method], which differs from prior work [cite]
   in two key ways: (1) [difference 1], and (2) [difference 2].
   ```

4. **Acknowledge trade-offs**
   ```latex
   It is important to note that [alternative approach] [cite]
   is better suited for [specific condition].
   Our approach is designed for [different condition].
   ```

5. **Include a method comparison table (REQUIRED)**
   - The Related Work section MUST contain a table comparing existing research methods, so readers can see the design space and the gap at a glance.
   - Suggested columns: Category / Method, Key References, Core Idea, Strengths, Limitations.
   - Place it near the positioning discussion; keep each cell concise (a phrase, not a sentence).
   - Markdown example:

   ```markdown
   | Category | Key References | Core Idea | Strengths | Limitations |
   |----------|----------------|-----------|-----------|-------------|
   | Location-sampling codebook | [2], [3], [4] | Sample angle–distance grid, focus each codeword on one point | Matches near-field channel directly | Assumes true user location lies on the sampling grid |
   | Hierarchical search | [5]–[10] | Layer-by-layer narrowing of the 2D search region | Low training overhead | Sensitive to angular estimation errors |
   | Beam-shape customization | [11]–[15] | Variable-width / ring / multi-beam patterns | Flexible coverage control | Idealizes continuous phase control |
   | Far-field codebook reuse | [17], [18] | Extract angle–range from DFT beam pattern | No dedicated codebook needed | Off-grid estimation adds complexity |
   ```

---

## Quick Example

### Before (Weak)
```latex
Several papers have studied resource allocation.
Smith et al. used optimization. Jones applied ML.
Williams proposed game theory. Our work uses deep RL.
```

### After (Strong)
```latex
\subsection{Optimization-Based Approaches}
Early work formulated resource allocation as mathematical
optimization [Smith, 2015; Johnson, 2016]. These achieve
optimal solutions but require perfect CSI and high complexity.

\subsection{Machine Learning Approaches}
Recent work applied ML to reduce complexity [Jones, 2019; Brown, 2021].
These methods don't adapt well to dynamic channel conditions.

\subsection{Positioning}
Existing approaches face a trade-off: optimization is optimal but
impractical, while learning is practical but suboptimal. We propose
deep RL that achieves near-optimal performance with real-time
adaptation, unlike prior learning approaches [Jones, 2019] that
use offline training.
```

---

## Quick Reference

```bash
# Search by theme
mcp__zotero-mcp__zotero_semantic_search
query: "[Theme] in [domain]"

# Find recent work
mcp__zotero-mcp__zotero_advanced_search
conditions: [{"field": "year", "condition": "isInLast", "value": "3Years"}]

# Find alternatives
mcp__zotero-mcp__zotero_semantic_search
query: "[Alternative approach] for [problem]"

# Extract limitations
mcp__zotero-mcp__zotero_get_item_fulltext
item_key: [key]
```
