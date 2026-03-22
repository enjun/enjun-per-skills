# Literature Search Strategies

This document details the literature search and information collection strategies for technical route research.

## Table of Contents

1. [Bib File Collection](#bib-file-collection)
2. [Zotero Search Strategies](#zotero-search-strategies)
3. [Literature Information Extraction](#literature-information-extraction)

---

## Bib File Collection

When the user provides a `.bib` file:

1. **Extract Entries**: Read the bib file and extract all literature entries
2. **Record Metadata**: For each entry, record:
   - Title
   - Author(s)
   - Year
   - Journal/Conference
3. **Cross-Reference with Zotero**: Use literature titles as keywords to search complete content in Zotero

---

## Zotero Search Strategies

Use the following strategies in priority order:

### Strategy A: Semantic Search (Preferred)

**Tool**: `mcp__zotero-mcp__zotero_semantic_search`

**Why Use It**: Semantic search understands the essence of a research problem and finds conceptually similar literature, even when keywords don't exactly match.

**Parameters**:
- `query`: Literature title or problem keywords
- `limit`: 20-50 (get sufficient relevant results)
- `filters` (optional): Filter by item type, tags, etc.

**Example**:
```json
{
  "query": "deep learning for image segmentation",
  "limit": 30
}
```

---

### Strategy B: Advanced Search (Alternative)

**Tool**: `mcp__zotero-mcp__zotero_advanced_search`

**Why Use It**: When you need precise multi-condition filtering, such as combining title keywords with date ranges.

**Parameters**:
- `conditions`: Array of search conditions
  - `condition`: Field name ("title", "year", "creator")
  - `operator`: Comparison operator ("contains", "isInLast", "equals")
  - `value`: Search value
- `join_mode`: "all" (AND) or "any" (OR)
- `sort_by`: Field to sort by
- `sort_direction`: "asc" or "desc"
- `limit`: Maximum results

**Example**:
```json
{
  "conditions": [
    {"condition": "title", "operator": "contains", "value": "neural network"},
    {"condition": "year", "operator": "isInLast", "value": "10"}
  ],
  "join_mode": "all",
  "limit": 50
}
```

---

### Strategy C: Tag Search (Supplementary)

**Tool**: `mcp__zotero-mcp__zotero_search_by_tag`

**Why Use It**: When literature tags are known and you want to filter by specific research areas or method categories.

**Parameters**:
- `tag`: Array of tag names (supports `||` for OR, `-` for exclusion)
- `item_type`: Default "-attachment" (exclude attachments)
- `limit`: Maximum results

**Example**:
```json
{
  "tag": ["deep-learning", "computer-vision"],
  "limit": 20
}
```

---

## Literature Information Extraction

For each relevant literature found, extract detailed information using the following tools:

### Get Metadata

**Tool**: `mcp__zotero-mcp__zotero_get_item_metadata`

**Parameters**:
- `item_key`: Unique identifier of the literature
- `format`: "markdown" (default) or "bibtex"
- `include_abstract`: true (default)

**What You Get**:
- Title, authors, year
- Abstract
- Keywords/tags
- Publication venue

---

### Get Notes (Critical!)

**Tool**: `mcp__zotero-mcp__zotero_get_notes`

**Parameters**:
- `item_key`: Literature identifier
- `limit`: 20 (default)
- `truncate`: true (default)

**Why This Is Critical**: Notes are often where researchers record:
- Method descriptions
- Key insights
- Comparison with other methods
- Implementation details

**Best Practice**: Always read notes first—they're a goldmine for technical route information.

---

### Get Child Items

**Tool**: `mcp__zotero-mcp__zotero_get_item_children`

**Parameters**:
- `item_key`: Literature identifier

**What You Get**:
- PDF attachments
- Supplementary notes
- Linked files

**Use For**: Check if there are highlighted notes in PDF attachments.

---

### Get Full Text (When Needed)

**Tool**: `mcp__zotero-mcp__zotero_get_item_fulltext`

**Parameters**:
- `item_key`: Literature identifier

**When to Use**: Only when note and abstract information is insufficient for deep analysis.

**Note**: This retrieves the full text content, which can be large. Use judiciously.

---

## Search Workflow Summary

1. Start with **semantic search** for broad coverage
2. Use **advanced search** to refine by date, author, or specific keywords
3. Use **tag search** to filter by domain or method category
4. For each relevant result:
   - Get metadata (for overview)
   - Get notes (for method details—priority!)
   - Get child items (for PDF highlights)
   - Get full text (only if needed)
