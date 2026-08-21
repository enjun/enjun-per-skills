---
name: scientific-thinking
description: Scientific thinking skills with two modes — brainstorming and critical thinking. Brainstorm mode generates novel research ideas, explores cross-disciplinary connections, challenges assumptions, and identifies research gaps with systematic problem depth assessment including SOTA analysis and literature evaluation (use whenever the user mentions 头脑风暴, 构思, 研究想法, 创新, 探索方向, 评估问题深度, SOTA现状分析, 避免重复研究, 研究价值评估, or needs help coming up with research directions). Critical-thinking mode evaluates scientific claims, evidence quality, experimental design, biases, statistical validity, and logical fallacies using established frameworks (GRADE, Cochrane risk of bias); use for "evaluate this methodology", "check the evidence", "批判分析", "帮我看看这篇论文的方法学有没有问题", "分析SOTA现状", "评估研究空白". For formal review writing use scientific-review; for writing papers use scientific-writing.
allowed-tools: [Read, Write, Edit, Bash]
license: MIT license
---

# Scientific Thinking

Two complementary thinking modes for the research process: **brainstorming** to generate ideas in the early research phase, and **critical thinking** to rigorously evaluate claims and evidence. Pick the mode that matches what the user needs right now.

## Why one skill covers both modes

Brainstorming and critical thinking are the two ends of the same creative-critical loop: you generate possibilities, then you evaluate them. They share the same scientific mindset — questioning assumptions, considering alternatives, and staying open to evidence — and both serve research at different stages. Keeping them together means the user can move from ideation into evaluation without switching skills.

## Mode Selection

Infer from the request, or ask with `AskUserQuestion` if ambiguous:

| Mode | When the user needs | Framework |
|------|--------------------|-----------|
| **Brainstorm** | Generate novel ideas, explore directions, challenge assumptions, find research gaps — early-stage research planning | [brainstorming.md](references/brainstorming.md) |
| **Critical thinking** | Evaluate a paper's methodology, evidence quality, biases, or statistical validity; check claims before trusting them | [critical-thinking.md](references/critical-thinking.md) |

---

## Brainstorm Mode

Read **→ [brainstorming.md](references/brainstorming.md)** and follow its five-stage conversational workflow.

**Essence of the mode:**
- Be a **collaborative thinking partner**, not a lecturer — the researcher should do at least half the talking
- Explore with "yes, and…" — build on ideas before critiquing them
- Ask provocative questions ("what if the opposite were true?", "what would the most radical approach look like?")
- Draw on cross-disciplinary analogies and emerging technologies
- End by synthesizing: most promising directions, feasibility notes, and concrete next steps

**Structured methods** (SCAMPER, Six Thinking Hats, morphological analysis, TRIZ, analogies) are in [brainstorming-methods.md](references/brainstorming-methods.md) — load them when the conversation stalls or the researcher asks for a specific technique. Output structured results as `brainstorming-results/session-YYYY-MM-DD.md`, `ideas-collected.md`, `next-steps.md` when saving is useful.

**Guidance:**
- Let ideas flow before evaluating (quantity over quality in the divergent phase)
- Don't announce which method you're using unless asked — apply it naturally
- Give people space to think; comfortable silence is productive

**Problem Depth Assessment:**
When refining research questions, avoid overly broad or superficial problems. Each question must address:

1. **Why research this** - Scientific value and practical significance
2. **Current research progress** - SOTA (State of the Art) status and precise positioning
3. **Is the problem solved** - Avoid redundant research

Standard evaluation process:
- Deep literature search (semantic retrieval + title search + key abstracts)
- Web search for important literature outside knowledge base (especially latest reviews and competing work)
- Issue a ruling for each question: valid / valid after narrowing / should be dropped as solved
- Clearly state "whose shoulders you're standing on" — cite key foundational work
- When important literature is found but full text unavailable, list title and source for user to download

**Why:** The value of grant applications/topic selection depends on precise distance from SOTA. If existing research has basically solved a problem, further research is wasted effort; you must stand on giants' shoulders.

---

## Critical Thinking Mode

Read **→ [critical-thinking.md](references/critical-thinking.md)** and follow its systematic evaluation framework.

**Essence of the mode:**
- Evaluate methodology (design validity, controls, measurement) and statistics (power, assumptions, multiple comparisons, effect sizes)
- Detect bias systematically — cognitive, selection, measurement, analysis, confounding
- Grade evidence quality (study design hierarchy, GRADE, convergence of evidence)
- Identify logical fallacies by name, and explain what evidence would be needed instead
- Always separate **data** (what was observed) from **interpretation** (what it means), and correlate findings with causality

**Evaluation should be:**
- **Constructive** — name strengths as well as weaknesses; distinguish fatal flaws from minor limitations
- **Specific** — point to concrete instances ("In the Methods section…") and quote problematic statements
- **Proportionate** — match criticism severity to the issue's impact on the main conclusions
- **Consistent** — apply the same criteria across studies; judge methodology, not results

**Reference depth** (load on demand):
| Reference | Content |
|-----------|---------|
| [scientific-method.md](references/scientific-method.md) | Core scientific methodology principles, causal inference, open science |
| [common-biases.md](references/common-biases.md) | Bias taxonomy with detection and mitigation strategies |
| [statistical-pitfalls.md](references/statistical-pitfalls.md) | Common statistical errors and correct practices |
| [evidence-hierarchy.md](references/evidence-hierarchy.md) | Evidence hierarchy, GRADE system, quality assessment |
| [logical-fallacies.md](references/logical-fallacies.md) | Fallacy catalog with examples and detection |
| [experimental-design.md](references/experimental-design.md) | Comprehensive design checklist (question → dissemination) |

Use `grep` to search these references for specific topics rather than reading them wholesale.

---

## Moving Between Modes

The two modes compose naturally:
- After brainstorming yields promising directions, switch to critical thinking to pressure-test the top candidates ("实际测试这个需要什么？最大障碍是什么？")
- When critical analysis of an existing paper finds weaknesses, switch to the `scientific-writing` skill's improvement workflow to fix them
- Formal peer review or scoring → use the `scientific-review` skill instead

---

## Bundled Resources

### references/
| File | When to read |
|------|--------------|
| [brainstorming.md](references/brainstorming.md) | Brainstorm mode — conversational workflow |
| [brainstorming-methods.md](references/brainstorming-methods.md) | Brainstorm — structured techniques (SCAMPER, Six Hats, etc.) |
| [critical-thinking.md](references/critical-thinking.md) | Critical-thinking mode — systematic evaluation framework |
| [scientific-method.md](references/scientific-method.md) | Critical thinking — methodology principles |
| [common-biases.md](references/common-biases.md) | Critical thinking — bias detection |
| [statistical-pitfalls.md](references/statistical-pitfalls.md) | Critical thinking — statistics review |
| [evidence-hierarchy.md](references/evidence-hierarchy.md) | Critical thinking — evidence grading |
| [logical-fallacies.md](references/logical-fallacies.md) | Critical thinking — fallacy identification |
| [experimental-design.md](references/experimental-design.md) | Critical thinking — design guidance |
