# Markdown Format Guide for Scientific Documents

This guide specifies how to structure and format scientific documents in Markdown for wireless communications research.

## Document Structure

### Frontmatter (Optional but Recommended)

```markdown
---
title: "Paper Title"
authors:
  - "Author Name"
  - "Second Author"
date: YYYY-MM-DD
keywords: [keyword1, keyword2, keyword3]
abstract: |
  Brief abstract text here...
---
```

### Main Sections

```markdown
# Title

## Abstract
[Abstract content]

## Keywords
[keyword1], [keyword2], [keyword3]

## I. Introduction
[Introduction content with background, problem statement, and contributions]

## II. Related Work
[Literature review and comparison with existing work]

## III. System Model / Methodology
[Detailed methodology description]

## IV. Proposed Approach
[Your proposed method or algorithm]

## V. Performance Evaluation
[Simulation results and analysis]

## VI. Conclusion
[Summary and future work]

## References
[Bibliography entries]
```

## Mathematical Notation

### Inline Math

Use single `$` delimiters for inline equations:

```markdown
The signal-to-noise ratio is defined as $\gamma = \frac{P_s}{N_0}$.
```

### Display Math

Use double `$$` delimiters for displayed equations:

```markdown
$$
\gamma = \frac{P_s}{N_0} = \frac{|h|^2 P_t}{N_0 B}
$$
```

### Equations with Alignment

For multi-line equations, use `\begin{align}` environment (will render in MathJax/katex):

```markdown
$$
\begin{align}
\gamma_1 &= \frac{P_s |h_1|^2}{N_0} \\
\gamma_2 &= \frac{P_s |h_2|^2}{N_0}
\end{align}
$$
```

## Figures

### Figure Inclusion

```markdown
![Figure caption description](path/to/figure.png)

**Figure 1:** System model showing the proposed architecture.
```

### Figure Guidelines

- Use descriptive file names (e.g., `system-model.png`, not `fig1.png`)
- Provide alt text for accessibility
- Include figure captions with numbering
- Place figures close to their first reference in text

### Example

```markdown
## III. System Model

The proposed system is shown in Figure 1.

![System model illustrating the transmitter-receiver chain with multiple antennas](assets/figures/system-model.png)

**Figure 1:** System model for MIMO transmission with $N_t$ transmit and $N_r$ receive antennas.

The channel matrix $\mathbf{H} \in \mathbb{C}^{N_r \times N_t}$ models the propagation environment.
```

## Tables

### Table Formatting

Use standard Markdown table syntax:

```markdown
| Algorithm | Complexity | Performance | Remarks |
|-----------|-----------|-------------|---------|
| ZF        | $O(N^3)$  | Moderate    | No interference cancellation |
| MMSE      | $O(N^3)$  | Good        | Balances interference and noise |
| ML        | $O(N!)$   | Optimal     | High computational cost |

**Table I:** Comparison of detection algorithms for MIMO systems.
```

### Table Guidelines

- Include column headers
- Number tables with Roman numerals (I, II, III, ...)
- Provide descriptive captions
- Use consistent decimal precision
- Include units in column headers when applicable

## Citations and References

### In-Text Citations

Use numerical citation style (IEEE standard):

```markdown
Recent work in MIMO systems [1]-[3] has shown significant improvements...
The proposed method builds upon [4] and extends it to...
```

Or author-year style (for non-IEEE venues):

```markdown
Recent work in MIMO systems (Smith et al., 2023; Johnson, 2024) has shown...
The proposed method builds upon Smith (2023) and extends it...
```

### Bibliography Section

```markdown
## References

[1] A. B. Smith, C. D. Johnson, and E. F. Williams, "Advanced MIMO techniques for 5G networks," *IEEE Trans. Commun.*, vol. 71, no. 4, pp. 1234-1245, Apr. 2023, doi: 10.1109/TCOMM.2023.1234567.

[2] Y. Zhang and L. Wang, "Efficient channel estimation in massive MIMO," in *Proc. IEEE GLOBECOM*, Singapore, Dec. 2024, pp. 1000-1005.

[3] M. Brown, *Wireless Communications: Principles and Practice*, 2nd ed. Upper Saddle River, NJ: Prentice Hall, 2023.
```

### Bibliography Guidelines

- Number references consecutively in order of appearance
- Use standard IEEE citation format
- Include DOIs when available
- For conference papers, include location and dates
- For books, include edition and publisher

### Linking to BibTeX (Optional)

For interoperability with LaTeX workflows, include a link to the BibTeX file:

```markdown
## References

The complete bibliography in BibTeX format is available in [`references/myref.bib`](references/myref.bib).

[1] A. B. Smith, C. D. Johnson, and E. F. Williams, "Advanced MIMO techniques...
```

## Code Blocks

### Algorithm Descriptions

```markdown
**Algorithm 1: Proposed Detection Method**

```
Input: Received signal y, channel matrix H
Output: Detected symbol vector x̂

1: Compute H^H y
2: Solve: x̂ = (H^H H)^(-1) H^H y
3: Quantize x̂ to constellation points
4: return x̂
```
```

### Simulation Code Snippets

```python
# Python simulation parameters
num_antennas = 4  # Number of antennas
modulation = '16QAM'  # Modulation scheme
snr_range = np.linspace(0, 20, 21)  # SNR in dB
```

## Formatting Best Practices

### Headings

- Use `#` for title, `##` for major sections (Abstract, Introduction, etc.)
- Use `###` for subsections
- Use `####` for sub-subsections (rarely needed)
- Number sections with Roman numerals for IEEE style: `## I. Introduction`

### Text Emphasis

- **Bold** for new terms on first definition
- *Italic* for emphasis and variable names in text
- `Code font` for algorithm names, function names, file names

### Lists

Use numbered lists for sequential items:

```markdown
1. First step
2. Second step
3. Third step
```

Use bullet lists for non-sequential items:

```markdown
- Key feature 1
- Key feature 2
- Key feature 3
```

### Special Characters

For wireless communications notation, use LaTeX math mode:
- Channel: $\mathbf{H}$, $h_{ij}$
- Noise: $n(t)$, $\mathbf{n}$
- Signal: $s(t)$, $\mathbf{s}$
- Matrices: $\mathbf{A}$, $\mathbf{B}$
- Vectors: $\mathbf{x}$, $\mathbf{y}$

## Conversion to LaTeX

This Markdown format is designed to be easily convertible to IEEE LaTeX format. Key conversion mappings:

| Markdown | LaTeX |
|-----------|-------|
| `# Title` | `\title{Title}` |
| `## I. Introduction` | `\section{Introduction}` |
| `### A. Background` | `\subsection{Background}` |
| `$\gamma$` | `$\gamma$` |
| `**Figure 1:**` | `\caption{Figure 1: ...}` |
| `[1]` | `\cite{ref1}` |

Tools for conversion:
- Pandoc: `pandoc main.md -o main.tex`
- Markdown to LaTeX converters
- Manual refinement may be needed for formatting

## Quality Checklist

Before finalizing your Markdown document:

- [ ] All sections have proper heading hierarchy
- [ ] All figures have captions and are referenced in text
- [ ] All tables have captions and column headers
- [ ] All equations use proper math delimiters
- [ ] All citations have bibliography entries
- [ ] Consistent formatting throughout
- [ ] No broken links to figures or references
- [ ] Proper capitalization in headings
- [ ] Mathematical notation defined at first use
