---
name: write-survey-paper
description: Wireless communications survey paper writing skill with Zotero integration. Use this skill when the user explicitly requests to write a survey paper, review paper, or academic综述 in the wireless communications field (e.g., RIS, near-field communications, beam management, MIMO, etc.) and has Zotero available. This skill guides through a comprehensive 9-step workflow from Zotero literature gathering to LaTeX compilation, with quality evaluation based on 7-dimension rubric (100-point scale). The skill includes IEEE LaTeX templates, writing examples, and self-evaluation criteria to ensure publication-quality survey papers. Requires Zotero with zotero-mcp integration.
---

# Wireless Communications Survey Paper Writing with Zotero

A comprehensive skill for writing publication-quality survey papers in wireless communications using Zotero for literature management. This skill follows a structured 9-step workflow with integrated quality evaluation.

## Requirements

**This skill requires:**
- Zotero installation with a reference library
- zotero-mcp integration for querying papers, notes, and full text
- A `.bib` file (typically `myref.bib`) with references to analyze

## Core Principles

**Survey papers are not just summaries** — they require critical evaluation, reorganization, and synthesis. You must:
- Analyze problems from multiple perspectives
- Show understanding of supporting and opposing viewpoints
- Evaluate argument validity, conclusion agreement, contradictions, and limitations
- Synthesize multiple papers from a higher perspective

**Writing methodology**:
- Keep each paper's analysis concise but preserve core content
- Do NOT write each paper as a separate paragraph
- Group papers by methodology/category and discuss them together
- Extract common features to classify papers meaningfully

## Workflow Overview

The complete workflow consists of 9 steps. Use `/clear` between major phases to manage token usage.

### Phase 1: Literature Preparation (Steps 1-3)

#### Step 1: Build References Index

1. Read the `.bib` file (typically `myref.bib` or references)
2. Use `zotero_search_items` to find each paper by title
3. Map `title` → `bibtex_key` → `zotero_key`
4. Optionally use `zotero_semantic_search` to find related papers
5. Save to `docs/references-index.json`

**Output format:**
```json
{
  "papers": [
    {
      "title": "Paper Title",
      "bibtex_key": "key2025",
      "zotero_key": "ABCD1234"
    }
  ]
}
```

#### Step 2: Extract Literature Summaries

Use subagents to query each paper via Zotero:
- Use `zotero_get_notes` to find H1-structured notes
- Extract: research problem, content, methods, limitations
- Papers with ⭐ tags are "important" — set `isImportant: true`
- Use `zotero_get_tags` to check for importance markers
- Save to `docs/references-summary.json`

**Output format:**
```json
{
  "papers": [
    {
      "title": "Paper Title",
      "bibtex_key": "key2025",
      "zotero_key": "ABCD1234",
      "tags": ["near-field", "beamforming", "⭐⭐"],
      "problem": "Research problem addressed",
      "method": "Methods and techniques used",
      "contributions": "Key contributions",
      "limitations": "Limitations and weaknesses",
      "isImportant": true
    }
  ]
}
```

**Zotero note structure expected:**
```html
<h1>Research Problem</h1>
<p>...</p>
<h1>Method</h1>
<p>...</p>
<h1>Limitations</h1>
<p>...</p>
```

#### Step 3: Deep Analysis of Important Papers

For papers marked `isImportant: true`:
- Retrieve full text using `zotero_get_item_fulltext`
- Analyze: method principles, advantages, assumptions, applicable scenarios, limitations, causes of limitations
- Add to `references-summary.json` under `methodAnalysis` field

**methodAnalysis format:**
```json
{
  "methodAnalysis": {
    "principles": "Theoretical foundations",
    "advantages": "Key benefits and innovations",
    "assumptions": "Underlying assumptions",
    "scenarios": "Applicable use cases",
    "limitations": "Known limitations",
    "limitationCauses": "Root causes of limitations"
  }
}
```

**After Step 3: Use `/clear` to start fresh session**

### Phase 2: Paper Writing (Steps 4-6)

#### Step 4: Read Prepared Data

Read `docs/references-summary.json` to understand all collected materials.

#### Step 5: Structure and Write

**Overall framework** — design around the central theme:
1. Introduction (background, motivation, contributions)
2. Background/Related Work
3. Main body sections (organized by technical dimensions)
4. Comparison and Analysis
5. Open Issues and Future Directions
6. Conclusion

**Section structure** — each section should:
1. Introduce background and related work
2. Present main contributions and innovations
3. Summarize with a concluding paragraph (for important subsections)

**Writing guidelines**:
- Use formal academic English
- Follow examples in `references/writing-examples.md`
- Group related papers together, discuss comparatively
- Use transitions between paragraphs and sections

#### Step 6: Detail Improvements

Iteratively refine the paper:

