# Knowledge Map Implementation

## Overview
A Python tool that allows users to explore topic prerequisites in a knowledge dependency graph. Users can search for topics, view their prerequisites (both direct and recursive), and add new entries to the knowledge base.

## Files Created

### `main.py`
- CLI interface with interactive menu
- Search functionality with fuzzy matching
- Option to view direct or recursive prerequisites
- Interactive entry addition
- Clean, formatted output with emoji icons

### `data_store.py`
- `KnowledgeGraphStore` class for data management
- JSON file persistence
- Search functionality
- Recursive prerequisite calculation
- Default data with quantum computing examples

### `knowledge_graph.json`
- Initial knowledge base with 23 interconnected concepts
- Focus on quantum computing and mathematics
- Hierarchical structure showing learning dependencies

## Features Implemented

✅ **Core Requirements:**
- User input for topics/papers/books
- JSON-based dependency database
- Item types: concept, paper, book
- Prerequisites with names and types

✅ **Extra Features:**
- Interactive entry addition
- Recursive prerequisite lookup
- Search functionality
- Clean, modular code structure

✅ **Future-Ready:**
- Extensible data structure
- Modular architecture
- Easy to add GUI or graph visualization

## Usage

```bash
cd knowl-map
python main.py
```

## Example Output
```
Prerequisites for 'Quantum Fourier Transform' (recursive):
--------------------------------------------------

📚 CONCEPTS:
  1. Classical Fourier Transform
  2. Complex Numbers
  3. Basic Algebra
  4. Integration
  5. Calculus
  6. Quantum Gates
  7. Linear Algebra
  8. Matrix Operations
  9. Hadamard Gate

Total prerequisites: 9
```

## Data Structure
Each item in the knowledge graph has:
- `name`: String identifier
- `type`: "concept", "paper", or "book"
- `prerequisites`: List of objects with `name` and `type`

The tool automatically handles circular dependencies and provides a clean learning path for any topic. 