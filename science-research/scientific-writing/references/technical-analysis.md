# Technical Route Analysis Framework

This document provides the framework for extracting, classifying, and analyzing technical routes from literature.

## Table of Contents

1. [Information Extraction](#information-extraction)
2. [Classification Strategy](#classification-strategy)
3. [Literature Relationships](#literature-relationships)
4. [Critical Analysis Dimensions](#critical-analysis-dimensions)
5. [Performance Comparison](#performance-comparison)

---

## Information Extraction

Extract technical route information from each literature in the following priority order:

### Priority 1: Extract from Notes

Notes are the richest source of technical information:
- Method description sections
- Core ideas and algorithm steps
- Mathematical formulas
- Experimental settings and performance metrics

### Priority 2: Extract from Abstract

When notes are unavailable:
- Focus on sentences with keywords like "proposed", "presented", "developed", "introduced"
- Extract the main method description
- Identify the problem being solved

### Priority 3: Analyze from Full Text

When abstract is insufficient:
- Carefully read the Method/Methodology section
- Extract algorithm flow
- Identify system architecture
- Note key technologies and innovations

---

## Classification Strategy

### Classification Dimensions

Use these dimensions to group literature into technical route categories:

| Dimension | Description | Examples |
|-----------|-------------|----------|
| **Theoretical Foundation** | Core theory or mathematical model | Deep Learning / Graph Theory / Optimization Theory |
| **Technical Architecture** | Overall structure and component relationships | Centralized / Distributed / End-to-End |
| **Core Algorithm** | Main algorithm or technology | CNN / RNN / Transformer / Reinforcement Learning |
| **Problem Modeling** | How the problem is formalized | Classification / Regression / Sequence Modeling |
| **Optimization Objective** | What the method tries to optimize | Accuracy-first / Efficiency-first / Robustness-first |
| **Application Scenario** | Specific field of application | Medical Imaging / NLP / Recommender Systems |

### Classification Steps

1. **Single-Dimension Preliminary Classification**
   - Choose the most appropriate dimension (usually "Theoretical Foundation" or "Core Algorithm")
   - Divide literature into 3-6 categories
   - Ensure each category has clear feature definitions

2. **Multi-Dimension Refinement** (if needed)
   - For large categories, use a second dimension to subdivide
   - Example: First by "Theoretical Foundation", then refine by "Technical Architecture"

3. **Category Naming**
   - Use concise, professional terminology
   - Format: "[Core Feature] Methods" or "[Technology Name] Methods"
   - Examples: "Deep Learning-based Methods", "Graph Neural Network Methods"

4. **Cross-Validation**
   - Verify each literature's classification is reasonable
   - If a paper involves multiple categories, classify by its primary method
   - Explain multi-method characteristics in the analysis

**Evidence rule**: classify from full texts, not abstracts; record the original-text evidence sentence for every classification conclusion in a persistent file (grep-verifiable). See Core Principles in [related-work-improvement.md](related-work-improvement.md).

---

## Literature Relationships

While classifying, establish relationship networks between literature:

### Relationship Types

| Type | Description | Example |
|------|-------------|---------|
| **Citation** | A cites B → A improves or extends B | ResNet cites VGG → ResNet extends VGG |
| **Improvement** | A solves a problem of B | Attention mechanism solves RNN's long-range dependency |
| **Extension** | A adds new features based on B | BERT adds pre-training to Transformer |
| **Fusion** | C combines A and B | Graph CNN combines CNN and Graph Theory |
| **Comparison** | Methods compared in experiments | Indicates competing technical routes |

### Relationship Record Format

```
Literature X ←→ Literature Y: [Relationship Type]
- Brief explanation of the relationship
```

---

## Critical Analysis Dimensions

Analyze each technical route category from six dimensions:

### 1. Assumptions

**What to examine**:
- What prerequisites are necessary for the method to work?
- Are these assumptions reasonable in real scenarios?
- What are the consequences of violating assumptions?

**Why it matters**: Assumptions determine the boundary conditions where a method is valid.

### 2. Core Advantages

**What to examine**:
- What are the core advantages compared to other methods?
- Where are the innovations?
- What key problems does it solve?

**Why it matters**: Understanding advantages helps identify when to use this method.

### 3. Limitations

**What to examine**:
- What is the computational complexity?
- What are the data quality requirements?
- In which scenarios does it perform poorly?

**Why it matters**: Limitations define where the method should NOT be used.

### 4. Applicability

**What to examine**:
- What types of problems/data does it apply to?
- What are the scale limitations?
- How is domain adaptability?

**Why it matters**: Applicability determines if the method fits the target problem.

### 5. Practical Challenges

**What to examine**:
- What are the engineering implementation challenges?
- What resource support is needed (compute, memory, data)?
- What are the deployment and maintenance challenges?

**Why it matters**: Practical challenges affect real-world adoption.

### 6. Relevance

**What to examine**:
- Which aspect of the target problem does the method directly solve?
- How similar is the research scenario to the target problem?
- What is the transferability of results?

**Why it matters**: Relevance determines if the method is applicable to the user's specific problem.

---

## Performance Comparison

### Performance Metrics to Collect

#### Accuracy Metrics
- Precision, Recall, F1 Score
- Accuracy, Error Rate
- Domain-specific metrics (mAP, BLEU, PSNR, etc.)

#### Efficiency Metrics
- Time complexity (Big O notation)
- Actual running time (training/inference)
- Space complexity (memory usage)
- Parameter count, FLOPs

#### Robustness Metrics
- Noise resistance capability
- Sensitivity to outliers
- Generalization ability (cross-dataset performance)

#### Practicality Metrics
- Implementation difficulty
- Interpretability
- Scalability

### Weighted Ranking Method

1. **Clarify Problem Requirements**
   - Real-time application → efficiency has higher weight
   - Safety-critical → accuracy has higher weight
   - Resource-constrained → resource consumption has higher weight

2. **Build Scoring Matrix**
   ```
   Technical Route | Metric1 (w1) | Metric2 (w2) | ... | Composite Score
   ----------------|--------------|--------------|-----|----------------
   Route A         |     sA1      |     sA2      | ... |   Σ(wi×si)
   Route B         |     sB1      |     sB2      | ... |   Σ(wi×si)
   ```

3. **Normalize Scores**
   - Normalize each metric to [0,1] interval
   - Distinguish "higher is better" vs "lower is better" metrics

4. **Calculate Composite Score and Rank**

---

## Analysis Output Format

For each technical route category, produce:

1. **Method Principles** (1-2 paragraphs)
   - Core idea
   - Mathematical model or algorithm (if applicable)
   - Key technical points

2. **Representative Literature** (2-3 papers)
   - Status in this technical route (groundbreaking/improvement/summary)
   - Specific contributions
   - Performance data

3. **Evolution Lineage**
   - Chronological development
   - Key turning points and breakthroughs
   - Current research trends

4. **Critical Analysis** (six dimensions)
   - Assumptions: Are they reasonable?
   - Advantages: What makes it stand out?
   - Limitations: What constraints exist?
   - Applicability: When to use it?
   - Challenges: What's hard to implement?
   - Relevance: Does it solve the target problem?
