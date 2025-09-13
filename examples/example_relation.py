#!/usr/bin/env python3
"""
Example of extracting child tables from array of objects.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import extract_child_table, extract_nested_relations

# Example 1: Simple array of objects
parent = {
    "id": 1,
    "name": "John",
    "orders": [
        {"order_id": 10, "amount": 100},
        {"order_id": 11, "amount": 200},
        {"order_id": 10, "amount": 100}  # duplicate
    ]
}

print("Example 1: Extract child table")
result = extract_child_table(parent, "orders", "user_id", remove_duplicates=True)
print("Main:", result["main"])
print("Child table:", result["child"])
print("Child table name:", result["child_table_name"])
print()

# Example 2: Nested relations
nested_obj = {
    "user_id": 1,
    "name": "Alice",
    "orders": [
        {
            "order_id": 100,
            "items": [
                {"item_id": 1, "name": "Book", "price": 20},
                {"item_id": 2, "name": "Pen", "price": 5}
            ]
        },
        {
            "order_id": 101,
            "items": [
                {"item_id": 3, "name": "Notebook", "price": 15}
            ]
        }
    ]
}

print("Example 2: Extract nested relations")
result = extract_nested_relations(nested_obj, fk_name="parent_id")
print("Main:", result["main"])
print("Relations:")
for table, records in result["relations"].items():
    print(f"  {table}: {records}")
print()
