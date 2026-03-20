# HTML Templates for Course Materials

This file contains all HTML templates used in the course, following the modern design system.

## lessons/index.html (Main Course Index)

The course homepage with modern card-based layout.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[System Name] - Web开发实战课程</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="course-layout">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <h1>📚 [System Name]</h1>
                <p>Web开发实战课程</p>
            </div>
            <nav class="sidebar-nav">
                <div class="nav-section">
                    <div class="nav-section-title">课程</div>
                    <a href="index.html" class="nav-item active">课程首页</a>
                    <a href="../docs/quick-start.html" class="nav-item">快速开始</a>
                    <a href="../docs/syllabus.html" class="nav-item">课程大纲</a>
                    <a href="../docs/homework.html" class="nav-item">课后作业</a>
                </div>
                <div class="nav-section">
                    <div class="nav-section-title">课程内容</div>
                    <a href="lesson-1.html" class="nav-item">第 1 课：[Title]</a>
                    <a href="lesson-2.html" class="nav-item">第 2 课：[Title]</a>
                    <!-- Repeat for each lesson -->
                </div>
            </nav>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <div class="top-nav">
                <div class="breadcrumb">
                    <a href="index.html">课程首页</a>
                </div>
            </div>

            <div class="content">
                <header class="page-header">
                    <h1 class="page-title">📚 [System Name]</h1>
                    <p class="page-subtitle">Web开发实战课程 - 从零构建企业级应用</p>
                </header>

                <!-- Course Introduction -->
                <section class="section">
                    <h2 class="section-title">课程简介</h2>
                    <p>[Course description paragraph]</p>

                    <div class="card">
                        <h3 class="card-title">🎯 学习目标</h3>
                        <div class="card-content">
                            <ul>
                                <li>Learning objective 1</li>
                                <li>Learning objective 2</li>
                                <li>Learning objective 3</li>
                            </ul>
                        </div>
                    </div>
                </section>

                <!-- Technology Stack -->
                <section class="section">
                    <h2 class="section-title">技术栈</h2>
                    <div class="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>技术</th>
                                    <th>版本</th>
                                    <th>说明</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>[Technology 1]</td>
                                    <td>[Version]</td>
                                    <td>[Description]</td>
                                </tr>
                                <!-- Add more technologies -->
                            </tbody>
                        </table>
                    </div>
                </section>

                <!-- Course Outline -->
                <section class="section">
                    <h2 class="section-title">课程大纲</h2>
                    <div class="steps">
                        <div class="step">
                            <div class="step-number">1</div>
                            <div class="step-content">
                                <h3 class="step-title">[Lesson 1 Title]</h3>
                                <p>[Brief description of content]</p>
                                <a href="lesson-1.html">开始学习 →</a>
                            </div>
                        </div>
                        <div class="step">
                            <div class="step-number">2</div>
                            <div class="step-content">
                                <h3 class="step-title">[Lesson 2 Title]</h3>
                                <p>[Brief description of content]</p>
                                <a href="lesson-2.html">开始学习 →</a>
                            </div>
                        </div>
                        <!-- Repeat for each lesson -->
                    </div>
                </section>

                <!-- Architecture Section (Optional) -->
                <section class="section">
                    <h2 class="section-title">项目架构</h2>
                    <p>[Architecture description]</p>

                    <div class="code-block" data-lang="架构图">
<pre>[ASCII architecture diagram or text representation]</pre>
                    </div>
                </section>

                <!-- Core Features (Optional) -->
                <section class="section">
                    <h2 class="section-title">核心功能</h2>

                    <h3 class="section-subtitle">用户功能</h3>
                    <ul>
                        <li>Feature 1</li>
                        <li>Feature 2</li>
                    </ul>

                    <h3 class="section-subtitle">管理员功能</h3>
                    <ul>
                        <li>Admin feature 1</li>
                        <li>Admin feature 2</li>
                    </ul>
                </section>

                <!-- Call to Action -->
                <section class="section">
                    <div class="success">
                        <strong>🚀 准备好了吗？</strong>
                        <p>从 <a href="lesson-1.html">第 1 课</a> 开始你的学习之旅！</p>
                        <p>如果还没有配置开发环境，请先查看 <a href="../docs/quick-start.html">快速开始指南</a>。</p>
                    </div>
                </section>
            </div>
        </main>
    </div>
