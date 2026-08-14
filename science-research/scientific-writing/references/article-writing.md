# Article Writing Workflow

# Write Article: Wireless Communications Research

Write original research articles in wireless communications. Search your Zotero library for relevant literature, structure manuscripts using IMRAD format, and generate publication-ready LaTeX documents.

## Quick Start

This skill follows a streamlined four-phase workflow with progressive disclosure support:

1. **Topic Definition** - Define the research topic and scope
2. **Literature Review** - Search Zotero and extract relevant references
3. **Article Writing** - Structure and write the manuscript section by section
4. **Finalization** - Generate LaTeX and Markdown outputs

For detailed guidance on each phase, refer to the reference documents listed below.

---

## Progress Tracking

**IMPORTANT**: Always create a TodoWrite task list at the beginning to track progress through all phases.

```markdown
Tasks:
- 主题定义与模式选择
- 文献搜索与整理
- 论文结构规划
- 各章节写作
- 格式检查与完善
- 生成最终文档
```

Update task status as you complete each phase.

---

## Phase 1: Topic Definition & Mode Selection

### Step 1: Collect Research Information

Use `AskUserQuestion` tool to collect:

1. **Research Topic**: Specific wireless communication topic (e.g., "NOMA in 6G networks")
2. **Article Type**:
   - A: Full research paper (IMRAD structure)
   - B: Short communication / Letter
   - C: Review article
3. **Target Venue** (optional): Journal or conference name for style guidelines

Store responses as variables:
- `research_topic`: The wireless communication topic
- `article_type`: A/B/C
- `target_venue`: (if provided) Target journal or conference

### Step 2: Select Guidance Mode

**CRITICAL**: Ask the user to select their preferred guidance mode using `AskUserQuestion`:

**A. 快速模式 (Quick Mode)** - Minimal guidance, direct output
- Suitable for experienced users
- Skips detailed explanations
- Focuses on generating content quickly
- Best for: Short communications, letter papers, tight deadlines

**B. 标准模式 (Standard Mode)** - [DEFAULT] Balanced guidance
- Step-by-step guidance with key confirmations
- Explains important decisions
- Provides examples when helpful
- Best for: Most research papers, first-time users

**C. 详细模式 (Detailed Mode)** - Comprehensive guidance
- Detailed explanations for each step
- Extensive examples and best practices
- Covers edge cases and common pitfalls
- Best for: First-time authors, complex topics, learning purposes

**Store the selected mode as**: `guidance_mode` (quick/standard/detailed)

### Step 3: Adapt Workflow Based on Mode

**Quick Mode**:
- Minimize confirmations
- Use concise prompts
- Skip to direct content generation
- Provide only critical feedback

**Standard Mode**:
- Confirm key decisions (structure, main contributions)
- Provide moderate explanation
- Show examples when requested
- Balance guidance with efficiency

**Detailed Mode**:
- Explain rationale for each decision
- Provide extensive examples from reference docs
- Discuss alternatives and trade-offs
- Cover best practices and common mistakes

---

## Phase 2: Literature Review

Search your Zotero library to gather relevant literature and contextualize your research.

### Mode-Specific Guidance

**Quick Mode**:
- Perform semantic search with the research topic
- Extract metadata from top 5-10 results
- Create a brief citation list
- Skip detailed analysis

**Standard Mode**:
- Perform semantic search, then refine with advanced search
- Extract metadata and notes from relevant papers
- Create organized literature summary
- Identify key papers and recent advances
- Confirm search results with user before proceeding

**Detailed Mode**:
- Follow the three-phase search strategy (broad → focused → deep dive)
- Extract metadata, notes, full text, and child items
- Create detailed paper summaries using the template from literature-search.md
- Build citation network and identify research gaps
- Explain search strategy and findings thoroughly

For detailed search strategies and information extraction methods, see:
**→ [literature-search.md](literature-search.md)**

### Quick Reference

**Search Tools** (in priority order):
- Semantic search: `mcp__zotero-mcp__zotero_semantic_search`
- Advanced search: `mcp__zotero-mcp__zotero_advanced_search`
- Tag search: `mcp__zotero-mcp__zotero_search_by_tag`

**Extraction Tools**:
- Metadata: `mcp__zotero-mcp__zotero_get_item_metadata`
- Notes: `mcp__zotero-mcp__zotero_get_notes`
- Children: `mcp__zotero-mcp__zotero_get_item_children`
- Full text: `mcp__zotero-mcp__zotero_get_item_fulltext`

