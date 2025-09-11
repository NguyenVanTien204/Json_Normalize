# JSON Normalize

A comprehensive Python library for normalizing complex JSON data structures into flat, relational formats. Supports flattening nested objects, handling arrays, t## Documentation

- **[User Guide](docs/User_Guide.md)**: Comprehensive guide with examples and best practices
- **[API Reference](docs/API_Reference.md)**: Complete API documentation
- **[Core Module](docs/Core_Module.md)**: Detailed core functionality documentation
- **[Utils Module](docs/Utils_Module.md)**: Utilities and helper functions
- **[Contributing](CONTRIBUTING.md)**: Development guidelines
- **[Changelog](CHANGELOG.md)**: Version history and changes

## Project Structure

```
json-normalize/
├── json_normalize/          # Main package
│   ├── __init__.py         # Package initialization
│   ├── core/               # Core functionality
│   │   ├── __init__.py
│   │   ├── flattener.py    # Dictionary flattening
│   │   ├── null_handler.py # Null value handling
│   │   ├── transformer.py  # Main transformation logic
│   │   ├── relation.py     # Relationship extraction
│   │   ├── type_cast.py    # Type casting
│   │   └── dedup.py        # Deduplication
│   └── utils/              # Utilities
│       ├── __init__.py
│       ├── config.py       # Configuration management
│       ├── naming.py       # Key naming conventions
│       ├── validation.py   # Data validation
│       └── error_handler.py # Error handling
├── examples/               # Usage examples
├── tests/                  # Test suite
├── docs/                   # Documentation
├── requirements.txt        # Dependencies
├── README.md              # This file
├── CONTRIBUTING.md        # Contributing guidelines
├── CHANGELOG.md           # Version history
└── LICENSE                # License information
```ng, schema validation, and more.

## Features

- **🔄 Nested Object Flattening**: Convert deep nested JSON to flat key-value pairs
- **📊 Array Handling**: Support for primitive arrays, object arrays, and nested arrays
- **🔗 Relationship Extraction**: Automatically extract nested arrays of objects into separate relational tables with foreign keys
- **🎯 Type Casting**: Automatic type conversion with schema support
- **🔧 Key Normalization**: Convert keys to snake_case, camelCase, or custom formats
- **✅ Data Validation**: Schema-based validation with detailed error reporting
- **🗑️ Deduplication**: Remove duplicates globally or per table
- **📈 Multiple Output Formats**: Support for list, DataFrame, and relational (main + relations) formats
- **⚙️ Configurable Processing**: Extensive configuration options for all transformation steps
- **⚙️ Configurable**: Extensive configuration options for all behaviors
- **🚨 Error Handling**: Comprehensive error handling with logging
- **📈 Output Formats**: Support for list[dict], pandas DataFrame, and more

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/json-normalize.git
cd json-normalize

# Install dependencies (if any)
pip install -r requirements.txt
```

## Quick Start

```python
from json_normalize import normalize_json

# Simple nested object
data = {
    "user": {
        "name": "John",
        "address": {
            "street": "123 Main St",
            "city": "Anytown"
        }
    },
    "age": 30
}

# Normalize with default settings
result = normalize_json(data)
print(result)
# Output: [{'user.name': 'John', 'user.address.street': '123 Main St', 'user.address.city': 'Anytown', 'age': 30}]

# Complex data with nested arrays (relational extraction)
complex_data = {
    "movie": "Fight Club",
    "genres": [{"id": 18, "name": "Drama"}],
    "production_companies": [
        {"id": 711, "name": "Fox 2000 Pictures"},
        {"id": 508, "name": "Regency Enterprises"}
    ]
}

