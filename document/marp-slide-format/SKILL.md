---
name: marp-slide-format
description: Marp幻灯片格式控制技能。当用户需要制作Marp幻灯片、调整表格/图片布局、设置样式、控制页面显示时使用。适用于任何需要Marp格式调整的场景，包括表格居中、图片大小控制、双列布局、高亮框、参考文献页（IEEE标准引用格式并附Obsidian本地知识库链接）等。
---

# Marp幻灯片格式控制技能

本技能提供Marp幻灯片的常用格式控制方法和代码模板。

## 核心原则

Marp的Markdown语法对某些格式控制有限制，需要使用特定的workaround来实现预期效果。

**为什么这很重要**：直接使用标准的Markdown语法（如`{:width=500}`）在Marp中往往无效，需要使用HTML或CSS方法来实现。

## 常用格式控制方法

### 1. 表格居中

**问题**：Marp中表格默认左对齐，无法用简单的Markdown语法居中。

**解决方案**：使用CSS类配合section配置

```yaml
---
marp: true
style: |
  section.center-table {
    display: flex;
    justify-content: center;
  }
---
```

然后在需要居中表格的页面使用：
```markdown
<!-- _header: "页面标题" _class: center-table -->

| 列1 | 列2 |
|:---|:---|
| 内容 | 内容 |
```

### 2. 图片大小控制

**问题**：Markdown的图片属性语法（`{:height=200}`）在Marp中无效。

**解决方案**：使用HTML `<img>` 标签

```markdown
<!-- 无效 -->
![图片](path/to/image.png){:height=200}

<!-- 有效 -->
<img src="path/to/image.png" height="250" />
```

**为什么**：Marp不支持Markdown属性扩展，必须使用HTML标签来设置图片尺寸。

### 3. 图片居中

**问题**：Marp中图片默认左对齐，且`_align: center`属性可能无效。

**解决方案**：使用表格包裹

```markdown
<table style="margin: 0 auto;">
<tr>
<td style="padding: 0; border: none; background: transparent;">
<img src="path/to/image.png" height="350" />
</td>
</tr>
</table>
```

**为什么这样有效**：表格本身可以通过`margin: 0 auto`居中，而将图片放在无样式的表格单元格中可以实现图片居中效果。

**参数说明**：
- `height="350"`：图片高度（像素），根据需要调整
- `padding: 0`：去除单元格内边距
- `border: none`：去除边框
- `background: transparent`：透明背景

### 4. 双列布局

**用途**：在幻灯片中创建左右两列内容

**代码模板**：
```markdown
<div class="columns">

<div>

**左列内容**

- 要点1
- 要点2

</div>

<div>

**右列内容**

- 要点1
- 要点2

</div>

</div>
```

**CSS配置**（在frontmatter的style部分）：
```yaml
style: |
  .columns { display: flex; gap: 20px; }
  .columns > div { flex: 1; }
```

### 5. 高亮框

**用途**：突出显示重要信息、关键发现

**代码模板**：
```markdown
<div class="highlight">

**关键发现**：
- 要点1
- 要点2

</div>
```

**CSS配置**：
```yaml
style: |
  .highlight {
    background-color: #fff3cd;
    padding: 8px 12px;
    border-radius: 4px;
    border-left: 4px solid #ffc107;
  }
```

### 6. 数学公式

**配置**：在frontmatter中启用MathJax
```yaml
---
marp: true
math: mathjax
---
```

**行内公式**：`$E = mc^2$`

**块级公式**：
```markdown
$$
f(x) = \int_{-\infty}^{\infty} e^{-x^2} dx
$$
```

### 7. 页面配置

**常用属性**：

- `_header: "标题"`：设置页眉
- `_class: class-name`：应用自定义CSS类
- `_align: center`：设置对齐方式（但图片居中建议使用表格方法）

```markdown
<!-- _header: "系统模型" _class: center-table -->

内容...
```

### 8. 参考文献页

**规则**：
- 参考文献必须使用 IEEE 标准引用格式：正文用 `[1]`、`[2]` 编号标注，文献页按序号排列
- 每条文献末尾附上 Obsidian 本地知识库中对应资料的链接。生成文献页前，先在知识库目录中按文献标题/关键词检索笔记（Grep 检索 `.md` 文件，路径由用户指定），命中则取笔记内记录的链接（URL/DOI）或笔记本身的 `obsidian://` 链接

**IEEE 引用格式模板**（作者姓+名首字母，论文标题加引号，期刊/会议名用斜体）：