</body>
</html>
```

## lessons/lesson-N.html (Individual Lesson)

Template for each lesson page with complete structure.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>第 N 课：[Lesson Title] - [System Name]</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="course-layout">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <h1>📚 [System Name]</h1>
                <p>Web开发实战课程</p>
            </div>
            <nav class="sidebar-nav">
                <div class="nav-section">
                    <div class="nav-section-title">课程</div>
                    <a href="index.html" class="nav-item">课程首页</a>
                    <a href="../docs/quick-start.html" class="nav-item">快速开始</a>
                    <a href="../docs/syllabus.html" class="nav-item">课程大纲</a>
                    <a href="../docs/homework.html" class="nav-item">课后作业</a>
                </div>
                <div class="nav-section">
                    <div class="nav-section-title">课程内容</div>
                    <a href="lesson-1.html" class="nav-item">第 1 课：[Title]</a>
                    <a href="lesson-2.html" class="nav-item">第 2 课：[Title]</a>
                    <!-- All lessons, mark current as active -->
                    <a href="lesson-N.html" class="nav-item active">第 N 课：[Current Title]</a>
                </div>
            </nav>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <div class="top-nav">
                <div class="breadcrumb">
                    <a href="index.html">课程首页</a>
                </div>
            </div>

            <div class="content">
                <header class="page-header">
                    <h1 class="page-title">第 N 课：[Lesson Title]</h1>
                    <p class="page-subtitle">[Brief subtitle or description]</p>
                </header>

                <!-- 本课目标 -->
                <section class="section">
                    <h2 class="section-title">📚 本课目标</h2>
                    <!-- 动态生成学习目标列表 -->
                </section>

                <!-- 涉及文件 -->
                <section class="section">
                    <h2 class="section-title">本节课涉及的文件</h2>
                    <!-- 动态生成文件列表和源码链接 -->
                </section>

                <!-- 重要知识点 (2-3个) -->
                <section class="section">
                    <h2 class="section-title">🔥 [知识点名称]</h2>
                    <!-- 知识点讲解：概念、原理、源码、设计原则、执行流程 -->
                </section>

                <!-- 其他知识点 -->
                <section class="section">
                    <h2 class="section-title">📌 [知识点名称]</h2>
                    <!-- 简要讲解 -->
                </section>

                <!-- 检查点 -->
                <section class="section">
                    <div class="checkpoint">
                        <div class="checkpoint-title">检查点</div>
                        <!-- 动态生成检查点列表 -->
                    </div>
                </section>

                <!-- 提示/警告 -->
                <section class="section">
                    <!-- 使用 .note / .warning / .error / .success 等样式类 -->
                </section>

                <!-- 课后思考 -->
                <section class="section">
                    <h2 class="section-title">课后思考</h2>
                    <!-- 动态生成思考题列表 -->
                </section>

                <!-- 课程导航 -->
                <section class="section">
                    <div style="display: flex; justify-content: space-between; gap: 16px;">
                        <a href="lesson-N-1.html">← 上一课</a>
                        <a href="lesson-N+1.html">下一课 →</a>
                    </div>
                </section>
            </div>
        </main>
    </div>
</body>
</html>
```

## docs/quick-start.html

Environment setup and launch guide.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>快速开始 - [System Name]</title>
    <link rel="stylesheet" href="../lessons/css/style.css">
</head>
<body>
    <div class="course-layout">
        <!-- Sidebar (simplified for docs) -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <h1>📚 [System Name]</h1>
                <p>Web开发实战课程</p>
            </div>
            <nav class="sidebar-nav">
                <div class="nav-section">
                    <div class="nav-section-title">文档</div>
                    <a href="../lessons/index.html" class="nav-item">课程首页</a>
                    <a href="quick-start.html" class="nav-item active">快速开始</a>
                    <a href="syllabus.html" class="nav-item">课程大纲</a>
                    <a href="homework.html" class="nav-item">课后作业</a>
                </div>
            </nav>
        </aside>

        <main class="main-content">
            <div class="top-nav">
                <div class="breadcrumb">
                    <a href="../lessons/index.html">课程首页</a> / 快速开始
                </div>
            </div>

            <div class="content">
                <header class="page-header">
                    <h1 class="page-title">快速开始指南</h1>
                    <p class="page-subtitle">环境配置与项目启动</p>
                </header>

                <!-- System Requirements -->
                <section class="section">
                    <h2 class="section-title">系统要求</h2>
                    <ul>
                        <li>操作系统: Windows 10+, macOS 10.14+, Linux</li>
                        <li>内存: 至少 4GB RAM</li>
                        <li>磁盘空间: 至少 1GB 可用空间</li>
                    </ul>
                </section>

                <!-- Prerequisites -->
                <section class="section">
                    <h2 class="section-title">前置要求</h2>

                    <h3 class="section-subtitle">1. [Tool Name]</h3>
                    <p><strong>用途：</strong> What it's used for</p>
                    <p><strong>下载：</strong> <a href="#">Official Download Link</a></p>
                    <p><strong>安装：</strong> Step-by-step instructions</p>
                    <p><strong>验证：</strong> <code>command --version</code></p>
                    <!-- More prerequisites -->
                </section>

                <!-- Project Setup -->
                <section class="section">
                    <h2 class="section-title">项目设置</h2>
                    <div class="steps">
                        <div class="step">
                            <div class="step-number">1</div>
                            <div class="step-content">
                                <h3 class="step-title">克隆/下载项目</h3>
                                <div class="code-block" data-lang="bash">
