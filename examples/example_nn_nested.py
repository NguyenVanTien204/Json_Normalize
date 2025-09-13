#!/usr/bin/env python3
"""
Example of handling N-N relationships and nested arrays.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import extract_junction_table, flatten_nested_array, normalize_json

# Example 1: N-N relationship with junction table
student = {
    "student_id": 1,
    "name": "Alice",
    "courses": [101, 102, 103]
}

print("Example 1: Extract junction table for N-N")
result = extract_junction_table(student, "courses", "student_id", "course_id")
print("Main:", result["main"])
print("Junction:", result["junction"])
print("Junction table name:", result["junction_table_name"])
print()

# Example 2: Flatten nested array
nested_arr = [[1, 2], [3, 4], 5]
print("Example 2: Flatten nested array")
flattened = flatten_nested_array(nested_arr, "flat")
print("Original:", nested_arr)
print("Flattened:", flattened)
print()

# Example 3: Normalize JSON with nested arrays
obj_with_nested = {
    "user": "Bob",
    "matrix": [[1, 2], [3, 4]],
    "tags": ["a", "b"]
}

print("Example 3: Normalize with nested array flattening")
result = normalize_json(obj_with_nested, flatten_nested=True)
print("Result:", result)
print()

# Example 4: Complex N-N with nested
complex_obj = {
    "student_id": 2,
    "courses": [201, 202],
    "details": {
        "grades": [[85, 90], [88, 92]]
    }
}

print("Example 4: Complex object with N-N and nested arrays")
# First extract junction
junction_result = extract_junction_table(complex_obj, "courses", "student_id", "course_id")
print("After junction extraction:")
print("Main:", junction_result["main"])
print("Junction:", junction_result["junction"])

# Then normalize the main
normalized = normalize_json(junction_result["main"], flatten_nested=True)
print("Normalized main:", normalized)
