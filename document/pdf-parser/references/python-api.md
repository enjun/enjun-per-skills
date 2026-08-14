# Python API Reference

## Installation

```bash
pip install -U opendataloader-pdf
# With hybrid mode:
pip install -U "opendataloader-pdf[hybrid]"
```

## Core Function: `convert()`

```python
import opendataloader_pdf

opendataloader_pdf.convert(
    input_path=["file1.pdf", "file2.pdf", "folder/"],
    output_dir="output/",
    format="json,markdown",
)
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `input_path` | `str` or `list[str]` | **Required** | PDF file(s) or directory |
| `output_dir` | `str` | Input dir | Output directory |
| `format` | `str` or `list[str]` | `"json"` | Output format(s): `json`, `text`, `html`, `pdf`, `markdown`, `markdown-with-html`, `markdown-with-images` |
| `password` | `str` | `None` | Password for encrypted PDFs |
| `quiet` | `bool` | `False` | Suppress console logging |
| `content_safety_off` | `str` or `list[str]` | `None` | Disable filters: `all`, `hidden-text`, `off-page`, `tiny`, `hidden-ocg` |
| `sanitize` | `bool` | `False` | Redact PII (emails, phones, IPs, credit cards, URLs) |
| `keep_line_breaks` | `bool` | `False` | Preserve original line breaks |
| `replace_invalid_chars` | `str` | `" "` | Replacement for unrecognized characters |
| `use_struct_tree` | `bool` | `False` | Use PDF structure tree (tagged PDFs) |
| `table_method` | `str` | `"default"` | Table detection: `"default"`, `"cluster"` |
| `reading_order` | `str` | `"xycut"` | Reading order: `"off"`, `"xycut"` |
| `markdown_page_separator` | `str` | `None` | Page separator in Markdown (supports `%page-number%`) |
| `text_page_separator` | `str` | `None` | Page separator in text output |
| `html_page_separator` | `str` | `None` | Page separator in HTML output |
| `image_output` | `str` | `"external"` | Image handling: `"off"`, `"embedded"`, `"external"` |
| `image_format` | `str` | `"png"` | Image format: `"png"`, `"jpeg"` |
| `image_dir` | `str` | `None` | Custom directory for extracted images |
| `pages` | `str` | `None` | Pages to extract (e.g., `"1,3,5-7"`) |
| `include_header_footer` | `bool` | `False` | Include headers and footers |
| `detect_strikethrough` | `bool` | `False` | Detect strikethrough (experimental) |
| `hybrid` | `str` | `"off"` | Backend: `"off"`, `"docling-fast"` |
| `hybrid_mode` | `str` | `"auto"` | Triage: `"auto"`, `"full"` |
| `hybrid_url` | `str` | `None` | Backend server URL |
| `hybrid_timeout` | `str` | `"30000"` | Backend timeout in ms |
| `hybrid_fallback` | `bool` | `True` | Fallback to Java if backend fails |
| `to_stdout` | `bool` | `False` | Write to stdout (single format only) |

## Code Examples

### Basic Conversion

```python
import opendataloader_pdf

# Parse a single PDF to Markdown
opendataloader_pdf.convert(
    input_path="document.pdf",
    output_dir="./output",
    format="markdown",
)

# Batch parse multiple PDFs to JSON and Markdown
opendataloader_pdf.convert(
    input_path=["paper1.pdf", "paper2.pdf", "./papers/"],
    output_dir="./output",
    format=["json", "markdown"],
)
```

### Page Selection and Image Control

```python
opendataloader_pdf.convert(
    input_path="report.pdf",
    output_dir="./output",
    format="markdown",
    pages="1,3,5-7",
    image_output="embedded",  # Base64 images inline
    image_format="jpeg",
)
```

### Encrypted PDF

```python
opendataloader_pdf.convert(
    input_path="encrypted.pdf",
    output_dir="./output",
    format="json",
    password="my_password",
)
```

### Sanitization

```python
opendataloader_pdf.convert(
    input_path="sensitive.pdf",
    output_dir="./output",
    format="markdown",
    sanitize=True,  # Redact emails, phones, IPs, URLs
)
```

### Hybrid Mode

```python
# Start the hybrid server first (separate process):
# opendataloader-pdf-hybrid --port 5002

import opendataloader_pdf

# Auto triage: simple pages local, complex pages to AI backend
opendataloader_pdf.convert(
    input_path="complex_tables.pdf",
    output_dir="./output",
    format="markdown,json",
    hybrid="docling-fast",
    hybrid_mode="auto",
)

# Full mode: all pages processed by AI backend (formulas + descriptions)
opendataloader_pdf.convert(
    input_path="paper_with_formulas.pdf",
    output_dir="./output",
    format="markdown,json",
    hybrid="docling-fast",
    hybrid_mode="full",
)
```

### OCR for Scanned Documents

```python
# Start the hybrid server with OCR:
# opendataloader-pdf-hybrid --port 5002 --force-ocr --ocr-lang "en"

import opendataloader_pdf

opendataloader_pdf.convert(
    input_path="scanned_document.pdf",
    output_dir="./output",
    format="markdown",
    hybrid="docling-fast",
)
```

### Custom Table Detection

```python
opendataloader_pdf.convert(
    input_path="tables.pdf",
    output_dir="./output",
    format="json",
    table_method="cluster",  # Better for borderless tables
)
```

## LangChain Integration

```bash
pip install -U langchain-opendataloader-pdf
```

```python
from langchain_opendataloader_pdf import OpenDataLoaderPDFLoader

loader = OpenDataLoaderPDFLoader(
    file_path=["paper1.pdf", "paper2.pdf", "./papers/"],
    format="text",  # Also supports "json", "markdown", "html"
)
documents = loader.load()
```

## Performance Tips

1. **Batch files**: Each `convert()` call spawns a JVM process. Combine multiple PDFs into one call to avoid JVM startup overhead.
2. **Format selection**: JSON with bounding boxes is the most detailed; Markdown is lighter and better for LLM context.
3. **Local vs Hybrid**: Use local mode when speed matters and PDFs are simple. Use hybrid mode for complex tables, OCR, or formula extraction.
4. **Output to stdout**: Use `to_stdout=True` for pipeline integration (single format only).
