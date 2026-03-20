# Content Writing Guidelines

Guidelines for creating high-quality course content with the modern design system.

## Core Principles

### 搭积木式教学原则 (Building Block Teaching)

**CRITICAL**: 课程内容的组织必须遵循源码库中系统开发的实际顺序，每节课像搭积木一样逐步构建系统。

#### 课程排列顺序

1. **遵循开发顺序**：课程顺序必须与源码库中的开发顺序一致
   - 从基础到高级，从简单到复杂
   - 每节课建立在前面课程的基础上
   - 系统功能按照实际开发的先后顺序讲解

2. **依赖关系明确**：
   - 前面课程的知识点是后续课程的前置条件
   - 在讲解新知识时，明确引用前面课程的相关内容
   - 使用 "在第 X 课中，我们学习了..." 的表述

#### 每节课的内容组织

1. **逐步构建目标**：
   - 每节课都有明确的阶段性目标
   - 课程内容按照实现该目标的逻辑顺序展开
   - 从概念设计 → 原理理解 → 源码实现 → 执行验证

2. **知识点递进**：
   - 重要知识点 1 → 重要知识点 2 → 重要知识点 3
   - 每个知识点都为后续知识点铺垫
   - 最终实现本节课的整体目标

3. **前后呼应**：
   - 课程开始说明本课要实现什么
   - 课程中间逐步讲解如何实现
   - 课程结尾总结实现了什么，为下节课铺垫

### 1. 重点突出与详解 (Highlight Key Points)

**每节课必须有明确的重点，对重点内容进行详细解释。**

每节课开始时，在"学习目标"之后添加"本课重点"部分，明确标注核心知识点（建议3-5个）。

**详解重点内容的要求：**
- 每个重点使用 `.card` 组件独立展示
- 标题使用 `重点 N：[标题]` 格式
- 说明"为什么这是重点"（学习价值）
- 列出"关键要点"（具体知识点）
- 对复杂概念添加 `.note` 框进行深入解释

```html
<!-- 复杂概念的深入解释示例 -->
<div class="card">
    <h4 class="card-title">重点 4：三层架构设计</h4>
    <p>三层架构是企业级应用开发的标准模式。</p>

    <div class="note">
        <strong>为什么需要三层架构？</strong><br>
        如果所有代码都写在 Servlet 中，会出现以下问题：<br>
        1. 代码臃肿，难以维护<br>
        2. 业务逻辑和数据访问混在一起<br>
        3. 无法复用代码<br>
        4. 难以进行单元测试<br>
        <br>
        三层架构通过职责分离解决了这些问题。
    </div>

    <p><strong>关键要点：</strong></p>
    <ul>
        <li><strong>Controller 层：</strong>接收请求，调用 Service，返回响应</li>
        <li><strong>Service 层：</strong>处理业务逻辑，事务控制</li>
        <li><strong>DAO 层：</strong>数据访问，CRUD 操作</li>
    </ul>
</div>
```

### 2. Design First

Always explain design principles (3-5 points) before showing code.

```html
<!-- ✅ CORRECT ORDER -->
<section class="section">
    <h2 class="section-title">设计思路</h2>
    <ul>
        <li><strong>单一职责原则：</strong>每个类只负责一个功能，DAO层只处理数据访问，Service层处理业务逻辑</li>
        <li><strong>依赖注入：</strong>Controller通过Service获取业务功能，降低层与层之间的耦合</li>
        <li><strong>接口抽象：</strong>使用接口定义契约，便于后续扩展和测试</li>
    </ul>
</section>

<section class="section">
    <h2 class="section-title">代码实现</h2>
    <div class="code-block" data-lang="Java">
<pre><code>// Code comes after design explanation</code></pre>
    </div>
</section>
```

### 3. Scenario-Based Explanations

Use specific business scenarios to explain technical concepts.

```html
<!-- ❌ TOO ABSTRACT -->
<h3 class="section-subtitle">代码执行流程</h3>
<p>首先调用方法A，然后调用方法B，最后返回结果。</p>

<!-- ✅ SCENARIO-BASED -->
<h3 class="section-subtitle">代码执行流程</h3>
<p>当用户点击"查询图书"按钮时：</p>
<ol>
    <li>浏览器发送 GET 请求到 <code>/books</code></li>
    <li><code>BookController.doGet()</code> 接收请求</li>
    <li>调用 <code>BookService.getAllBooks()</code> 获取所有图书</li>
    <li>Service 层调用 <code>BookDAO.findAll()</code> 查询数据库</li>
    <li>查询结果封装成 <code>List&lt;Book&gt;</code> 返回</li>
    <li>数据存入 request，转发到 JSP 页面展示</li>
</ol>
```

### 4. Concept Explanation

Technical terms need plain language explanations. Use the `.note` class.

```html
<p>在这个项目中，我们使用了 <strong>DTO（Data Transfer Object，数据传输对象）</strong>模式。</p>

<div class="note">
DTO 是一种设计模式，用于在不同层之间传输数据。比如从数据库查询到的数据需要展示给用户，直接使用实体类可能暴露敏感信息或包含不必要的字段。DTO 只包含需要传输的字段，更加安全和高效。
</div>
```


## Section Guidelines

### Learning Objectives (学习目标)

Use a clean section with list.

```html
<section class="section">
    <h2 class="section-title">📚 本课目标</h2>
    <ul>
        <li>理解 Servlet 请求处理流程</li>
        <li>掌握 doGet 和 doPost 方法的使用</li>
        <li>学会使用 HttpServletRequest 获取请求参数</li>
        <li>能够实现简单的图书查询功能</li>
    </ul>
</section>
```



## Homework Exercise Structure

**IMPORTANT**: All homework exercises MUST follow this structure.

### Exercise Types

- **📝 基础练习** - Core concepts, all students should complete
- **🚀 进阶练习** - Advanced challenges for motivated students
- **🎯 综合练习** - Cross-lesson integration projects

### For Each Exercise

Each exercise must include the following elements:

1. **🎯 目标** - Clear learning objective
2. **📋 任务描述** - Detailed description of what to do
3. **👣 实施步骤** - Step-by-step instructions using `.steps` class
4. **✅ 验证方法** - How to verify the solution works (in `.note` box)
5. **参考答案** - Hidden by default, use `<details><summary>` pattern


