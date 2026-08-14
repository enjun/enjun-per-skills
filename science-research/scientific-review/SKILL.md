---
name: scientific-review
description: Structured scientific review and evaluation. Use whenever the user needs to peer-review a research manuscript (期刊稿件同行评审), review a National Natural Science Foundation of China (NSFC) proposal (国自然基金申请书评审), or quantitatively evaluate/score a survey paper (综述文章打分). Covers methodological rigor assessment, novelty and feasibility evaluation, constructive feedback writing, and formal review reports. Also use for self-checking a manuscript or proposal before submission. For improving a paper based on review feedback, use the scientific-writing skill; for deep methodological critique, use scientific-thinking.
allowed-tools: [Read, Write, Edit, Bash]
license: MIT license
---

# Scientific Review

Structured, evidence-based review of scientific outputs — research manuscripts, NSFC proposals, and survey papers. Choose the review target, then follow the corresponding evaluation framework.

## Why a shared review skill

All three review tasks follow the same discipline: evaluate against explicit criteria, separate major from minor issues, be specific and constructive, and produce a structured report the author can act on. Only the target-specific evaluation framework differs. So this skill routes to the right framework instead of repeating the common principles.

## Review Target Selection

Use `AskUserQuestion` (or infer from the request) to identify what is being reviewed:

| Target | Typical request | Framework |
|--------|----------------|-----------|
| **Research manuscript** | "review this paper", "同行评审", "帮我审稿" | [review-article.md](references/review-article.md) |
| **NSFC proposal** | "评审基金申请书", "帮我看看国自然本子" | [review-nsfc.md](references/review-nsfc.md) |
| **Survey paper** | "给综述打分", "evaluate this survey", "综述评价" | [review-survey.md](references/review-survey.md) |

Read the matching framework reference and follow its workflow.

---

## Shared Review Principles

Apply these across all review targets:

1. **Be constructive** — frame criticism as an opportunity for improvement; be specific with examples and actionable suggestions, not vague complaints.
2. **Be evidence-based** — judge methodology and evidence, not results you happen to like; base every major concern on something concrete in the document.
3. **Be proportionate** — distinguish critical issues (threaten validity), important issues (affect interpretation), and minor issues (polish); don't overstate.
4. **Be respectful** — focus on the science, not the scientist; never resort to personal attacks, sarcasm, or condescension.
5. **Be complete but scoped** — cover reproducibility, data availability, and figures where relevant, but keep the review proportionate to the document's length and purpose.

## Shared Report Structure

All review outputs follow this layered structure (targets vary in scoring detail):

1. **Summary statement** — concise overall assessment: brief overview, recommendation (accept / minor / major revision / reject), key strengths (2-3), key weaknesses (2-3).
2. **Major comments** — numbered issues that materially affect validity, interpretation, or significance. For each: state the problem, explain why it matters, suggest a concrete solution, and indicate whether resolving it is essential for acceptance.
3. **Minor comments** — numbered, lower-severity issues: unclear labels, missing details, typos, presentation suggestions.
4. **Questions to the author** — clarifications needed (methodological details, seemingly contradictory results, missing information).
5. **Specific scoring** — only where the framework defines one (see [review-survey.md](references/review-survey.md) for the 100-point, 7-dimension rubric; [review-nsfc.md](references/review-nsfc.md) for the funding-tier conclusion).

Where a target framework defines its own output format, follow that format over this generic one.

---

## Self-Check Before Submitting a Review

- [ ] Summary statement clearly conveys the overall assessment
- [ ] Major concerns identified, argued, and prioritized
- [ ] Suggested revisions are specific and actionable
- [ ] Minor issues recorded but correctly de-emphasized
- [ ] Reproducibility and data availability assessed
- [ ] Figures/tables quality and integrity assessed
- [ ] Tone is constructive and professional throughout

---

## Bundled Resources

| Reference | When to read |
|-----------|--------------|
| [review-article.md](references/review-article.md) | Reviewing a research manuscript — 6-stage evaluation (overview, section-by-section, methodology, reproducibility, figures, writing) with checklists |
| [review-nsfc.md](references/review-nsfc.md) | Reviewing an NSFC proposal — 4-part framework (立项依据, 研究内容与目标, 研究方案及可行性, 创新特色) plus funding-tier conclusion |
| [review-survey.md](references/review-survey.md) | Scoring a survey paper — 7-dimension, 100-point rubric with per-dimension scoring bands and report template |
