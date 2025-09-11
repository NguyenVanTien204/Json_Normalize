# JSON Normalize API Reference

## Core Module

### `flatten_dict(obj, sep=".", explode_arrays=False, flatten_nested=False)`

Flattens a nested dictionary into a flat structure with optional array handling.

**Parameters:**
- `obj` (dict): The nested dictionary to flatten
- `sep` (str): Separator for flattened keys (default: ".")
- `explode_arrays` (bool): If True, explode primitive arrays into multiple rows (default: False)
- `flatten_nested` (bool): If True, flatten nested arrays (default: False)

**Returns:**
- `list[dict]`: List of flattened dictionaries

**Example:**
```python
from json_normalize.core import flatten_dict

data = {"user": {"name": "John", "tags": ["a", "b"]}}
result = flatten_dict(data, explode_arrays=True)
# Output: [{'user.name': 'John', 'user.tags': 'a'}, {'user.name': 'John', 'user.tags': 'b'}]
```

### `normalize_nulls(data)`

Normalizes null values to None and adds missing fields with None.

**Parameters:**
- `data` (list[dict]): List of dictionaries to normalize

**Returns:**
- `list[dict]`: Normalized list of dictionaries with consistent fields

**Example:**
```python
from json_normalize.core import normalize_nulls

data = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "city": "NYC"}
]
result = normalize_nulls(data)
# Output: [
#     {"name": "Alice", "age": 25, "city": None},
#     {"name": "Bob", "age": None, "city": "NYC"}
# ]
```

### `normalize_json(obj, **kwargs)`

Main entry point for comprehensive JSON normalization.

**Parameters:**
- `obj` (dict): JSON object to normalize
- `sep` (str): Key separator (default: ".")
- `explode_arrays` (bool): Explode primitive arrays (default: False)
- `flatten_nested` (bool): Flatten nested arrays (default: False)
- `schema` (dict): Type casting schema
- `key_convention` (str): Key naming convention ('snake', 'camel', 'keep')
- `output_format` (str): Output format ('list', 'dataframe')
- `config`: Configuration object

**Returns:**
- `list[dict]` or `pandas.DataFrame`: Normalized data

**Example:**
```python
from json_normalize.core import normalize_json

data = {"user": {"full_name": "John", "age": "25"}}
schema = {"user.age": "int"}
result = normalize_json(data, schema=schema, key_convention='snake')
# Output: [{'user_full_name': 'John', 'user_age': 25}]
```

### `apply_type_casting(data, schema)`

Applies type casting to data based on schema.

**Parameters:**
- `data` (list[dict]): Data to cast
- `schema` (dict): Mapping of field names to target types

**Returns:**
- `list[dict]`: Data with casted values

**Supported Types:**
- 'int', 'float', 'str', 'bool', 'date', 'datetime'

### `infer_schema(data)`

Infers schema from data by analyzing value types.

**Parameters:**
- `data` (list[dict]): Data to analyze

**Returns:**
- `dict`: Inferred schema mapping field names to types

## Relations Module

### `extract_child_table(parent, field, fk_name, remove_duplicates=False)`

Extracts array of objects into a separate child table.

**Parameters:**
- `parent` (dict): Parent object containing the array
- `field` (str): Field name of the array
- `fk_name` (str): Foreign key name for child records
- `remove_duplicates` (bool): Remove duplicate child records

**Returns:**
- `dict`: Contains 'main', 'child', 'child_table_name'

**Example:**
```python
from json_normalize.core import extract_child_table

parent = {"id": 1, "orders": [{"order_id": 100}, {"order_id": 101}]}
result = extract_child_table(parent, "orders", "user_id")
# Output: {
#     "main": {"id": 1},
#     "child": [{"user_id": 1, "order_id": 100}, {"user_id": 1, "order_id": 101}],
#     "child_table_name": "orders_table"
# }
```

### `extract_junction_table(parent, field, fk_name, ref_name, remove_duplicates=False)`

Extracts array of references into a junction table for N-N relationships.

**Parameters:**
- `parent` (dict): Parent object containing reference array
- `field` (str): Field name of the reference array
- `fk_name` (str): Foreign key name for parent
- `ref_name` (str): Foreign key name for references
- `remove_duplicates` (bool): Remove duplicate junctions

**Returns:**
- `dict`: Contains 'main', 'junction', 'junction_table_name'

**Example:**
```python
from json_normalize.core import extract_junction_table

parent = {"student_id": 1, "courses": [101, 102]}
result = extract_junction_table(parent, "courses", "student_id", "course_id")
# Output: {
#     "main": {"student_id": 1},
#     "junction": [
#         {"student_id": 1, "course_id": 101},
#         {"student_id": 1, "course_id": 102}
#     ],
#     "junction_table_name": "courses_junction"
# }
```