### Progress Update

After completing literature review, update the TodoWrite status:
- Mark "文献搜索与整理" as completed`

---

## Phase 3: Article Writing

Structure your manuscript using IMRAD format (Introduction, Methods, Results, And Discussion).

### Mode-Specific Guidance

**Quick Mode**:
- Generate each section directly with minimal explanation
- Use standard templates from article-structure.md
- Focus on completing content efficiently
- Skip detailed writing advice

**Standard Mode**:
- Write each section with brief explanation of structure
- Reference article-structure.md for detailed guidance
- Confirm key sections (abstract, main contributions) with user
- Provide examples when helpful
- Ensure consistency and completeness

**Detailed Mode**:
- Explain the purpose and structure of each section before writing
- Provide extensive examples from article-structure.md
- Discuss writing principles and best practices
- Review and refine each section together
- Cover common mistakes and how to avoid them

For detailed writing guidance for each section, see:
**→ [article-structure.md](article-structure.md)**

**IMPORTANT**: When generating LaTeX output, all content **MUST** comply with IEEEtran.cls format requirements. See **→ [ieeetran-format-guide.md](ieeetran-format-guide.md)** for mandatory formatting rules.

**IMPORTANT**: When including simulation results with Python code, all figures **MUST** be output in EPS format. See **→ [simulation-code.md](simulation-code.md)** for Python code requirements.

### Quick Reference

**Section Structure**:
- **Title**: Concise and descriptive (≤15 words)
- **Abstract**: 150-250 words summarizing the entire paper
- **Introduction**: Background, problem statement, literature review, contributions
- **System Model**: Network topology, channel model, assumptions
- **Proposed Method**: Algorithm design, optimization formulation
- **Simulation Results**: Setup, metrics, performance analysis
- **Discussion**: Interpretation, comparison with state-of-the-art
- **Conclusion**: Summary and future work
- **References**: Cited literature in BibTeX format

**Writing Principles**:
- Use complete paragraphs, not bullet points (except in methods)
- Maintain consistent notation throughout
- Define all symbols at first use
- Include equations with proper numbering
- Cite relevant literature appropriately

### Section-by-Section Workflow

**For ALL modes**, follow this order:

1. **Title & Abstract** - Start here to frame the paper
2. **Introduction** - Establish motivation and contributions
3. **System Model** - Define the mathematical framework
4. **Proposed Method** - Present your solution
5. **Simulation Results** - Show performance
6. **Discussion** - Interpret findings
7. **Conclusion** - Summarize and future work
8. **References** - Format citations

**Standard/Detailed Mode Only**: After each major section, ask user if they want to review before proceeding.

### Progress Update

Update TodoWrite as you complete sections:
- Mark "论文结构规划" as completed after outlining
- Mark "各章节写作" as completed after all sections done

---

## Phase 4: Finalization & Quality Check

Generate publication-ready documents using the IEEE LaTeX template.

**CRITICAL REQUIREMENT**: All generated LaTeX documents **MUST** comply with IEEEtran.cls format requirements. See **→ [ieeetran-format-guide.md](ieeetran-format-guide.md)** for mandatory formatting rules.

### Mode-Specific Guidance

**Quick Mode**:
- Copy template files and generate LaTeX directly
- Compile without detailed explanation
- Skip quality checklist (user responsible)

**Standard Mode**:
- Copy template files and explain structure
- Generate LaTeX with brief comments
- Run basic quality checks:
  - All references cited
  - Equations numbered sequentially
  - Figures/tables referenced in text
  - **IEEEtran.cls format compliance verified** (see ieeetran-format-guide.md)
- Confirm compilation success

**Detailed Mode**:
- Explain template structure in detail
- Add helpful comments in LaTeX code
- Run comprehensive quality checks (see below)
- **Verify IEEEtran.cls format compliance** (see ieeetran-format-guide.md)
- Review compiled PDF with user
- Suggest improvements and refinements

### Quality Checklist

**For Standard and Detailed modes**, verify:

**Content Quality**:
- [ ] All sections present and complete
- [ ] Abstract matches paper content
- [ ] Introduction clearly states contributions
- [ ] All equations numbered and referenced
- [ ] All figures/tables numbered and referenced
- [ ] Conclusion matches abstract and results

**Citation Quality**:
- [ ] All references in BibTeX format
- [ ] All citations have matching bibliography entries
- [ ] No orphan citations (cited but not in bib)
- [ ] No unused references (in bib but not cited)
- [ ] IEEE citation format followed

**Format Quality**:
- [ ] Consistent notation throughout
- [ ] All symbols defined at first use
- [ ] No missing equation numbers
- [ ] Proper figure/table placement
- [ ] All figures in EPS format (see simulation-code.md)
- [ ] Compilation succeeds without errors
- [ ] **IEEEtran.cls compliance verified** (see ieeetran-format-guide.md):
  - [ ] Document class uses `\documentclass[10pt,journal]{IEEEtran}` or `\documentclass[10pt,conference]{IEEEtran}`
  - [ ] Package loading order follows IEEEtran recommendations (hyperref last)
  - [ ] Author block uses `\IEEEauthorblockN` and `\IEEEauthorblockA`
  - [ ] Keywords use `\begin{IEEEkeywords}...\end{IEEEkeywords}`
  - [ ] Figures use appropriate width (`\columnwidth` for double-column, `\textwidth` for single-column)
  - [ ] Algorithm environment uses proper `algorithmic` syntax

**Language Quality**:
- [ ] Complete paragraphs (no bullet points in main text)
- [ ] Consistent terminology
- [ ] No undefined abbreviations
- [ ] Smooth transitions between sections

### Quick Reference

**Directory Setup**:
```bash
mkdir -p latex
cp assets/* latex/
```

**Compilation**:
```bash
cd latex
latexmk -xelatex main.tex
```

**Important**:
- Chinese documents MUST use `xelatex`, not `pdflatex`
- **All LaTeX output MUST comply with IEEEtran.cls format requirements** (see ieeetran-format-guide.md)

### Progress Update

Update TodoWrite:
- Mark "格式检查与完善" as completed after quality check
- Mark "生成最终文档" as completed after successful compilation

---

## Output to User

After completing all phases, provide output based on the selected mode:

### Quick Mode Output
1. **Generated Files**:
   - LaTeX source: `latex/main.tex`
   - Compiled PDF: `latex/main.pdf`
   - Bibliography: `latex/myref.bib`
2. **Brief Summary**: Title and key contributions

### Standard Mode Output
1. **Article Summary**:
   - Title and abstract
   - Key contributions
   - Main results
2. **Structure Overview**:
   - Section list with brief descriptions
   - Equation and figure count
3. **Literature Summary**:
   - Number of references cited
   - Key references overview
4. **Generated Files**:
   - LaTeX source: `latex/main.tex`
   - Compiled PDF: `latex/main.pdf`
   - Bibliography: `latex/myref.bib`

### Detailed Mode Output
1. **Comprehensive Article Summary**:
   - Title and abstract
   - Detailed contribution breakdown
   - Main results with quantitative metrics
   - Comparison with related work
2. **Detailed Structure Overview**:
   - Section list with detailed descriptions
   - Equation and figure count with locations
   - Notation table summary
3. **Comprehensive Literature Summary**:
   - Number of references cited
   - Key references with detailed summaries
   - Citation analysis and connections
4. **Quality Check Report**:
   - Checklist completion status
   - Any issues found and resolved
   - Recommendations for improvement
5. **Generated Files**:
   - LaTeX source: `latex/main.tex`
   - Compiled PDF: `latex/main.pdf`
   - Bibliography: `latex/myref.bib`

### Final Progress Update

Mark all TodoWrite tasks as completed and provide a final summary of the work completed.

### assets/
For this document type, use `main-article.tex` (copy to `latex/main.tex`) plus the shared IEEE files:
- `main-article.tex` - IEEE-style article template for wireless communications (includes custom commands for wireless notation)
- `IEEEtran.cls` - IEEE document class
- `IEEEtran.bst` - IEEE bibliography style
- `IEEEabrv.bib` - IEEE standard abbreviations
- `myref-article.bib` - Example bibliography file with wireless communications reference

### references/
Detailed guidance documents:
- **literature-search.md** - Zotero search strategies and information extraction
- **article-structure.md** - IMRAD structure and section-by-section writing guidance
- **ieeetran-format-guide.md** - IEEEtran.cls LaTeX format requirements (MANDATORY for all LaTeX output)
- **simulation-code.md** - Python simulation code requirements (EPS format, reproducibility, code organization)

### scripts/
No script files. All operations use standard tools (zotero-mcp, latexmk).
