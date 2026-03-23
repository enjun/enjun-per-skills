# Agent Prompts Reference

本文档包含各阶段 Agent 的详细 prompt 模板。主 SKILL.md 中的 Agent 调用应引用此文件。

---

## Stage 2: Proposer Agent

此 Agent 单独执行，通过**内部头脑风暴**提出创新解决方案。**不运行实验**，专注于方案设计。

**→ 详细的头脑风暴方法见 `references/proposer_brainstorming.md`**

### Prompt 模板

```python
Agent(
    subagent_type="general-purpose",
    prompt="""
You are proposing a solution to a wireless communications research problem through internal brainstorming.

PROBLEM: {research_problem}
CONTEXT: {research_context}
LITERATURE FOUNDATION: {from Stage 1}

Your task: Use internal brainstorming to generate an innovative solution, then propose it comprehensively.

## Brainstorming Process (Internal)

Follow this four-phase brainstorming process:

### Phase 1: Divergent Exploration (Generate Ideas)

Use these core techniques to generate 5-10 diverse ideas:

| Technique | Description | Apply to Problem |
|-----------|-------------|------------------|
| **Cross-domain analogy** | Find similarities in other fields | "How would [other field] solve this?" |
| **Assumption reversal** | Flip core assumptions | "What if the opposite is true?" |
| **Scale transformation** | Change problem scale | "What changes at chip/network/global scale?" |
| **Constraint manipulation** | Add/remove constraints | "What if we could measure anything?" |
| **Technology speculation** | Apply emerging technologies | "What becomes possible with RIS/THz/AI?" |

Ask yourself for each technique:
- How does this apply to the current problem?
- What new possibilities emerge?
- What's the most radical variant?

### Phase 2: Pattern Recognition (Find Connections)

From your generated ideas:
- Find common threads and themes
- Identify complementary ideas that can combine
- Discover unexpected connections
- Map relationships between ideas

**Output**: 2-3 promising directions, each integrating multiple idea seeds.

### Phase 3: Critical Evaluation (Constructive Screening)

For each promising direction, assess:
- **Novelty**: How is this different from existing methods?
- **Feasibility**: Is it technically viable? What resources are needed?
- **Impact**: If successful, what improvement does it bring?
- **Risk**: What are the potential failure points?

**Output**: Select 1 most promising direction for development.

### Phase 4: Solution Synthesis (Concretization)

Transform the selected direction into a specific solution with:
- Problem definition
- Methodology design
- Implementation considerations
- Literature positioning

## Proposal Output

After brainstorming, provide a comprehensive proposal:

1. Problem Analysis
   - Core technical challenge
   - Key constraints and assumptions
   - Performance requirements

2. Proposed Solution
   - Technical methodology
   - Key innovations
   - Expected advantages
   - Theoretical foundation

3. Implementation Considerations
   - Required resources
   - Potential challenges
   - Validation approach (what should be tested)

4. Literature Positioning
   - How your solution relates to existing work
   - Gaps it addresses
   - Novel contributions

5. Brainstorming Trace (IMPORTANT)
   - Ideas generated: [list 5-10 ideas]
   - Patterns identified: [key themes]
   - Promising directions: [2-3 directions with rationale]
   - Selected direction: [your choice]
   - Rationale: [why this direction]

DO NOT run experiments at this stage. Focus on solution design and theoretical justification.

Output format:
{
  "problem_analysis": {
    "core_challenge": "...",
    "constraints": [...],
    "assumptions": [...],
    "requirements": [...]
  },
  "proposed_solution": {
    "methodology": "...",
    "innovations": [...],
    "advantages": [...],
    "theoretical_basis": "..."
  },
  "implementation": {
    "resources_required": [...],
    "potential_challenges": [...],
    "validation_approach": "..."
  },
  "literature_positioning": {
    "related_work": ["cite 2-3 key papers"],
    "gaps_addressed": [...],
    "novel_contributions": [...]
  },
  "brainstorming_trace": {
    "ideas_generated": ["idea1", "idea2", ...],
    "patterns_identified": ["pattern1", "pattern2"],
    "promising_directions": [
      {
        "direction": "...",
        "novelty": "...",
        "feasibility": "..."
      }
    ],
    "selected_direction": "...",
    "rationale": "why this direction was chosen"
  }
}
""",
    description="Propose solution through brainstorming",
    run_in_background=false
)
```

### 输出处理

保存到 `docs/proposal.json`：
- `problem_analysis`: 问题分析
- `proposed_solution`: 提出的解决方案
- `implementation`: 实现考虑
- `literature_positioning`: 文献定位

---

## Stage 3: Supporter Agent

此 Agent 并行执行，提供支持证据并运行实验验证方案。

### Prompt 模板

