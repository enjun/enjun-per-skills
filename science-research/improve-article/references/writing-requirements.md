# Writing Requirements

Essential requirements for research paper writing to ensure data authenticity, theoretical rigor, and proper LaTeX formatting.

---

## 1. Data Authenticity Verification

### 1.1 Data Source Validation

| Requirement | Check | Action |
|-------------|-------|--------|
| **Data provenance** | Verify data source is legitimate | Trace data to original collection/experiment |
| **Data integrity** | Check for fabrication signs | Verify internal consistency, statistical plausibility |
| **Reproducibility** | Ensure methods can reproduce results | Provide sufficient detail for replication |
| **Raw data access** | Confirm data availability | Archive raw data with clear documentation |

### 1.2 Red Flags Checklist

- [ ] No citation for data source
- [ ] Statistical patterns appear too perfect
- [ ] Missing error bars or uncertainty measures
- [ ] Inconsistent sample sizes across analyses
- [ ] Unusual rounding patterns
- [ ] Missing methodology details

### 1.3 Verification Actions

```
For each dataset in the paper:
1. Locate original source citation
2. Verify data collection methodology is described
3. Check statistical plausibility (effect sizes, variances)
4. Confirm ethical approval if human/animal data
5. Verify data deposition in public repository (if required)
```

---

## 2. Mathematical Derivations & Theoretical Proofs

### 2.1 Appendix Requirements

**All significant derivations must be included in the Appendix**:

| Element | Appendix Content | When Required |
|---------|-----------------|---------------|
| **Theorem proofs** | Complete step-by-step derivation | All novel theorems |
| **Formula derivations** | Full mathematical derivation | Key formulas not in literature |
| **Optimization problems** | KKT conditions, Lagrangian analysis | All optimization formulations |
| **Inequalities** | Proof of inequality bounds | When establishing performance bounds |
| **Algorithm analysis** | Complexity proof, convergence proof | All proposed algorithms |

### 2.2 Proof Structure

```markdown
## Appendix A: Mathematical Derivations

### A.1 Proof of Theorem 1

**Statement**: [Restate theorem clearly]

**Proof**:
1. [Step 1: Initial assumptions]
2. [Step 2: Key transformation]
   - Show: [equation]
   - Because: [justification]
3. [Step 3: Application of Lemma X]
4. [Step 4: Final result]

∎

### A.2 Derivation of Equation (X)

Starting from [known result/equation]:
\[
[LaTeX equation]
\]

Apply [transformation]:
\[
[LaTeX equation]
\]

Simplifying yields:
\[
[Final equation form]
\]
```

### 2.3 Required Elements

| Element | Description | Example |
|---------|-------------|---------|
| **Assumptions** | State all assumptions explicitly | "We assume the channel is quasi-static..." |
| **Notation** | Define all mathematical symbols | "Let $\mathcal{H}$ denote the set..." |
| **Intermediate steps** | Show key transformations | "From (A.2), substituting x yields..." |
| **Justifications** | Cite lemmas, theorems used | "By Jensen's inequality..." |
| **Q.E.D. symbol** | Mark proof completion | "∎" or "■" |

### 2.4 What Belongs in Appendix

✅ **Include**:
- Novel theorem proofs
- Derivation of key equations
- Algorithm convergence proofs
- Complexity analysis details
- Extension of results to special cases

❌ **Do NOT include**:
- Standard textbook results (cite instead)
- Trivial algebraic manipulations
- Well-known inequalities without modification
- Routine calculus operations

---

## 3. LaTeX Formatting Requirements

### 3.1 Table & Figure Width

| Element | Maximum Width | Action if Exceeded |
|---------|---------------|-------------------|
| **Single-column table** | `\columnwidth` | Use `\small`, `\footnotesize`, or convert to two-column |
| **Two-column table** | `\textwidth` | Use landscape or split into multiple tables |
| **Single-column figure** | `\columnwidth` | Use `\resizebox` or `\width=\columnwidth` |
| **Two-column figure** | `\textwidth` | Use `figure*` environment |