1. **Mathematical expressions**: Convert text like "O(log₂ N)" to proper LaTeX math mode
2. **Table layout**: Use two-column tables for single-column overflow
3. **Section summaries**: Ensure important subsections have concluding paragraphs
4. **Logical flow**: Add clear transitions between sections
5. **Label references**: Use `\label{}` and `\ref{}` for tables/figures — no hardcoded references
6. **Citation check**: Verify all references are properly cited
7. **Language check**: Remove any Chinese punctuation (parentheses, commas, etc.)

### Phase 3: Evaluation and Iteration (Steps 7-9)

#### Step 7: Self-Evaluation

Use the rubric in `references/evaluation-rubric.md` to score the paper:

| Dimension | Points |
|-----------|--------|
| Content comprehensiveness | 20 |
| Structure and logic | 15 |
| Literature currency | 20 |
| Critical analysis depth | 15 |
| Accuracy and readability | 10 |
| Practical value | 10 |
| Innovation and foresight | 10 |
| **Total** | **100** |

**If score < 90**: Return to Step 5 for revisions

#### Step 8: LaTeX Compilation

When the paper is ready:

```bash
cd latex
latexmk -xelatex main.tex
latexmk -c
```

This generates the PDF and cleans auxiliary files.

## Citation Format Guidelines

Follow these patterns for proper academic citation:

**Good examples:**
```latex
% 1. Citation at sentence end
Therefore, the reflection coefficient is defined as... \cite{ref36}.

% 2. Reference as subject
As previously mentioned, \cite{ref128} derived an upper bound...

% 3. Reference in other sentence positions
The numerical results in \cite{ref112} indicate that...

% 4. Multiple citations
Deep learning methods of \cite{ref1,ref2,ref3} represent a paradigm shift...
```

**Bad examples to avoid:**
```latex
% Don't use author names directly
Hu et al.'s "2D+1D" framework...  % Bad
"The '2D+1D' framework of \cite{ref}..."  % Good

% Don't bold terms before citations
\textbf{Deep learning methods} (\cite{...})  % Bad
Deep learning methods of \cite{...}  % Good
```

## LaTeX Template Usage

The skill includes IEEE journal template files in `assets/`:
- `IEEEtran.cls` — IEEE document class
- `IEEEabrv.bib` — IEEE abbreviation database
- `IEEEtran.bst` — IEEE bibliography style
- `main.tex` — Template main file
- `myref.bib` — References database

**Key template features:**
- `\documentclass[journal]{IEEEtran}` — Two-column journal format
- `\graphicspath{{figures/}}` — Image path configuration
- `\IEEEPARstart` — Large drop cap at section start
- `\IEEEkeywords` — Keyword environment

**Adding content:**
- Images: Place in `figures/` directory
- References: Add to `myref.bib` using standard BibTeX entry types
- Abstract: Edit `\begin{abstract}...\end{abstract}` section

## Zotero Integration

This skill requires Zotero with zotero-mcp integration.

**Searching notes efficiently:**
- Search for H1-structured notes first
- Use semantic search to find related papers
- Check tags for importance markers (⭐)

**Key Zotero MCP functions:**
- `zotero_search_items` — Find papers by title/author
- `zotero_get_notes` — Retrieve paper notes
- `zotero_get_item_fulltext` — Get full text content
- `zotero_get_tags` — Check importance tags (⭐)
- `zotero_semantic_search` — Find semantically related papers

**Recommended Zotero organization:**
- Use consistent tag naming (e.g., "near-field", "RIS", "beamforming")
- Mark important papers with ⭐ tags (1-3 stars)
- Structure notes with H1 headers for easy extraction

## File Structure

After execution, the working directory should contain:

```
project/
├── docs/
│   ├── references-index.json      # Title → Zotero key mapping
│   └── references-summary.json    # Extracted paper summaries
├── latex/
│   ├── main.tex                    # Main LaTeX document
│   ├── myref.bib                   # Bibliography
│   ├── figures/                    # Images directory
│   └── main.pdf                    # Compiled output
└── assets/                         # Template files (bundled)
```

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Zotero not found | Verify zotero-mcp is installed and configured |
| Token limit exceeded | Use `/clear` after Phase 1, reload `references-summary.json` |
| Missing references | Cross-check `.bib` file with citations, use Zotero to find missing entries |
| LaTeX compilation error | Check for Chinese punctuation, unescaped characters |
| Low evaluation score | Focus on weak dimensions in rubric, iterate |

## Quality Checklist

Before final submission, verify:
- [ ] Zotero integration working (zotero-mcp accessible)
- [ ] All references properly cited
- [ ] No Chinese punctuation remains
- [ ] All math in proper LaTeX mode
- [ ] Tables use `\label{}` and `\ref{}`
- [ ] Important sections have summary paragraphs
- [ ] Logical transitions between sections
- [ ] Evaluation score ≥ 90/100
- [ ] LaTeX compiles without errors