# Extract relations into separate tables
result = normalize_json(complex_data, output_format="relational")
print("Main:", result["main"])
print("Relations:", list(result["relations"].keys()))
# Output: Main record with flattened fields, Relations: ['genres_table', 'production_companies_table']
```

## Core Functions

### `normalize_json(obj, **options)`

The main entry point for JSON normalization with comprehensive options.

**Parameters:**
- `obj` (dict): The JSON object to normalize
- `sep` (str): Separator for flattened keys (default: ".")
- `explode_arrays` (bool): Whether to explode primitive arrays (default: False)
- `flatten_nested` (bool): Whether to flatten nested arrays (default: False)
- `schema` (dict): Schema for type casting
- `key_convention` (str): Key naming convention ('snake', 'camel', 'keep')
- `output_format` (str): Output format ('list', 'dataframe', 'relational')
- `config`: Configuration object
- `extract_relations` (bool): Whether to extract nested relations (default: True)
- `fk_name` (str): Foreign key name for extracted relations (default: "parent_id")

**Returns:** List of normalized records, pandas DataFrame, or dict with 'main' and 'relations'

### `extract_child_table(parent, field, fk_name, remove_duplicates=False)`

Extract array of objects into a separate child table.

**Parameters:**
- `parent` (dict): Parent object containing the array
- `field` (str): Field name of the array
- `fk_name` (str): Foreign key name for child records
- `remove_duplicates` (bool): Whether to remove duplicate child records

**Returns:** Dict with 'main', 'child', and 'child_table_name'

### `extract_junction_table(parent, field, fk_name, ref_name, remove_duplicates=False)`

Extract array of references into a junction table for N-N relationships.

**Parameters:**
- `parent` (dict): Parent object containing the array
- `field` (str): Field name of the reference array
- `fk_name` (str): Foreign key name for parent
- `ref_name` (str): Foreign key name for references
- `remove_duplicates` (bool): Whether to remove duplicate junctions

**Returns:** Dict with 'main', 'junction', and 'junction_table_name'

## Advanced Usage

### Configuration

```python
from json_normalize import JsonNormalizeConfig, normalize_json

config = JsonNormalizeConfig(
    sep="_",
    explode_arrays=True,
    key_convention='snake',
    remove_duplicates=True,
    log_level='DEBUG'
)

result = normalize_json(data, config=config)
```

### Schema and Type Casting

```python
schema = {
    "age": "int",
    "salary": "float",
    "is_active": "bool",
    "birth_date": "date"
}

result = normalize_json(data, schema=schema)
```

### Relationship Extraction

```python
from json_normalize import extract_nested_relations

complex_data = {
    "user_id": 1,
    "orders": [
        {"order_id": 100, "items": [{"name": "Book"}, {"name": "Pen"}]},
        {"order_id": 101, "items": [{"name": "Notebook"}]}
    ]
}

relations = extract_nested_relations(complex_data)
print(relations['main'])  # Main user record
print(relations['relations'])  # All extracted tables
```

### Validation

```python
from json_normalize import validate_data

validation_schema = {
    "age": {"type": "int", "min": 0, "max": 120},
    "name": {"type": "str", "required": True}
}

results = validate_data(records, validation_schema)
for result in results:
    if not result['valid']:
        print(f"Errors: {result['errors']}")
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `sep` | str | "." | Separator for flattened keys |
| `explode_arrays` | bool | False | Explode primitive arrays into multiple rows |
| `flatten_nested` | bool | False | Flatten nested arrays |
| `key_convention` | str | 'snake' | Key naming convention |
| `remove_duplicates` | bool | False | Remove duplicate records |
| `max_depth` | int | 10 | Maximum nesting depth |
| `error_handling` | str | 'warn' | Error handling strategy |
| `log_level` | str | 'INFO' | Logging level |

## Error Handling

The library provides comprehensive error handling:

- **Strategies**: 'raise', 'warn', 'skip'
- **Custom Exceptions**: `SchemaValidationError`, `TypeCastError`, `NestingDepthError`
- **Logging**: Detailed logs for debugging
- **Safe Operations**: Graceful handling of malformed data

## Examples

See the `examples/` directory for comprehensive examples:

- `example_basic.py`: Basic flattening and array handling
- `example_relation.py`: Relationship extraction
- `example_nn_nested.py`: N-N relationships and nested arrays
- `example_schema.py`: Schema and type handling
- `example_helpers.py`: Configuration and error handling

## API Reference

### Core Module

#### `flatten_dict(obj, sep=".", explode_arrays=False, flatten_nested=False)`
Flatten nested dictionary with array handling.

#### `normalize_nulls(data)`
Normalize null values and handle missing fields.

#### `apply_type_casting(data, schema)`
Apply type casting based on schema.

#### `normalize_keys(data, convention='snake')`
Normalize key names according to convention.

### Relations Module

#### `extract_nested_relations(obj, fk_name="parent_id", remove_duplicates=False)`
Recursively extract all nested relations.

#### `flatten_nested_array(arr, flatten_config="flat")`
Flatten nested arrays.

### Utils Module

#### `JsonNormalizeConfig(**options)`
Configuration class for all normalization options.

#### `validate_data(data, schema)`
Validate data against schema.

#### `deduplicate_records(records, key_fields=None, keep='first')`
Remove duplicate records.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Changelog

### v1.0.0
- Initial release with full JSON normalization capabilities
- Support for nested objects, arrays, relationships
- Schema validation and type casting
- Comprehensive configuration and error handling
