# CSS Templates for Course Materials

This file contains all CSS styles used in the course HTML pages.

## lessons/css/style.css (Main Style File)

Complete style system with CSS variables, modern layout, and responsive design.

```css
/* Course Styles - Modern Design System */

/* Global Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* CSS Variables - Design Tokens */
:root {
    --primary-color: #2563eb;
    --primary-dark: #1e40af;
    --primary-light: #3b82f6;
    --secondary-color: #64748b;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --bg-light: #f8fafc;
    --bg-white: #ffffff;
    --border-color: #e2e8f0;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 16px;
    line-height: 1.75;
    color: var(--text-primary);
    background-color: var(--bg-light);
}

/* Layout Structure */
.course-layout {
    display: flex;
    min-height: 100vh;
}

/* ========== SIDEBAR ========== */
.sidebar {
    width: 280px;
    background: var(--bg-white);
    border-right: 1px solid var(--border-color);
    position: fixed;
    height: 100vh;
    overflow-y: auto;
    top: 0;
    left: 0;
}

.sidebar-header {
    padding: 24px 20px;
    border-bottom: 1px solid var(--border-color);
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
    color: white;
}

.sidebar-header h1 {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 8px;
}

.sidebar-header p {
    font-size: 13px;
    opacity: 0.9;
}

.sidebar-nav {
    padding: 16px 0;
}

.nav-section {
    margin-bottom: 24px;
}

.nav-section-title {
    padding: 8px 20px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-secondary);
}

.nav-item {
    display: block;
    padding: 10px 20px;
    color: var(--text-primary);
    text-decoration: none;
    transition: all 0.2s;
    border-left: 3px solid transparent;
}

.nav-item:hover {
    background-color: var(--bg-light);
    color: var(--primary-color);
}

.nav-item.active {
    background-color: #eff6ff;
    color: var(--primary-color);
    border-left-color: var(--primary-color);
    font-weight: 500;
}

/* ========== MAIN CONTENT ========== */
.main-content {
    flex: 1;
    margin-left: 280px;
    padding: 0;
}

/* Top Navigation */
.top-nav {
    background: var(--bg-white);
    border-bottom: 1px solid var(--border-color);
    padding: 16px 32px;
    position: sticky;
    top: 0;
    z-index: 100;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.breadcrumb {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: var(--text-secondary);
}

.breadcrumb a {
    color: var(--text-secondary);
    text-decoration: none;
}

.breadcrumb a:hover {
    color: var(--primary-color);
}

/* Content Area */
.content {
    padding: 32px;
    max-width: 900px;
}

/* ========== PAGE HEADER ========== */
.page-header {
    margin-bottom: 32px;
}

.page-title {
    font-size: 36px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 12px;
    line-height: 1.2;
}

.page-subtitle {
    font-size: 18px;
    color: var(--text-secondary);
    font-weight: 400;
}

/* ========== SECTIONS ========== */
.section {
    margin-bottom: 48px;
}

.section-title {
    font-size: 28px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--border-color);
}

.section-subtitle {
    font-size: 22px;
    font-weight: 600;
    color: var(--text-primary);
    margin-top: 32px;
    margin-bottom: 16px;
}

.section-tertiary-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin-top: 24px;
    margin-bottom: 12px;
}

/* ========== TEXT ELEMENTS ========== */
p {
    margin-bottom: 16px;
}

ul, ol {
    margin-bottom: 16px;
    padding-left: 24px;
}

li {
    margin-bottom: 8px;
}

/* ========== CODE BLOCKS ========== */
.code-block {
    background: #1e293b;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
    overflow-x: auto;
    position: relative;
}

.code-block::before {
    content: attr(data-lang);
    position: absolute;
    top: 12px;
    right: 12px;
    font-size: 12px;
    color: #64748b;
    text-transform: uppercase;
}

pre {
    margin: 0;
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco', monospace;
    font-size: 14px;
    line-height: 1.6;
    color: #e2e8f0;
}

code {
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco', monospace;
}

:not(pre) > code {
    background: #f1f5f9;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.9em;
    color: var(--primary-color);
}

/* Syntax Highlighting */
.keyword { color: #c792ea; }
.string { color: #c3e88d; }
.comment { color: #64748b; font-style: italic; }
.type { color: #ffcb6b; }
.method { color: #82aaff; }
.variable { color: #f78c6c; }

/* ========== FILE PATH ========== */
.file-path {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #f1f5f9;
    padding: 6px 12px;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--text-primary);
    margin: 8px 0;
}

.file-path::before {
    content: '📄';
    font-size: 14px;
}

/* ========== INFO BOXES ========== */
.note {
    background: #eff6ff;
    border-left: 4px solid var(--primary-color);
    padding: 16px 20px;
    border-radius: 0 8px 8px 0;
    margin: 20px 0;
}

.note::before {
    content: '💡 提示';
    display: block;
    font-weight: 600;
    color: var(--primary-color);
    margin-bottom: 8px;
}

.warning {
    background: #fffbeb;
    border-left: 4px solid var(--warning-color);
    padding: 16px 20px;
    border-radius: 0 8px 8px 0;
    margin: 20px 0;
}

.warning::before {
    content: '⚠️ 注意';
    display: block;
    font-weight: 600;
    color: var(--warning-color);
    margin-bottom: 8px;
}

.error {
    background: #fef2f2;
    border-left: 4px solid var(--danger-color);
    padding: 16px 20px;
    border-radius: 0 8px 8px 0;
    margin: 20px 0;
}

.error::before {
    content: '❌ 错误';
    display: block;
    font-weight: 600;
    color: var(--danger-color);
    margin-bottom: 8px;
}

.success {
    background: #f0fdf4;
    border-left: 4px solid var(--success-color);
    padding: 16px 20px;
    border-radius: 0 8px 8px 0;
    margin: 20px 0;
}

.success::before {
    content: '✅ 成功';
    display: block;
    font-weight: 600;
    color: var(--success-color);
    margin-bottom: 8px;
}

/* ========== TABLES ========== */
.table-wrapper {
    overflow-x: auto;
    margin: 20px 0;
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}

thead {
    background: var(--bg-light);
}

th {
    padding: 12px 16px;
    text-align: left;
    font-weight: 600;
    color: var(--text-primary);
    border-bottom: 2px solid var(--border-color);
}

td {
    padding: 12px 16px;
    border-bottom: 1px solid var(--border-color);
}

tbody tr:last-child td {
    border-bottom: none;
}

tbody tr:hover {
    background: #f8fafc;
}

/* ========== CARDS ========== */
.card {
    background: var(--bg-white);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 24px;
    margin: 20px 0;
    box-shadow: var(--shadow-sm);
}

.card-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 16px;
}

.card-content {
    color: var(--text-secondary);
    line-height: 1.75;
}

/* ========== CHECKPOINT ========== */
.checkpoint {
    background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    border: 1px solid #86efac;
    border-radius: 12px;
    padding: 20px;
    margin: 24px 0;
}

.checkpoint-title {
    font-size: 16px;
    font-weight: 600;
    color: #16a34a;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.checkpoint-title::before {
    content: '✓';
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    background: #16a34a;
    color: white;
    border-radius: 50%;
    font-size: 14px;
}

.checkpoint-list {
    list-style: none;
    padding: 0;
}

.checkpoint-list li {
    padding: 8px 0 8px 32px;
    position: relative;
}

.checkpoint-list li::before {
    content: '✓';
    position: absolute;
    left: 8px;
    color: #16a34a;
    font-weight: 600;
}

/* ========== STEPS ========== */
.steps {
    counter-reset: step;
}

.step {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
}

.step-number {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    background: var(--primary-color);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 14px;
}

.step-content {
    flex: 1;
    padding-top: 4px;
}

.step-title {
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 8px;
}

/* ========== LINKS ========== */
a {
    color: var(--primary-color);
    text-decoration: none;
    transition: color 0.2s;
}

a:hover {
    color: var(--primary-dark);
    text-decoration: underline;
}

/* Source Code Link */
.source-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    background: #f1f5f9;
    border-radius: 4px;
    font-size: 13px;
    font-family: 'JetBrains Mono', monospace;
    color: var(--primary-color);
    text-decoration: none;
    margin: 4px 0;
}

.source-link:hover {
    background: #e2e8f0;
    text-decoration: none;
}

.source-link::before {
    content: '🔗';
}

/* Tech Tag */
.tech-tag {
    display: inline-block;
    padding: 4px 12px;
    background: var(--primary-color);
    color: white;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
    margin: 4px 4px 4px 0;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1024px) {
    .sidebar {
        transform: translateX(-100%);
        transition: transform 0.3s;
    }

    .sidebar.open {
        transform: translateX(0);
    }

    .main-content {
        margin-left: 0;
    }

    .content {
        padding: 20px;
    }

    .page-title {
        font-size: 28px;
    }
}

@media (max-width: 640px) {
    .top-nav {
        padding: 12px 16px;
    }

    .content {
        padding: 16px;
    }

    .page-title {
        font-size: 24px;
    }

    .section-title {
        font-size: 22px;
    }

    .code-block {
        padding: 16px;
        font-size: 12px;
    }
}

/* ========== PRINT STYLES ========== */
@media print {
    .sidebar,
    .top-nav {
        display: none;
    }

    .main-content {
        margin-left: 0;
    }

    .content {
        padding: 0;
    }

    .code-block {
        page-break-inside: avoid;
    }
}
```