```python
Agent(
    subagent_type="general-purpose",
    prompt="""
You are supporting a proposed research solution with evidence and experiments.

PROBLEM: {research_problem}
PROPOSED SOLUTION: {from Stage 2}
LITERATURE FOUNDATION: {from Stage 1}

Your task: Provide rigorous support for the proposal through literature and experiments.

1. Literature Support
   - Search Zotero for papers that support the approach
   - Cite specific results or methods that validate the proposal
   - Identify prior work that demonstrates feasibility
   - Find theoretical foundations

2. Quantitative Arguments
   - Mathematical analysis showing why the solution should work
   - Performance predictions with specific numbers
   - Complexity analysis
   - Theoretical bounds

3. EXPERIMENTAL VALIDATION (IMPORTANT)
   - Design and execute Python experiments to validate key claims
   - Focus on 1-2 critical assumptions or performance predictions
   - Generate publication-quality figures
   - Interpret results to support the proposal

When to run experiments:
- When making quantitative performance claims (e.g., "30% improvement")
- When validating theoretical assumptions
- When comparing with baseline methods
- When demonstrating feasibility of key components

EXPERIMENT GUIDELINES:
- Keep experiments focused and fast (< 3 minutes each)
- Use reproducible parameters (set random seeds)
- Generate clear, labeled visualizations
- Save code to scripts/ and figures to docs/figures/

4. Practical Evidence
   - Existing implementations or demonstrations
   - Industry adoption evidence
   - Real-world applicability

Output format:
{
  "literature_support": [
    {"paper": "citation", "supporting_point": "...", "relevance": "..."}
  ],
  "quantitative_analysis": {
    "performance_predictions": [...],
    "complexity_analysis": "...",
    "theoretical_bounds": [...]
  },
  "experimental_evidence": {
    "experiments_run": ["list of experiments"],
    "results": "summary of findings",
    "figures": ["paths to generated figures"],
    "conclusion": "how results strongly support the proposal"
  },
  "practical_evidence": {
    "existing_work": "...",
    "feasibility_assessment": "..."
  }
}
""",
    description="Support proposal with experiments",
    run_in_background=false
)
```

### 输出处理

保存到 `docs/support.json`：
- `literature_support`: 文献支持
- `quantitative_analysis`: 定量分析
- `experimental_evidence`: 实验证据
- `practical_evidence`: 实践证据

---

## Stage 3: Critic Agent

此 Agent 与 Supporter 并行执行，提供批判性证据并运行实验挑战方案。

### Prompt 模板

```python
Agent(
    subagent_type="general-purpose",
    prompt="""
You are critically evaluating a proposed research solution with evidence and experiments.

PROBLEM: {research_problem}
PROPOSED SOLUTION: {from Stage 2}
LITERATURE FOUNDATION: {from Stage 1}

Your task: Provide rigorous critique through literature analysis and experiments.

1. Theoretical Concerns
   - Limitations of the theoretical foundation
   - Assumptions that may not hold in practice
   - Theoretical bounds that constrain applicability
   - Missing considerations

2. Literature Counter-evidence
   - Search Zotero for papers showing limitations of similar approaches
   - Find failed attempts or known issues
   - Identify alternative state-of-the-art methods
   - Highlight unaddressed research gaps

3. Practical Challenges
   - Implementation difficulties
   - Resource requirements (computational, energy, etc.)
   - Scalability concerns
   - Real-world constraints

4. EXPERIMENTAL CHALLENGE (IMPORTANT)
   - Design experiments to test the proposal's weak points
   - Focus on edge cases, stress conditions, or failure modes
   - Compare with alternative approaches
   - Run experiments that could reveal flaws

When to run challenging experiments:
- When theoretical assumptions seem optimistic
- When performance claims seem unsubstantiated
- When edge cases are not addressed
- When comparing with baselines is necessary

EXPERIMENT GUIDELINES:
- Target specific weaknesses or assumptions
- Use realistic or adversarial parameters
- Generate comparative visualizations
- Save code to scripts/ and figures to docs/figures/

5. Issues by Impact
   - High impact: Critical flaws that must be addressed
   - Medium impact: Significant concerns that should be addressed
   - Low impact: Minor issues that could be addressed

Output format:
{
  "theoretical_concerns": [
    {"concern": "...", "impact": "high|medium|low", "explanation": "..."}
  ],
  "literature_counter_evidence": [
    {"paper": "citation", "counter_point": "...", "relevance": "..."}
  ],
  "practical_challenges": [
    {"challenge": "...", "impact": "high|medium|low", "mitigation": "..."}
  ],
  "experimental_challenges": {
    "experiments_run": ["list of challenging experiments"],
    "results": "summary of findings",
    "figures": ["paths to generated figures"],
    "conclusion": "how results challenge the proposal"
  },
  "issues_summary": {
    "high": [...],
    "medium": [...],
    "low": [...]
  }
}
""",
    description="Critique proposal with experiments",
    run_in_background=false
)
```

### 输出处理

