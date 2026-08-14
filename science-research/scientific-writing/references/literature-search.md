# Literature Search with Zotero

This guide explains how to search your Zotero library for relevant literature, and how to work from a user-provided `.bib` file. It applies to all document types in this skill (research articles, survey papers, technical route reports, and article improvement).

## Table of Contents

1. [Bib File Collection](#bib-file-collection)
2. [Search Tools Overview](#search-tools-overview)
3. [Information Extraction](#information-extraction)
4. [Search Strategy for Wireless Communications](#search-strategy-for-wireless-communications)
5. [Wireless Communications Search Examples](#wireless-communications-search-examples)
6. [Extracting Key Information for Your Article](#extracting-key-information-for-your-article)
7. [Organizing Findings](#organizing-findings)
8. [Best Practices](#best-practices)

---

## Bib File Collection

When the user provides a `.bib` file (common for survey papers and technical route reports):

1. **Extract Entries**: Read the bib file and extract all literature entries
2. **Record Metadata**: For each entry, record:
   - Title
   - Author(s)
   - Year
   - Journal/Conference
3. **Cross-Reference with Zotero**: Use literature titles as keywords to search complete content in Zotero

---

## Search Tools Overview

The Zotero MCP integration provides multiple search methods, each suited for different purposes:

### 1. Semantic Search (Recommended for Exploratory Research)

**Tool**: `mcp__zotero-mcp__zotero_semantic_search`

Use semantic search when:
- Exploring a new research area
- Looking for papers on a general topic
- Unsure of exact keywords or tags
- Discovering related work across different terminology

**Why Use It**: Semantic search understands the essence of a research problem and finds conceptually similar literature, even when keywords don't exactly match.

**Example Usage**:
```
Query: "non-orthogonal multiple access in 6G networks"
Query: "beamforming for millimeter wave massive MIMO"
Query: "resource allocation in cognitive radio networks"
```

**Parameters**:
- `query`: Natural language description of your research topic
- `limit`: Number of results to return (default: 10)
- `filters` (optional): Filter by item type, tags, etc.

### 2. Advanced Search (For Precise Queries)

**Tool**: `mcp__zotero-mcp__zotero_advanced_search`

Use advanced search when:
- Searching for specific combinations of criteria
- Filtering by publication type, year, or author
- Conducting systematic literature reviews

**Example Usage**:
```python
conditions = [
    {"field": "title", "condition": "contains", "value": "NOMA"},
    {"field": "year", "condition": "isGreaterThan", "value": "2020"},
    {"field": "publicationTitle", "condition": "contains", "value": "IEEE"}
]
```

**Parameters**:
- `conditions`: List of search criteria
- `join_mode`: "all" (AND) or "any" (OR)
- `sort_by`: Field to sort by
- `sort_direction`: "asc" or "desc"
- `limit`: Maximum number of results

### 3. Tag Search (For Organized Collections)

**Tool**: `mcp__zotero-mcp__zotero_search_by_tag`

Use tag search when:
- Your library uses consistent tagging
- Looking for papers in a specific category
- Filtering by research methodology or topic

**Example Usage**:
```
Tags: ["6G", "massive-MIMO", "beamforming"]
Tags: ["resource-allocation", "optimization"]
```

**Parameters**:
- `tag`: Array of tag names (supports `||` for OR, `-` for exclusion)
- `item_type`: Default "-attachment" (exclude attachments)
- `limit`: Maximum results

---

## Information Extraction

After finding relevant papers, extract key information using these tools:

### Get Metadata

**Tool**: `mcp__zotero-mcp__zotero_get_item_metadata`

Extracts:
- Title, authors, publication year
- Journal/conference name
- DOI, ISBN, ISSN
- Abstract (if available)
- Tags and collections

**Parameters**:
- `item_key`: Unique identifier of the literature
- `format`: "markdown" (default) or "bibtex"
- `include_abstract`: true (default)

### Get Notes (Critical for Your Research)

**Tool**: `mcp__zotero-mcp__zotero_get_notes`

Notes often contain:
- Key findings and contributions
- Method summaries
- Your personal annotations
- Connection to other papers

**Parameters**:
- `item_key`: Literature identifier
- `limit`: 20 (default)
- `truncate`: true (default)

**Why This Is Critical**: Notes are where researchers record method descriptions, key insights, comparisons with other methods, and implementation details. Always read notes first — they're a goldmine for technical route information and paper context.

### Get Full Text

**Tool**: `mcp__zotero-mcp__zotero_get_item_fulltext`

Retrieves:
- Full PDF content (if indexed)
- Complete text for detailed analysis
- All figures, tables, and equations

**When to Use**: Only when note and abstract information is insufficient for deep analysis. This retrieves the full text content, which can be large — use judiciously.

### Get Child Items

**Tool**: `mcp__zotero-mcp__zotero_get_item_children`

Retrieves:
- Attached PDFs
- Supplementary materials
- Notes and annotations

**Use For**: Check if there are highlighted notes in PDF attachments.

---

## Search Strategy for Wireless Communications

### Phase 1: Broad Exploration

1. Start with semantic search using your research topic
2. Cast a wide net to understand the landscape
3. Identify key authors and venues
4. Note common terminology and concepts

**Example**:
```
Query: "intelligent reflecting surface assisted communication"
Limit: 20
```

### Phase 2: Focused Search

1. Use advanced search to filter by:
   - Publication year (last 5 years for active fields)
   - Top-tier venues (IEEE journals, conferences)
   - Specific authors or groups

2. Combine multiple conditions:
   - Title contains "NOMA" OR "non-orthogonal"
   - Year > 2020
   - Venue contains "IEEE" OR "Transactions"

### Phase 3: Deep Dive

1. For key papers, retrieve full text and notes
2. Extract detailed methodology and results
3. Identify references cited in key papers
4. Build citation network

---

## Wireless Communications Search Examples

### Topic: NOMA in 5G/6G

**Semantic Search Queries**:
- "non-orthogonal multiple access 5G"
- "power domain NOMA performance analysis"
- "NOMA with massive MIMO"
- "user pairing in NOMA systems"

**Advanced Search Conditions**:
```python
conditions = [
    {"field": "title", "condition": "contains", "value": "NOMA"},
    {"field": "year", "condition": "isGreaterThan", "value": "2019"}
]
```

### Topic: Millimeter Wave Communications

**Semantic Search Queries**:
- "millimeter wave beamforming"
- "mmWave channel modeling"
- "hybrid beamforming massive MIMO"
- "mmWave path loss models"

**Tag-Based Search**:
```
Tags: ["mmWave", "beamforming", "channel-modeling"]
```

### Topic: Resource Allocation

**Semantic Search Queries**:
- "resource allocation wireless networks"
- "power allocation optimization"
- "subcarrier allocation OFDMA"
- "energy efficiency resource allocation"

---

## Extracting Key Information for Your Article

For each relevant paper, extract:

### From Metadata
- Citation information (for bibliography)
- Publication venue and year
- Author names and affiliations

### From Abstract
- Research problem addressed
- Proposed solution/approach
- Key results and metrics
- Main contributions

### From Notes/Full Text
- System model and assumptions
- Mathematical formulation
- Algorithm details
- Simulation parameters
- Performance metrics and results
- Comparison with baseline methods

### From References
- Related prior work
- Key papers in the field
- Foundational concepts

---

## Organizing Findings

Create a structured summary for each paper:

```markdown
## Paper Title (Year)

**Authors**: [Author list]
**Venue**: [Journal/Conference]

### Problem
- What problem does this paper address?
- What are the limitations of prior work?

### Approach
- What is the key idea/contribution?
- What is the system model?
- What is the mathematical formulation?

### Results
- What are the key performance metrics?
- How does it compare to baselines?
- What are the main findings?

### Relevance to Your Work
- How does this relate to your research topic?
- What can you build upon?
- What gaps remain?
```

---

## Search Workflow Summary

1. Start with **semantic search** for broad coverage
2. Use **advanced search** to refine by date, author, or specific keywords
3. Use **tag search** to filter by domain or method category
4. For each relevant result:
   - Get metadata (for overview)
   - Get notes (for method details — priority!)
   - Get child items (for PDF highlights)
   - Get full text (only if needed)

---

## Best Practices

1. **Start Broad, Then Narrow**: Use semantic search first, then refine with advanced search
2. **Check Multiple Sources**: Don't rely on a single search method
3. **Verify Relevance**: Always read abstracts before including papers
4. **Track Citations**: Note which papers cite and are cited by key works
5. **Extract Key Metrics**: Focus on performance metrics relevant to your comparison
6. **Note Assumptions**: System model assumptions are crucial for fair comparison
7. **Organize by Theme**: Group papers by approach, technique, or application
