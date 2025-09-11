# JSON Normalize User Guide

## Overview

JSON Normalize is a comprehensive Python library designed to transform complex, nested JSON data structures into normalized, relational formats. Whether you're dealing with API responses, configuration files, or database exports, this library provides powerful tools to flatten, validate, and restructure your data.

## Getting Started

### Installation

```bash
git clone <repository-url>
cd json-normalize
pip install -r requirements.txt
```

### Basic Usage

```python
from json_normalize import normalize_json

# Your complex JSON data
data = {
    "user": {
        "name": "John Doe",
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "country": "USA"
        },
        "tags": ["developer", "python", "json"]
    },
    "metadata": {
        "created_at": "2023-01-15",
        "version": "1.0"
    }
}

# Normalize it
result = normalize_json(data)
print(result)
```

## Core Concepts

### 1. Flattening

The library's primary function is to flatten nested JSON structures into flat key-value pairs.

```python
# Nested structure
{
    "user": {
        "name": "John",
        "address": {
            "street": "123 Main St"
        }
    }
}

# Becomes
{
    "user.name": "John",
    "user.address.street": "123 Main St"
}
```

### 2. Array Handling

JSON Normalize provides flexible options for handling arrays:

- **Primitive Arrays**: `["a", "b", "c"]`
- **Object Arrays**: `[{"id": 1}, {"id": 2}]`
- **Nested Arrays**: `[[1, 2], [3, 4]]`

### 3. Relationships

Extract complex relationships into separate tables:

- **1-N Relationships**: Parent with array of child objects
- **N-N Relationships**: Junction tables for many-to-many relationships

### 4. Schema and Validation

Define schemas for type casting and validation:

```python
schema = {
    "age": "int",
    "salary": "float",
    "is_active": "bool",
    "birth_date": "date"
}

validation_schema = {
    "age": {"type": "int", "min": 0, "max": 120},
    "name": {"type": "str", "required": True}
}
```

## Advanced Features

### Configuration

Use the `JsonNormalizeConfig` class for fine-grained control:

```python
from json_normalize import JsonNormalizeConfig, normalize_json

config = JsonNormalizeConfig(
    sep="_",  # Use underscore instead of dot
    explode_arrays=True,  # Explode primitive arrays
    key_convention='camel',  # Convert keys to camelCase
    remove_duplicates=True,  # Remove duplicate records
    log_level='DEBUG'  # Detailed logging
)

result = normalize_json(data, config=config)
```

### Error Handling

The library provides comprehensive error handling:

```python
from json_normalize import JsonNormalizeConfig

config = JsonNormalizeConfig(
    error_handling='warn',  # Options: 'raise', 'warn', 'skip'
    max_depth=10  # Prevent infinite recursion
)

# Errors are logged and handled according to strategy
result = normalize_json(data, config=config)
```

### Deduplication

Remove duplicates at various levels:

```python
from json_normalize import deduplicate_records

# Remove duplicates based on specific fields
deduplicated = deduplicate_records(records, key_fields=['name', 'email'])

# Or remove exact duplicates
deduplicated = deduplicate_records(records)
```

## Use Cases

### 1. API Data Processing

```python
# Process API response with nested data
api_response = {
    "users": [
        {
            "id": 1,
            "profile": {"name": "John", "email": "john@example.com"},
            "posts": [{"title": "Hello", "content": "World"}]
        }
    ]
}

# Extract relationships
from json_normalize import extract_nested_relations
relations = extract_nested_relations(api_response)
```

### 2. Database Migration

```python
# Convert nested JSON to relational format
nested_data = {
    "company": {
        "departments": [
            {
                "name": "Engineering",
                "employees": [
                    {"name": "Alice", "role": "Developer"},
                    {"name": "Bob", "role": "Manager"}
                ]
            }
        ]
    }
}

# Normalize for database insertion
normalized = normalize_json(nested_data, explode_arrays=True)
```

### 3. Data Validation Pipeline

```python
from json_normalize import validate_data, apply_type_casting

# Define schema
schema = {
    "user.age": "int",
    "user.salary": "float",
    "user.is_active": "bool"
}

# Validate and cast
validation_results = validate_data(data, schema)
casted_data = apply_type_casting(data, schema)
```

## Best Practices

### 1. Configuration Management

```python
# Create reusable configurations
default_config = JsonNormalizeConfig(
    key_convention='snake',
    error_handling='warn'
)

api_config = JsonNormalizeConfig(
    explode_arrays=True,
    flatten_nested=True
)
```

### 2. Schema Definition

```python
# Define comprehensive schemas
user_schema = {
    "id": "int",
    "name": "str",
    "email": "str",
    "age": "int",
    "is_active": "bool",
    "created_at": "datetime"
}

# Use for both casting and validation
casted = apply_type_casting(data, user_schema)
validated = validate_data(data, user_schema)
```

### 3. Error Handling

```python
# Set up proper error handling
config = JsonNormalizeConfig(
    error_handling='warn',
    log_level='INFO'
)

try:
    result = normalize_json(data, config=config)
except Exception as e:
    print(f"Normalization failed: {e}")
```

### 4. Performance Considerations

```python
# For large datasets, consider:
config = JsonNormalizeConfig(
    remove_duplicates=True,  # Reduce data size
    max_depth=5,  # Limit nesting
    error_handling='skip'  # Skip problematic records
)
```

## Troubleshooting

### Common Issues

1. **Memory Errors**: Reduce `max_depth` or use streaming for large files
2. **Type Casting Failures**: Check schema definitions and data types
3. **Key Conflicts**: Use different `sep` values or `key_convention`
4. **Performance**: Enable deduplication and adjust logging level

### Debugging

```python
# Enable detailed logging
config = JsonNormalizeConfig(log_level='DEBUG')

# Check intermediate results
flattened = flatten_dict(data)
validated = validate_data(flattened, schema)
```

## Integration Examples

### With Pandas

```python
import pandas as pd
from json_normalize import normalize_json

# Normalize to DataFrame
df = normalize_json(data, output_format='dataframe')

# Further processing
df['processed_column'] = df['original_column'].apply(lambda x: x.upper())
```

### With SQLAlchemy

```python
from sqlalchemy import create_engine, MetaData, Table
from json_normalize import extract_nested_relations

# Extract relations
relations = extract_nested_relations(data)

# Create tables dynamically
engine = create_engine('sqlite:///data.db')
metadata = MetaData()

for table_name, records in relations['relations'].items():
    if records:
        # Infer columns from first record
        columns = infer_table_columns(records[0])
        table = Table(table_name, metadata, *columns)
        table.create(engine)
```

### With FastAPI

```python
from fastapi import FastAPI, HTTPException
from json_normalize import normalize_json, validate_data

app = FastAPI()

@app.post("/normalize")
async def normalize_endpoint(data: dict, schema: dict = None):
    try:
        if schema:
            validation = validate_data([data], schema)
            if not validation[0]['valid']:
                raise HTTPException(status_code=400, detail=validation[0]['errors'])

        result = normalize_json(data, schema=schema)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Migration Guide

### From v0.x to v1.0

- Configuration moved to `JsonNormalizeConfig` class
- Error handling strategies changed
- Schema format updated for validation
- Some function signatures modified

### Compatibility

- Python 3.7+
- pandas (optional, for DataFrame output)
- No external dependencies for core functionality

## Contributing

See CONTRIBUTING.md for development guidelines and testing procedures.

## License

MIT License - see LICENSE file for details.