#### Table Width Solutions

```latex
% Solution 1: Resize table
\begin{table}[h]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tabular}{...}
...
\end{tabular}%
}
\caption{...}
\label{tab:example}
\end{table}

% Solution 2: Use smaller font
\begin{table}[h]
\centering
\small  % or \footnotesize
\begin{tabular}{...}
...
\end{tabular}
\caption{...}
\label{tab:example}
\end{table}

% Solution 3: Two-column table (single-column layout)
\begin{table*}[t]
\centering
\begin{tabular}{...}
...
\end{tabular}
\caption{...}
\label{tab:example}
\end{table*}
```

#### Figure Width Solutions

```latex
% Solution 1: Fixed width
\begin{figure}[h]
\centering
\includegraphics[width=\columnwidth]{figure.pdf}
\caption{...}
\label{fig:example}
\end{figure}

% Solution 2: Rescaled (maintains aspect ratio)
\begin{figure}[h]
\centering
\includegraphics[width=\columnwidth,height=0.5\textheight,keepaspectratio]{figure.pdf}
\caption{...}
\label{fig:example}
\end{figure}
```

### 3.2 Labeling & Cross-Referencing

#### ❌ FORBIDDEN: Hard-coded References

```latex
% DO NOT DO THIS
As shown in Table 1, the results...
From Figure 3, we observe...
Equation (5) demonstrates...
```

#### ✅ REQUIRED: Label + Cross-Reference

```latex
% DO THIS INSTEAD
\begin{table}[h]
\centering
\begin{tabular}{...}
...
\end{tabular}
\caption{Performance comparison}\label{tab:performance}
\end{table}

% In text:
As shown in Table~\ref{tab:performance}, the results...

\begin{figure}[h]
\centering
\includegraphics{...}
\caption{System architecture}\label{fig:architecture}
\end{figure}

% In text:
From Figure~\ref{fig:architecture}, we observe...

\begin{equation}
y = mx + b\label{eq:linear}
\end{equation}

% In text:
Equation~(\ref{eq:linear}) demonstrates...
```

#### Labeling Convention

| Element | Label Format | Example |
|---------|--------------|---------|
| Tables | `tab:descriptive-name` | `\label{tab:performance}` |
| Figures | `fig:descriptive-name` | `\label{fig:architecture}` |
| Equations | `eq:descriptive-name` | `\label{eq:optimization}` |
| Sections | `sec:descriptive-name` | `\label{sec:methodology}` |
| Algorithms | `alg:descriptive-name` | `\label{alg:proposed}` |

### 3.3 Bibliography Citation Verification

#### Citation Requirements

- [ ] **Every bib entry is cited**: Check for unused references
- [ ] **Every citation exists**: Verify all `\cite{}` commands have matching `.bib` entries
- [ ] **No orphan citations**: No citations to non-existent sources
- [ ] **Proper citation style**: Use journal/conference specified format

#### Verification Commands

```bash
# Check for unused references (after bibtex run)
grep -r "Warning.*citation" *.log

# Manual check: Extract all labels from .bib file
grep "@.*{" references.bib | sed 's/.*{\(.*\),.*/\1/' > bib_keys.txt

# Manual check: Extract all citations from .tex file
grep -oh '\\cite{[^}]*}' *.tex | sed 's/\\cite{//;s/}//' | tr ',' '\n' | sort -u > cited.txt

# Compare (missing in .bib = problem)
diff bib_keys.txt cited.txt
```

#### Common Citation Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Missing `.bib` entry | Compilation fails | Add entry to `.bib` file |
| Uncited reference | Wastes space | Remove unused entry or cite it |
| Inconsistent author names | Appears as multiple entries | Standardize format |
| Missing DOI/URL | Harder to verify | Add DOI field |

### 3.4 Chinese Character Detection

