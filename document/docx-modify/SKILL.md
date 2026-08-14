---
name: docx-modify
description: 在不破坏原有格式、表格、样式的前提下，对现有Word文档（.docx）进行精确的增删改查操作。支持替换文本、修改表格单元格、添加/删除段落、批量更新字段等。当用户需要修改、更新、编辑已有的docx文件内容但保持原有排版时触发。
---

# 现有Word文档精确编辑

## 核心工作流

```
原始文件 → 备份 → 解压 → 分析XML → 精确编辑 → 重新打包 → 验证 → 替换原文件
```

### 1. 备份原始文件

编辑前必须备份：
```bash
cp original.docx original_backup.docx
```

### 2. 解压文档

```bash
python scripts/office/unpack.py input.docx unpacked/
```

### 3. 分析document.xml

读取 `unpacked/word/document.xml`，理解文档结构：
- 文本内容位于 `<w:t>` 标签内
- 段落由 `<w:p>` 包裹
- 表格由 `<w:tbl>` → `<w:tr>` → `<w:tc>` 层级构成
- 格式属性在 `<w:rPr>`（字体、大小、颜色）和 `<w:pPr>`（对齐、缩进）中

### 4. 精确编辑

使用 Edit 工具做字符串替换。**必须**包含精确的缩进空格才能匹配成功。

编辑原则：
- **最小修改**：只替换目标文本，不动周围的XML结构
- **格式继承**：复制相邻段落的 `<w:rPr>` 属性，保持字体、大小、颜色一致
- **段落ID**：新增 `<w:p>` 需要随机生成 `w14:paraId`（8位十六进制）

### 5. 重新打包

```bash
python scripts/office/pack.py unpacked/ output.docx --original input.docx --validate false
```

> 中文文档打包时经常出现 GBK 编码验证错误，使用 `--validate false` 跳过即可。

### 6. 验证

重新解压输出文件，用 Grep 确认修改内容已正确写入。

---

## 常见操作模式

### 模式A：替换现有文本

定位包含目标文本的最小唯一字符串，替换 `<w:t>` 内容：

```xml
<!-- 替换前 -->
<w:r><w:rPr>...</w:rPr><w:t>旧文本</w:t></w:r>

<!-- 替换后 -->
<w:r><w:rPr>...</w:rPr><w:t>新文本</w:t></w:r>
```

### 模式B：填充空白段落

空段落只有 `<w:pPr>` 没有 `<w:r><w:t>`。将其替换为带内容的段落：

```xml
<!-- 空白段落 -->
<w:p w14:paraId="XXXX">
  <w:pPr><w:jc w:val="center"/></w:pPr>
</w:p>

<!-- 替换为带内容的段落（可能需追加多个段落） -->
<w:p w14:paraId="XXXX">
  <w:pPr><w:jc w:val="center"/></w:pPr>
  <w:r><w:rPr>...</w:rPr><w:t>新内容</w:t></w:r>
</w:p>
```

### 模式C：修改表格单元格内容

表格单元格 `<w:tc>` 内包含一个或多个 `<w:p>`。精确定位单元格内的目标段落进行修改。

**注意**：
- 表格列宽由 `<w:tblGrid>` 中的 `<w:gridCol>` 定义
- 单元格合并通过 `<w:vMerge>` 和 `<w:gridSpan>` 实现
- 修改表格内容时不要改动 `<w:tcPr>` 中的宽度属性

### 模式D：批量替换同一文本

如果同一文本在多处出现且需要全部替换，使用 Edit 工具的 `replace_all: true`。

---

## 格式一致性规则

### 字体继承

修改时复制相邻文本的 `<w:rPr>`：
```xml
<w:rPr>
  <w:rFonts w:hint="eastAsia" w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
  <w:color w:val="000000" w:themeColor="text1"/>
  <w:szCs w:val="21"/>
  <w:lang w:val="en-US" w:eastAsia="zh-CN"/>
</w:rPr>
```

### 段落对齐继承

复制 `<w:pPr>` 中的对齐方式：
```xml
<w:pPr>
  <w:jc w:val="center"/>    <!-- 居中对齐 -->
  <w:jc w:val="left"/>      <!-- 左对齐 -->
</w:pPr>
```

### 新增段落ID生成

```bash
python -c "import random; print(''.join(random.choices('0123456789ABCDEF', k=8)))"
```

---

## 中文文档特殊处理

### 编码问题

- unpack/pack 过程中的 GBK 编码错误属于验证器问题，不影响文档正确性
- 始终使用 `--validate false` 跳过验证
- 编辑时确保新写入的中文内容在 XML 中正确保存为 UTF-8

### 中文字体

| 场景 | 字体属性 |
|------|----------|
| 正文/宋体 | `<w:rFonts w:hint="eastAsia" w:ascii="宋体" w:eastAsia="宋体"/>` |
| 黑体标题 | `<w:rFonts w:hint="eastAsia" w:ascii="黑体" w:eastAsia="黑体"/>` |
| 英文/数字 | `<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>` |

---

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| Edit 工具报错 "not found" | 缩进空格不匹配 | 用 Read 工具重新读取目标区域，复制精确的缩进 |
| 打包后文档打不开 | XML 语法错误 | 检查是否遗漏了闭合标签 |
| 格式丢失 | 替换时删除了 `<w:rPr>` | 只替换 `<w:t>` 内容，保留 `<w:rPr>` |
| 表格错位 | 修改了 `<w:tcW>` 或 `<w:gridSpan>` | 不要改动表格结构属性 |

---

## 与docx skill的关系

- **docx skill**：负责新建文档、提取文本、PDF转换等通用操作
- **本 skill（docx-modify）**：专注于在保留原有格式的前提下修改现有文档
- 两者配合使用：先用 docx skill 解压/分析，再用本 skill 指导精确编辑
