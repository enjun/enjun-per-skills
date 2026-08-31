---
name: scientific-writing
description: Write and improve scientific documents in wireless communications — original research articles, survey papers (综述), technical route reports, and improvement of existing manuscripts. Integrates Zotero literature search, structured per-type writing workflows, quality evaluation, and publication-ready IEEE LaTeX output. MUST use this skill whenever the user wants to write a research paper, write a survey on a wireless topic, investigate/analyze technical routes, or improve an existing paper — including "write my paper", "写一篇综述", "调研技术路线", "improve my article", "strengthen methodology", "enhance Related Work", "address reviewer comments". Use the scientific-review skill for evaluating others' work, and scientific-thinking for brainstorming or critical analysis.
---

# Scientific Writing

Produce or improve scientific documents — original research articles, survey papers, technical route reports — with Zotero-backed literature grounding and publication-ready IEEE LaTeX output.

## Why one skill covers four workflows

These four tasks share the same foundation: Zotero literature search, structured drafting, IEEE LaTeX compilation, and quality checking. The differences are in how the document is structured and what the quality bar is. So the skill routes you to the right workflow instead of repeating the shared parts.

## Quick Start

```
Step 0: Determine document type
   ↓ (article / survey / technical route / improve existing)
Step 1: Literature search (shared, Zotero + bib)
   ↓
Step 2: Type-specific workflow (references/<type>.md)
   ↓
Step 3: LaTeX finalization + quality check (shared)
```

Always create a TodoWrite task list at the start to track progress through these steps.

---

## ⚠️ CRITICAL: Academic Integrity Requirements

**FUNDAMENTAL PRINCIPLE**: Never fabricate or falsify research data, results, or numerical claims.

### Data and Results Policy

**ABSOLUTELY PROHIBITED**:
- ❌ Fabricating simulation results with fake numbers
- ❌ Inventing performance metrics (dB gains, percentages, throughput numbers)
- ❌ Creating comparison tables with made-up data
- ❌ Stating "simulation results show X" when no simulations were run
- ❌ Citing non-existent experimental validation

**REQUIRED APPROACH**:
- ✅ **Theoretical Papers**: Focus on mathematical analysis, bounds, and theoretical contributions
- ✅ **Framework Papers**: Present methodology, algorithms, and theoretical evaluation
- ✅ **Simulation-Based Papers**: ONLY if user provides real simulation data/code
- ✅ **Clear Disclaimers**: If no experimental validation, clearly state this limitation

### Valid Paper Structures

**Option 1: Pure Theoretical Contribution** (Recommended when no data available)
```
Title + Abstract
Introduction (motivation + contributions)
System Model (mathematical framework)
Proposed Method (algorithm design + theoretical analysis)
Performance Analysis (theoretical bounds + mathematical evaluation)
Discussion (theoretical comparison with existing work)
Conclusion (theoretical contributions + future work)
References
```

**Option 2: Simulation-Based Paper** (ONLY when user provides real data)
```
Title + Abstract
Introduction
System Model
Proposed Method
Simulation Results (MUST use user-provided data)
Discussion
Conclusion
References
```

### Writing Guidelines

**When NO real data available**:
- Focus on theoretical contributions and analysis
- Use phrases like "theoretical analysis suggests," "we expect that," "preliminary evaluation indicates"
- Present mathematical derivations and bounds
- Compare methodologies theoretically, not numerically
- Clearly state: "This paper presents a theoretical framework. Experimental validation is left for future work."

**When user provides simulation data**:
- Ask for raw simulation results, plots, or code
- Use ONLY the provided data
- Clearly cite data source: "Based on simulations provided by [user/research group]"
- Include data acquisition methodology in reproducibility section

### Quality Check Addition

Add to ALL quality checklists:
- [ ] **Academic Integrity**: No fabricated data, all numerical claims have legitimate sources
- [ ] **Results Verification**: If simulation results presented, they come from real experiments
- [ ] **Clear Attribution**: Data sources clearly disclosed

---

## Step 0: Determine Document Type and Preferences

Use `AskUserQuestion` to confirm the following preferences with the user before proceeding:

### 0.1 Document Type

