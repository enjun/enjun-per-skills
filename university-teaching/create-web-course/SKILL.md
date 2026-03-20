---
name: create-web-course
description: Create complete web development courses from existing source code. Use this skill when the user wants to generate educational course materials from a working web system, create programming tutorials based on real projects, build step-by-step lessons from existing codebases, or needs to generate course documentation including syllabus, lessons, and homework exercises. Always use this skill when converting existing web projects into educational materials or when the user mentions teaching web development from an existing codebase.
---

# Create Web Course from Source Code

This skill guides you through creating a complete web development course from an existing source code repository.

## Overview

Generate comprehensive teaching materials including:
- Lesson documents (step-by-step tutorials)
- Quick start guide (environment setup)
- Teaching syllabus (course outline)
- Homework exercises (assessment questions)


## Process Flow

### Step 1: Gather Course Information

Use `AskUserQuestion` tool to collect:

1. **Course Name**: Used as directory name and throughout materials
2. **Source Code Path**: Absolute path to the repository
3. **Course Language**:
   - Chinese (中文) - All content in Chinese
   - English - All content in English
   - Bilingual (中英双译) - Separate zh/ and en/ directories
4. **Number of Lessons**: User MUST explicitly confirm this number

### Step 2: Initialize Course Structure

**IMPORTANT**: Current working directory becomes the course root.

```bash
# Initialize git
git init

# Create directories
mkdir -p main/src main/lessons main/docs
mkdir -p claude_docs

# Copy source code
cp -r [source-path]/* main/src/

# Initial commit
git add .
git commit -m "Initial course setup with source code"
```

Create `CLAUDE.md` with project-specific instructions.

### Step 3: Analyze Source Code

Before planning, understand the codebase:

1. **Project Structure**: Read directory organization, build files
2. **Technology Stack**: Language, framework, database, build tools
3. **Core Modules**: Main features, architecture patterns, entities
4. **Development Sequence**: Identify the actual development order from the codebase
5. **Content Distribution**: Map concepts to the confirmed lesson count


**CRITICAL**: Course organization MUST follow the actual development sequence in the source code repository. Each lesson should build upon previous lessons like building blocks - students implement features step-by-step in the same order the system was originally developed.

**Write Analysis Results**: After completing the analysis, create `claude_docs/codebase-analysis.md` with the following structure:

```markdown
# [Course Name] 源码分析报告

## 项目结构
[Directory organization and key files]

## 技术栈
- **编程语言**: [Language version]
- **框架/库**: [Frameworks and libraries]
- **数据库**: [Database type and version]
- **构建工具**: [Build tools]
- **其他依赖**: [Other dependencies]

## 核心模块
[Main features and architecture patterns]

## 开发顺序分析
[The actual development sequence identified from the codebase]

## 课程内容分配
[How concepts map to the confirmed lesson count]

## 关键设计点
[Important design patterns and architectural decisions]
```

**DO NOT proceed to Step 4 until analysis is complete and written to claude_docs/.**

### Step 4: Create Implementation Plan

Create `claude_docs/implementation-plan.md` with:

```markdown
# [Course Name] 课程实施计划

## 课程信息
- **课程名称**: [Course Name]
- **技术栈**: [Technology Stack]
- **课时数量**: [N] 节课
- **课程语言**: [Chinese | English | Bilingual]
- **源码位置**: [source-code-path]

## 课程详细规划

### 第 1 课：[Title]
**目标**: [Learning objectives]
**本课重点**:
  - 重点 1: [Key concept] - [Learning value]
  - 重点 2: [Key concept] - [Learning value]
  - 重点 3: [Key concept] - [Learning value]
**涉及文件**: [List files with descriptions]
**主要内容**: [Concepts, implementation, flow]
**检查点**: [Understanding outcomes]
**设计思路**: [Design principles]

... (repeat for each lesson)

## 实施步骤
1. Set directory structure (READ references/directory-structure.md first)
2. Generate CSS files (READ references/css-templates.md first)
3. Create HTML pages (lessons/ and docs/) (READ references/html-templates.md first)
4. Write code examples (READ references/code-standards.md first)
5. Write content (READ references/writing-guidelines.md first)
6. Handle languages (READ references/language-guidelines.md first, if bilingual)
7. Create README.md
8. Git commit
```

**PRESENT PLAN TO USER AND WAIT FOR EXPLICIT APPROVAL**

### Step 5: Execute Implementation

**ONLY PROCEED AFTER USER APPROVAL**


## Output Summary

When complete, provide:

```
课程创建完成！

课程名称: [course-name]
源码位置: [source-code-path]
课程位置: [current-directory]/

已生成内容:
- Git 仓库: 已初始化
- main/src/ 源代码
- main/lessons/ 课程文档 (N 节课)
- main/docs/ 支持文档
- README.md

技术栈: [technologies]
课程节数: N
课程语言: [Chinese | English | Bilingual]
```