## Color System Reference

| Variable | Value | Usage |
|----------|-------|-------|
| `--primary-color` | #2563eb | Links, buttons, accents |
| `--primary-dark` | #1e40af | Hover states |
| `--success-color` | #10b981 | Success messages |
| `--warning-color` | #f59e0b | Warnings |
| `--danger-color` | #ef4444 | Errors |
| `--text-primary` | #1e293b | Headings, body text |
| `--text-secondary` | #64748b | Secondary text |
| `--bg-light` | #f8fafc | Page background |
| `--bg-white` | #ffffff | Cards, sidebar |
| `--border-color` | #e2e8f0 | Borders, dividers |

## Component Classes Quick Reference

| Class | Purpose |
|-------|---------|
| `.course-layout` | Main flex container |
| `.sidebar` | Fixed sidebar (280px) |
| `.main-content` | Content area with margin-left |
| `.top-nav` | Sticky navigation bar |
| `.breadcrumb` | Breadcrumb navigation |
| `.section` | Content section with margin |
| `.code-block` | Code with syntax highlight |
| `.note` | Blue info box |
| `.warning` | Yellow warning box |
| `.error` | Red error box |
| `.success` | Green success box |
| `.checkpoint` | Learning checkpoint |
| `.step` | Step in process |
| `.card` | Content card |
| `.source-link` | Source code file link |
| `.tech-tag` | Technology badge |
