Create a tool in Python that allows users to input a topic, paper, or book, and outputs its prerequisites. Each prerequisite should be tagged as either a “concept” or a “paper.” The tool should be structured to allow future expansion (like visual graph rendering).

Requirements:
1. The user should be able to enter a title (e.g., “Quantum Phase Estimation” or “Quantum Computation and Quantum Information”).
2. The system should maintain a growing dependency database (in a JSON or YAML format).
3. Each item should have:
   - A name
   - Type: "paper", "book", or "concept"
   - List of prerequisites, each with its own name and type

Create three files:
- `main.py`: CLI that prompts user for a topic and lists its prerequisites.
- `data_store.py`: Handles reading/writing the dependency graph.
- `knowledge_graph.json`: Starts with a few hardcoded examples, and can grow over time.

Extra features (optional if time permits):
- Allow user to add new entries interactively.
- Handle recursive prerequisites (i.e., return all prerequisites of prerequisites).

Code should be clean, modular, and allow for future GUI or graph integration.