| Type | User intent | Workflow reference |
|------|-------------|--------------------|
| **Research article** | Write a new original research paper (IMRAD) | [article-writing.md](references/article-writing.md) |
| **Survey paper** | Write a review/survey (综述) of a field | [survey-writing.md](references/survey-writing.md) |
| **Technical route** | Investigate/analyze technical methods for a problem | [technical-route.md](references/technical-route.md) |
| **Improve existing** | Revise/strengthen an existing manuscript or address reviewer comments | [article-improving.md](references/article-improving.md) |

### 0.2 Output Format

Choose the output format for the final document:
- **LaTeX (IEEE format)** — Publication-ready IEEE LaTeX with `.tex` source and compiled PDF
- **Markdown** — Structured Markdown with proper formatting, suitable for conversion to other formats or direct viewing

### 0.3 Literature Search Source

Select the source for literature search:
- **Zotero only** — Search and extract papers from your Zotero library using semantic/advanced/tag search
- **IEEE Xplore only** — Search IEEE Xplore database for papers in wireless communications and related fields
- **Both (Zotero + IEEE)** — Comprehensive search combining your Zotero library and IEEE Xplore for broader coverage

### 0.4 Additional Information

Also collect, as needed:
- **Research topic** — the specific wireless communication topic
- **Target venue** — journal/conference (optional, for style guidance)
- **Guidance mode** — quick / standard / detailed (article writing supports all three; others default to a balanced approach)

---

## Step 1: Literature Search (Shared)

Ground the document in the literature before writing. Search strategy depends on the source(s) selected in Step 0.3.

**Search Tools by Source:**

### Zotero Search (when Zotero only or Both selected)
For the full Zotero search strategy (semantic → advanced → tag), extraction methods, bib-file collection, and wireless-specific query examples, see:
**→ [references/literature-search.md](references/literature-search.md)**

- Semantic search: `mcp__zotero-mcp__zotero_semantic_search`
- Advanced search: `mcp__zotero-mcp__zotero_advanced_search`
- Tag search: `mcp__zotero-mcp__zotero_search_by_tag`

### IEEE Xplore Search (when IEEE only or Both selected)
Use the `ieee-literature-search` skill to systematically search IEEE Xplore database:
- Multi-dimensional keyword coverage
- Traceable search results
- Structured conclusions for analysis

### Combined Search (when Both selected)
Execute both Zotero and IEEE searches:
1. Start with Zotero search for papers in your library
2. Complement with IEEE Xplore search for broader coverage
3. Merge results, removing duplicates
4. Prioritize Zotero papers for full-text extraction (faster access)

**Extraction tools** (for Zotero papers):
- Metadata: `mcp__zotero-mcp__zotero_get_item_metadata`
- Notes (read first!): `mcp__zotero-mcp__zotero_get_notes`
- Children: `mcp__zotero-mcp__zotero_get_item_children`
- Full text: `mcp__zotero-mcp__zotero_get_item_fulltext`

**Note**: IEEE papers require PDF download and parsing; Zotero papers typically have PDFs already attached.

When the user provides a `.bib` file, also follow the **Bib File Collection** steps in the reference: extract entries, record metadata, then cross-reference each title with Zotero for full content.

---

## Step 2: Type-Specific Workflow

Open the reference matching the document type and follow its workflow. Each reference is self-contained — it contains the full step-by-step process for that document type.

**For each type, read:**
- **Research article** → [article-writing.md](references/article-writing.md) — IMRAD structure, quick/standard/detailed guidance modes, section-by-section workflow. Writing structure details in [article-structure.md](references/article-structure.md).
- **Survey paper** → [survey-writing.md](references/survey-writing.md) — 9-step workflow (references index → summaries → deep analysis → write → self-evaluate → compile). Rubric in [evaluation-rubric.md](references/evaluation-rubric.md), style examples in [writing-examples.md](references/writing-examples.md).
- **Technical route** → [technical-route.md](references/technical-route.md) — 5-phase workflow (collect → search → classify → compare → report). Classification/analysis/ranking framework in [technical-analysis.md](references/technical-analysis.md), report template in [report-template.md](references/report-template.md).
- **Improve existing** → [article-improving.md](references/article-improving.md) — Git-backed analyze → plan → implement → merge workflow. Strategies in [improvement-strategies.md](references/improvement-strategies.md), Related Work guidance in [related-work-improvement.md](references/related-work-improvement.md), and non-negotiable writing requirements in [writing-requirements.md](references/writing-requirements.md).

