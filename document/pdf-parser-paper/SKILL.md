---
name: pdf-parser-paper
description: >
  Batch process multiple academic papers from Zotero library. Downloads PDFs, parses them into
  structured Markdown, fixes formulas/tables/heading issues, and extracts key context information.
  Use this skill whenever the user wants to analyze one or more papers, process papers in batch,
  extract paper context, or mentions "analyze paper", "process paper", "batch papers", "多篇论文",
  "分析论文", "批量处理". Also trigger when the user provides a list of paper titles or authors
  to analyze. Handles everything from Zotero PDF retrieval through to clean paper.md and
  paper_context.md output.
---

# PDF Parser Paper

Process one or more academic papers from Zotero into clean, structured Markdown with extracted context.

## Overview

For each paper, the skill performs:
1. **Search Zotero** → find the paper and its PDF attachment
2. **Parse PDF** → convert to Markdown using opendataloader-pdf (local mode only)
3. **Clean paper.md** → fix headings, formulas, tables, ordering, formatting
4. **Extract context** → save key terminology, notation, and structure to paper_context.md
5. **Organize output** → create a named directory and clean up temporary files

## Directory Naming Convention

Each paper gets its own directory at the project root, named by:
**`<FirstAuthorLastName><TitleWord1><TitleWord2><TitleWord3><Year>`**

Rules:
- First author's last name in PascalCase (e.g., `de Almeida` → `Dealmeida`, `Li` → `Li`, `Nerini` → `Nerini`)
- First 3 words from the paper title, each capitalized (skip articles like "A", "An", "The" at the start)
- Publication year (4 digits)
- All concatenated with no spaces or separators

Examples:
- "Channel Estimation for Beyond Diagonal RIS..." by de Almeida, 2025 → `DealmeidaChannelEstimationBeyond2025`
- "Global Optimal Closed-Form Solutions..." by Nerini, 2026 → `NeriniGlobalOptimalClosedForm2026`
- "Near-Field Hierarchical Beam Management..." by Zhang, 2024 → `ZhangNearFieldHierarchical2024`

## Output Structure

After processing, each paper directory contains exactly two files:
```
<DirectoryName>/
├── paper.md          # Cleaned, structured paper content
└── paper_context.md  # Extracted context (terminology, notation, structure)
```

No other files or subdirectories should remain. Clean up everything else (PDF, temp dirs, opendataloader output folders, etc.).

---

## Step-by-Step Workflow

Process papers sequentially (one at a time) to avoid resource conflicts.

### Step 1: Collect Paper List

Ask the user which papers to process. They may provide:
- Paper titles (full or partial)
- Author names
- DOI numbers
- A Zotero collection name
- Or any combination

For each paper, search Zotero to get metadata (title, first author, year). Build a processing queue and show it to the user for confirmation before starting.

### Step 2: For Each Paper — Get PDF from Zotero

```
1. Search: zotero_search_items(query="<paper title or author>")
   → Get parent item key (e.g., "P9KCJ6HN")

2. Get attachments: zotero_get_item_children(item_key="<parent key>")
   → Get attachment key (e.g., "MVXCKSAX") for the PDF

3. Retrieve local path via Zotero API:
   curl -s http://localhost:23119/api/users/0/items/<attachment_key> | grep -oP '"href"\s*:\s*"\K[^"]+' | grep -i pdf
   → Returns the local file path

4. Copy PDF to a temp location:
   cp "<retrieved_path>" "paper.pdf"
```

### Step 3: For Each Paper — Parse PDF

Run opendataloader-pdf in **local mode only** (never use hybrid mode):

```bash
opendataloader-pdf paper.pdf -o ./pdf_output -f markdown
```

Wait for parsing to complete. The output directory `./pdf_output/` will contain a `.md` file.

### Step 4: For Each Paper — Clean paper.md

Read the raw parsed Markdown and systematically fix all issues described below. This is the most labor-intensive step — be thorough.

