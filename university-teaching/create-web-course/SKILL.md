---
name: create-web-course
description: Create complete web development courses from existing source code. Use this skill when the user wants to generate educational course materials from a working web system, create programming tutorials based on real projects, build step-by-step lessons from existing codebases, or needs to generate course documentation including syllabus, lessons, and homework exercises. Always use this skill when converting existing web projects into educational materials or when the user mentions teaching web development from an existing codebase.
---

# Create Web Course from Source Code

This skill guides you through creating a complete web development course from an existing source code repository. You will analyze the codebase and generate comprehensive teaching materials.

## Overview

The course creation process analyzes existing source code and produces:

1. **Lesson documents** - Step-by-step tutorials corresponding to the codebase structure
2. **Quick start guide** - Comprehensive environment setup and launch instructions
3. **Teaching syllabus** - Course outline with learning objectives
4. **Homework exercises** - Assessment questions and exercises for each lesson

## Step 1: Gather Source Code Information

Before generating any content, ask the user for:

### 1.1 Source Code Location

```
Please provide the absolute path to the source code repository you want to create a course from.
```

### 1.2 Course Language

```
What language should the course materials be in?
- Chinese (中文)
- English
- Bilingual (中英双译)
```

Use the AskUserQuestion tool to gather this information when appropriate.

### Language Options Details

- **Chinese (中文)**: All lesson content, titles, and documentation in Chinese
- **English**: All lesson content, titles, and documentation in English
- **Bilingual (中英双译)**: Generate both Chinese and English versions:
  - `lessons/zh/` - Chinese lessons
  - `lessons/en/` - English lessons
  - Separate index pages for each language
  - Language switcher in the sidebar

## Step 2: Analyze the Source Code

Once you have the source code path, analyze the project:

### 2.1 Identify Project Structure

- Read the main project directory structure
- Identify the source code organization (packages, modules, directories)
- Look for build configuration files (pom.xml, package.json, requirements.txt, etc.)
- Identify the technology stack

### 2.2 Determine Technology Stack

From configuration files, identify:
- **Programming language**: Java, Python, JavaScript, PHP, etc.
- **Framework**: Spring Boot, Django, Express, Laravel, etc.
- **Database**: MySQL, PostgreSQL, MongoDB, etc.
- **Build tool**: Maven, Gradle, npm, Composer, etc.
- **Frontend**: JSP, Thymeleaf, React, Vue, etc.

### 2.3 Analyze Core Modules

Identify the main functional modules:
- What are the main features of the system?
- How is the code organized (Controller-Service-DAO, MVC, etc.)?
- What are the key entities/models?
- What are the main user workflows?

### 2.4 Suggest Course Structure

Based on your analysis, suggest a course structure:

```
Based on the source code analysis, I recommend [N] lessons:

Lesson 1: [Topic] - [Brief description]
Lesson 2: [Topic] - [Brief description]
...
Lesson N: [Topic] - [Brief description]

Each lesson will cover approximately [X] files/concepts.

How many lessons would you like?
```

## Step 3: Plan the Course Structure

After user confirmation, design a logical progression:

- **Lesson 1**: Project overview and environment setup - Understand the project structure
- **Early lessons**: Foundation concepts - Core framework basics, data models, configuration
- **Middle lessons**: Progressive features - Add capabilities following the dependency chain
- **Final lessons**: Advanced features and polish - Complete the application understanding

Each lesson should:
- Build on previous concepts
- Cover specific source files and their functionality
- Take approximately 2-3 hours for students to complete
- Include clear checkpoints (what students should understand by end of lesson)

## Step 4: Create the Course Structure

Create a well-organized course documentation structure based on the selected language:

### 4.1 Single Language Structure (Chinese or English)

```
project-root/
├── lessons/          # HTML lesson documents
│   ├── css/          # Common stylesheets
│   │   ├── common.css       # Common styles
│   │   ├── sidebar.css      # Sidebar styles
│   │   └── content.css      # Content styles
│   ├── index.html    # Main course index page
│   ├── lesson-1.html # Individual lesson pages
│   ├── lesson-2.html
│   └── ...
└── docs/             # Additional documentation
    ├── quick-start.html
    ├── syllabus.html
    └── homework.html        # Homework and exercises (was questions.html)
```