---

## Step 3: Document Finalization & Quality Check (Shared)

The finalization step depends on the output format selected in Step 0.2.

### For LaTeX Output (IEEE format)

All document types compile to IEEE-format LaTeX. The IEEE class files are shared; only the main template differs per type.

#### Directory Setup

```bash
mkdir -p latex
cp assets/IEEEtran.cls assets/IEEEtran.bst assets/IEEEabrv.bib latex/
# Then copy the type-specific template, e.g.:
cp assets/main-article.tex latex/main.tex          # research article
# cp assets/main-survey.tex latex/main.tex         # survey paper
# cp assets/main-technical-route.tex latex/main.tex  # technical route report
```

For the bibliography, start from the example matching your type (`assets/myref-article.bib`, `assets/myref-survey.bib`) or copy the user's bib to `latex/myref.bib`.

#### Compilation

```bash
cd latex
latexmk -xelatex main.tex
```

**Important**: Chinese documents MUST use `xelatex`, not `pdflatex`. All LaTeX output MUST comply with IEEEtran format — see [ieeetran-format-guide.md](references/ieeetran-format-guide.md). When including simulation figures, follow the Python/EPS requirements in [simulation-code.md](references/simulation-code.md).

#### Quality Checklist for LaTeX

Verify before presenting the result:

**Academic Integrity** (CRITICAL)
- [ ] ❌ **NO FABRICATED DATA**: All numerical claims have legitimate sources
- [ ] ❌ **NO FAKE SIMULATIONS**: Simulation results only if user provided real data
- [ ] ✅ **CLEAR DISCLOSURE**: If no experiments, state "theoretical framework only"

**Content Quality**
- [ ] All sections present and complete; abstract matches content
- [ ] Introduction states contributions clearly
- [ ] Equations and figures/tables numbered and referenced
- [ ] Conclusion matches abstract and results
- [ ] If simulation results included, user provided real data

**Citation Quality**
- [ ] All references in BibTeX format; every citation has a bibliography entry
- [ ] No orphan citations (cited but not in bib), no unused references (in bib but not cited)
- [ ] IEEE citation format followed

**Format Quality**
- [ ] Consistent notation; all symbols defined at first use
- [ ] Cross-references use `\label{}` + `\ref{}` (no hard-coded "Table 1")
- [ ] Figures in EPS format (see simulation-code.md)
- [ ] Compilation succeeds without errors
- [ ] IEEEtran format compliance verified (see ieeetran-format-guide.md)

**Language Quality**
- [ ] Complete paragraphs (no bullet points in main text)
- [ ] Consistent terminology; no undefined abbreviations
- [ ] Smooth transitions between sections

### For Markdown Output

Generate well-structured Markdown with proper formatting for the document type.

#### File Structure

```bash
# Create main markdown file
# Main document (with frontmatter)
main.md

# Assets directory for figures
assets/
  figures/

# References directory
references/
  myref.bib    # Bibliography file (BibTeX format for reference)
```

#### Markdown Guidelines

Follow the standards in **→ [references/markdown-format-guide.md](references/markdown-format-guide.md)** for:
- Document structure and headers
- Citation formatting (link to BibTeX, inline citations)
- Figure/table inclusion
- Mathematical notation (LaTeX-style math for rendering compatibility)
- Code block formatting

#### Quality Checklist for Markdown

Verify before presenting the result:

**Academic Integrity** (CRITICAL)
- [ ] ❌ **NO FABRICATED DATA**: All numerical claims have legitimate sources
- [ ] ❌ **NO FAKE SIMULATIONS**: Simulation results only if user provided real data
- [ ] ✅ **CLEAR DISCLOSURE**: If no experiments, state "theoretical framework only"

