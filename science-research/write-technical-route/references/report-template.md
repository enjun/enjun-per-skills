# Technical Report Template and Compilation

This document provides the LaTeX report structure, writing principles, and compilation instructions.

## Table of Contents

1. [Directory Setup](#directory-setup)
2. [LaTeX Document Structure](#latex-document-structure)
3. [Writing Principles](#writing-principles)
4. [Citation Standards](#citation-standards)
5. [Compilation Instructions](#compilation-instructions)
6. [Markdown Version](#markdown-version)

---

## Directory Setup

```bash
# Create latex directory
mkdir -p latex

# Copy template files from assets
cp assets/* latex/

# If user provided a bib file, copy and rename
# cp "user_bib_file_path" latex/myref.bib
```

---

## LaTeX Document Structure

The `latex/main.tex` should follow this structure:

### Preamble

```latex
\documentclass[journal]{IEEEtran}
\usepackage{amsmath,amsfonts}
\usepackage{algorithmic}
\usepackage{algorithm}
\usepackage{graphicx}

% Chinese support (must be before other packages)
\usepackage{xeCJK}
\setCJKmainfont{SimSun}      % Chinese font: SimSun
\setCJKsansfont{SimHei}      % Chinese sans-serif: SimHei

\usepackage{cite}
\usepackage{booktabs}  % Optimize table lines
\usepackage{multirow}  % Table multi-row merging
\usepackage{array}     % Enhanced table functionality
\usepackage[unicode]{hyperref}
```

### Front Matter

```latex
\begin{document}

\title{[Research Question] Technical Route Investigation Report}
\author{}  % Leave blank
\maketitle

\begin{abstract}
Briefly describe:
- Report purpose: For the [research question]
- Scope: Systematically investigated XX relevant literature
- Findings: Identified N main technical routes
- Method: Conducted comparative analysis from multiple dimensions
- Outcome: Proposed improvement directions
\end{abstract}

\begin{IEEEkeywords}
Technical Route, [3-5 relevant keywords]
\end{IEEEkeywords}
```

### Main Content Structure

```latex
\section{Introduction}
\subsection{Problem Background}
Elaborate on:
- Background of the research question
- Importance and significance
- Application scenarios

\subsection{Technical Background}
Introduce:
- Overall technical status of related fields
- Current challenges
- Why technical route research is needed

\section{Technical Route Analysis}
% Organize by category, one section per category

\subsection{[Category1 Name] Methods}
\subsubsection{Method Principles}
- Core ideas (must cite references)
- Key technologies (must cite references)
- Mathematical model or algorithm description (if applicable)

\subsubsection{Representative Work}
- Analyze 2-3 representative literature
- For each: explain its status, contributions, and performance

\subsubsection{Evolution Lineage}
- Trace development process chronologically
- Identify key breakthroughs

\subsubsection{Critical Analysis}
- Assumptions: Are they reasonable?
- Core advantages and limitations
- Applicability and practical challenges

\subsection{[Category2 Name] Methods}
% Same structure as above

% ... more categories as needed

\section{Technical Route Comparison}

% Comprehensive comparison table
\begin{table*}[htbp]
\centering
\caption{Comprehensive Comparison of Technical Routes (all data must cite literature)}
\begin{tabular}{lcccc}
\toprule
Technical Route & Theoretical Foundation & Core Advantage & Main Limitation & Applicable Scenario \\
\midrule
Route A\cite{ref1,ref2} & ... & ... & ... & ... \\
Route B\cite{ref3} & ... & ... & ... & ... \\
\bottomrule
\end{tabular}
\end{table*}

% Performance metrics comparison table
\begin{table*}[htbp]
\centering
\caption{Performance Metrics Comparison (all data must cite literature)}
\begin{tabular}{lcccc}
\toprule
Technical Route & Metric1 & Metric2 & Metric3 & Computational Complexity \\
\midrule
Route A\cite{ref1} & 95.2\% & O(n²) & ... & ... \\
Route B\cite{ref3} & 92.8\% & O(n log n) & ... & ... \\
\bottomrule
\end{tabular}
\end{table*}

\section{Conclusion and Outlook}
\subsection{Problem Resolution Status}
- Is the research problem fully solved?
- Contribution level of each technical route
- Remaining challenges

\subsection{Improvement Directions}
- Possible directions for technology fusion
- Promising emerging technologies
- Specific improvement suggestions (based on limitations analyzed above)

\bibliographystyle{IEEEtran}
\bibliography{myref}

\end{document}
```

---

## Writing Principles

### Content Organization

1. **Organize by Category, Not Individual Literature**
   - Each technical route category as a section or subsection
   - Discuss literature belonging to the same category together
   - Explain their connections and differences

2. **Logical Coherence**
   - Use transition sentences between paragraphs
   - Form a complete logical chain: problem → analysis → comparison → conclusion
   - Use connecting words: "furthermore", "however", "therefore", "in contrast"

3. **Balance Depth and Readability**
   - Deep analysis for important technical routes
   - Supplement formulas with textual explanations
   - Avoid being overly technical to the point of being difficult to understand

### Section-by-Section Guidelines

#### Introduction
- **Problem Background**: Why is this question important? What problems does it solve?
- **Technical Background**: What is the current state? What are the gaps?

#### Technical Route Analysis
- **Method Principles**: Clear description of how the method works
- **Representative Work**: Select papers that best represent the category
- **Evolution Lineage**: Show how the field has evolved
- **Critical Analysis**: Apply the six-dimension framework from technical-analysis.md

#### Comparison
- **Comprehensive Table**: High-level comparison across all dimensions
- **Performance Table**: Quantitative comparison with metrics
- **All data must cite sources**

#### Conclusion
- **Resolution Status**: Be honest about what is solved and what isn't
- **Improvement Directions**: Suggestions should be based on the analysis, not speculation

---

## Citation Standards

### When to Cite
- Each technical route must cite its original literature
- Performance data must indicate sources
- Specific claims or findings must be supported

### Citation Format
```latex
% Single citation
\cite{ref1}

% Multiple consecutive citations
\cite{ref1,ref2,ref3}

% Citation with page number
\cite[page=10]{ref1}

% Citation in text
As proposed by Smith \cite{ref1}...
```

### BibTeX Entry Format
```bibtex
@article{ref1,
  author = {Author, Name},
  title = {Paper Title},
  journal = {Journal Name},
  year = {2024},
  volume = {10},
  number = {1},
  pages = {1--15}
}
```

---

## Compilation Instructions

### Method 1: Using latexmk (Recommended)

```bash
cd latex
latexmk -xelatex main.tex
```

### Method 2: Manual Compilation

```bash
cd latex
xelatex main.tex      # First compilation
bibtex main           # Generate bibliography
xelatex main.tex      # Second compilation (embed citations)
xelatex main.tex      # Third compilation (update citation numbers)
```

### Clean Auxiliary Files

```bash
latexmk -c
```

Or manually remove `.aux`, `.log`, `.out`, `.fls`, etc.

### Important Notes

1. **Chinese Documents**: Must use `xelatex`, NOT `pdflatex`
2. **Font Requirements**: Ensure Chinese fonts are installed (SimSun, SimHei)
3. **Font Substitution**: If font missing error occurs, replace with available system fonts
4. **Error Checking**: Check the `.log` file for compilation errors and fix them

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Font missing error | Replace with available system font (e.g., `FandolSong`) |
| Citation appears as `?` | Run `bibtex` and recompile with `xelatex` |
| Table formatting issues | Check `\\` at end of rows and `&` separators |

---

## Markdown Version

Generate `main.md` in the `latex` directory alongside the LaTeX version.

### Conversion Guidelines

1. **Maintain Structure**: Use same heading levels
2. **Syntax Conversion**:
   - `\section{}` → `#`
   - `\subsection{}` → `##`
   - `\subsubsection{}` → `###`
3. **Tables**: Convert LaTeX tables to Markdown table format
4. **Formulas**: Use `$$...$$` for display math, `$...$` for inline
5. **Citations**: Use `[text](citation-key)` format or `[1]` style
6. **References**: Include reference list at the end

### Markdown Table Example

```markdown
| Technical Route | Theoretical Foundation | Core Advantage | Main Limitation |
|-----------------|------------------------|----------------|-----------------|
| Route A | ... | ... | ... |
| Route B | ... | ... | ... |
```

---

## Output Summary

After completing the technical route research, the user receives:

1. **Problem Overview**: Background and significance
2. **Technical Route Overview**: List of identified categories
3. **Key Findings**:
   - Core characteristics of each route
   - Relationships between routes
   - Advantages and limitations
4. **Performance Comparison Summary**: Based on weighted ranking
5. **Problem Resolution Status**: What's solved, what remains
6. **Suggested Directions**: Most promising routes and specific improvements

**Deliverables**:
- `latex/main.tex` - LaTeX source
- `latex/main.pdf` - Compiled PDF report
- `latex/main.md` - Markdown version
- `latex/myref.bib` - Reference file
