# CLI Options Reference

## Client CLI: `opendataloader-pdf`

### Usage

```bash
opendataloader-pdf [OPTIONS] <input_path> [input_path ...]
```

`<input_path>` can be one or more PDF files, or a directory containing PDFs.

### Options

| Option | Short | Type | Default | Description |
|---|---|---|---|---|
| `--output-dir` | `-o` | string | Input dir | Output directory |
| `--password` | `-p` | string | — | Password for encrypted PDFs |
| `--format` | `-f` | string | `json` | Output formats (comma-separated): `json`, `text`, `html`, `pdf`, `markdown`, `markdown-with-html`, `markdown-with-images` |
| `--quiet` | `-q` | flag | false | Suppress console logging |
| `--content-safety-off` | — | string | — | Disable safety filters: `all`, `hidden-text`, `off-page`, `tiny`, `hidden-ocg` |
| `--sanitize` | — | flag | false | Redact PII (emails, phones, IPs, credit cards, URLs) |
| `--keep-line-breaks` | — | flag | false | Preserve original line breaks |
| `--replace-invalid-chars` | — | string | `" "` | Replacement for unrecognized characters |
| `--use-struct-tree` | — | flag | false | Use PDF structure tree (tagged PDFs) |
| `--table-method` | — | string | `default` | Table detection: `default` (border-based), `cluster` (borderless) |
| `--reading-order` | — | string | `xycut` | Reading order: `off`, `xycut` |
| `--markdown-page-separator` | — | string | — | Page separator in Markdown (supports `%page-number%`) |
| `--text-page-separator` | — | string | — | Page separator in text output |
| `--html-page-separator` | — | string | — | Page separator in HTML output |
| `--image-output` | — | string | `external` | Image handling: `off`, `embedded` (Base64), `external` (files) |
| `--image-format` | — | string | `png` | Image format: `png`, `jpeg` |
| `--image-dir` | — | string | — | Custom directory for extracted images |
| `--pages` | — | string | — | Pages to extract (e.g., `"1,3,5-7"`) |
| `--include-header-footer` | — | flag | false | Include headers and footers |
| `--detect-strikethrough` | — | flag | false | Detect strikethrough (wraps with `~~`, experimental) |
| `--hybrid` | — | string | `off` | Backend name: `off`, `docling-fast` |
| `--hybrid-mode` | — | string | `auto` | Triage: `auto` (dynamic), `full` (all pages to backend) |
| `--hybrid-url` | — | string | — | Backend server URL (overrides default) |
| `--hybrid-timeout` | — | string | `30000` | Backend timeout in ms |
| `--hybrid-fallback` | — | flag | true | Fallback to Java if backend fails |
| `--to-stdout` | — | flag | false | Write output to stdout (single format only) |

---

## Server CLI: `opendataloader-pdf-hybrid`

### Usage

```bash
opendataloader-pdf-hybrid [OPTIONS]
```

### Options

| Option | Default | Description |
|---|---|---|
| `--port PORT` | `5002` | Server port |
| `--host HOST` | `0.0.0.0` | Bind address |
| `--force-ocr` | false | Force full-page OCR on all pages |
| `--ocr-lang LANG` | — | OCR languages, comma-separated (e.g., `ch_sim,en`, `ko`, `ja`) |
| `--enrich-formula` | false | Enable LaTeX formula extraction |
| `--no-enrich-formula` | — | Disable formula extraction |
| `--enrich-picture-description` | false | Enable AI picture descriptions |
| `--no-enrich-picture-description` | — | Disable picture descriptions |
| `--picture-description-prompt TEXT` | — | Custom prompt for picture description |
| `--log-level LEVEL` | — | Log level: `debug`, `info`, `warning`, `error` |

---

## Usage Examples

### Basic Conversion

```bash
# Single PDF to Markdown and JSON
opendataloader-pdf document.pdf -o ./output -f markdown,json

# Entire folder
opendataloader-pdf ./pdf-folder/ -o ./output -f json
```

### Image Handling

```bash
# Extract images as separate files (default)
opendataloader-pdf document.pdf -f markdown --image-output external

# Embed images as Base64
opendataloader-pdf document.pdf -f markdown --image-output embedded

# No image extraction
opendataloader-pdf document.pdf -f markdown --image-output off

# JPEG format instead of PNG
opendataloader-pdf document.pdf -f markdown --image-format jpeg
```

### Page Selection

```bash
# Specific pages
opendataloader-pdf document.pdf -f json --pages "1,3,5-7"

# With page separators in Markdown
opendataloader-pdf document.pdf -f markdown --markdown-page-separator "--- Page %page-number% ---"
```

### Encrypted PDFs

```bash
opendataloader-pdf encrypted.pdf -p mypassword -o ./output -f json
```

### Sanitization (PII Redaction)

```bash
opendataloader-pdf document.pdf --sanitize -o ./output -f markdown
```

### Hybrid Mode

```bash
# Start server (Terminal 1)
opendataloader-pdf-hybrid --port 5002

# Run client (Terminal 2) — auto triage
opendataloader-pdf --hybrid docling-fast file1.pdf file2.pdf -o ./output -f markdown,json

# Full mode (all pages to AI backend)
opendataloader-pdf --hybrid docling-fast --hybrid-mode full file1.pdf -o ./output -f json
```

### OCR Mode

```bash
# Start server with OCR (Terminal 1)
opendataloader-pdf-hybrid --port 5002 --force-ocr --ocr-lang "en"

# Run client (Terminal 2)
opendataloader-pdf --hybrid docling-fast scanned.pdf -o ./output -f markdown
```

### Formula + Picture Description

```bash
# Start server with enrichments (Terminal 1)
opendataloader-pdf-hybrid --port 5002 --enrich-formula --enrich-picture-description

# Run client in full mode (Terminal 2) — required for enrichment output
opendataloader-pdf --hybrid docling-fast --hybrid-mode full paper.pdf -o ./output -f json,markdown
```

### Tagged PDFs

```bash
# Use native PDF structure tags instead of heuristic analysis
opendataloader-pdf tagged.pdf --use-struct-tree -o ./output -f json
```

### Stdout Output

```bash
# Pipe output to another command (single format only)
opendataloader-pdf document.pdf -f json --to-stdout | jq '.kids[].type'
```

---

## Performance Notes

- **Batch files**: Each invocation spawns a JVM. Always combine multiple PDFs into one command.
- **Local mode**: ~0.05s/page (20+ pages/sec). Best for simple, text-heavy documents.
- **Hybrid mode**: ~0.43s/page (2+ pages/sec). Best for accuracy on complex documents.
- **Multi-process**: With 8+ CPU cores, multi-process batch can exceed 100 pages/sec.
- **No GPU required**: Both modes run entirely on CPU.