```markdown
<!-- 期刊论文 -->
[1] A. Author, B. Author, and C. Author, "论文标题," *IEEE Trans. Wireless Commun.*, vol. 68, no. 3, pp. 1234-1246, Mar. 2020.

<!-- 会议论文 -->
[2] A. Author and B. Author, "论文标题," in *Proc. IEEE GLOBECOM*, Rio de Janeiro, Brazil, Dec. 2022, pp. 1-6.

<!-- 3GPP 规范 -->
[3] 3GPP, "Study on channel model for frequencies from 0.5 to 100 GHz," TR 38.901, V17.0.0, Mar. 2022.

<!-- 网络资源 -->
[4] Author or Organization, "页面标题," Year. [Online]. Available: https://...
```

**知识库链接追加**：检索命中的文献，在条目末尾追加链接（`obsidian://open?vault=库名&file=笔记路径` 可直接跳转到对应笔记）：

```markdown
[1] A. Author, "论文标题," *IEEE Trans. Wireless Commun.*, vol. 68, no. 3, pp. 1234-1246, Mar. 2020. [知识库笔记](obsidian://open?vault=MyVault&file=文献/论文标题)

[2] 3GPP, "NR; Physical channels and modulation," TS 38.211, V18.1.0, Apr. 2024. [Online]. Available: https://笔记中记录的URL
```

**整页代码模板**：

```markdown
---

<!-- _header: "参考文献" -->

<div class="refs">

[1] A. Author, "论文标题," *IEEE Trans. Wireless Commun.*, vol. 68, no. 3, pp. 1234-1246, Mar. 2020. [知识库笔记](obsidian://open?vault=MyVault&file=文献/论文标题)

[2] ...

</div>
```

**CSS 配置**（字号明显小于正文，一般一页放 6-8 条）：

```yaml
style: |
  .refs {
    font-size: 16px;
    line-height: 1.5;
  }
  .refs p { margin-bottom: 6px; }
```

## 完整CSS模板

以下是一个完整的Marp CSS配置示例，包含了常用的样式定义：

```yaml
---
marp: true
theme: default
paginate: true
size: 16:9
math: mathjax
style: |
  section {
    font-size: 28px;
    padding: 25px 40px;
  }
  section.lead {
    font-size: 36px;
  }
  section.lead h1 {
    font-size: 60px;
  }
  section.center-table {
    display: flex;
    justify-content: center;
  }
  header {
    font-size: 28px;
    color: #2c3e50;
    font-weight: bold;
    border-bottom: 3px solid #3498db;
    padding-bottom: 8px;
    margin-bottom: 20px;
    width: 95%;
  }
  h1 { font-size: 40px; color: #1a5276; margin-top: 20px; }
  h2 { font-size: 32px; color: #2c3e50; margin-top: 10px; }
  h3 { font-size: 26px; color: #2874a6; margin-top: 20px; }
  p { margin-top: 0; margin-bottom: 8px; line-height: 1.3; }
  table { font-size: 20px; margin-left: auto; margin-right: auto; }
  th { background-color: #d5e8d4; color: #1e6f31; }
  td { padding: 3px 6px; }
  blockquote {
    border-left: 4px solid #e74c3c;
    background: #fdf2f2;
    padding: 6px 10px;
    font-size: 18px;
  }
  .columns { display: flex; gap: 20px; }
  .columns > div { flex: 1; }
  .highlight {
    background-color: #fff3cd;
    padding: 8px 12px;
    border-radius: 4px;
    border-left: 4px solid #ffc107;
  }
  .refs {
    font-size: 16px;
    line-height: 1.5;
  }
  .refs p { margin-bottom: 6px; }
---
```

## 常见问题排查

### 图片大小设置无效

**症状**：使用`{:height=200}`或Markdown属性语法，图片大小不变

**原因**：Marp不支持Markdown属性扩展

**解决**：改用HTML `<img src="..." height="xxx" />`

### 表格无法居中

**症状**：表格始终左对齐

**解决**：使用`_class: center-table`配合CSS中的flex布局

### 图片无法居中

**症状**：使用`_align: center`或flex布局，图片仍然不居中

**解决**：使用表格包裹方法（见"图片居中"部分）

## 工作流程

当用户需要格式控制时：

1. 识别用户的具体需求（表格居中？图片大小？双列布局？参考文献页？）
2. 提供对应的代码模板
3. 解释为什么需要使用这种方法
4. 如需要，提供完整的frontmatter配置
5. 涉及参考文献页时：条目一律用IEEE标准引用格式，并先在用户的Obsidian本地知识库中检索对应笔记，把笔记链接附到文献条目末尾
6. 确保用户理解代码的工作原理
