# Improvement Strategies

Quick reference for common paper issues and their fixes.

---

## Methodology Improvements

| Issue | Fix | Implementation |
|-------|-----|----------------|
| No power analysis | Add a priori power analysis with effect size | "Power analysis (G*Power) showed N needed for 80% power to detect d=0.5" |
| Unclear inclusion criteria | Specify precise criteria | "Inclusion: age 18-65, fluent in English, no neurological disorders" |
| Missing control | Add control or explain why not feasible | "Control group received sham treatment" |
| Unvalidated instrument | Add validation info | "Scale showed α=0.87, consistent with prior validation [cite]" |

---

---

## Logic/Claim Improvements

| Issue | Fix | Example |
|-------|-----|---------|
| Causal language from correlational data | Change to associative language | "Proves" → "Suggests", "Causes" → "Associated with" |
| Overgeneralized claims | Add scope limitations | "Applies to all" → "Applies to X under condition Y" |
| Unwarranted certainty | Add hedging | "Clearly demonstrates" → "Indicates", "Proves" → "Suggests" |
| Missing limitations | Add limitations section | "Several limitations should be noted: First..." |
| Ignoring alternatives | Add alternative explanations | "While X suggests Y, alternative explanation Z is also possible" |

---

## Clarity Improvements

| Issue | Fix | Example |
|-------|-----|---------|
| Ambiguous terminology | Define at first use | "SINR (signal-to-interference-plus-noise ratio) is defined as..." |
| Inconsistent notation | Create notation table | "Table I: Notation used throughout this paper" |
| Missing figure/table references | Add in text | "As shown in Figure 3, the throughput increases..." |
| Poor transitions | Add transition sentences | "Having established X, we now present Y" |
| Incomplete paragraphs | Ensure claim-evidence-warrant | "[Claim]. [Evidence]. [Warrant/Explanation]." |

---

## Citation Improvements

| Issue | Fix | Zotero Search |
|-------|-----|---------------|
| Missing citations | Add relevant references | `semantic_search: "[claim]"` |
| Cherry-picking | Add countervailing evidence | `semantic_search: "[alternative viewpoint]"` |
| Citing non-empirical sources | Replace with empirical | `advanced_search: filter by publication type` |

---

## Related Work Improvements

**Common Issues**:
- List-like coverage (no thematic organization)
- Missing recent work
- No clear gap identification
- Weak positioning

**Quick Fixes**:
1. **Organize thematically**: Group by approach/method
2. **Add recent work**: Search last 3 years
3. **Identify gap**: "While X addresses A, it doesn't consider B"
4. **Position clearly**: "Unlike X, we use Y which achieves Z"

---

## Priority Framework

| Priority | Issues | Effort |
|----------|--------|--------|
| P1 | Threatens validity | Any |
| P2 | Affects interpretation | High/Medium |
| P3 | Polish | Low/Medium |
| P4 | Optional | Low |

**Fix Order**: P1 → (P2 + High Impact) → P2 → P3 → P4

---

## Common Mistakes to Avoid

1. **Over-correcting**: Don't add caveats that undermine legitimate findings
2. **Under-claiming**: Don't hedge when evidence is strong
3. **Inconsistent terminology**: Define once, use consistently
4. **Missing structure**: Ensure claim → evidence → warrant
5. **Selective citations**: Include contradictory evidence