### 4.2 Bilingual Structure (中英双译)

```
project-root/
├── lessons/          # HTML lesson documents
│   ├── css/          # Common stylesheets (shared)
│   │   ├── common.css
│   │   ├── sidebar.css
│   │   └── content.css
│   ├── zh/           # Chinese lessons
│   │   ├── index.html
│   │   ├── lesson-1.html
│   │   └── ...
│   └── en/           # English lessons
│       ├── index.html
│       ├── lesson-1.html
│       └── ...
└── docs/             # Additional documentation
    ├── zh/           # Chinese docs
    │   ├── quick-start.html
    │   ├── syllabus.html
    │   └── homework.html
    └── en/           # English docs
        ├── quick-start.html
        ├── syllabus.html
        └── homework.html
```

## Step 5: Generate Common CSS Files

Create the shared CSS files that all lesson pages will use:

### 5.1 lessons/css/common.css

```css
/* Reset and Base Styles */
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.7;
    color: #444;
}

/* Links */
a { color: #3498db; text-decoration: none; transition: color 0.3s; }
a:hover { color: #2980b9; }

/* Code Links */
a code { color: inherit; }

/* Responsive */
@media (max-width: 768px) {
    body { font-size: 14px; }
}
```

### 5.2 lessons/css/sidebar.css

```css
/* Page Layout */
.page-container { display: flex; min-height: 100vh; }

/* Sidebar */
.sidebar {
    width: 280px;
    background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    color: white;
    position: fixed;
    height: 100vh;
    overflow-y: auto;
    padding: 20px 0;
    box-shadow: 2px 0 10px rgba(0,0,0,0.1);
}

.sidebar-header {
    padding: 0 20px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.sidebar-header h2 {
    font-size: 1.2em;
    margin-bottom: 5px;
}

.sidebar-header p {
    font-size: 0.85em;
    opacity: 0.8;
}

.sidebar-back { padding: 15px 20px; }

.sidebar-back a {
    color: #3498db;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}

.sidebar-back a:hover { color: #5dade2; }

.sidebar-nav { padding: 10px 0; }

.sidebar-nav h3 {
    font-size: 0.85em;
    text-transform: uppercase;
    opacity: 0.6;
    padding: 15px 20px 10px;
    letter-spacing: 1px;
}

.sidebar-nav ul { list-style: none; }
.sidebar-nav li { margin: 0; }

.sidebar-nav a {
    display: block;
    padding: 12px 20px;
    color: rgba(255,255,255,0.8);
    transition: all 0.3s;
    border-left: 3px solid transparent;
}

.sidebar-nav a:hover,
.sidebar-nav a.active {
    background: rgba(255,255,255,0.1);
    color: white;
    border-left-color: #3498db;
}

.sidebar-nav .current {
    background: rgba(52, 152, 219, 0.3);
    color: white;
    border-left-color: #3498db;
}

/* Language Switcher (for bilingual courses) */
.lang-switcher {
    padding: 10px 20px;
    margin: 10px 0;
    text-align: center;
    border-top: 1px solid rgba(255,255,255,0.1);
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.lang-switcher .lang-link {
    color: rgba(255,255,255,0.7);
    text-decoration: none;
    padding: 5px 10px;
    border-radius: 4px;
    transition: all 0.3s;
}

.lang-switcher .lang-link:hover {
    color: white;
    background: rgba(255,255,255,0.1);
}

.lang-switcher .lang-link.current {
    color: white;
    background: rgba(52, 152, 219, 0.5);
    font-weight: bold;
}

.lang-switcher .lang-divider {
    color: rgba(255,255,255,0.3);
    margin: 0 5px;
}

/* Responsive */
@media (max-width: 768px) {
    .sidebar {
        width: 100%;
        height: auto;
        position: relative;
    }
}
```

### 5.3 lessons/css/content.css

