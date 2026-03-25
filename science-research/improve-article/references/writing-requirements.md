# Writing Requirements

Essential requirements for research paper writing: data authenticity, theoretical rigor, and proper LaTeX formatting.

---

## ⚠️ General Principles

### Task Completion Policy

**If a requirement cannot be completed due to technical limitations, clearly mark it as incomplete and explain why.**

| Requirement | If Unachievable | Action |
|-------------|-----------------|--------|
| **Mathematical proof** | Derivation too complex | Mark as "Open Problem" or "Conjecture", explain difficulty |
| **Data verification** | Original source inaccessible | State limitation, describe verification attempts |
| **Theoretical analysis** | Beyond current methods | Acknowledge as "Future Work" or "Open Question" |
| **Experimental validation** | Resources unavailable | Explain constraints, suggest alternative approaches |

**Examples**:
- *"The complete proof of Theorem 3 requires advanced tools from [area] which are beyond the scope of this work. We provide a sketch in Appendix A and leave the full proof as an open problem."*
- *"Due to the proprietary nature of the dataset, we could not independently verify the results. We validated the methodology through [alternative method]."*

**Principle**: Transparency about limitations is preferable to incomplete or incorrect claims.

---

## 1. Data Authenticity Verification

### Red Flags Checklist

- [ ] No citation for data source
- [ ] Statistical patterns appear too perfect
- [ ] Missing error bars or uncertainty measures
- [ ] Inconsistent sample sizes across analyses
- [ ] Unusual rounding patterns
- [ ] Missing methodology details

### Verification Steps

1. Locate original source citation
2. Verify data collection methodology is described
3. Check statistical plausibility (effect sizes, variances)
4. Confirm ethical approval if human/animal data
5. Verify data deposition in public repository (if required)

---

## 2. Mathematical Derivations & Theoretical Proofs

### Appendix Requirements

| Element | When Required |
|---------|---------------|
| Theorem proofs | All novel theorems |
| Formula derivations | Key formulas not in literature |
| Optimization problems | KKT conditions, Lagrangian analysis |
| Inequalities | When establishing performance bounds |
| Algorithm analysis | Complexity proof, convergence proof |

### Proof Structure Template

```markdown
### A.1 Proof of Theorem 1

**Statement**: [Restate theorem clearly]

**Proof**:
1. [Initial assumptions]
2. [Key transformation] → [justification]
3. [Application of Lemma X]
4. [Final result]

∎
```

### What to Include/Exclude

✅ **Include**: Novel proofs, key derivations, convergence proofs, complexity analysis
❌ **Exclude**: Standard textbook results (cite), trivial manipulations, well-known inequalities

### When Proof Is Incomplete

⚠️ **If a complete proof cannot be provided**:

| Situation | Approach | Example Statement |
|-----------|----------|-------------------|
| Proof too complex | Provide proof sketch | *"We outline the main ideas; full proof requires [advanced technique] beyond scope."* |
| Missing intermediate step | Acknowledge gap | *"The connection between (A.2) and (A.3) relies on [lemma] which we conjecture holds."* |
| Unproven conjecture | Mark as open problem | *"This step assumes Conjecture 1, which remains to be proven."* |
| Partial result | State clearly | *"We prove the theorem for the special case of X; general case remains open."* |

**Never**: Claim a theorem is proven when the proof is incomplete or relies on unverified assumptions.

---

## 3. LaTeX Formatting Requirements

### 3.1 Table & Figure Width

| Element | Max Width | Solution |
|---------|-----------|----------|
| Single-column table/figure | `\columnwidth` | `\resizebox{\columnwidth}{!}{...}` or `\small` |
| Two-column table/figure | `\textwidth` | Use `table*`/`figure*` environment |

```latex
% Table width fix
\begin{table}[h]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tabular}{...}
...
\end{tabular}%
}
\caption{...}\label{tab:name}
\end{table}

% Figure width fix
\begin{figure}[h]
\centering
\includegraphics[width=\columnwidth]{file.eps}
\caption{...}\label{fig:name}
\end{figure}
```

### 3.1.1 Figure File Format

**⚠️ CRITICAL REQUIREMENT**: All figures inserted into LaTeX must be in **EPS (Encapsulated PostScript)** format.

| Format | Allowed | Reason |
|--------|---------|--------|
| `.eps` | ✅ **REQUIRED** | Standard for academic LaTeX, vector quality |
| `.pdf` | ⚠️ Acceptable alternative | When EPS unavailable |
| `.png`, `.jpg` | ❌ **NOT RECOMMENDED** | Raster format, quality loss |

**Python Code Requirements** (matplotlib):

