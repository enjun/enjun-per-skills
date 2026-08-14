# Technical Route Writing Workflow

# Write Technical Route

Systematically investigate and analyze technical routes for scientific or engineering problems. Query references through Zotero library, extract and critically examine technical methods, and generate a structured LaTeX technical report.

## Quick Start

This skill follows a five-phase workflow:

1. **Information Collection** - Understand the research question and literature source
2. **Literature Search** - Search Zotero and extract detailed information
3. **Technical Analysis** - Classify routes and analyze from multiple dimensions
4. **Performance Comparison** - Compare metrics and rank technical routes
5. **Report Generation** - Create LaTeX and Markdown technical reports

For detailed guidance on each phase, refer to the reference documents listed below.

---

## Phase 0: Information Collection

Use `AskUserQuestion` tool to collect:

1. **Research Question**: Specific description of the problem to investigate
2. **Literature Source**:
   - A: Zotero search only
   - B: User-provided bib file only
   - C: Both combined
3. **File Path** (if B or C selected): Path to the bib file

Store responses as variables:
- `research_question`: The problem described by the user
- `literature_source`: A/B/C
- `bib_file_path`: (if applicable) The file path provided

---

## Phase 1: Literature Search

For detailed search strategies and information extraction methods, see:
**→ [literature-search.md](literature-search.md)**

### Quick Reference

**Search Tools** (in priority order):
- Semantic search: `mcp__zotero-mcp__zotero_semantic_search`
- Advanced search: `mcp__zotero-mcp__zotero_advanced_search`
- Tag search: `mcp__zotero-mcp__zotero_search_by_tag`

**Extraction Tools**:
- Metadata: `mcp__zotero-mcp__zotero_get_item_metadata`
- Notes (critical!): `mcp__zotero-mcp__zotero_get_notes`
- Children: `mcp__zotero-mcp__zotero_get_item_children`
- Full text: `mcp__zotero-mcp__zotero_get_item_fulltext`

---

## Phase 2: Technical Route Classification

For detailed classification strategy and relationship analysis, see:
**→ [technical-analysis.md](technical-analysis.md#classification-strategy)**

### Quick Reference

**Classification Dimensions**:
- Theoretical Foundation (e.g., Deep Learning / Graph Theory)
- Technical Architecture (e.g., Centralized / Distributed)
- Core Algorithm (e.g., CNN / Transformer)
- Problem Modeling (e.g., Classification / Regression)
- Optimization Objective (e.g., Accuracy-first / Efficiency-first)
- Application Scenario (e.g., Medical Imaging / NLP)

**Steps**:
1. Choose the most appropriate dimension
2. Divide literature into 3-6 categories
3. Name categories professionally: "[Feature] Methods"
4. Validate each classification

---

## Phase 3: Critical Analysis

For the complete six-dimensional analysis framework, see:
**→ [technical-analysis.md](technical-analysis.md#critical-analysis-dimensions)**

### Quick Reference

Analyze each technical route from six dimensions:

| Dimension | Key Questions |
|-----------|---------------|
| **Assumptions** | What prerequisites are needed? Are they reasonable? |
| **Advantages** | What are the core strengths and innovations? |
| **Limitations** | What are the weaknesses and constraints? |
| **Applicability** | When should this method be used? |
| **Challenges** | What are the implementation difficulties? |
| **Relevance** | Does it solve the target problem? |

For each category, also identify:
- Method principles (1-2 paragraphs)
- Representative literature (2-3 papers)
- Evolution lineage (chronological development)

---

## Phase 4: Performance Comparison

For detailed metrics and weighted ranking method, see:
**→ [technical-analysis.md](technical-analysis.md#performance-comparison)**

### Quick Reference

**Metrics to Collect**:
- **Accuracy**: Precision, Recall, F1, domain-specific metrics
- **Efficiency**: Time/space complexity, runtime, FLOPs
- **Robustness**: Noise resistance, generalization
- **Practicality**: Implementation difficulty, interpretability

**Ranking Steps**:
1. Clarify problem requirements (determine weights)
2. Build scoring matrix
3. Normalize scores to [0,1]
4. Calculate composite score and rank

---

## Phase 5: Report Generation

For LaTeX structure, writing principles, and compilation instructions, see:
**→ [report-template.md](report-template.md)**

### Quick Reference

**Directory Setup**:
```bash
mkdir -p latex
cp assets/IEEEtran.cls assets/IEEEtran.bst assets/IEEEabrv.bib latex/
cp assets/main-technical-route.tex latex/main.tex
cp "user_bib_file" latex/myref.bib  # if applicable
```

**Compilation**:
```bash
cd latex
latexmk -xelatex main.tex
# or manually:
# xelatex main.tex && bibtex main && xelatex main.tex && xelatex main.tex
```

**Important**: Chinese documents MUST use `xelatex`, not `pdflatex`.

---

## Output to User

After completing all phases, provide:

1. **Problem Overview**: Background and significance of the research question
2. **Technical Route Overview**: List of identified main categories and count
3. **Key Findings**:
   - Core characteristics of each technical route (2-3 sentences)
   - Relationships between technical routes
   - Advantages and limitations of each route
4. **Performance Comparison Summary**: Based on weighted ranking results
5. **Problem Resolution Status**:
   - Is the research problem fully solved?
   - Remaining major challenges
6. **Suggested Directions**:
   - Most promising technical routes
   - Specific improvement suggestions (based on analyzed limitations)
   - Research directions yet to be explored

Then inform user of generated files:
- LaTeX report: `latex/main.tex` and `latex/main.pdf`
- Markdown version: `latex/main.md`
- Reference file: `latex/myref.bib`

---

## Bundled Resources

### assets/
LaTeX template files (copy the type-specific template to `latex/main.tex`):
- `main-technical-route.tex` - LaTeX document template with Chinese support
- `IEEEabrv.bib` - IEEE standard abbreviations
- `IEEEtran.bst` - IEEE bibliography style
- `IEEEtran.cls` - IEEE document class

### references/
Detailed guidance documents:
- **literature-search.md** - Zotero search strategies and information extraction
- **technical-analysis.md** - Classification, analysis framework, and performance comparison
- **report-template.md** - LaTeX structure, writing principles, and compilation

### scripts/
No script files. All operations use standard tools (zotero-mcp, latexmk).
