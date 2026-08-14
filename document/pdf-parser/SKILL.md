---
name: pdf-parser
description: >-
  Use this skill when the user wants to parse, extract, or convert PDF files into
  structured formats (Markdown, JSON, HTML, plain text). Supports multi-column layouts,
  tables, headings, lists, images, formulas, and OCR for scanned documents.
  Based on opendataloader-pdf (Apache 2.0). Requires Java 11+ and Python 3.10+.
  Note: Does NOT extract or save images from papers.
---

# PDF Parser (opendataloader-pdf)

Parse PDF files into AI-ready structured data using opendataloader-pdf — a high-accuracy PDF parser that ranks #1 in benchmarks (0.90 overall accuracy across reading order, table extraction, and heading detection).

## Requirements

| Dependency | Version | Purpose |
|---|---|---|
| Java (JDK) | 11+ | Core PDF parsing engine |
| Python | 3.10+ | CLI and SDK runtime |
| pip | Latest | Package installation |

**-> [references/installation-guide.md](references/installation-guide.md)** for detailed setup instructions.

## Core Principles

1. **Batch first** — Each CLI invocation spawns a JVM process. Always combine multiple PDFs into a single command rather than running separate calls.
2. **Choose the right mode** — Use local mode for simple, text-heavy PDFs (0.05s/page). Use hybrid mode for complex tables, scanned documents, or when maximum accuracy is needed (0.43s/page).
3. **Markdown output** — Always output Markdown format for reading/RAG.
4. **No image extraction** — Do NOT use `--image-output external` or any image extraction options. Only extract text content.
5. **Content safety by default** — The tool automatically filters hidden text, off-page content, and invisible layers. Use `--sanitize` for PII redaction.

## Quick Start

```bash
# Parse a single PDF to Markdown
opendataloader-pdf document.pdf -o ./output -f markdown

# Parse all PDFs in a folder
opendataloader-pdf ./pdfs/ -o ./output -f markdown
```

## Workflow Overview

```
Phase 1: Determine Processing Mode
    |
Phase 2: Execute Conversion
    |
Phase 3: Review Output
```

---

## Phase 1: Determine Processing Mode

Ask the user about their use case, or infer from context:

### Decision Matrix

| Scenario | Recommended Mode | Why |
|---|---|---|
| Simple text PDFs (articles, reports) | **Local** | Fast (0.05s/page), sufficient accuracy |
| PDFs with complex/borderless tables | **Hybrid** | Table accuracy: 0.49 → 0.93 |
| Scanned documents / image-based PDFs | **Hybrid + OCR** | Requires OCR for text extraction |
| Formulas or mathematical notation | **Hybrid (full mode)** | LaTeX extraction requires hybrid backend |
| Batch processing many simple PDFs | **Local** | Speed priority |
| Maximum accuracy regardless of speed | **Hybrid** | Accuracy priority |
| Air-gapped / offline environments | **Local** | No model downloads required |

### For Hybrid Mode

Hybrid mode requires two terminals:

```bash
# Terminal 1: Start the backend server
opendataloader-pdf-hybrid --port 5002

# Terminal 2: Run the client (in a new Bash session or background)
opendataloader-pdf --hybrid docling-fast <files> -o ./output -f markdown
```

For OCR or formula extraction, start the server with additional flags:

```bash
# OCR support
opendataloader-pdf-hybrid --port 5002 --force-ocr --ocr-lang "en"

# Formula + picture description
opendataloader-pdf-hybrid --port 5002 --enrich-formula --enrich-picture-description
```

**-> [references/cli-options.md](references/cli-options.md)** for all server options.

---

## Phase 2: Execute Conversion (Markdown Output Only)

### Step 2.1: Identify Input Files

Determine the PDF file(s) or folder to process. Use the Bash tool to list files if the path is a directory:

```bash
ls ./pdfs/*.pdf
```

### Step 3.2: Construct and Run the Command

**Local mode (basic):**

```bash
opendataloader-pdf input.pdf -o ./output -f markdown
```

**Local mode (batch):**

```bash
opendataloader-pdf ./pdfs/ -o ./output -f markdown
```

**Local mode (with options):**

```bash
opendataloader-pdf input.pdf -o ./output -f markdown \
  --pages "1,3,5-7" \
  --table-method cluster
```

> **Note:** Do NOT add `--image-output external` or similar image extraction flags. Images from papers are not extracted or saved.

**Hybrid mode:**

```bash
# Ensure backend is running first (see Phase 1)
opendataloader-pdf --hybrid docling-fast input.pdf -o ./output -f markdown

# Full hybrid mode (formulas + picture descriptions)
opendataloader-pdf --hybrid docling-fast --hybrid-mode full input.pdf -o ./output -f markdown
```

**With sanitization (PII redaction):**

```bash
opendataloader-pdf input.pdf --sanitize -o ./output -f markdown
```

**Encrypted PDF:**

```bash
opendataloader-pdf encrypted.pdf -p "password" -o ./output -f json
```

**-> [references/cli-options.md](references/cli-options.md)** for the complete options reference.

---

## Phase 3: Review Output

### Step 3.1: Locate Output Files

```bash
ls ./output/
```

Output files are named after the source PDF (e.g., `document.md`). Images are NOT extracted.

### Step 3.2: Present Results to the User

- Read the output file(s) using the Read tool
- Present the extracted Markdown text directly
- Report any issues encountered during parsing

### Output to User

Provide the user with:
1. The output file path(s)
2. A brief summary of what was extracted (pages, tables, headings)
3. Any warnings or issues (e.g., pages that fell back to local mode in hybrid)

---

## Common Issues and Solutions

| Problem | Cause | Solution |
|---|---|---|
| `java: command not found` | Java not installed or not on PATH | Install JDK 11+ and add to PATH. See [references/installation-guide.md](references/installation-guide.md) |
| `pip install` fails | Python version too old or pip outdated | Upgrade Python to 3.10+; run `pip install --upgrade pip` first |
| `Could not connect to hybrid backend` | Server not running | Start server: `opendataloader-pdf-hybrid --port 5002` |
| Hybrid mode falls back to Java | Backend unavailable or timeout | Check server is running; increase `--hybrid-timeout` |
| OCR quality is poor | Wrong language or low scan quality | Specify correct `--ocr-lang`; ensure scans are 300 DPI+ |
| Tables are not detected accurately | Borderless tables in local mode | Switch to hybrid mode or use `--table-method cluster` |
| Output is empty or minimal | Encrypted PDF without password | Provide password via `-p` flag |
| Large document processing is slow | JVM spawn overhead | Batch all files into one command; use local mode for speed |

---

## Reference Materials

| File | Description |
|---|---|
| **-> [references/installation-guide.md](references/installation-guide.md)** | Prerequisites, installation commands, Java setup per OS |
| **-> [references/cli-options.md](references/cli-options.md)** | Complete CLI options reference (client + hybrid server) |
| **-> [references/python-api.md](references/python-api.md)** | Python API reference with code examples |
