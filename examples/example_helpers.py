#!/usr/bin/env python3
"""
Example of helper utilities and error handling.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import normalize_json
from utils.config import JsonNormalizeConfig, set_config, get_config
from utils.error_handler import create_error_summary
from utils.validation import validate_data
from core.dedup import deduplicate_records, find_duplicates

# Example 1: Configuration usage
print("Example 1: Configuration")
config = JsonNormalizeConfig(
    sep="_",
    explode_arrays=True,
    key_convention='camel',
    remove_duplicates=True,
    log_level='INFO'
)
print("Config:", config.to_dict())

# Example 2: Error handling and validation
data_with_errors = [
    {"name": "Alice", "age": 25, "score": 95},
    {"name": "Bob", "age": "invalid", "score": 87},  # Type error
    {"name": "Charlie", "age": 30},  # Missing score
    {"name": "Alice", "age": 25, "score": 95},  # Duplicate
]

schema = {
    "age": {"type": "int", "min": 0, "max": 120},
    "score": {"type": "float", "required": True},
    "name": {"type": "str", "required": True}
}

print("\nExample 2: Validation with error summary")
validation_results = validate_data(data_with_errors, schema)
error_summary = create_error_summary(validation_results)
print("Validation Summary:")
print(f"  Total records: {error_summary['total_records']}")
print(f"  Valid records: {error_summary['valid_records']}")
print(f"  Invalid records: {error_summary['invalid_records']}")
print(f"  Error types: {error_summary['error_types']}")

# Example 3: Deduplication
print("\nExample 3: Deduplication")
duplicates = find_duplicates(data_with_errors)
print("Found duplicates:")
for key, group in duplicates.items():
    print(f"  Group {key}: {len(group)} records")

deduped = deduplicate_records(data_with_errors)
print(f"Original count: {len(data_with_errors)}, Deduped count: {len(deduped)}")

# Example 4: Full normalization with config
complex_data = {
    "user": {
        "full-name": "Test User",
        "age-str": "28",
        "tags": ["python", "json", "test"]
    },
    "metadata": {
        "created_at": "2023-01-15",
        "version": 1.0
    }
}

full_schema = {
    "user.age_str": "int",
    "metadata.created_at": "date",
    "metadata.version": "float"
}

print("\nExample 4: Full normalization with custom config")
result = normalize_json(
    complex_data,
    schema=full_schema,
    config=config
)
print("Result:", result)

# Example 5: Global config update
print("\nExample 5: Global config update")
set_config(sep="__", key_convention='snake')
print("Updated global config sep:", get_config().sep)

print("\nAll examples completed successfully!")
