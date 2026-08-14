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

## Step 0: Determine Document Type

Use `AskUserQuestion` to confirm which document type the user wants. If ambiguous, infer from the request:

| Type | User intent | Workflow reference |
|------|-------------|--------------------|
| **Research article** | Write a new original research paper (IMRAD) | [article-writing.md](references/article-writing.md) |
| **Survey paper** | Write a review/survey (综述) of a field | [survey-writing.md](references/survey-writing.md) |
| **Technical route** | Investigate/analyze technical methods for a problem | [technical-route.md](references/technical-route.md) |
| **Improve existing** | Revise/strengthen an existing manuscript or address reviewer comments | [article-improving.md](references/article-improving.md) |

Also collect, as needed:
- **Research topic** — the specific wireless communication topic
- **Target venue** — journal/conference (optional, for style guidance)
- **Literature source** — Zotero search, user-provided bib file, or both
- **Guidance mode** — quick / standard / detailed (article writing supports all three; others default to a balanced approach)

---

## Step 1: Literature Search (Shared)

Ground the document in the literature before writing. Search strategy and extraction tools are shared across all document types.

For the full search strategy (semantic → advanced → tag), extraction methods, bib-file collection, and wireless-specific query examples, see:
**→ [references/literature-search.md](references/literature-search.md)**

**Search tools** (in priority order):
- Semantic search: `mcp__zotero-mcp__zotero_semantic_search`
- Advanced search: `mcp__zotero-mcp__zotero_advanced_search`
- Tag search: `mcp__zotero-mcp__zotero_search_by_tag`

**Extraction tools**:
- Metadata: `mcp__zotero-mcp__zotero_get_item_metadata`
- Notes (read first!): `mcp__zotero-mcp__zotero_get_notes`
- Children: `mcp__zotero-mcp__zotero_get_item_children`
- Full text: `mcp__zotero-mcp__zotero_get_item_fulltext`

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

## Step 3: LaTeX Finalization & Quality Check (Shared)

All document types compile to IEEE-format LaTeX. The IEEE class files are shared; only the main template differs per type.

### Directory Setup

```bash
mkdir -p latex
cp assets/IEEEtran.cls assets/IEEEtran.bst assets/IEEEabrv.bib latex/
# Then copy the type-specific template, e.g.:
cp assets/main-article.tex latex/main.tex          # research article
# cp assets/main-survey.tex latex/main.tex         # survey paper
# cp assets/main-technical-route.tex latex/main.tex  # technical route report
```

For the bibliography, start from the example matching your type (`assets/myref-article.bib`, `assets/myref-survey.bib`) or copy the user's bib to `latex/myref.bib`.

### Compilation

```bash
cd latex
latexmk -xelatex main.tex
```

**Important**: Chinese documents MUST use `xelatex`, not `pdflatex`. All LaTeX output MUST comply with IEEEtran format — see [ieeetran-format-guide.md](references/ieeetran-format-guide.md). When including simulation figures, follow the Python/EPS requirements in [simulation-code.md](references/simulation-code.md).

### Quality Checklist

Verify before presenting the result:

**Content Quality**
- [ ] All sections present and complete; abstract matches content
- [ ] Introduction states contributions clearly
- [ ] Equations and figures/tables numbered and referenced
- [ ] Conclusion matches abstract and results

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

---

## Output to User

After completing all phases, summarize:

1. **Document summary** — title, abstract, key contributions/results (survey: 7-dimension score; technical route: ranked routes)
2. **Literature grounding** — number of references, key papers
3. **Generated files** — `latex/main.tex`, `latex/main.pdf`, `latex/myref.bib`
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
| [literature-search.md](references/literature-search.md) | Step 1 — always, for search & extraction strategy |
| [article-writing.md](references/article-writing.md) | Type = research article |
| [article-structure.md](references/article-structure.md) | Article writing — section-by-section guidance |
| [ieeetran-format-guide.md](references/ieeetran-format-guide.md) | Any LaTeX output — mandatory IEEEtran rules |
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