#### 4.1 Heading Level Fixes
- PDF extraction often produces scattered markdown markers (e.g., `# M`, `### y = Xh + n`) — these are paragraph initials misidentified as headings.
- Normalize to the paper's original hierarchy: `##` for Section, `###` for Subsection, `####` for Sub-subsection.
- The paper title should be `# Title`.

#### 4.2 Formula Reconstruction
- Verify every formula for correctness.
- Inline math: `$...$`. Display math: `$$...$$`.
- Number display equations with `\tag{n}` at the end.
- **Never use multiple `\tag` in a single `$$...$$` block** (e.g., in `aligned` environments, only one `\tag` per block — use plain text for the rest).
- **Never use `\tag` in inline math** (e.g., `$x=1 \tag{1}$` is wrong — use `$x=1$ (1)` instead).
- All LaTeX subscripts must use braces: `\delta_{\alpha}`, not `\delta\alpha`.
- Function calls like `\sin\theta`, `\cos\varphi` are NOT subscripts — no braces needed.

#### 4.3 Table and Figure Fixes
- Simple empty tables (header-only): reconstruct from the paper's textual description.
- Complex tables: remove the table but keep the surrounding descriptive text.
- Figures: remove image references but keep all descriptive text about the figures.
- Figure/table captions should be preserved.

#### 4.4 Content Ordering
- Fix cross-mixed sections (e.g., Section V.A and V.B content interleaved).
- Remove IEEE headers, footers, copyright notices, DOI lines.
- Keep author biographies but separate them with a horizontal rule (`---`).

#### 4.5 Formatting
- Bold for key terms and contribution points (e.g., **Firstly**, **Property 1**).
- Theorem/Property/Corollary names in bold. Proof markers in italics (*Proof*).
- References: numbered, with author, "title", *journal*, vol/issue/pages, month year.
- Footnote markers (IEEE DOI lines) → inline citation format or delete.

Save the cleaned result as `paper.md`.

### Step 5: For Each Paper — Extract Context

Read the cleaned `paper.md` and extract into `paper_context.md`:

```markdown
# Paper Context: <Title>

## Paper Information
- **Title**: <full title>
- **Authors**: <author list>
- **Publication**: <journal/conference, year>
- **DOI**: <doi if available>

## Problem Formulation
- <What problem does the paper solve?>

## Methodology Summary
- <Main techniques and algorithms used>

## Key Results
- <Main findings, performance gains, theoretical results>

```

### Step 6: For Each Paper — Create Directory and Organize

```
1. Determine directory name from metadata:
   - First author's last name (PascalCase)
   - First 3 title words (PascalCase, skip leading articles)
   - Publication year

2. Create directory: mkdir -p <DirectoryName>

3. Move files:
   mv paper.md <DirectoryName>/paper.md
   mv paper_context.md <DirectoryName>/paper_context.md

4. Clean up ALL temporary files:
   rm -f paper.pdf
   rm -rf ./pdf_output/
   rm -rf <any other temp dirs or files created during processing>
```

The directory should contain **only** `paper.md` and `paper_context.md`. Verify with `ls -la <DirectoryName>/`.

---

## Processing Multiple Papers

When the user provides multiple papers:
1. Build the full queue first and display it
2. Process one paper at a time (sequential)
3. After each paper completes, report progress: "Paper N/M done: <DirectoryName>"
4. If a paper fails (not found in Zotero, no PDF, parse error), log it and move to the next
5. At the end, summarize: successful papers with directory names, and any failures

## Error Handling

| Problem | Action |
|---------|--------|
| Paper not found in Zotero | Report to user, skip to next paper |
| No PDF attachment | Report to user, skip to next paper |
| PDF parse fails | Try once more; if still fails, report and skip |
| Directory name collision | Append a suffix like `_2` to the directory name |

## Important Notes

- Always use opendataloader-pdf in **local mode** — never hybrid mode
- The cleaning step (Step 4) is the most critical — take your time and be thorough
- After cleaning, read through the entire `paper.md` once more to catch any remaining issues
- The `paper_context.md` should be comprehensive enough that someone can understand the paper's key contributions without reading the full paper.md
