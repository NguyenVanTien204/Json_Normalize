# Core Module Documentation

## Overview

The `core` module contains the primary functionality for JSON normalization, including flattening, type casting, transformation, and deduplication.

## Functions

### `flatten_dict(obj, sep=".", explode_arrays=False, flatten_nested=False)`

**Purpose:** Flattens nested dictionary structures into flat key-value pairs.

**Parameters:**
- `obj` (dict): The nested dictionary to flatten
- `sep` (str): Separator used for flattened keys (default: ".")
- `explode_arrays` (bool): Whether to explode primitive arrays into multiple rows
- `flatten_nested` (bool): Whether to flatten nested arrays within the structure

**Returns:** `list[dict]` - List of flattened dictionaries

**Algorithm:**
1. Recursively traverse the dictionary structure
2. For each nested object, prepend parent keys with separator
3. Handle arrays based on configuration:
   - If `explode_arrays=True` and array contains primitives, create separate rows
   - If `flatten_nested=True`, flatten nested arrays
   - Otherwise, keep arrays as-is
4. Return list of flattened records

**Examples:**

```python
# Basic flattening
data = {"user": {"name": "John", "age": 30}}
flatten_dict(data)
# Output: [{"user.name": "John", "user.age": 30}]

# With array explosion
data = {"user": {"name": "John", "tags": ["a", "b"]}}
flatten_dict(data, explode_arrays=True)
# Output: [
#     {"user.name": "John", "user.tags": "a"},
#     {"user.name": "John", "user.tags": "b"}
# ]
```

**Edge Cases:**
- Empty dictionaries return `[{}]`
- Circular references not supported (would cause infinite recursion)
- Mixed data types in arrays handled gracefully

---

### `normalize_nulls(data)`

**Purpose:** Standardizes null handling and ensures consistent field presence across records.

**Parameters:**
- `data` (list[dict]): List of dictionaries to normalize

**Returns:** `list[dict]` - Normalized list with consistent fields

**Algorithm:**
1. Collect all unique field names from all records
2. For each record, ensure all fields are present
3. Convert various null representations to Python `None`
4. Fill missing fields with `None`

**Examples:**

```python
data = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "city": "NYC"}
]
normalize_nulls(data)
# Output: [
#     {"name": "Alice", "age": 25, "city": None},
#     {"name": "Bob", "age": None, "city": "NYC"}
# ]
```

**Null Representations Handled:**
- `None`
- `"null"` (string)
- `"NULL"`
- `null` (if present in JSON)

---

### `normalize_json(obj, **kwargs)`

**Purpose:** Main entry point providing comprehensive JSON normalization with all features.

**Parameters:**
- `obj` (dict): JSON object to normalize
- `sep` (str): Key separator (default: ".")
- `explode_arrays` (bool): Explode primitive arrays
- `flatten_nested` (bool): Flatten nested arrays
- `schema` (dict): Type casting schema
- `key_convention` (str): Key naming convention
- `output_format` (str): Output format ('list' or 'dataframe')
- `config`: Configuration object

**Returns:** `list[dict]` or `pandas.DataFrame`

**Processing Pipeline:**
1. **Configuration**: Apply configuration settings
2. **Logging**: Log processing start
3. **Flattening**: Flatten nested structure
4. **Null Normalization**: Standardize nulls and missing fields
5. **Key Normalization**: Apply naming convention
6. **Type Casting**: Cast values according to schema
7. **Deduplication**: Remove duplicates if configured
8. **Output Formatting**: Return in requested format

**Examples:**

```python
# Full normalization pipeline
data = {
    "user": {
        "full-name": "John Doe",
        "age-str": "30",
        "tags": ["dev", "python"]
    }
}

schema = {"user.age_str": "int"}
config = JsonNormalizeConfig(key_convention='snake', explode_arrays=True)

result = normalize_json(data, schema=schema, config=config)
```

---

### `apply_type_casting(data, schema)`

**Purpose:** Applies type conversion to data fields based on schema definition.

**Parameters:**
- `data` (list[dict]): Data to cast
- `schema` (dict): Field-to-type mapping

**Returns:** `list[dict]` - Data with casted values

**Supported Types:**
- `"int"`: Convert to integer
- `"float"`: Convert to float
- `"str"`: Convert to string
- `"bool"`: Convert to boolean
- `"date"`: Convert to date object
- `"datetime"`: Convert to datetime object

**Type Casting Logic:**
- Uses safe casting with fallback to original value
- Handles common string representations
- Supports multiple date formats
- Logs casting failures

**Examples:**

```python
data = [{"age": "25", "active": "true", "score": "95.5"}]
schema = {"age": "int", "active": "bool", "score": "float"}
apply_type_casting(data, schema)
# Output: [{"age": 25, "active": True, "score": 95.5}]
```

---

### `infer_schema(data)`

**Purpose:** Automatically infers data types from sample data.

**Parameters:**
- `data` (list[dict]): Sample data to analyze

**Returns:** `dict` - Inferred schema mapping

**Inference Rules:**
- `int`: Python int type
- `float`: Python float type
- `str`: Python str type or strings containing date-like patterns
- `bool`: Python bool type
- `date`: Strings matching date patterns

**Examples:**

