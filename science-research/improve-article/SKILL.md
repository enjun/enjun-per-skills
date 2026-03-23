---
name: improve-article
description: Improve research articles through systematic critical analysis, Git workflow, and Zotero literature integration. Use when improving papers, addressing reviewer comments, strengthening methodology, or enhancing Related Work sections. Automatically invoked for: "improve my paper", "fix research issues", "strengthen methodology", "enhance Related Work", "address reviewer feedback".
---

# Improve Article: Research Paper Enhancement

Systematically improve research articles through critical analysis, targeted revision, and comprehensive tracking. Integrates scientific rigor, Git version control, and Zotero literature search.

---

## Quick Start

```
Phase 0: Setup
   ↓ Initialize Git, create directories

Phase 1: Analyze
   ↓ Critical thinking + Zotero literature check

Phase 2: Plan
   ↓ Generate improvement plan → User approves

Phase 3: Implement
   ↓ Create branch → Make changes → Commit

Phase 4: Finalize
   ↓ Verify → Merge → Generate report
```

---

## Progress Tracking

Always create TodoWrite task list:
```markdown
Tasks:
- Phase 0: Initialize Git project
- Phase 1: Critical analysis + literature check
- Phase 2: Generate plan → User approval
- Phase 3: Create branch → Implement changes
- Phase 4: Verify → Merge → Report
```

---

## Phase 0: Project Setup

**Goal**: Initialize Git repository and create directory structure.

**Skip if**: Git repo already exists with required directories.

**Quick Setup**:
```bash
git init
mkdir -p latex code history plans

# Create .gitignore
cat > .gitignore << 'EOF'
# LaTeX build artifacts
*.aux
*.log
*.out
*.toc
*.lof
*.lot
*.bbl
*.blg
*.fls
*.synctex.gz
*.fdb_latexmk
*.pdf
*.dvi
*.ps
*.eps
*.thm
*.idx
*.ind
*.ilg
*.lot
*.lof

# LaTeX temporary files
*.tmp
*.bak
*~
*.fls
*.fdb_latexmk
*.synctex.gz
*.synctex.gz(busy)

# BibTeX
*.blg
*.bbl

# Python
__pycache__/
*.py[cod]
*.pyo
*.so
*.so.*
*.egg
*.egg-info/
dist/
build/
venv/
env/
.env/

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
*.swp
*.swo
*~

# IDE
.vscode/
.idea/
*.sublime-*
*.sublime-project
*.sublime-workspace

# Temporary files
*.tmp
*.bak
*~
*.log
EOF

git add -A && git commit -m "Initial: Set up project structure"
```

---

## Phase 1: Critical Analysis

**Goal**: Evaluate paper using scientific-critical-thinking framework.

### Step 1: Apply Critical Thinking

```
/scientific-critical-thinking latex/main.tex
```

**Evaluates**:
- Methodology (design, validity, controls)
- Bias (cognitive, selection, measurement)
- Statistics (tests, assumptions, effect sizes)
- Evidence (quality, convergence)
- Logic (fallacies, claim strength)
- Literature (coverage, recency, balance)

### Step 2: Check Writing Requirements

⚠️ **IMPORTANT**: Verify essential writing quality requirements:

```
Consult: [writing-requirements.md](references/writing-requirements.md)
```

**Check**:
- **Data authenticity**: Verify data sources, check for fabrication signs
- **Mathematical rigor**: Ensure proofs and derivations in Appendix
- **LaTeX formatting**: Table/figure widths, cross-references, citations, Chinese characters

**Document findings** in the analysis report (see Step 3).

### Step 3: Document Analysis

Save to `history/YYYY-MM-DD-HHMMSS-analysis.md`:

```markdown
# Critical Analysis Report

## Paper Overview
- Title, research question, design, main claims

## Strengths
[What was done well]

## Issues by Category

### Critical Issues (threaten validity)
- Issue → Location → Impact → Action needed

### Important Issues (affect interpretation)
- Issue → Location → Impact → Action needed

### Minor Issues (don't change conclusions)
- Issue → Location → Action needed

## Literature Assessment
- Coverage: [Complete/Incomplete]
- Recent work: [Adequate/Needs update]
- Gap identification: [What's missing]
```

