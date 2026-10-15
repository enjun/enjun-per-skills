---
name: scientific-thinking
description: Scientific thinking skills with three modes. Problem-refinement (the most important mode) distills vague interests or candidate directions into precise, testable scientific questions through iterative co-thinking with the user, enforcing 创新性/科学性 and SOTA-distance assessment; use for 凝练科学问题, 提出科学问题, 选题, 国自然/NSFC选题. Brainstorm mode generates novel research ideas, cross-disciplinary connections, and research gaps; use for 头脑风暴, 构思, 研究想法, 探索方向, 分析SOTA现状. Critical-thinking mode evaluates methodology, evidence quality, simulation design, baseline fairness, biases, and statistics, with dedicated wireless/engineering-simulation checklists; use for 批判分析, 论文方法学有没有问题, 评估研究空白, 评估基线公平性. For formal review use scientific-review; for writing papers use scientific-writing.
allowed-tools: [Read, Write, Edit, Bash]
license: MIT license
---

# 科研思维（Scientific Thinking）

科研过程环环相扣的三种思维模式：**头脑风暴**在研究早期发散生成方向，**科学问题凝练**把方向收敛为精确的科学问题，**批判性思维**严格评估论断与证据。按用户当前需要选择模式。

## 为什么一个技能覆盖三种模式

三种模式是同一条研究主干线的三个环节：先**生成**可能性（头脑风暴），再**收敛**为合格的科学问题（凝练），再**评估**问题与证据的质量（批判性思维）。三者共享同一种科学心态——质疑假设、考虑替代方案、对证据保持开放。合在一起，用户可以从灵感走到定稿的问题表述，无需切换技能。

**三种模式中，科学问题凝练是重中之重，也是最具挑战性的环节**——它要求与用户反复讨论、一起思考，而不只是工具性的生成或评估。

## 模式选择

从请求推断；模糊时用 `AskUserQuestion` 询问：

| 模式 | 适用需求 | 框架文件 |
|------|---------|---------|
| **科学问题凝练** | 把兴趣/观察/候选方向收敛为精确、可证伪、有新知识增量的科学问题；申请书选题与立项的核心环节 | [problem-refinement.md](references/problem-refinement.md) |
| **头脑风暴** | 生成新想法、探索方向、挑战假设、寻找研究空白——研究早期规划 | [brainstorming.md](references/brainstorming.md) |
| **批判性思维** | 评估论文方法学、证据质量、偏倚、统计有效性；在采信一个论断前先检验它 | [critical-thinking.md](references/critical-thinking.md) |

---

## 头脑风暴模式

阅读 **→ [brainstorming.md](references/brainstorming.md)** 并遵循其五阶段对话工作流。

**模式要点：**
- 做**协作式思维伙伴**，不是讲课者——每轮回应精炼，用具体问题收尾，把话筒交回研究人员
- 用"是的，而且……"探索——先构建，再批评
- 提挑衅性问题（"如果相反成立会怎样？""最激进的方法长什么样？"）
- 调用跨领域类比与新兴技术
- 以综合收尾：最有前景的方向、可行性备注、具体下一步

**结构化方法**（SCAMPER、六顶思考帽、形态分析、TRIZ、类比法）在 [brainstorming-methods.md](references/brainstorming-methods.md)——当对话停滞或研究人员点名要某项技术时加载。需要保存时输出 `brainstorming-results/session-YYYY-MM-DD.md`、`ideas-collected.md`、`next-steps.md`。

**指引：**
- 发散阶段先让想法流动再评估（数量优先于质量）
- 除非被问起，不宣布正在使用哪种方法——自然应用
- 一次只抛 2-3 个想法并等待反应，不要一次性倾倒完整的想法清单
- 头脑风暴只负责发散出**方向**；把方向收敛为合格科学问题时，切换到科学问题凝练模式

---

## 科学问题凝练模式（重中之重）

阅读 **→ [problem-refinement.md](references/problem-refinement.md)** 并遵循其迭代式凝练工作流。

**模式要点：**
- **必须和用户反复讨论、一起思考**——问题属于研究人员；每轮给 2-3 个候选 + 待决分叉点，等回应后再继续
- **不可以简单复制、罗列已有文献中的问题**——文献用于定位空白与"站在谁的肩膀上"，问题必须从用户自己的观察与切入点中长出来
- 每个候选问题过**两性检验**：
  - **创新性**——解答应推动新知识产生；新特性及其影响的分析要具体、清晰；创新点体现在标题和关键词等重要位置（评审专家关注的重点）
  - **科学性**——答案应可被证明或证伪，避免模糊和夸大其词；采用自然科学公认的研究方法；允许失败，重在过程
