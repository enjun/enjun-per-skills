---
name: independent-scientific-research
description: Fully automated multi-agent scientific research skill for wireless communications. Uses hybrid parallel pipeline (Problem Analysis → Proposer → Supporter+Critic Parallel → Evaluator → Output) where experiments are autonomously executed by agents to support their arguments. Automatically searches Zotero literature, runs Python experiments, and generates IEEE LaTeX papers. Use when users need to solve wireless communication research problems with rigorous validation. Use this skill whenever the user asks to "solve a research problem", "develop a technical solution", "design a wireless system", or "investigate a scientific question" in wireless communications.
disable-model-invocation: true
---

# Independent Scientific Research: Hybrid Parallel Pipeline

A fully automated multi-agent scientific research skill that develops rigorous solutions through a hybrid parallel pipeline. Proposer generates solutions, then Supporter and Critic work in parallel with experiments, and Evaluator makes the final decision.

## Requirements

- Zotero installation with zotero-mcp integration
- Python environment for validation experiments
- LaTeX compiler (pdflatex/xelatex) for document generation

---

## Core Philosophy

**Quality through parallel debate with experimental rigor, then informed decision.**

Hybrid parallel pipeline:
1. **Problem Analysis** - Literature foundation
2. **Proposer** - Generate initial solution
3. **Parallel Debate** - Supporter + Critic work simultaneously with experiments
4. **Evaluator** - Weigh evidence, make decision with rationale
5. **Final Output** - IEEE LaTeX + PDF

**Key innovation**: Supporter and Critic run in parallel, both using experiments to back their arguments.

---

## Stage 1: Problem Analysis

### Step 1.1: Collect Information

Gather from user:
- Research problem
- Context (scenario, constraints, requirements)
- Output focus (theoretical / system / algorithm)

### Step 1.2: Literature Foundation

Single-pass Zotero search:
```python
mcp__zotero-mcp__zotero_semantic_search(query=research_problem, limit=15)
mcp__zotero-mcp__zotero_search_items(query=key_techniques, limit=10)
```

Extract: state-of-the-art (3-5 papers), limitations, recent advances.

### Output

Save literature summary to `docs/literature-summary.md`

---

## Stage 2: Proposer (Serial)

**→ Detailed prompt in `references/agent_prompts.md`**
**→ Brainstorming methods in `references/proposer_brainstorming.md`**

### Overview

Spawn Proposer Agent to:
- Perform **internal brainstorming** using four-phase process
- Generate diverse ideas through cross-domain analogy, assumption reversal, etc.
- Select and synthesize the most promising direction
- Propose a comprehensive technical solution

**Brainstorming techniques:**
- Cross-domain analogy, assumption reversal, scale transformation
- Constraint manipulation, technology speculation
- Pattern recognition, critical evaluation

**No experiments at this stage** - focus on creative solution design.

### Output

Save to `docs/proposal.json`:
- Problem analysis
- Proposed solution (methodology, innovations, advantages)
- Implementation considerations
- Validation approach
- **Brainstorming trace** (ideas generated, patterns, rationale)

---

## Stage 3: Parallel Debate (Parallel)

**→ Detailed prompts in `references/agent_prompts.md`**
**→ Experiment guide in `references/experiment_guide.md`**

### Overview

Spawn **both** agents in parallel:

**Supporter Agent:**
- Search Zotero for supporting literature
- Run experiments to validate claims
- Provide quantitative arguments

**Critic Agent:**
- Search Zotero for counter-evidence
- Run experiments to challenge assumptions
- Identify theoretical and practical issues

### Parallel Execution

```python
# Spawn both in parallel
Agent(subagent_type="general-purpose",
     prompt=SUPPORTER_PROMPT,
     description="Support with experiments",
     run_in_background=false)

Agent(subagent_type="general-purpose",
     prompt=CRITIC_PROMPT,
     description="Critique with experiments",
     run_in_background=false)
```

### Outputs

Save to:
- `docs/support.json` - Supporting evidence and experiments
- `docs/critique.json` - Critical evidence and experiments

---

## Stage 4: Evaluator (Serial)

**→ Detailed prompt in `references/agent_prompts.md`**

### Overview

Spawn Evaluator Agent to:
- Weigh supporting vs challenging evidence
- Assess experimental validity from both sides
- Identify issues by impact level
- Make decision: **ACCEPT / REVISE / REJECT**
- Provide clear rationale

### Decision Criteria

| Decision | Conditions |
|----------|------------|
| **ACCEPT** | Supporting evidence > challenging, no high-impact issues |
| **REVISE** | Mixed evidence, high-impact issues addressable |
| **REJECT** | Challenging >> supporting, fatal flaws |

### Actions

- **ACCEPT** → Go to Stage 5
- **REVISE** → Return to Stage 2 (max 3 revision)
- **REJECT** → Report failure with rationale

### Output

Save to `docs/evaluation.json`:
- Decision (ACCEPT/REVISE/REJECT)
- Evidence balance summary
- Issues by impact level
- **Rationale** - clear explanation of the decision
- Revision guidance (if REVISE)

---

## Stage 5: Final Output

### Step 5.1: Generate LaTeX

Use IEEE journal format. Copy templates from `assets/`:
- `IEEEtran.cls`, `IEEEtran.bst`, `IEEEabrv.bib`
- `main.tex`

### Step 5.2: Compile to PDF

**CRITICAL**: Must compile to produce final PDF.

```bash
cd latex
latexmk -xelatex main.tex
```

Verify: `main.pdf` generated, no errors, figures displayed.

### Output

- `latex/main.tex` - Source
- `latex/main.pdf` - **Final deliverable**

---

## Output

Upon completion, provide:
1. Final solution summary
2. **Evaluator's decision and rationale**
3. Evidence balance (supporting vs challenging)
4. LaTeX source files
5. All experimental code
6. **PDF paper** (`latex/main.pdf`)
