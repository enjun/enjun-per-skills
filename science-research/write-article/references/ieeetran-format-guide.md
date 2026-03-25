# IEEEtran.cls LaTeX Format Guide

This guide provides the essential requirements for writing LaTeX documents using IEEEtran.cls document class. **All generated LaTeX documents MUST comply with these requirements.**

## Document Class Setup

### Correct Document Class Declaration
```latex
\documentclass[10pt,journal]{IEEEtran}    % Journal papers use 10pt
\documentclass[10pt,conference]{IEEEtran} % Conference papers use 10pt
```

**Important Notes**:
- IEEE journal papers should use `10pt` font size, **NOT** `12pt`
- Use `journal` option for journals, `conference` for conferences

## Package Loading Order

### Recommended Order
```latex
\documentclass[10pt,journal]{IEEEtran}

% Math packages
\usepackage{amsmath,amsfonts,amssymb,amsthm}

% Algorithms and code
\usepackage{algorithm}
\usepackage{algpseudocode}

% Tables
\usepackage{booktabs}

% Graphics
\usepackage{graphicx}
\graphicspath{{figures/}}

% References
\usepackage{cite}

% Hyperref MUST be loaded last
\usepackage[unicode]{hyperref}
```

**Critical**: `hyperref` package MUST be loaded AFTER all other packages to avoid conflicts.

## Theorem Environment Definitions

### IEEEtran Recommended Approach
```latex
% Text theorem styles
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{corollary}{Corollary}
\newtheorem{proposition}{Proposition}

% Definition-style environments
\theoremstyle{definition}
\newtheorem{definition}{Definition}
\newtheorem{assumption}{Assumption}
\newtheorem{remark}{Remark}
\newtheorem{example}{Example}
```

**Tip**: Use `\theoremstyle{definition}` to distinguish definition-style environments.

## Author Information Format

### Standard IEEEtran Author Block
```latex
\author{\IEEEauthorblockN{Author Name\thanks{Manuscript received xxxx; revised xxxx.}}
\IEEEauthorblockA{\textit{Department Name}}
\IEEEauthorblockA{Institution Name}
\IEEEauthorblockA{City, Country}
\IEEEauthorblockA{email: author@institution.edu}}
```

### Multiple Authors
```latex
\author{\IEEEauthorblockN{Author One\thanks{...}}
\IEEEauthorblockA{Affiliation One\\ City, Country\\ email: one@affiliation.edu}
\and
\IEEEauthorblockN{Author Two}
\IEEEauthorblockA{Affiliation Two\\ City, Country\\ email: two@affiliation.edu}}
```

## Figure Format Requirements

### Recommended Formats
- **Vector graphics**: `.eps` (preferred)
- **Raster images**: `.png`, `.jpg` (only when vector graphics unavailable)
- **Avoid**: `.bmp`, `.tif`

### Figure Insertion Example
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.85\columnwidth]{filename.eps}
    \caption{Figure caption text.}
    \label{fig:filename}
\end{figure}
```

**Note**: For IEEE double-column format, figure width is typically `\columnwidth`. For single-column figures, use `\textwidth` or `0.75\textwidth`.

## Algorithm Environment

### Recommended Usage
```latex
\begin{algorithm}[H]
\caption{Algorithm Title}
\label{alg:label}
\begin{algorithmic}[1]
\State \textbf{Input:} ...
\State \textbf{Output:} ...
\For{$i = 1$ \textbf{to} $N$}
    \State ...
\EndFor
\State \textbf{return} ...
\end{algorithmic}
\end{algorithm}
```

## Running Head Setup

### Journal Papers
```latex
\markboth{Journal Name,~Vol.~xx, No.~xx, xxxx}%
{Author \MakeLowercase{\textit{et al.}}: Paper Title}
```

### Conference Papers
```latex
% Conference papers typically do not need \markboth
```

## Keywords

### IEEE Keyword Format
```latex
\begin{IEEEkeywords}
keyword1, keyword2, keyword3, keyword4
\end{IEEEkeywords}
```

## Additional Requirements

### Mathematics
- Use `\eqref{}` for equation references (requires `amsmath`)
- Number all equations that will be referenced
- Define all symbols at first use

### Tables
- Use `booktabs` for professional tables: `\toprule`, `\midrule`, `\bottomrule`
- Place captions above tables
- Use `\label{}` after `\caption{}`

### Bibliography
- Use IEEE style: `\bibliographystyle{IEEEtran}`
- Include all cited references in `.bib` file
- Verify all DOIs are correct

## References

- IEEEtran official documentation: `IEEEtran_HOWTO.pdf`
- IEEE Author Center: https://ieeeauthorcenter.ieee.org/