- **问题深度评估**：每个问题必须回答"为什么研究 / 已有研究进展（SOTA 精确距离）/ 是否已解决"，给出裁决——**成立 / 收窄后成立 / 已被解决应砍掉**，并明确站在谁的肩膀上
- 以"科学问题凝练卡"收尾：主问题 + 子问题分解 + 两性论证 + 基础工作清单 + 标题关键词建议

**为什么：** 申请书的价值取决于科学问题的两性成色与和 SOTA 的精确距离。已有研究基本解决的问题再研究就是白费工夫；从文献抄来的问题没有自己的视角，创新性存疑。

---

## 批判性思维模式

阅读 **→ [critical-thinking.md](references/critical-thinking.md)** 并遵循其系统评估框架。

**模式要点：**
- 评估方法学（设计效度、基线与消融、测量）与统计（重复次数、假设检验、多重比较、效应量）
- 系统检测偏倚——认知、选择、测量、分析、混杂
- 分级证据质量（工程实证等级、证据收敛性）
- 点名识别逻辑谬误，并说明需要什么证据才能成立
- 始终区分**数据**（观察到了什么）与**解读**（意味着什么），区分相关与因果

**评估应当：**
- **建设性**——先讲优点再讲问题；区分致命缺陷与次要局限
- **具体**——指向具体位置（"在方法部分……"）并引用问题语句
- **成比例**——批评严重度与该问题对主要结论的影响相匹配
- **一致**——跨研究用同一标准；评判方法学，而非结果

**参考深度**（按需加载）：
| 参考 | 内容 |
|------|------|
| [wireless-eval.md](references/wireless-eval.md) | 无线通信/工程仿真研究专属评估：基线公平性、仿真严谨性、信道模型、ML 方法陷阱、指标规范 |
| [scientific-method.md](references/scientific-method.md) | 科学方法核心原则、工程语境因果论证、开放科学 |
| [common-biases.md](references/common-biases.md) | 偏倚分类与检测/缓解策略 |
| [statistical-pitfalls.md](references/statistical-pitfalls.md) | 常见统计错误与正确做法 |
| [evidence-hierarchy.md](references/evidence-hierarchy.md) | 工程实证证据等级、单项研究质量判据 |
| [logical-fallacies.md](references/logical-fallacies.md) | 谬误目录与识别 |
| [experimental-design.md](references/experimental-design.md) | 仿真与原型实验设计检查单（问题→发表） |

需要特定主题时用 `grep` 在这些参考中检索，不要整读。

---

## 模式间切换

三种模式构成研究主干线，自然衔接：
- 头脑风暴产出有前景的方向 → **科学问题凝练**收敛为精确问题 → **批判性思维**对问题做压力测试（"评审会问什么？证伪路径是什么？"）
- 凝练卡定稿后 → `scientific-writing` 技能写入申请书/论文
- 批判性分析发现已有论文的弱点后 → 切换到 `scientific-writing` 的改进工作流去修复
- 正式同行评审或打分 → 改用 `scientific-review` 技能

---

## 技能资源

### references/
| 文件 | 何时阅读 |
|------|---------|
| [problem-refinement.md](references/problem-refinement.md) | 科学问题凝练模式——迭代式凝练工作流与两性检验 |
| [brainstorming.md](references/brainstorming.md) | 头脑风暴模式——对话工作流 |
| [brainstorming-methods.md](references/brainstorming-methods.md) | 头脑风暴——结构化技术（SCAMPER、六顶思考帽等） |
| [critical-thinking.md](references/critical-thinking.md) | 批判性思维模式——系统评估框架 |
| [wireless-eval.md](references/wireless-eval.md) | 批判性思维——无线通信/工程仿真专属评估清单 |
| [scientific-method.md](references/scientific-method.md) | 批判性思维——方法论原则 |
| [common-biases.md](references/common-biases.md) | 批判性思维——偏倚检测 |
| [statistical-pitfalls.md](references/statistical-pitfalls.md) | 批判性思维——统计陷阱 |
| [evidence-hierarchy.md](references/evidence-hierarchy.md) | 批判性思维——证据分级 |
| [logical-fallacies.md](references/logical-fallacies.md) | 批判性思维——谬误识别 |
| [experimental-design.md](references/experimental-design.md) | 批判性思维——设计指导 |