<pre><code>git clone [repository-url]
cd [project-directory]</code></pre>
                                </div>
                            </div>
                        </div>
                        <div class="step">
                            <div class="step-number">2</div>
                            <div class="step-content">
                                <h3 class="step-title">安装依赖</h3>
                                <div class="code-block" data-lang="bash">
<pre><code>[install-command]</code></pre>
                                </div>
                            </div>
                        </div>
                        <div class="step">
                            <div class="step-number">3</div>
                            <div class="step-content">
                                <h3 class="step-title">配置环境</h3>
                                <p>Edit configuration files as needed...</p>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Running the Application -->
                <section class="section">
                    <h2 class="section-title">运行应用</h2>
                    <div class="code-block" data-lang="bash">
<pre><code>[run-command]</code></pre>
                    </div>
                    <p>访问: <code>http://localhost:PORT</code></p>
                </section>

                <!-- Verification -->
                <section class="section">
                    <h2 class="section-title">验证清单</h2>
                    <ul class="checkpoint-list">
                        <li>Tool X installed (version Y)</li>
                        <li>Project downloaded</li>
                        <li>Dependencies installed</li>
                        <li>Server running on port Z</li>
                        <li>Application accessible</li>
                    </ul>
                </section>

                <!-- Troubleshooting -->
                <section class="section">
                    <h2 class="section-title">常见问题</h2>

                    <div class="error">
                        <strong>问题：</strong> Error message description
                        <br><strong>解决：</strong> Solution steps
                    </div>
                </section>
            </div>
        </main>
    </div>
</body>
</html>
```

## docs/syllabus.html

Course outline with learning objectives.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>课程大纲 - [System Name]</title>
    <link rel="stylesheet" href="../lessons/css/style.css">
</head>
<body>
    <div class="course-layout">
        <aside class="sidebar">
            <div class="sidebar-header">
                <h1>📚 [System Name]</h1>
                <p>Web开发实战课程</p>
            </div>
            <nav class="sidebar-nav">
                <div class="nav-section">
                    <div class="nav-section-title">文档</div>
                    <a href="../lessons/index.html" class="nav-item">课程首页</a>
                    <a href="quick-start.html" class="nav-item">快速开始</a>
                    <a href="syllabus.html" class="nav-item active">课程大纲</a>
                    <a href="homework.html" class="nav-item">课后作业</a>
                </div>
            </nav>
        </aside>

        <main class="main-content">
            <div class="top-nav">
                <div class="breadcrumb">
                    <a href="../lessons/index.html">课程首页</a> / 课程大纲
                </div>
            </div>

            <div class="content">
                <header class="page-header">
                    <h1 class="page-title">课程大纲</h1>
                    <p class="page-subtitle">完整的学习路径规划</p>
                </header>

                <!-- Prerequisites -->
                <section class="section">
                    <h2 class="section-title">前置要求</h2>
                    <div class="card">
                        <div class="card-content">
                            <ul>
                                <li>Prerequisite 1</li>
                                <li>Prerequisite 2</li>
                                <li>Prerequisite 3</li>
                            </ul>
                        </div>
                    </div>
                </section>

                <!-- Course Overview -->
                <section class="section">
                    <h2 class="section-title">课程概述</h2>
                    <p>Brief description of what students will build and learn...</p>
                </section>

                <!-- Lesson Details -->
                <section class="section">
                    <h2 class="section-title">课程安排</h2>
                    <div class="steps">
                        <div class="step">
                            <div class="step-number">1</div>
                            <div class="step-content">
                                <h3 class="step-title">第1课：[Title]</h3>
                                <p><strong>内容：</strong> Brief description...</p>
                                <p><strong>目标：</strong> What students will learn...</p>
                                <a href="../lessons/lesson-1.html">查看详情 →</a>
                            </div>
                        </div>
                        <!-- Repeat for each lesson -->
                    </div>
                </section>

                <!-- Learning Outcomes -->
                <section class="section">
                    <h2 class="section-title">学习成果</h2>
                    <div class="success">
                        After completing this course, students will be able to:
                        <ul class="checkpoint-list">
                            <li>Outcome 1</li>
                            <li>Outcome 2</li>
                            <li>Outcome 3</li>
                        </ul>
                    </div>
                </section>
            </div>
        </main>
    </div>
</body>
</html>
```