📖 **For Related Work Issues**: If literature assessment reveals problems with the Related Work section, consult [related-work-improvement.md](references/related-work-improvement.md) for targeted improvement strategies.

**Commit the analysis record**:
```bash
git add history/YYYY-MM-DD-HHMMSS-analysis.md
git commit -m "Add: Critical analysis report for YYYY-MM-DD

- Identified X critical, Y important, Z minor issues
- Literature assessment completed"
```

---

## Phase 2: Plan Generation & Approval

**Goal**: Create structured improvement plan and get user approval.

### Step 1: Categorize Issues

| Severity | When to Use | Priority |
|----------|-------------|----------|
| Critical | Threatens validity | P1 - Must fix |
| Important | Affects interpretation | P2 - Should fix |
| Minor | Polish | P3 - Nice to fix |

### Step 2: Generate Plan

📖 **Strategy References**: When developing action plans for specific issues, consult:
- [improvement-strategies.md](references/improvement-strategies.md) - Quick fixes by category (methodology, statistics, logic, clarity, citations)
- [related-work-improvement.md](references/related-work-improvement.md) - Related Work section improvement strategies

Create improvement plan at `plans/IMPROVEMENT_PLAN.md`:

```markdown
# Improvement Plan

## Overview
- Critical: X, Important: Y, Minor: Z issues
- Recommendation: [Major/Moderate/Minor revisions]

## Issues by Priority
### P1 - Critical Issues
[Detailed list with locations, impacts, actions]

### P2 - Important Issues
[Detailed list with locations, impacts, actions]

## Action Plan
[Ordered steps to address each issue]

## Approval
- [ ] Approved - Proceed
- [ ] Approved with modifications
- [ ] Needs revision
```

### Step 3: User Approval ⚠️

Use `AskUserQuestion`:
- ✅ Approve - Proceed to Phase 3
- ✏️ Approve with modifications
- 🔄 Needs revision

**CRITICAL**: Do not proceed without approval.

---

## Phase 3: Branch & Implement

**Goal**: Implement improvements on dedicated Git branch.

### Step 1: Create Branch

```bash
git checkout -b improvement-$(date +%Y%m%d-%H%M%S)
# Example: improvement-20250323-143022
```

### Step 2: Implement Changes

**For each issue in approved plan**:

1. **Read relevant section**: `Read latex/main.tex`
2. **Make changes**: `Edit latex/main.tex`
3. **Document**: Log change in improvement record

**Improvement Categories**:

| Category | Focus | Quick Fix |
|----------|-------|-----------|
| Methodology | Design, controls, blinding | Add missing details |
| Statistics | Effect sizes, CIs, assumptions | Add statistical info |
| Logic/Claims | Overstatements, limits | Tone down, add limits |
| Clarity | Notation, flow | Improve structure |
| Citations | Missing, outdated, cherry-picking | Add/balance citations |
| Related Work | Coverage, gaps, positioning | Organize, identify gap |

📖 **Quick Reference Guide**: For detailed strategies and examples for each category, consult [improvement-strategies.md](references/improvement-strategies.md)

**Special Focus - Related Work**: When improving literature review sections, use [related-work-improvement.md](references/related-work-improvement.md) for:
- Thematic organization strategies
- Gap identification techniques
- Positioning and framing methods

**Available Tools** (use when needed):

- **Zotero** - For literature search and citation improvements
- **Read** - To examine paper sections
- **Edit** - To make targeted changes

### Step 3: Commit Incrementally

```bash
git add -A
git commit -m "Fix: [Brief description]

- Addressed: [Issue name]
- Changed: [What/where]
- Rationale: [Why it helps]"
```

---

## Phase 4: Verify & Merge

**Goal**: Verify improvements and merge to master.