### `extract_nested_relations(obj, fk_name="parent_id", remove_duplicates=False)`

Recursively extracts all nested relations from an object.

**Parameters:**
- `obj` (dict): Object to process
- `fk_name` (str): Foreign key name for relations
- `remove_duplicates` (bool): Remove duplicates from relations

**Returns:**
- `dict`: Contains 'main' and 'relations' dict

### `flatten_nested_array(arr, flatten_config="flat")`

Flattens nested arrays.

**Parameters:**
- `arr` (list): Nested array to flatten
- `flatten_config` (str): Flattening strategy ('flat', 'keep')

**Returns:**
- `list`: Flattened array

## Utils Module

### Configuration

#### `JsonNormalizeConfig(**kwargs)`

Configuration class for normalization options.

**Parameters:**
- `sep` (str): Key separator
- `explode_arrays` (bool): Explode primitive arrays
- `flatten_nested` (bool): Flatten nested arrays
- `key_convention` (str): Key naming convention
- `remove_duplicates` (bool): Remove duplicates
- `max_depth` (int): Maximum nesting depth
- `error_handling` (str): Error handling strategy
- `log_level` (str): Logging level

**Methods:**
- `update(**kwargs)`: Update configuration
- `to_dict()`: Convert to dictionary

#### `get_config()`

Get the global default configuration.

**Returns:**
- `JsonNormalizeConfig`: Global configuration instance

#### `set_config(**kwargs)`

Update the global default configuration.

### Naming

#### `normalize_keys(data, convention='snake')`

Normalize key names in data.

**Parameters:**
- `data` (list[dict]): Data to normalize
- `convention` (str): Naming convention ('snake', 'camel', 'keep')

**Returns:**
- `list[dict]`: Data with normalized keys

#### `to_snake_case(s)`

Convert string to snake_case.

#### `to_camel_case(s)`

Convert string to camelCase.

#### `clean_special_chars(s)`

Remove special characters from string.

### Validation

#### `validate_data(data, schema)`

Validate data against schema.

**Parameters:**
- `data` (list[dict]): Data to validate
- `schema` (dict): Validation schema

**Returns:**
- `list[dict]`: Validation results for each record

#### `validate_record(record, schema)`

Validate a single record.

**Schema Format:**
```python
schema = {
    "field_name": {
        "type": "int",  # Required: data type
        "required": True,  # Optional: field is required
        "min": 0,  # Optional: minimum value
        "max": 100,  # Optional: maximum value
        "choices": ["A", "B"]  # Optional: allowed values
    }
}
```

#### `filter_valid_records(data, schema)`

Filter only valid records from data.

### Error Handling

#### `handle_error(error, context='', strategy=None)`

Handle errors based on configured strategy.

**Parameters:**
- `error` (Exception): Exception that occurred
- `context` (str): Context information
- `strategy` (str): Error handling strategy ('raise', 'warn', 'skip')

#### `safe_type_cast(value, target_type, context='')`

Safely cast value with error handling.

#### `validate_nesting_depth(depth, context='')`

Validate nesting depth doesn't exceed maximum.

#### `log_processing_step(step, details=None)`

Log a processing step with details.

#### `create_error_summary(errors)`

Create summary of validation errors.

**Returns:**
- `dict`: Summary with counts and error details

### Deduplication

#### `deduplicate_records(records, key_fields=None, keep='first')`

Remove duplicate records.

**Parameters:**
- `records` (list[dict]): Records to deduplicate
- `key_fields` (list): Fields to use as deduplication key
- `keep` (str): Which duplicate to keep ('first', 'last')

**Returns:**
- `list[dict]`: Deduplicated records

#### `deduplicate_relations(relations, dedup_rules=None)`

Deduplicate records in relations.

**Parameters:**
- `relations` (dict): Relations dictionary
- `dedup_rules` (dict): Deduplication rules per table

**Returns:**
- `dict`: Relations with deduplicated records

#### `find_duplicates(records, key_fields=None)`

Find duplicate records.

**Returns:**
- `dict`: Groups of duplicate records

#### `merge_duplicates(records, key_fields, merge_strategy=None)`

Merge duplicate records.

**Parameters:**
- `merge_strategy` (callable): Function to merge a group of records

## Exceptions

### `JsonNormalizeError`

Base exception for JSON normalization errors.

### `SchemaValidationError`

Exception for schema validation errors.

### `TypeCastError`

Exception for type casting errors.

### `NestingDepthError`

Exception for excessive nesting depth.

## Examples

See the `examples/` directory for comprehensive usage examples covering all functionality.