## docs/homework.html

Homework and exercises with step-by-step instructions and hidden reference answers.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>课后作业 - [System Name]</title>
    <link rel="stylesheet" href="../lessons/css/style.css">
</head>
<body>
    <div class="course-layout">
        <aside class="sidebar">
            <div class="sidebar-header">
                <h1>📚 [System Name]</h1>
                <p>Web开发实战课程</p>
            </div>
            <nav class="sidebar-nav">
                <div class="nav-section">
                    <div class="nav-section-title">文档</div>
                    <a href="../lessons/index.html" class="nav-item">课程首页</a>
                    <a href="quick-start.html" class="nav-item">快速开始</a>
                    <a href="syllabus.html" class="nav-item">课程大纲</a>
                    <a href="homework.html" class="nav-item active">课后作业</a>
                </div>
            </nav>
        </aside>

        <main class="main-content">
            <div class="top-nav">
                <div class="breadcrumb">
                    <a href="../lessons/index.html">课程首页</a> / 课后作业
                </div>
            </div>

            <div class="content">
                <header class="page-header">
                    <h1 class="page-title">课后作业与练习</h1>
                    <p class="page-subtitle">巩固知识，提升技能</p>
                </header>

                <!-- ========== 第1课作业 ========== -->
                <section class="section">
                    <h2 class="section-title">第1课作业</h2>

                    <!-- 基础练习 -->
                    <h3 class="section-subtitle">📝 基础练习</h3>

                    <div class="card">
                        <h4 class="card-title">练习1: [Practice Title]</h4>
                        <div class="card-content">
                            <p><strong>🎯 目标：</strong>Clear learning objective</p>

                            <p><strong>📋 任务描述：</strong>Practice description...</p>

                            <p><strong>👣 实施步骤：</strong></p>
                            <div class="steps">
                                <div class="step">
                                    <div class="step-number">1</div>
                                    <div class="step-content">
                                        <p>Step 1 instruction with specific command or action</p>
                                    </div>
                                </div>
                                <div class="step">
                                    <div class="step-number">2</div>
                                    <div class="step-content">
                                        <p>Step 2 instruction</p>
                                    </div>
                                </div>
                                <div class="step">
                                    <div class="step-number">3</div>
                                    <div class="step-content">
                                        <p>Step 3 instruction</p>
                                    </div>
                                </div>
                            </div>

                            <p><strong>✅ 验证方法：</strong></p>
                            <div class="note">
                                How to verify the solution works (e.g., "Run the application and access http://localhost:8080 to see the result")
                            </div>

                            <details style="margin-top: 20px;">
                                <summary style="cursor: pointer; color: var(--primary-color); font-weight: 600; padding: 12px; background: var(--bg-light); border-radius: 8px;">
                                    ▼ 查看参考答案
                                </summary>
                                <div style="margin-top: 16px; padding: 16px; background: var(--bg-light); border-radius: 8px; border-left: 4px solid var(--success-color);">
                                    <p><strong>参考答案：</strong></p>
                                    <div class="code-block" data-lang="[Language]">