```css
/* Main Content Area */
.main-content {
    margin-left: 280px;
    flex: 1;
    padding: 40px;
    max-width: 900px;
}

/* Headings */
h1 {
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
    padding-bottom: 15px;
    margin-bottom: 30px;
    font-size: 2em;
}

h2 {
    color: #34495e;
    margin-top: 40px;
    margin-bottom: 20px;
    font-size: 1.6em;
}

h3 {
    color: #555;
    margin-top: 30px;
    margin-bottom: 15px;
    font-size: 1.3em;
}

h4 {
    color: #666;
    margin-top: 25px;
    margin-bottom: 10px;
    font-size: 1.1em;
}

/* Paragraphs and Lists */
p { margin-bottom: 15px; }
ul, ol { margin: 15px 0 15px 25px; }
li { margin: 8px 0; }

/* Info Boxes */
.objectives {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    padding: 20px;
    border-radius: 10px;
    margin: 25px 0;
    border-left: 5px solid #2196f3;
}

.objectives h2 {
    color: #1976d2;
    margin-top: 0;
    font-size: 1.3em;
}

.checkpoint {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    padding: 20px;
    border-radius: 10px;
    margin: 25px 0;
    border-left: 5px solid #4caf50;
}

.checkpoint h3 { color: #2e7d32; margin-top: 0; }

.tip {
    background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
    padding: 15px 20px;
    border-radius: 10px;
    margin: 20px 0;
    border-left: 5px solid #ffc107;
}

.tip strong { color: #f57c00; }

.info {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    padding: 15px 20px;
    border-radius: 10px;
    margin: 20px 0;
    border-left: 5px solid #2196f3;
}

.info strong { color: #1976d2; }

/* Code Blocks */
.code-block {
    background: #263238;
    color: #aed581;
    padding: 20px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 20px 0;
    line-height: 1.5;
}

.code-block pre {
    margin: 0;
    white-space: pre;
    word-wrap: normal;
    overflow-x: auto;
}

.code-block code {
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 0.95em;
    color: inherit;
    background: transparent;
    padding: 0;
}

/* Inline Code */
p > code, li > code, td > code {
    background: #f5f5f5;
    padding: 3px 8px;
    border-radius: 4px;
    font-family: 'Consolas', monospace;
    font-size: 0.9em;
    color: #e91e63;
    white-space: nowrap;
}

/* Code Links */
a code.linked-code {
    color: #3498db;
    background: #e3f2fd;
    text-decoration: underline;
    text-decoration-style: dotted;
}

a code.linked-code:hover {
    color: #2980b9;
    background: #bbdefb;
}

/* Code Checklist */
.code-checklist {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
}

.code-checklist h3 {
    color: #2c3e50;
    margin-top: 0;
    margin-bottom: 15px;
}

.code-checklist ul {
    list-style: none;
    padding: 0;
}

.code-checklist li {
    padding: 8px 0;
    border-bottom: 1px solid #e0e0e0;
}

.code-checklist li:last-child {
    border-bottom: none;
}

.code-checklist .file-path {
    font-family: 'Consolas', monospace;
    font-weight: bold;
    color: #1976d2;
}

.code-checklist .file-desc {
    color: #666;
    font-size: 0.9em;
}

/* Design Decision */
.design-decision {
    background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
    padding: 20px;
    border-radius: 10px;
    margin: 25px 0;
    border-left: 5px solid #9c27b0;
}

.design-decision h3 {
    color: #6a1b9a;
    margin-top: 0;
}

.design-decision ul {
    margin-bottom: 0;
}

/* Navigation Buttons */
.lesson-nav {
    display: flex;
    justify-content: space-between;
    margin-top: 50px;
    padding-top: 30px;
    border-top: 2px solid #eee;
}

.lesson-nav a {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 12px 25px;
    background: #3498db;
    color: white;
    border-radius: 8px;
    transition: background 0.3s;
}

.lesson-nav a:hover { background: #2980b9; }

/* Responsive */
@media (max-width: 768px) {
    .main-content {
        margin-left: 0;
        padding: 20px;
    }

    .page-container {
        flex-direction: column;
    }

    h1 { font-size: 1.5em; }
    h2 { font-size: 1.3em; }
    h3 { font-size: 1.1em; }
}
```