**Content Quality**
- [ ] All sections present and complete; abstract matches content
- [ ] Proper heading hierarchy (H1 → H2 → H3)
- [ ] Introduction states contributions clearly
- [ ] Conclusion matches abstract and results
- [ ] If simulation results included, user provided real data

**Citation Quality**
- [ ] Citations properly formatted (numerical or author-year style)
- [ ] Bibliography section included with full references
- [ ] Links to bibliography entries work correctly

**Format Quality**
- [ ] Consistent notation; all symbols defined at first use
- [ ] Math in proper LaTeX delimiters (`$` for inline, `$$` for display)
- [ ] Figures properly referenced with alt text
- [ ] Tables properly formatted with alignment
- [ ] Code blocks properly syntax-highlighted

**Language Quality**
- [ ] Complete paragraphs (no bullet points in main text)
- [ ] Consistent terminology; no undefined abbreviations
- [ ] Smooth transitions between sections

### Common Quality Checks (Both Formats)

**Academic Integrity** (NON-NEGOTIABLE)
- [ ] ❌ **NO FABRICATED DATA**: Zero tolerance for fake numbers, results, or simulations
- [ ] ❌ **NO PLAGIARISM**: All content is original or properly cited
- [ ] ✅ **HONEST DISCLOSURE**: Limitations clearly stated, no misleading claims

**General Quality**
- [ ] All citations have corresponding bibliography entries
- [ ] No orphan citations or unused references
- [ ] Consistent formatting throughout
- [ ] Proper capitalization of section headings
- [ ] Figures and tables referenced in text

---

## Output to User

After completing all phases, summarize:

1. **Document summary** — title, abstract, key contributions/results (survey: 7-dimension score; technical route: ranked routes)
2. **Literature grounding** — number of references, key papers, search sources used (Zotero/IEEE/both)
3. **Generated files** — Depends on output format:
   - **LaTeX**: `latex/main.tex`, `latex/main.pdf`, `latex/myref.bib`
   - **Markdown**: `main.md`, `references/myref.bib`, `assets/figures/` (if any)
4. **Quality report** — checklist status, issues found/resolved

---

## Bundled Resources

### assets/
Shared IEEE class files plus type-specific templates and bibliographies:
- `IEEEtran.cls`, `IEEEtran.bst`, `IEEEabrv.bib` — shared IEEE format files
- `main-article.tex` — wireless research article template (custom commands for wireless notation)
- `main-survey.tex` — survey paper template
- `main-technical-route.tex` — technical route report template (Chinese support)
- `myref-article.bib`, `myref-survey.bib` — example bibliographies

### references/
| File | When to read |
|------|--------------|
| [**academic-integrity.md**](references/academic-integrity.md) | **MANDATORY**: Read before any writing. Prevents data fabrication and academic misconduct |
| [literature-search.md](references/literature-search.md) | Step 1 — always, for Zotero search & extraction strategy |
| [markdown-format-guide.md](references/markdown-format-guide.md) | Step 3 — when Markdown output selected |
| [article-writing.md](references/article-writing.md) | Type = research article |
| [article-structure.md](references/article-structure.md) | Article writing — section-by-section guidance |
| [ieeetran-format-guide.md](references/ieeetran-format-guide.md) | LaTeX output — mandatory IEEEtran rules |
| [simulation-code.md](references/simulation-code.md) | When adding simulation results/figures |
| [survey-writing.md](references/survey-writing.md) | Type = survey paper |
| [evaluation-rubric.md](references/evaluation-rubric.md) | Survey writing — self-evaluation rubric |
| [writing-examples.md](references/writing-examples.md) | Survey writing — style/format examples |
| [technical-route.md](references/technical-route.md) | Type = technical route |
| [technical-analysis.md](references/technical-analysis.md) | Technical route — classification & comparison framework |
| [report-template.md](references/report-template.md) | Technical route — report structure & compilation |
| [article-improving.md](references/article-improving.md) | Type = improve existing |
| [improvement-strategies.md](references/improvement-strategies.md) | Improvement — quick fixes by category |
| [related-work-improvement.md](references/related-work-improvement.md) | Improvement — Related Work section strategies |
| [writing-requirements.md](references/writing-requirements.md) | Improvement — data authenticity & formatting requirements |
