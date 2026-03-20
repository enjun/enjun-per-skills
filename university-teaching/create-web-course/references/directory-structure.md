# Directory Structure

Complete course directory layout for different language configurations.

## Single Language Structure (Chinese or English)

```
./                               # Current working directory (course root)
├── CLAUDE.md                   # Project-specific instructions
├── claude_docs/                # Claude-related documentation
│   └── implementation-plan.md  # Detailed course plan
└── main/                       # Main project directory
    ├── lessons/                # HTML lesson documents
    │   ├── css/                # Common stylesheets
    │   │   ├── style.css       # Global course styles
    │   ├── index.html          # Main course index page
    │   ├── lesson-1.html       # Individual lesson pages
    │   ├── lesson-2.html
    │   └── ... (lesson-N.html)
    ├── docs/                   # Additional documentation
    │   ├── quick-start.html    # Environment setup guide
    │   ├── syllabus.html       # Course outline
    │   └── homework.html       # Homework and exercises
    ├── src/                    # Source code (copied from original)
    │   └── [original project structure]
    └── README.md               # Course overview
```

## Bilingual Structure (中英双译)

```
./                               # Current working directory (course root)
├── CLAUDE.md                   # Project-specific instructions
├── claude_docs/                # Claude-related documentation
│   └── implementation-plan.md  # Detailed course plan
└── main/                       # Main project directory
    ├── lessons/                # HTML lesson documents
    │   ├── css/                # Common stylesheets (shared)
    │   │   ├── style.css       # Global course styles
    │   ├── zh/                 # Chinese lessons
    │   │   ├── index.html      # Chinese course index
    │   │   ├── lesson-1.html
    │   │   ├── lesson-2.html
    │   │   └── ... (lesson-N.html)
    │   └── en/                 # English lessons
    │       ├── index.html      # English course index
    │       ├── lesson-1.html
    │       ├── lesson-2.html
    │       └── ... (lesson-N.html)
    ├── docs/                   # Additional documentation
    │   ├── zh/                 # Chinese docs
    │   │   ├── quick-start.html
    │   │   ├── syllabus.html
    │   │   └── homework.html
    │   └── en/                 # English docs
    │       ├── quick-start.html
    │       ├── syllabus.html
    │       └── homework.html
    ├── src/                    # Source code (copied from original)
    │   └── [original project structure]
    └── README.md               # Course overview
```

## Path Reference Guide

### From Lesson to Source Code
- 使用相对路径引用源代码

### From Lesson to CSS

**Single language:**
```html
<link rel="stylesheet" href="css/common.css">
<link rel="stylesheet" href="css/sidebar.css">
<link rel="stylesheet" href="css/content.css">
```

**Bilingual:**
```html
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/sidebar.css">
<link rel="stylesheet" href="../css/content.css">
```

### From Lesson to Docs

**Single language:**
```html
<a href="docs/quick-start.html">快速开始</a>
<a href="docs/syllabus.html">课程大纲</a>
```

**Bilingual (from Chinese lesson):**
```html
<a href="../docs/zh/quick-start.html">快速开始</a>
<a href="../docs/zh/syllabus.html">课程大纲</a>
```

**Bilingual (from English lesson):**
```html
<a href="../docs/en/quick-start.html">Quick Start</a>
<a href="../docs/en/syllabus.html">Syllabus</a>
```

### Between Bilingual Lessons

Language switcher in sidebar:

```html
<!-- In Chinese lesson: main/lessons/zh/lesson-1.html -->
<div class="lang-switcher">
    <a href="../en/lesson-1.html" class="lang-link">English</a>
    <span class="lang-divider">|</span>
    <a href="../zh/lesson-1.html" class="lang-link current">中文</a>
</div>

<!-- In English lesson: main/lessons/en/lesson-1.html -->
<div class="lang-switcher">
    <a href="../en/lesson-1.html" class="lang-link current">English</a>
    <span class="lang-divider">|</span>
    <a href="../zh/lesson-1.html" class="lang-link">中文</a>
</div>
```


