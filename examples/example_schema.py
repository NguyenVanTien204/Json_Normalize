#!/usr/bin/env python3
"""
Example of schema and type handling.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import normalize_json, apply_type_casting, infer_schema
from utils.naming import normalize_keys
from utils.validation import validate_data

# Example 1: Type casting with schema
data = [
    {"name": "Alice", "age": "25", "salary": "50000.0", "active": "true", "birth_date": "1998-05-15"},
    {"name": "Bob", "age": "30", "salary": "60000", "active": "false", "birth_date": "1993-08-20"}
]

schema = {
    "age": "int",
    "salary": "float",
    "active": "bool",
    "birth_date": "date"
}

print("Example 1: Type casting with schema")
casted = apply_type_casting(data, schema)
print("Original:", data[0])
print("Casted:", casted[0])
print()

# Example 2: Key normalization
messy_data = [
    {"User-Name": "Alice", "User_Age": 25, "user.salary": 50000},
    {"User-Name": "Bob", "User_Age": 30, "user.salary": 60000}
]

print("Example 2: Key normalization")
normalized = normalize_keys(messy_data, 'snake')
print("Original keys:", list(messy_data[0].keys()))
print("Normalized keys:", list(normalized[0].keys()))
print()

# Example 3: Schema inference
sample_data = [
    {"id": 1, "name": "Alice", "score": 95.5, "active": True},
    {"id": 2, "name": "Bob", "score": 87.0, "active": False}
]

print("Example 3: Schema inference")
inferred_schema = infer_schema(sample_data)
print("Inferred schema:", inferred_schema)
print()

# Example 4: Full normalization with schema
complex_obj = {
    "user": {
        "full-name": "Charlie Brown",
        "age-str": "35",
        "is_active": "true",
        "join_date": "2020-01-15"
    },
    "scores": [85, 90, 88]
}

full_schema = {
    "user.age_str": "int",
    "user.is_active": "bool",
    "user.join_date": "date"
}

print("Example 4: Full normalization with schema and key convention")
result = normalize_json(complex_obj, schema=full_schema, key_convention='snake')
print("Result:", result)
print()

# Example 5: Validation
validation_schema = {
    "age": {"type": "int", "min": 0, "max": 120},
    "name": {"type": "str", "required": True},
    "score": {"type": "float", "min": 0, "max": 100}
}

test_records = [
    {"name": "Alice", "age": 25, "score": 95.5},
    {"name": "Bob", "age": 150, "score": 87.0},  # Invalid age
    {"age": 30, "score": 80.0}  # Missing name
]

print("Example 5: Validation")
validation_results = validate_data(test_records, validation_schema)
for i, result in enumerate(validation_results):
    print(f"Record {i+1}: Valid={result['valid']}, Errors={result['errors']}")