## Step 6: Generate Lesson Documents

### 6.1 Create Main Index Page (lessons/index.html)

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>课程主页 - [System Name]</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        .header {
            background: white;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .header h1 { color: #333; font-size: 2.5em; margin-bottom: 15px; }
        .header p { color: #666; font-size: 1.1em; }
        .lessons-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }
        .lesson-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }
        .lesson-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        .lesson-card .lesson-number {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .lesson-card h3 { color: #333; margin-bottom: 10px; font-size: 1.3em; }
        .lesson-card p { color: #666; font-size: 0.95em; line-height: 1.5; margin-bottom: 15px; }
        .lesson-card a {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            transition: background 0.3s;
        }
        .lesson-card a:hover { background: #5568d3; }
        .footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.9;
        }
        .footer a { color: white; text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>[System Name] 课程</h1>
            <p>完整的Web开发实战教程 - 从源码学习开发</p>
        </div>
        <div class="lessons-grid">
            <div class="lesson-card">
                <span class="lesson-number">第1课</span>
                <h3>[Lesson 1 Title]</h3>
                <p>[Brief description of lesson content]</p>
                <a href="lesson-1.html">开始学习 →</a>
            </div>
            <!-- Repeat for each lesson -->
        </div>
        <div class="footer">
            <p>建议按顺序学习，每节课大约需要2-3小时完成</p>
            <p>
                <a href="docs/quick-start.html">快速开始</a> |
                <a href="docs/syllabus.html">课程大纲</a> |
                <a href="docs/homework.html">课后作业</a>
            </p>
        </div>
    </div>
</body>
</html>
```

### 6.2 Create Individual Lesson Pages

For each lesson, create `lessons/lesson-N.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>第 N 课：[Lesson Title] - [System Name] 课程</title>
    <link rel="stylesheet" href="css/common.css">
    <link rel="stylesheet" href="css/sidebar.css">
    <link rel="stylesheet" href="css/content.css">
</head>
<body>
    <div class="page-container">
        <!-- Fixed Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <h2>[System Name] 课程</h2>
                <p>Web开发实战教程</p>
            </div>
            <div class="sidebar-back">
                <a href="index.html">← 返回课程主页</a>
            </div>

            <!-- Language Switcher (for bilingual courses only) -->
            <!-- <div class="lang-switcher">
                <a href="../en/lesson-N.html" class="lang-link">English</a>
                <span class="lang-divider">|</span>
                <a href="../zh/lesson-N.html" class="lang-link current">中文</a>
            </div> -->

            <nav class="sidebar-nav">
                <h3>课程目录</h3>
                <ul>
                    <li><a href="lesson-1.html" class="current">第1课：[Title]</a></li>
                    <li><a href="lesson-2.html">第2课：[Title]</a></li>
                    <!-- All lessons listed here -->
                </ul>
            </nav>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <h1>第 N 课：[Lesson Title]</h1>

            <div class="objectives">
                <h2>📚 本课目标</h2>
                <ul>
                    <li>Learning objective 1</li>
                    <li>Learning objective 2</li>
                </ul>
            </div>

            <!-- Code Checklist -->
            <div class="code-checklist">
                <h3>本节课涉及的文件</h3>
                <ul>
                    <li>
                        <span class="file-path"><a href="../src/path/to/File.java"><code class="linked-code">File.java</code></a></span>
                        <div class="file-desc">文件功能说明</div>
                    </li>
                    <!-- More files -->
                </ul>
            </div>

            <h2>前置知识</h2>
            <p>What students should know before starting this lesson...</p>

            <h2>课程内容</h2>

            <!-- Design Decision Section -->
            <div class="design-decision">
                <h3>设计思路</h3>
                <ul>
                    <li>设计原则1：说明为什么这样设计</li>
                    <li>设计原则2：说明核心考虑因素</li>
                    <li>设计原则3：说明与其他模块的关系</li>
                </ul>
            </div>

            <h3>概念讲解</h3>
            <p>Explain the concepts clearly with examples...</p>

            <div class="info">
                <strong>ℹ️ 概念解释：</strong>
                技术术语的通俗解释（如：DTO是数据传输对象，用于在不同层之间传递数据）
            </div>

            <h3>代码实现</h3>
            <div class="code-block">
                <pre><code>// Show actual code from source with explanations
// Use relative paths for links to source files
// Code must match source exactly, including comments
function example() {
    // Explain what this does
    return result;
}</code></pre>
            </div>

            <p>相关代码: <a href="../src/path/to/File.java"><code class="linked-code">File.java:42</code></a></p>

            <h3>代码执行流程</h3>
            <p>Use business scenarios to explain how the code works...</p>

            <div class="checkpoint">
                <h3>✅ 检查点</h3>
                <p>By the end of this lesson, you should understand:</p>
                <ul>
                    <li>Concept X and how it works</li>
                    <li>How File Y implements feature Z</li>
                </ul>
            </div>

            <div class="tip">
                <strong>💡 提示：</strong> Common pitfall or helpful hint...
            </div>

            <h2>课后思考</h2>
            <ul>
                <li>Question to think about...</li>
            </ul>

            <!-- Lesson Navigation -->
            <div class="lesson-nav">
                <a href="lesson-N-1.html" style="visibility: hidden;">← 上一课</a>
                <a href="lesson-N+1.html">下一课 →</a>
            </div>
        </main>
    </div>
</body>
</html>
```

### 6.3 Lesson Navigation Requirements

For each lesson page:

1. **Fixed Sidebar** with:
   - Course title and description
   - "Return to Index" link (返回课程主页)
   - Complete lesson list with current lesson highlighted (class="current")
   - All lesson links

2. **Bottom Navigation** with:
   - "Previous Lesson" link (上一课) - hidden on first lesson
   - "Next Lesson" link (下一课) - hidden on last lesson

3. **Active State**: Current lesson in sidebar should have `class="current"` for visual distinction

## Step 7: Course Documentation Standards

### 7.1 Code Consistency Rules

**CRITICAL**: All code in lesson pages must be consistent with the source code:

1. **Exact Match**: Code content in `<code>` blocks must match source code exactly
2. **Include Comments**: If source code has comments, they must be included
3. **HTML Entity Encoding**: Use `&lt;` and `&gt;` for `<` and `>` in code
4. **Code Links**: Add hyperlinks to source code for all actual project code
   ```html
   <a href="../src/main/java/com/library/model/Book.java"><code class="linked-code">Book.java</code></a>
   ```

### 7.2 Content Writing Guidelines

- **Code Block Length**: Single code block should not exceed 50 lines. Split longer code into multiple sections.
- **Design First**: Explain design principles (3-5 points) before showing code
- **Scenario-Based**: Use specific business scenarios to explain technical concepts
- **Concept Explanation**: Technical terms need plain language explanations
- **Remove Redundancy**: Delete duplicate, confusing, or irrelevant content
- **Logical Order**: Organize by learning sequence, dependencies first

### 7.3 Lesson Structure Best Practices

Each lesson should follow this structure:

1. **Learning Objectives** (本课目标)
2. **Code Checklist** (涉及的文件) - List all source files covered
3. **Prerequisites** (前置知识)
4. **Design Decisions** (设计思路) - 3-5 core principles
5. **Concept Explanation** (概念讲解) - With plain language definitions
6. **Code Implementation** (代码实现) - With source links, max 50 lines per block
7. **Execution Flow** (执行流程) - Scenario-based explanation
8. **Checkpoint** (检查点) - What students should understand
9. **Tips** (提示) - Common pitfalls
10. **Reflection Questions** (课后思考)

### 7.4 Special Section Templates

**Application Startup Flow** (for Lesson 1):
```html
<div class="startup-flow">
    <div class="flow-phase">
        <div class="flow-step">
            <span class="step-number">1</span>
            <h4>阶段名称</h4>
            <p>描述</p>
            <code>关键代码</code>
        </div>
    </div>
</div>
```

**Code Checklist** (beginning of each lesson):
```html
<div class="code-checklist">
    <h3>本节课涉及的文件</h3>
    <ul>
        <li>
            <span class="file-path"><a href="../src/..."><code class="linked-code">File.java</code></a></span>
            <div class="file-desc">文件功能说明</div>
        </li>
    </ul>
</div>
```

### 7.5 Language Guidelines

**Chinese Course (中文)**:
- Use Chinese for all content (titles, descriptions, explanations)
- Keep technical terms in English where appropriate (e.g., HTTP, REST API)
- Code comments can remain in original language from source
- Section titles: 本课目标、涉及的文件、前置知识、设计思路、概念讲解、代码实现、执行流程、检查点、提示、课后思考

**English Course**:
- Use English for all content
- Keep technical terms in their standard form
- Code comments remain as in source code
- Section titles: Learning Objectives, Code Checklist, Prerequisites, Design Decisions, Concept Explanation, Code Implementation, Execution Flow, Checkpoint, Tips, Reflection Questions

**Bilingual Course (中英双译)**:
- Create separate directories for each language (lessons/zh/ and lessons/en/)
- Use consistent section titles in each language
- Add language switcher in sidebar for easy navigation
- Link to corresponding lesson in other language
- Example language switcher:
```html
<div class="lang-switcher">
    <a href="../en/lesson-1.html" class="lang-link">English</a>
    <span class="lang-divider">|</span>
    <a href="../zh/lesson-1.html" class="lang-link current">中文</a>
</div>
```

## Step 8: Create Quick Start Guide (docs/quick-start.html)

A comprehensive HTML guide covering:

### System Requirements
- Operating system support (Windows, macOS, Linux)
- Hardware requirements (if any)

### Prerequisites Installation
**For each required tool:**
- What it is and why it's needed
- Download links for each OS
- Step-by-step installation instructions
- How to verify installation
- Common installation issues and solutions

### Project Setup
1. Clone/download instructions
2. Dependency installation
3. Configuration files explanation
4. Environment variables (if any)

### Running the Application
- Development server startup command
- How to access the application (URL)
- Expected output on success
- Basic troubleshooting

### IDE Recommendations
- Suggested editors/IDEs
- Helpful extensions

### Verification Checklist
A section where students can confirm:
- [ ] Tool X installed (version Y)
- [ ] Project downloaded/unzipped
- [ ] Dependencies installed
- [ ] Server running on port Z
- [ ] Application accessible at http://localhost:PORT

## Step 9: Create Syllabus (docs/syllabus.html)

An HTML document with:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>课程大纲 - [System Name]</title>
    <style>
        /* Similar styling to lessons */
        .lesson { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .prerequisites { background: #f8f9fa; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>课程大纲：[System Name] Web 开发实战</h1>

    <div class="prerequisites">
        <h2>前置要求</h2>
        <p>List student prerequisites...</p>
    </div>

    <h2>课程概述</h2>
    <p>Brief description of what students will build and learn...</p>

    <h2>课程安排</h2>
    <div class="lesson">
        <h3>第1课：[Title]</h3>
        <p><strong>内容：</strong> Brief description...</p>
        <p><strong>目标：</strong> What students will learn...</p>
    </div>
    <!-- Repeat for each lesson -->

    <h2>学习成果</h2>
    <p>After completing this course, students will be able to...</p>
</body>
</html>
```

## Step 10: Create Homework Document (docs/homework.html)

An HTML document with homework and exercises for each lesson:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>课后作业 - [System Name]</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 15px; }
        h2 { color: #34495e; margin-top: 30px; }
        .exercise { margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; }
        .answer { display: none; margin-top: 10px; padding: 10px; background: #e7f3ff; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>课后作业与练习</h1>

    <h2>第1课作业</h2>
    <div class="exercise">
        <p><strong>练习1:</strong> Exercise description...</p>
        <details>
            <summary>查看参考答案</summary>
            <div class="answer">Reference answer...</div>
        </details>
    </div>
    <!-- Include 3-5 exercises per lesson -->

    <h2>综合练习</h2>
    <div class="exercise">
        <p><strong>综合项目:</strong> Cross-lesson exercise that integrates concepts...</p>
    </div>
</body>
</html>
```

### Exercise Types to Include

- **Conceptual questions**: Test understanding of principles
- **Code reading**: "What does this code do?"
- **Debugging**: "Find and fix the bug"
- **Extension**: "How would you add feature X?"
- **Comparison**: "What's the difference between approach A and B?"

## Step 11: Create README.md

Add a README.md to the project root with:

```markdown
# [System Name] - Web开发课程项目

这是一个用于学习Web开发的教学项目。

## 快速开始

请参阅 [快速开始指南](docs/quick-start.html) 获取详细的安装和运行说明。

## 课程内容

- 课程大纲: [docs/syllabus.html](docs/syllabus.html)
- 课程文件: [lessons/](lessons/) 目录
- 课后作业: [docs/homework.html](docs/homework.html)

## 项目结构

```
project-root/
├── lessons/          # 课程文档
│   ├── css/          # 公共样式
│   ├── index.html    # 课程主页
│   └── lesson-*.html # 各节课内容
├── docs/             # 教学文档
│   ├── quick-start.html
│   ├── syllabus.html
│   └── homework.html
├── src/              # 源代码
└── README.md         # 本文件
```

## 技术栈

- [List the technologies used]
```

## Technology-Specific Adaptation

When analyzing different technology stacks:

### For Java (Spring Boot, Jakarta Servlet)
- Look for pom.xml or build.gradle
- Identify main classes with @SpringBootApplication or @WebServlet
- Analyze package structure: controller, service, dao, model
- Check for application.properties or application.yml

### For Python (Django, Flask, FastAPI)
- Look for requirements.txt or setup.py
- Identify manage.py (Django) or app.py (Flask/FastAPI)
- Analyze models.py, views.py, urls.py structure
- Check for settings.py or config files

### For JavaScript/Node.js (Express, NestJS)
- Look for package.json
- Identify main entry point (index.js, app.js, main.ts)
- Analyze routes, controllers, services structure
- Check for .env files

### For PHP (Laravel)
- Look for composer.json
- Identify artisan commands and routes/api.php
- Analyze app/ directory structure
- Check for .env files

## Before Completing

Verify you have created:

- [ ] **Main course index page** (lessons/index.html) with links to all lessons
- [ ] **Common CSS files** (lessons/css/common.css, sidebar.css, content.css)
- [ ] All lesson HTML files (lessons/lesson-1.html through lesson-N.html)
- [ ] Each lesson page has **fixed sidebar** with course navigation
- [ ] Each lesson page has **current lesson highlighted** in sidebar
- [ ] Each lesson page has **previous/next navigation** at bottom
- [ ] Each lesson has **code checklist** at the beginning
- [ ] Each lesson has **design decision** section before code
- [ ] All code has **source links** with relative paths
- [ ] Quick start guide (docs/quick-start.html)
- [ ] Syllabus (docs/syllabus.html)
- [ ] Homework document (docs/homework.html)
- [ ] README.md in project root
- [ ] All code in lessons matches source code exactly
- [ ] Each lesson builds on previous ones
- [ ] Setup guide covers multiple operating systems

## Output Format

After completing the course generation, summarize what was created:

```
课程创建完成！

源码位置: [source-code-path]
课程位置: [current-directory]

已生成内容:
- 课程主页: lessons/[zh|en/]index.html
- 公共样式: lessons/css/ (common.css, sidebar.css, content.css)
- 课程文档: lessons/[zh|en/] 目录 (N 节课)
- 快速开始: docs/[zh|en/]quick-start.html
- 课程大纲: docs/[zh|en/]syllabus.html
- 课后作业: docs/[zh|en/]homework.html

技术栈: [list technologies]
课程节数: N
课程语言: [Chinese | English | Bilingual (Chinese + English)]

课程特色:
- 基于真实源码分析生成
- 每节课代码清单清晰
- 设计决策说明详细
- 代码与源码完全一致
- 所有代码包含源码链接
- [Bilingual only] 支持中英双语切换

下一步:
1. 打开 lessons/[zh|en/]index.html 查看课程主页
2. 点击任意课程卡片开始学习
3. 查看 docs/quick-start.html 了解如何启动项目
```