保存到 `docs/critique.json`：
- `theoretical_concerns`: 理论关注点
- `literature_counter_evidence`: 文献反证
- `practical_challenges`: 实践挑战
- `experimental_challenges`: 实验挑战
- `issues_summary`: 问题摘要（按影响程度）

---

## Stage 4: Evaluator Agent

此 Agent 综合所有信息，做出决策并提供清晰理由。

### Prompt 模板

```python
Agent(
    subagent_type="general-purpose",
    prompt="""
You are evaluating a research proposal and its supporting/critical evidence.

PROBLEM: {research_problem}
PROPOSAL: {from Stage 2}
SUPPORTING EVIDENCE: {from Stage 3 Supporter}
CRITICAL EVIDENCE: {from Stage 3 Critic}

Your task: Weigh all evidence and make an informed decision with clear rationale.

ANALYSIS FRAMEWORK:

1. Evidence Balance
   - Supporting evidence: literature + quantitative + experimental
   - Challenging evidence: literature + theoretical + experimental
   - Which side has stronger and more credible evidence?

2. Experimental Validity
   - Do Supporter's experiments properly validate the claims?
   - Do Critic's experiments reveal genuine weaknesses?
   - Are experimental methodologies sound on both sides?

3. Issue Assessment
   - High-impact issues from Critic: [list]
   - Are these addressable with revisions?
   - Do critical flaws outweigh the proposal's merits?

4. Literature Positioning
   - Does the proposal address genuine gaps?
   - Is it sufficiently novel compared to existing work?
   - Does it advance the state-of-the-art?

DECISION CRITERIA:

→ ACCEPT if:
- Supporting evidence significantly outweighs challenging evidence
- No high-impact issues, OR high-impact issues are minor/addressable
- Experimental evidence (if any) supports key claims
- The proposal makes a genuine contribution

→ REVISE if:
- Evidence is mixed but promising
- High-impact issues exist but are addressable with modifications
- Experimental validation is insufficient but can be improved
- The core idea is sound but needs refinement

→ REJECT if:
- Challenging evidence significantly outweighs support
- Fatal theoretical flaws identified
- Experimental evidence contradicts key claims
- The proposal does not advance the state-of-the-art

DECISION OUTPUT:

Provide:
1. Your decision (ACCEPT / REVISE / REJECT)
2. Evidence summary (supporting vs challenging)
3. Rationale - Clear, detailed explanation of your reasoning
4. Issue assessment (by impact level)
5. Revision guidance (if REVISE)

Output format:
{
  "decision": "ACCEPT|REVISE|REJECT",
  "evidence_summary": {
    "supporting_strength": "strong|moderate|weak",
    "challenging_strength": "strong|moderate|weak",
    "balance": "supporting_outweighs|mixed|challenging_outweighs"
  },
  "rationale": {
    "key_reasons": [...],
    "evidence_analysis": "...",
    "experimental_assessment": "...",
    "literature_assessment": "..."
  },
  "issues": {
    "high": [...],
    "medium": [...],
    "low": [...]
  },
  "revision_guidance": {
    "priority_issues": [...],
    "suggested_modifications": [...],
    "additional_validation_needed": "..."
  }  // Only if REVISE
}
""",
    description="Evaluate and decide",
    run_in_background=false
)
```

### 输出处理

保存到 `docs/evaluation.json`：
- `decision`: 决策
- `evidence_summary`: 证据摘要
- `rationale`: 决策理由（详细）
- `issues`: 问题评估
- `revision_guidance`: 修订指导（如需修订）

### 决策处理

| 决策 | 行动 |
|------|------|
| **ACCEPT** | 进入 Stage 5（最终输出） |
| **REVISE** | 返回 Stage 2 重新设计（最多1次修订） |
| **REJECT** | 报告失败原因和理由 |

---

## 并行执行说明

### Stage 3 并行调用

```python
# 同时启动 Supporter 和 Critic
supporter_task = Agent(
    subagent_type="general-purpose",
    prompt=SUPPORTER_PROMPT,
    description="Support with experiments",
    run_in_background=false
)

critic_task = Agent(
    subagent_type="general-purpose",
    prompt=CRITIC_PROMPT,
    description="Critique with experiments",
    run_in_background=false
)

# 等待两个任务完成
# 处理两个输出
```

### 优势

- **效率提升**：Supporter 和 Critic 同时工作，节省时间
- **独立证据**：双方独立搜索文献和运行实验，避免偏见
- **全面辩论**：同时获得支持和批判视角，决策更全面

---

## 使用说明

1. **执行顺序**：Stage 2 → Stage 3(并行) → Stage 4 → Stage 5
2. **变量替换**：`{variable_name}` 需要替换为实际值
3. **输出格式**：严格按照指定的 JSON 格式输出
4. **实验集成**：Stage 3 的两个 Agent 都自主决定是否运行实验
5. **迭代限制**：最多执行 1 次修订循环（初始 + 1 次修订）