<pre><code>// Reference solution code
// Or step-by-step explanation</code></pre>
                                    </div>
                                </div>
                            </details>
                        </div>
                    </div>

                    <!-- 进阶练习 -->
                    <h3 class="section-subtitle">🚀 进阶练习</h3>

                    <div class="card">
                        <h4 class="card-title">挑战题: [Challenge Title]</h4>
                        <div class="card-content">
                            <p><strong>🎯 目标：</strong>Advanced learning objective</p>

                            <p><strong>📋 任务描述：</strong>Challenge description requiring deeper understanding...</p>

                            <p><strong>👣 实施步骤：</strong></p>
                            <div class="steps">
                                <div class="step">
                                    <div class="step-number">1</div>
                                    <div class="step-content">
                                        <p>Step 1 instruction</p>
                                    </div>
                                </div>
                                <!-- More steps -->
                            </div>

                            <p><strong>✅ 验证方法：</strong></p>
                            <div class="note">
                                Verification instructions with expected output
                            </div>

                            <details style="margin-top: 20px;">
                                <summary style="cursor: pointer; color: var(--primary-color); font-weight: 600; padding: 12px; background: var(--bg-light); border-radius: 8px;">
                                    ▼ 查看参考答案
                                </summary>
                                <div style="margin-top: 16px; padding: 16px; background: var(--bg-light); border-radius: 8px; border-left: 4px solid var(--warning-color);">
                                    <p><strong>参考答案：</strong></p>
                                    <div class="code-block" data-lang="[Language]">
<pre><code>// Advanced solution code
// Or detailed explanation</code></pre>
                                    </div>
                                    <p style="margin-top: 12px;"><strong>💡 提示：</strong>Additional hints or alternative approaches</p>
                                </div>
                            </details>
                        </div>
                    </div>
                </section>

                <!-- ========== 第2课作业 ========== -->
                <section class="section">
                    <h2 class="section-title">第2课作业</h2>
                    <!-- Repeat pattern for each lesson -->
                </section>

                <!-- ========== 综合练习 ========== -->
                <section class="section">
                    <h2 class="section-title">综合练习</h2>

                    <div class="card" style="border: 2px solid var(--primary-color);">
                        <h3 class="card-title">🎯 综合项目: [Integration Challenge]</h3>
                        <div class="card-content">
                            <p><strong>🎯 目标：</strong>Integrate concepts from multiple lessons to build a complete feature</p>

                            <p><strong>📋 项目描述：</strong>Description of the comprehensive project...</p>

                            <p><strong>👣 实施步骤：</strong></p>
                            <div class="steps">
                                <div class="step">
                                    <div class="step-number">1</div>
                                    <div class="step-content">
                                        <h4 class="step-title">Phase 1: [Phase Name]</h4>
                                        <p>Detailed instruction for this phase</p>
                                        <div class="code-block" data-lang="[Language]">
<pre><code>// Example code for this phase</code></pre>
                                        </div>
                                    </div>
                                </div>
                                <!-- More phases/steps -->
                            </div>

                            <p><strong>✅ 验收标准：</strong></p>
                            <ul class="checkpoint-list">
                                <li>Acceptance criterion 1</li>
                                <li>Acceptance criterion 2</li>
                                <li>Acceptance criterion 3</li>
                            </ul>

                            <details style="margin-top: 20px;">
                                <summary style="cursor: pointer; color: var(--primary-color); font-weight: 600; padding: 12px; background: var(--bg-light); border-radius: 8px;">
                                    ▼ 查看完整参考答案
                                </summary>
                                <div style="margin-top: 16px; padding: 16px; background: var(--bg-light); border-radius: 8px;">
                                    <p><strong>完整实现方案：</strong></p>
                                    <div class="code-block" data-lang="[Language]">
