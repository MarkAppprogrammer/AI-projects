#!/usr/bin/env python3
"""
Knowledge Map CLI - A tool for exploring topic prerequisites
"""

import sys
from typing import List, Dict
from data_store import KnowledgeGraphStore

def print_banner():
    """Print application banner."""
    print("=" * 60)
    print("           KNOWLEDGE MAP - Prerequisite Explorer")
    print("=" * 60)
    print()

def print_prerequisites(name: str, prerequisites: List[Dict[str, str]], recursive: bool = False):
    """Print prerequisites in a formatted way."""
    if not prerequisites:
        print(f"No prerequisites found for '{name}'")
        return
    
    print(f"\nPrerequisites for '{name}' ({'recursive' if recursive else 'direct'}):")
    print("-" * 50)
    
    # Group by type
    concepts = [p for p in prerequisites if p["type"] == "concept"]
    papers = [p for p in prerequisites if p["type"] == "paper"]
    books = [p for p in prerequisites if p["type"] == "book"]
    
    if concepts:
        print("\n📚 CONCEPTS:")
        for i, concept in enumerate(concepts, 1):
            print(f"  {i}. {concept['name']}")
    
    if papers:
        print("\n📄 PAPERS:")
        for i, paper in enumerate(papers, 1):
            print(f"  {i}. {paper['name']}")
    
    if books:
        print("\n📖 BOOKS:")
        for i, book in enumerate(books, 1):
            print(f"  {i}. {book['name']}")
    
    print(f"\nTotal prerequisites: {len(prerequisites)}")

def get_user_input(prompt: str) -> str:
    """Get user input with proper handling."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\nGoodbye!")
        sys.exit(0)

def add_new_entry(store: KnowledgeGraphStore):
    """Interactive function to add a new entry."""
    print("\n" + "=" * 40)
    print("ADD NEW ENTRY")
    print("=" * 40)
    
    # Get item name
    name = get_user_input("Enter the name of the item: ")
    if not name:
        print("Name cannot be empty.")
        return
    
    # Check if item already exists
    if store.get_item(name):
        print(f"Item '{name}' already exists in the knowledge graph.")
        return
    
    # Get item type
    print("\nItem types:")
    print("1. concept")
    print("2. paper") 
    print("3. book")
    
    type_choice = get_user_input("Select item type (1-3): ")
    type_map = {"1": "concept", "2": "paper", "3": "book"}
    
    if type_choice not in type_map:
        print("Invalid choice. Using 'concept' as default.")
        item_type = "concept"
    else:
        item_type = type_map[type_choice]
    
    # Get prerequisites
    prerequisites = []
    print(f"\nAdding prerequisites for '{name}' ({item_type})")
    print("Enter prerequisite names (press Enter twice to finish):")
    
    while True:
        prereq_name = get_user_input("Prerequisite name: ")
        if not prereq_name:
            break
        
        # Get prerequisite type
        print("Prerequisite types:")
        print("1. concept")
        print("2. paper")
        print("3. book")
        
        prereq_type_choice = get_user_input("Select prerequisite type (1-3): ")
        if prereq_type_choice not in type_map:
            print("Invalid choice. Using 'concept' as default.")
            prereq_type = "concept"
        else:
            prereq_type = type_map[prereq_type_choice]
        
        prerequisites.append({"name": prereq_name, "type": prereq_type})
    
    # Add the item
    store.add_item(name, item_type, prerequisites)
    print(f"\n✅ Successfully added '{name}' to the knowledge graph!")

def search_and_select(store: KnowledgeGraphStore) -> str:
    """Search for items and let user select one."""
    query = get_user_input("Enter search term: ")
    if not query:
        return ""
    
    matches = store.search_items(query)
    
    if not matches:
        print(f"No items found matching '{query}'")
        return ""
    
    if len(matches) == 1:
        return matches[0]
    
    print(f"\nFound {len(matches)} matches:")
    for i, match in enumerate(matches, 1):
        item = store.get_item(match)
        if item:
            print(f"  {i}. {match} ({item['type']})")
        else:
            print(f"  {i}. {match} (unknown type)")
    
    while True:
        choice = get_user_input(f"Select item (1-{len(matches)}): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(matches):
                return matches[index]
            else:
                print(f"Please enter a number between 1 and {len(matches)}")
        except ValueError:
            print("Please enter a valid number")

def main():
    """Main CLI loop."""
    store = KnowledgeGraphStore()
    
    print_banner()
    
    while True:
        print("\nOptions:")
        print("1. Search for prerequisites")
        print("2. Add new entry")
        print("3. List all items")
        print("4. Exit")
        
        choice = get_user_input("\nSelect option (1-4): ")
        
        if choice == "1":
            # Search for prerequisites
            selected_item = search_and_select(store)
            if selected_item:
                item = store.get_item(selected_item)
                if item:
                    print(f"\nFound: {selected_item} ({item['type']})")
                    
                    # Ask for recursive or direct prerequisites
                    recursive_choice = get_user_input("Show recursive prerequisites? (y/n): ").lower()
                    recursive = recursive_choice in ['y', 'yes']
                    
                    prerequisites = store.get_prerequisites(selected_item, recursive=recursive)
                    print_prerequisites(selected_item, prerequisites, recursive)
                else:
                    print(f"\nError: Item '{selected_item}' not found in database.")
        
        elif choice == "2":
            # Add new entry
            add_new_entry(store)
        
        elif choice == "3":
            # List all items
            items = store.get_all_items()
            if not items:
                print("No items in the knowledge graph.")
            else:
                print(f"\nAll items ({len(items)} total):")
                print("-" * 40)
                for name, data in items.items():
                    prereq_count = len(data["prerequisites"])
                    print(f"• {name} ({data['type']}) - {prereq_count} prerequisites")
        
        elif choice == "4":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main() 