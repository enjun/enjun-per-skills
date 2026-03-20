# Code Consistency Standards

**CRITICAL**: All code in lesson pages must be consistent with the source code.

## Core Rules

### 1. Exact Match

Code content in `<code>` blocks must match source code exactly.



### 3. HTML Entity Encoding

Use HTML entities for special characters:

- `<` → `&lt;`
- `>` → `&gt;`
- `&` → `&amp;`

```html
<!-- ❌ WRONG -->
<code>if (a < b && c > d) { ... }</code>

<!-- ✅ CORRECT -->
<code>if (a &lt; b &amp;&amp; c &gt; d) { ... }</code>
```

### 4. Source Code Links

All actual project code MUST have hyperlinks to source files.

**IMPORTANT**: Use relative path format to link to source files.

**推荐模式：路径 + 源码链接（两行模式）**

```html
<!-- 先显示文件路径，再提供源码链接 -->
<div class="file-path">文件路径</div>
<a href="文件路径" class="source-link">查看完整源码</a>
```


### 5. Code Block Length

Single code block should not exceed 50 lines. Split longer code into multiple sections with proper headings.


### 6. Language Attribute

Always set the `data-lang` attribute on code blocks to display the language label:

```html
<div class="code-block" data-lang="Java">
<div class="code-block" data-lang="SQL">
<div class="code-block" data-lang="XML">
<div class="code-block" data-lang="bash">
<div class="code-block" data-lang="架构图">
```