When generating figures with Python, use the following code pattern:

```python
import matplotlib.pyplot as plt

# Create your plot
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_title('Figure Title')

# ⚠️ CRITICAL: Save as EPS format
plt.savefig('figure_name.eps', format='eps', bbox_inches='tight')
plt.close()
```

**Required parameters**:
- `format='eps'` - Explicitly set EPS format
- `bbox_inches='tight'` - Remove extra whitespace

**Recommended additional parameters**:
```python
plt.savefig('figure_name.eps',
            format='eps',
            bbox_inches='tight',
            dpi=300,           # High resolution
            transparent=False)  # White background (default)
```

**Conversion commands**:
```bash
# Convert PDF to EPS
pdftops -eps input.pdf output.eps

# Convert PNG to EPS (low quality)
convert input.png output.eps

# Convert using GIMP (better quality)
# Open PNG in GIMP → File → Export As → Select EPS
```

**Verification**:
```bash
# Check figure formats in LaTeX
grep -n "\includegraphics" *.tex | grep -v "\.eps"

# Check Python code for EPS format
grep -n "savefig" code/*.py | grep -v "format='eps'"
```

### 3.2 Labeling & Cross-Referencing

❌ **FORBIDDEN**: Hard-coded references (`Table 1`, `Figure 2`)

✅ **REQUIRED**: `\label{}` + `\ref{}`

| Element | Label Format |
|---------|--------------|
| Tables | `\label{tab:descriptive-name}` |
| Figures | `\label{fig:descriptive-name}` |
| Equations | `\label{eq:descriptive-name}` |
| Sections | `\label{sec:descriptive-name}` |

```latex
% Text reference
As shown in Table~\ref{tab:performance}...
From Figure~\ref{fig:architecture}, we observe...
Equation~(\ref{eq:linear}) demonstrates...
```

### 3.3 Citation Verification

**Requirements**:
- [ ] Every `.bib` entry is cited
- [ ] Every `\cite{}` has matching `.bib` entry
- [ ] No orphan citations

**Check commands**:
```bash
# Extract bib keys
grep "@.*{" references.bib | sed 's/.*{\(.*\),.*/\1/' > bib_keys.txt

# Extract citations
grep -oh '\\cite{[^}]*}' *.tex | sed 's/\\cite{//;s/}//' | tr ',' '\n' | sort -u > cited.txt

# Compare
diff bib_keys.txt cited.txt
```

### 3.4 Chinese Character Detection

**Forbidden**: Full-width punctuation `（）。，；：""`

**Detection**:
```bash
grep -n "[，。；：（）【】《》]" *.tex
```

**Replacement**:
| Chinese | English |
|---------|---------|
| （） | `()` |
| ， | `,` |
| 。 | `.` |
| ； | `;` |
| ： | `:` |

### 3.5 Multi-Line Equation Alignment

**推荐使用 `align` 环境进行多行公式对齐**

```latex
% 两行对齐（单个编号）
\begin{equation}
\begin{aligned}
&\text{第一行} \\
&= \text{第二行}
\end{aligned}
\end{equation}

% 多行对齐（每行独立编号）
\begin{align}
a &= b + c \\
&= d + e
\end{align}

% 多行对齐（不编号）
\begin{align*}
a &= b + c \\
&= d + e
\end{align*}
```

**对齐说明**：
- `&` 符号指定对齐位置（通常放在等号前）
- `\\` 换行
- `align` 每行独立编号，`equation` 整体一个编号
- `align*` 不编号

---

## 4. Pre-Submission Checklist

### Data & Methods
- [ ] All data sources verified and cited
- [ ] No signs of data fabrication
- [ ] Methodology sufficiently detailed for replication

### Mathematics & Theory
- [ ] All novel theorems proved in Appendix
- [ ] Key equation derivations included
- [ ] Algorithm convergence proved

### LaTeX Formatting
- [ ] All tables/figures within width limits
- [ ] All elements use `\label{}` + `\ref{}` (no hard-coded references)
- [ ] All references cited, all citations valid
- [ ] No Chinese characters in English text
- [ ] Document compiles without errors

---

## 5. Quick Reference

| Category | Key Check | Command/Action |
|----------|-----------|----------------|
| **Data** | Authenticity | Trace sources, verify methodology |
| **Proofs** | Appendix | Complete step-by-step proofs |
| **Width** | Tables/Figures | `\resizebox{\columnwidth}{!}{...}` |
| **References** | Cross-reference | `\label{}` + `\ref{}` |
| **Citations** | Valid | Check `.bib` vs `\cite{}` |
| **Language** | No Chinese | `grep -n "[，。；：（）]" *.tex` |

---