#### Forbidden Characters

| Category | Chinese | English | LaTeX |
|----------|---------|---------|-------|
| Parentheses | （） | () | `()` |
| Commas | ， | , | `,` |
| Periods | 。 | . | `.` |
| Colons | ： | : | `:` |
| Semicolons | ； | ; | `;` |
| Quotes | "" `` | "" | `""` or `` ` `` `''` |
| Spaces | (full-width) | (regular) | Single space after punctuation |

#### Detection Commands

```bash
# Detect Chinese characters (excluding Chinese bibliography)
grep -n "[\u4e00-\u9fff]" *.tex

# Detect full-width punctuation
grep -n "[，。；：（）【】《》]" *.tex

# Specific patterns to check
grep -n "（" *.tex    # Full-width left parenthesis
grep -n "）" *.tex    # Full-width right parenthesis
grep -n "，" *.tex    # Full-width comma
grep -n "。" *.tex    # Full-width period
grep -n "：" *.tex    # Full-width colon
```

#### Auto-Replacement Pattern

```latex
% Find and replace
% （ → \(
% ） → \)
% ， → ,
% 。 → .
% ； → ;
% ： → :
% " → `` or '' (context-dependent)
```

### 3.5 Formatting Checklist

#### Tables

- [ ] Width does not exceed `\columnwidth` (single-column) or `\textwidth` (two-column)
- [ ] Has `\label{}` for cross-referencing
- [ ] Has descriptive caption
- [ ] Column headers are clear
- [ ] Units specified in headers or footnote
- [ ] No vertical lines (unless required by format)
- [ ] Horizontal lines used appropriately (`\toprule`, `\midrule`, `\bottomrule`)

#### Figures

- [ ] Width does not exceed column/text width
- [ ] Has `\label{}` for cross-referencing
- [ ] Has descriptive caption
- [ ] Resolution sufficient for publication (≥300 dpi)
- [ ] Fonts are readable when printed
- [ ] Axes are labeled with units
- [ ] Legend is clear and positioned appropriately

#### Equations

- [ ] Key equations numbered
- [ ] Has `\label{}` for referenced equations
- [ ] Symbols defined at first use or in notation table
- [ ] Complex derivations moved to Appendix
- [ ] Equation punctuation (period at end if ending sentence)

#### References

- [ ] All entries in `.bib` file are cited
- [ ] All citations have matching `.bib` entries
- [ ] Consistent formatting (check journal style)
- [ ] DOIs included where available
- [ ] No Chinese characters in English papers

---

## 4. Pre-Submission Checklist

### Data & Methods

- [ ] All data sources verified and cited
- [ ] No signs of data fabrication
- [ ] Methodology sufficiently detailed for replication
- [ ] Ethical approval noted if applicable

### Mathematics & Theory

- [ ] All novel theorems proved in Appendix
- [ ] Key equation derivations included
- [ ] Algorithm convergence proved
- [ ] Complexity analysis provided

### LaTeX Formatting

- [ ] All tables/figures within width limits
- [ ] All labeled elements use `\label{}` and `\ref{}`
- [ ] No hard-coded references (Table 1, Figure 2, etc.)
- [ ] All references cited and all citations valid
- [ ] No Chinese characters in English text
- [ ] Document compiles without errors
- [ ] PDF output clean and professional

---

## 5. Quick Reference

| Category | Key Requirement | Verification |
|----------|----------------|--------------|
| **Data** | Authenticity verified | Trace sources, check plausibility |
| **Proofs** | Appendix for derivations | Complete step-by-step proofs |
| **Tables** | Width + label | `\resizebox` or two-column |
| **Figures** | Width + label | `width=\columnwidth` |
| **References** | Cross-reference only | `\label{}` + `\ref{}` |
| **Citations** | All valid | Check `.bib` vs `\cite{}` |
| **Language** | No Chinese characters | `grep -n "[\u4e00-\u9fff]"` |

---

