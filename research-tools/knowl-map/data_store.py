import json
import os
from typing import Dict, List, Optional, Any

class KnowledgeGraphStore:
    """Handles reading and writing the knowledge dependency graph."""
    
    def __init__(self, file_path: str = "knowledge_graph.json"):
        self.file_path = file_path
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load data from JSON file, create if doesn't exist."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return self._get_default_data()
        else:
            return self._get_default_data()
    
    def _get_default_data(self) -> Dict[str, Any]:
        """Return default data structure with example entries."""
        return {
            "items": {
                "Quantum Phase Estimation": {
                    "type": "concept",
                    "prerequisites": [
                        {"name": "Quantum Fourier Transform", "type": "concept"},
                        {"name": "Phase Kickback", "type": "concept"},
                        {"name": "Quantum Measurement", "type": "concept"}
                    ]
                },
                "Quantum Fourier Transform": {
                    "type": "concept",
                    "prerequisites": [
                        {"name": "Classical Fourier Transform", "type": "concept"},
                        {"name": "Quantum Gates", "type": "concept"},
                        {"name": "Hadamard Gate", "type": "concept"}
                    ]
                },
                "Quantum Computation and Quantum Information": {
                    "type": "book",
                    "prerequisites": [
                        {"name": "Linear Algebra", "type": "concept"},
                        {"name": "Probability Theory", "type": "concept"},
                        {"name": "Basic Quantum Mechanics", "type": "concept"}
                    ]
                },
                "Linear Algebra": {
                    "type": "concept",
                    "prerequisites": [
                        {"name": "Basic Algebra", "type": "concept"},
                        {"name": "Matrix Operations", "type": "concept"}
                    ]
                },
                "Classical Fourier Transform": {
                    "type": "concept",
                    "prerequisites": [
                        {"name": "Complex Numbers", "type": "concept"},
                        {"name": "Integration", "type": "concept"}
                    ]
                }
            }
        }
    
    def save_data(self) -> None:
        """Save current data to JSON file."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def get_item(self, name: str) -> Optional[Dict[str, Any]]:
        """Get an item by name."""
        return self.data["items"].get(name)
    
    def get_all_items(self) -> Dict[str, Any]:
        """Get all items in the knowledge graph."""
        return self.data["items"]
    
    def add_item(self, name: str, item_type: str, prerequisites: List[Dict[str, str]]) -> None:
        """Add a new item to the knowledge graph."""
        self.data["items"][name] = {
            "type": item_type,
            "prerequisites": prerequisites
        }
        self.save_data()
    
    def get_prerequisites(self, name: str, recursive: bool = False) -> List[Dict[str, str]]:
        """Get prerequisites for an item, optionally recursive."""
        item = self.get_item(name)
        if not item:
            return []
        
        if not recursive:
            return item["prerequisites"]
        
        # Recursive prerequisites
        all_prereqs = []
        seen = set()
        
        def collect_prereqs(item_name: str) -> None:
            if item_name in seen:
                return
            seen.add(item_name)
            
            item_data = self.get_item(item_name)
            if item_data:
                for prereq in item_data["prerequisites"]:
                    if prereq["name"] not in seen:
                        all_prereqs.append(prereq)
                        collect_prereqs(prereq["name"])
        
        # Start with direct prerequisites
        for prereq in item["prerequisites"]:
            all_prereqs.append(prereq)
            collect_prereqs(prereq["name"])
        
        return all_prereqs
    
    def search_items(self, query: str) -> List[str]:
        """Search for items by name (case-insensitive partial match)."""
        query_lower = query.lower()
        matches = []
        
        for name in self.data["items"].keys():
            if query_lower in name.lower():
                matches.append(name)
        
        return matches 