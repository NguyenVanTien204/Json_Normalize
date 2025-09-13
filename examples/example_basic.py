#!/usr/bin/env python3
"""
Basic example of using the JSON Normalize module.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import normalize_json, normalize_nulls

# Example 1: Flatten nested object
nested_obj = {
    "user": {
        "name": "John",
        "address": {
            "street": "123 Main St",
            "city": "Anytown"
        }
    },
    "age": 30
}

print("Example 1: Flatten nested object")
result = normalize_json(nested_obj)
print(result)
print()

# Example 2: Explode primitive array
obj_with_array = {
    "user": "John",
    "tags": ["python", "json", "normalize"]
}

print("Example 2: Explode primitive array")
result = normalize_json(obj_with_array, explode_arrays=True)
print(result)
print()

# Example 3: With nulls and missing fields
data = [
    {"name": "Alice", "age": 25, "city": "NYC"},
    {"name": "Bob", "age": None, "country": "USA"},
    {"name": "Charlie", "city": "LA"}
]

print("Example 3: Normalize nulls and missing fields")
result = normalize_nulls(data)
print(result)