```python
data = [
    {"id": 1, "name": "John", "score": 95.5, "active": True},
    {"id": 2, "name": "Jane", "score": 87.0, "active": False}
]
infer_schema(data)
# Output: {"id": "int", "name": "str", "score": "float", "active": "bool"}
```

---

## Relations Functions

### `extract_child_table(parent, field, fk_name, remove_duplicates=False)`

**Purpose:** Extracts array of objects into separate child table with foreign key relationship.

**Parameters:**
- `parent` (dict): Parent object containing array
- `field` (str): Field name of the array
- `fk_name` (str): Foreign key field name
- `remove_duplicates` (bool): Whether to remove duplicate child records

**Returns:** `dict` with 'main', 'child', 'child_table_name'

**Algorithm:**
1. Extract array from parent object
2. Create child records with foreign key
3. Remove duplicates if requested
4. Return separated main and child data

**Examples:**

```python
parent = {
    "user_id": 1,
    "name": "John",
    "orders": [
        {"order_id": 100, "amount": 50},
        {"order_id": 101, "amount": 75}
    ]
}

result = extract_child_table(parent, "orders", "user_id")
# Output: {
#     "main": {"user_id": 1, "name": "John"},
#     "child": [
#         {"user_id": 1, "order_id": 100, "amount": 50},
#         {"user_id": 1, "order_id": 101, "amount": 75}
#     ],
#     "child_table_name": "orders_table"
# }
```

---

### `extract_junction_table(parent, field, fk_name, ref_name, remove_duplicates=False)`

**Purpose:** Creates junction table for N-N relationships from array of references.

**Parameters:**
- `parent` (dict): Parent object
- `field` (str): Field containing reference array
- `fk_name` (str): Parent foreign key name
- `ref_name` (str): Reference foreign key name
- `remove_duplicates` (bool): Remove duplicate junctions

**Returns:** `dict` with 'main', 'junction', 'junction_table_name'

**Examples:**

```python
parent = {"student_id": 1, "courses": [101, 102, 103]}
result = extract_junction_table(parent, "courses", "student_id", "course_id")
# Output: {
#     "main": {"student_id": 1},
#     "junction": [
#         {"student_id": 1, "course_id": 101},
#         {"student_id": 1, "course_id": 102},
#         {"student_id": 1, "course_id": 103}
#     ],
#     "junction_table_name": "courses_junction"
# }
```

---

### `extract_nested_relations(obj, fk_name="parent_id", remove_duplicates=False)`

**Purpose:** Recursively extracts all nested relations from complex object.

**Parameters:**
- `obj` (dict): Object to process
- `fk_name` (str): Foreign key name for relations
- `remove_duplicates` (bool): Remove duplicates from extracted relations

**Returns:** `dict` with 'main' and 'relations'

**Algorithm:**
1. Recursively traverse object structure
2. Extract arrays of objects into separate tables
3. Maintain foreign key relationships
4. Apply deduplication if requested

---

## Deduplication Functions

### `deduplicate_records(records, key_fields=None, keep='first')`

**Purpose:** Removes duplicate records based on specified criteria.

**Parameters:**
- `records` (list[dict]): Records to deduplicate
- `key_fields` (list): Fields to use as deduplication key
- `keep` (str): Which duplicate to keep ('first' or 'last')

**Returns:** `list[dict]` - Deduplicated records

**Deduplication Methods:**
- **By Fields**: Use specific fields as key
- **By Content**: Use entire record content as key
- **Hash-based**: Use MD5 hash for large records

**Examples:**

```python
records = [
    {"name": "John", "age": 25},
    {"name": "John", "age": 25},  # Duplicate
    {"name": "Jane", "age": 30}
]

# Deduplicate by specific fields
deduplicate_records(records, key_fields=['name', 'age'])
# Output: [{"name": "John", "age": 25}, {"name": "Jane", "age": 30}]

# Deduplicate by entire content
deduplicate_records(records)
# Output: [{"name": "John", "age": 25}, {"name": "Jane", "age": 30}]
```

---

### `deduplicate_relations(relations, dedup_rules=None)`

**Purpose:** Applies deduplication rules to extracted relations.

**Parameters:**
- `relations` (dict): Relations dictionary from extraction
- `dedup_rules` (dict): Deduplication rules per table

**Returns:** `dict` - Relations with deduplicated records

**Rule Format:**
```python
dedup_rules = {
    "table_name": {
        "key_fields": ["field1", "field2"],
        "keep": "first"
    }
}
```

---

## Error Handling

All functions include comprehensive error handling:

- **Type Casting Errors**: Logged and continue with original values
- **Schema Validation Errors**: Detailed error messages
- **Nesting Depth Errors**: Prevent infinite recursion
- **Configuration Errors**: Validate configuration parameters

## Performance Considerations

- **Memory Usage**: Large nested structures may consume significant memory
- **Processing Time**: Deep nesting and large arrays impact performance
- **Deduplication**: Hash-based deduplication for large datasets
- **Streaming**: Consider streaming for very large datasets

## Best Practices

1. **Use Configuration**: Leverage `JsonNormalizeConfig` for consistent settings
2. **Validate Early**: Use schema validation before processing
3. **Handle Errors**: Set appropriate error handling strategy
4. **Monitor Performance**: Use logging to identify bottlenecks
5. **Test Edge Cases**: Validate with various data structures