### Step 1: Quality Verification

- [ ] All critical issues addressed
- [ ] All high-importance improvements done
- [ ] Claims supported by evidence
- [ ] Limitations acknowledged

⚠️ **Writing Requirements Check** (see [writing-requirements.md](references/writing-requirements.md)):
- [ ] **Data authenticity**: All sources verified, no fabrication signs
- [ ] **Mathematical rigor**: All proofs/derivations in Appendix
- [ ] **LaTeX formatting**: Tables/figures within width limits
- [ ] **Cross-references**: All use `\label{}` + `\ref{}` (no hard-coded "Table 1")
- [ ] **Citations**: All references cited, all citations valid
- [ ] **Language**: No Chinese characters in English text


**Compile**:
```bash
cd latex && latexmk -xelatex main.tex
```

### Step 2: Create Improvement Record

Save to `history/YYYY-MM-DD-HHMMSS-improvement.md`:
```markdown
# Improvement Record

## Changes Made
### Critical Issues Resolved
1. [Issue] - [Solution, location, rationale]

### Important Improvements
1. [Issue] - [Solution, location, rationale]

## Quality Metrics
- Before: X critical, Y important, Z minor
- After: X' critical, Y' important, Z' minor

## Files Modified
- latex/main.tex (sections/lines changed)
```

**Commit the improvement record**:
```bash
git add history/YYYY-MM-DD-HHMMSS-improvement.md
git commit -m "Add: Improvement record for YYYY-MM-DD

- Resolved X critical issues
- Addressed Y important improvements
- Quality metrics updated"
```

### Step 3: Merge to Master

```bash
git checkout master
git merge improvement-YYYYMMDD-HHMMSS
```

---

## Output to User

Provide summary:

1. **Git Status**
   - Repository, branch, commits

2. **Analysis Summary**
   - Strengths, issues by severity
   - Analysis saved to: `history/*-analysis.md`

3. **Improvements Made**
   - Changes with locations and rationale
   - Improvement branch: `improvement-YYYYMMDD-HHMMSS`

4. **Quality Metrics**
   - Before/after comparison

5. **Output Files**
   - `latex/main.tex` - Improved paper
   - `latex/main.pdf` - Compiled PDF
   - `plans/IMPROVEMENT_PLAN.md` - Approved plan
   - `history/*.md` - Analysis and records

---

## Special Cases

### Addressing Reviewer Comments

1. Parse comments into issues
2. Create branch: `reviewer-N-comments`
3. Address systematically
4. Document responses

### Limited Scope

When only specific aspects need improvement:
1. Focus analysis on specified area
2. Generate targeted plan
3. Implement only requested changes

---

## Available Tools

**Use these tools as needed during the improvement process**:

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `Skill: scientific-critical-thinking` | Comprehensive paper evaluation | Phase 1: Analysis |
| **Zotero MCP Tools** | **Literature search and citation improvements** | **As needed** |

**Zotero Tools** (available when needed):

- `mcp__zotero-mcp__zotero_semantic_search` - Exploratory literature search
- `mcp__zotero-mcp__zotero_advanced_search` - Precise filtering (year, venue, author)
- `mcp__zotero-mcp__zotero_get_item_metadata` - Extract citation information
- `mcp__zotero-mcp__zotero_get_notes` - Get quick summaries and annotations
- `mcp__zotero-mcp__zotero_get_item_fulltext` - Detailed content analysis

**Use Zotero when**:
- Verifying literature coverage
- Finding missing citations
- Improving Related Work section
- Checking for cherry-picking or contradictory evidence

---

## Reference Materials

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[improvement-strategies.md](references/improvement-strategies.md)** | Quick fix strategies by category | Implementing specific improvements |
| **[related-work-improvement.md](references/related-work-improvement.md)** | Related Work improvement guide | Improving literature review |
| **[writing-requirements.md](references/writing-requirements.md)** | Data authenticity, mathematical proofs, LaTeX formatting | Ensuring paper quality and formatting standards |