<pre><code>// Complete solution code</code></pre>
                                    </div>
                                    <p style="margin-top: 12px;"><strong>🔍 关键点解析：</strong></p>
                                    <ul>
                                        <li>Key insight 1</li>
                                        <li>Key insight 2</li>
                                    </ul>
                                </div>
                            </details>
                        </div>
                    </div>
                </section>

                <!-- ========== 练习类型说明 ========== -->
                <section class="section">
                    <h2 class="section-title">练习类型说明</h2>

                    <div class="note">
                        <strong>📝 基础练习：</strong>巩固本节课学到的核心概念和技能，难度适中，所有学生都应该能完成。
                    </div>

                    <div class="warning">
                        <strong>🚀 进阶练习：</strong>需要更深入的理解和综合运用多个知识点，适合学有余力的学生挑战。
                    </div>

                    <div class="card">
                        <h4 class="card-title">练习类型说明</h4>
                        <div class="card-content">
                            <table style="width: 100%;">
                                <thead>
                                    <tr>
                                        <th>类型</th>
                                        <th>说明</th>
                                        <th>难度</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>概念理解题</td>
                                        <td>测试对原理的理解</td>
                                        <td>⭐</td>
                                    </tr>
                                    <tr>
                                        <td>代码阅读题</td>
                                        <td>分析代码功能</td>
                                        <td>⭐⭐</td>
                                    </tr>
                                    <tr>
                                        <td>调试练习</td>
                                        <td>找出并修复错误</td>
                                        <td>⭐⭐</td>
                                    </tr>
                                    <tr>
                                        <td>实现练习</td>
                                        <td>编写新功能</td>
                                        <td>⭐⭐⭐</td>
                                    </tr>
                                    <tr>
                                        <td>扩展练习</td>
                                        <td>在现有基础上添加新特性</td>
                                        <td>⭐⭐⭐⭐</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </section>

                <!-- ========== 提交与反馈 ========== -->
                <section class="section">
                    <h2 class="section-title">提交与反馈</h2>

                    <div class="success">
                        <strong>📌 作业提交建议：</strong>
                        <ul style="margin-top: 12px;">
                            <li>完成基础练习是最低要求</li>
                            <li>尝试进阶练习可以获得更深入的理解</li>
                            <li>综合练习建议在完成所有相关课程后进行</li>
                            <li>遇到困难时可以先查看提示，再参考答案</li>
                        </ul>
                    </div>
                </section>
            </div>
        </main>
    </div>
</body>
</html>
```

## Homework Template Guidelines

### Structure for Each Exercise

1. **标题** - 清晰描述练习内容
2. **目标** - 明确学习目标
3. **任务描述** - 详细说明要做什么
4. **实施步骤** - 分步骤指导
5. **验证方法** - 如何检查结果
6. **参考答案** - 默认隐藏，点击展开

### Exercise Levels

| 级别 | 类型 | 目标受众 | 标识 |
|------|------|----------|------|
| 基础 | 巩固核心概念 | 所有学生 | 📝 |
| 进阶 | 深入理解和综合 | 学有余力 | 🚀 |
| 综合 | 跨课程整合 | 完成相关课程后 | 🎯 |

### Steps Format

```html
<div class="steps">
    <div class="step">
        <div class="step-number">1</div>
        <div class="step-content">
            <p>Step instruction</p>
        </div>
    </div>
</div>
```

### Collapsible Answer Pattern

```html
<details>
    <summary style="cursor: pointer; color: var(--primary-color); font-weight: 600; padding: 12px; background: var(--bg-light); border-radius: 8px;">
        ▼ 查看参考答案
    </summary>
    <div style="margin-top: 16px; padding: 16px; background: var(--bg-light); border-radius: 8px;">
        <!-- Answer content -->
    </div>
</details>
```

### Verification Pattern

```html
<div class="note">
    <strong>✅ 验证方法：</strong>
    How to verify the solution works
</div>
```

## Component Quick Reference

| Component | Class | Description |
|-----------|-------|-------------|
| Layout | `.course-layout` | Main flex container |
| Sidebar | `.sidebar` | Fixed navigation sidebar |
| Nav Section | `.nav-section` | Sidebar navigation group |
| Nav Item | `.nav-item` | Navigation link |
| Top Nav | `.top-nav` | Sticky navigation bar |
| Breadcrumb | `.breadcrumb` | Breadcrumb navigation |
| Page Header | `.page-header` | Page title section |
| Section | `.section` | Content section |
| Card | `.card` | Content card with shadow |
| Code Block | `.code-block` | Code with syntax highlighting |
| Note Box | `.note` | Blue info box |
| Warning Box | `.warning` | Yellow warning box |
| Error Box | `.error` | Red error box |
| Success Box | `.success` | Green success box |
| Checkpoint | `.checkpoint` | Learning checkpoint |
| Step | `.step` | Process step |
| File Path | `.file-path` | File path display |
| Source Link | `.source-link` | Source code link |
| Tech Tag | `.tech-tag` | Technology badge |

## HTML Structure Best Practices

1. **Semantic HTML**: Use proper semantic elements (`<aside>`, `<main>`, `<section>`, `<header>`)
2. **Breadcrumb**: Always include breadcrumb navigation for easy navigation
3. **Active State**: Mark current page in sidebar with `class="nav-item active"`
4. **Source Links**: Always link to source code using relative paths `../src/...`
5. **Code Language**: Always set `data-lang` attribute on code blocks
6. **Responsive**: All templates are responsive by default
