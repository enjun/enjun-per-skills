# Related Work Improvement

Systematic approach to improving a paper's Related Work section using Zotero.

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
