# Utils Module Documentation

## Overview

The `utils` module provides supporting functionality for configuration management, error handling, naming conventions, validation, and deduplication.

## Configuration Module

### `JsonNormalizeConfig`

**Purpose:** Central configuration class for all normalization options.

**Attributes:**
- `sep` (str): Key separator for flattening
- `explode_arrays` (bool): Explode primitive arrays
- `flatten_nested` (bool): Flatten nested arrays
- `key_convention` (str): Key naming convention
- `remove_duplicates` (bool): Global deduplication
- `max_depth` (int): Maximum nesting depth
- `error_handling` (str): Error handling strategy
- `log_level` (str): Logging level

**Methods:**

#### `__init__(**kwargs)`
Initialize configuration with default or custom values.

#### `update(**kwargs)`
Update configuration parameters dynamically.

**Parameters:**
- `**kwargs`: Configuration parameters to update

**Examples:**
```python
config = JsonNormalizeConfig(sep="_", explode_arrays=True)
config.update(log_level='DEBUG', max_depth=5)
```

#### `to_dict()`
Convert configuration to dictionary.

**Returns:** `dict` - Configuration as dictionary

---

### `get_config()`

**Purpose:** Get the global default configuration instance.

**Returns:** `JsonNormalizeConfig` - Global configuration

**Examples:**
```python
from json_normalize.utils import get_config
config = get_config()
config.sep = "_"
```

---

### `set_config(**kwargs)`

**Purpose:** Update the global default configuration.

**Parameters:**
- `**kwargs`: Configuration parameters to update

**Examples:**
```python
from json_normalize.utils import set_config
set_config(sep="_", key_convention='camel')
```

---

## Naming Module

### `normalize_keys(data, convention='snake')`

**Purpose:** Normalize key names in data according to naming convention.

**Parameters:**
- `data` (list[dict]): Data to normalize
- `convention` (str): Naming convention ('snake', 'camel', 'keep')

**Returns:** `list[dict]` - Data with normalized keys

**Examples:**
```python
data = [{"User-Name": "John", "User_Age": 25}]
normalize_keys(data, 'snake')
# Output: [{"user_name": "John", "user_age": 25}]
```

---

### `to_snake_case(s)`

**Purpose:** Convert string to snake_case.

**Parameters:**
- `s` (str): String to convert

**Returns:** `str` - String in snake_case

**Algorithm:**
1. Insert underscore before uppercase letters
2. Replace spaces and hyphens with underscores
3. Remove special characters
4. Convert to lowercase

**Examples:**
```python
to_snake_case("UserName")  # "user_name"
to_snake_case("user-name")  # "user_name"
to_snake_case("User Name")  # "user_name"
```

---

### `to_camel_case(s)`

**Purpose:** Convert string to camelCase.

**Parameters:**
- `s` (str): String to convert

**Returns:** `str` - String in camelCase

**Algorithm:**
1. Convert to snake_case first
2. Split by underscore
3. Capitalize words except first
4. Join without separators

**Examples:**
```python
to_camel_case("user_name")  # "userName"
to_camel_case("user-name")  # "userName"
```

---

### `normalize_key(key, convention='snake')`

**Purpose:** Normalize a single key.

**Parameters:**
- `key` (str): Key to normalize
- `convention` (str): Naming convention

**Returns:** `str` - Normalized key

---

### `clean_special_chars(s)`

**Purpose:** Remove and replace special characters in strings.

**Parameters:**
- `s` (str): String to clean

**Returns:** `str` - Cleaned string

**Examples:**
```python
clean_special_chars("user@domain.com")  # "user_domain_com"
clean_special_chars("user.name")  # "user_name"
```

---

## Validation Module

### `validate_data(data, schema)`

**Purpose:** Validate list of records against schema.

**Parameters:**
- `data` (list[dict]): Data to validate
- `schema` (dict): Validation schema

**Returns:** `list[dict]` - Validation results for each record

**Result Format:**
```python
{
    "valid": bool,
    "errors": ["error message 1", "error message 2"]
}
```

**Examples:**
```python
schema = {
    "age": {"type": "int", "min": 0, "max": 120},
    "name": {"type": "str", "required": True}
}

data = [{"name": "John", "age": 25}, {"age": 150}]
results = validate_data(data, schema)
# Output: [
#     {"valid": True, "errors": []},
#     {"valid": False, "errors": ["Field age: value 150 > maximum 120"]}
# ]
```

---

### `validate_record(record, schema)`

**Purpose:** Validate a single record.

**Parameters:**
- `record` (dict): Record to validate
- `schema` (dict): Validation schema

**Returns:** `dict` - Validation result

**Schema Format:**
```python
schema = {
    "field_name": {
        "type": "int",        # Required: data type
        "required": True,     # Optional: field must be present
        "min": 0,            # Optional: minimum value
        "max": 100,          # Optional: maximum value
        "choices": ["A", "B"] # Optional: allowed values
    }
}
```

**Validation Rules:**
- **Type Check**: Value matches specified type
- **Required Check**: Field presence if required=True
- **Range Check**: Value within min/max bounds
- **Choice Check**: Value in allowed choices

---

### `filter_valid_records(data, schema)`

**Purpose:** Filter only valid records from data.

**Parameters:**
- `data` (list[dict]): Data to filter
- `schema` (dict): Validation schema

**Returns:** `list[dict]` - Only valid records

**Examples:**
```python
data = [
    {"name": "John", "age": 25},
    {"name": "Jane", "age": 150},  # Invalid
    {"age": 30}  # Invalid
]

valid_data = filter_valid_records(data, schema)
# Output: [{"name": "John", "age": 25}]
```

---

## Error Handler Module

### `handle_error(error, context='', strategy=None)`

**Purpose:** Handle errors based on configured strategy.

**Parameters:**
- `error` (Exception): Exception that occurred
- `context` (str): Context information
- `strategy` (str): Error handling strategy ('raise', 'warn', 'skip')

**Strategies:**
- `'raise'`: Re-raise the exception
- `'warn'`: Log warning and continue
- `'skip'`: Log info and return None

**Examples:**
```python
try:
    risky_operation()
except Exception as e:
    handle_error(e, "risky_operation", 'warn')
```

---

### `safe_type_cast(value, target_type, context='')`

**Purpose:** Safely cast value with error handling.

**Parameters:**
- `value`: Value to cast
- `target_type` (str): Target type
- `context` (str): Context for error reporting

**Returns:** Casted value or original value if casting fails

**Examples:**
```python
result = safe_type_cast("25", "int", "user_age")
# Output: 25

result = safe_type_cast("invalid", "int", "user_age")
# Output: "invalid" (original value, with warning logged)
```

---

### `validate_nesting_depth(depth, context='')`

**Purpose:** Validate nesting depth doesn't exceed maximum.

**Parameters:**
- `depth` (int): Current nesting depth
- `context` (str): Context for error reporting

**Raises:** `NestingDepthError` if depth exceeds maximum

---

### `log_processing_step(step, details=None)`

**Purpose:** Log a processing step with optional details.

**Parameters:**
- `step` (str): Description of processing step
- `details` (dict): Additional details to log

**Examples:**
```python
log_processing_step("Starting normalization", {"input_size": 1000})
log_processing_step("Flattened object", {"records_count": 50})
```

---

### `create_error_summary(errors)`

**Purpose:** Create summary of validation errors.

**Parameters:**
- `errors` (list[dict]): List of validation error results

**Returns:** `dict` - Error summary with counts and details

**Summary Format:**
```python
{
    "total_records": 100,
    "valid_records": 95,
    "invalid_records": 5,
    "error_types": {
        "Field age: value 150 > maximum 120": 3,
        "Missing required field: name": 2
    },
    "error_details": ["error1", "error2", ...]
}
```

---

## Custom Exceptions

### `JsonNormalizeError`

**Purpose:** Base exception for all JSON normalization errors.

### `SchemaValidationError`

**Purpose:** Exception for schema validation failures.

### `TypeCastError`

**Purpose:** Exception for type casting failures.

### `NestingDepthError`

**Purpose:** Exception for excessive nesting depth.

**Examples:**
```python
from json_normalize.utils import JsonNormalizeError, SchemaValidationError

try:
    validate_data(data, invalid_schema)
except SchemaValidationError as e:
    print(f"Schema validation failed: {e}")
except JsonNormalizeError as e:
    print(f"Normalization error: {e}")
```

---

## Integration Examples

### Using Configuration with Error Handling

```python
from json_normalize.utils import JsonNormalizeConfig, handle_error

config = JsonNormalizeConfig(
    error_handling='warn',
    log_level='INFO',
    max_depth=10
)

try:
    result = normalize_json(data, config=config)
except Exception as e:
    handle_error(e, "normalization", config.error_handling)
```

### Comprehensive Validation Pipeline

```python
from json_normalize.utils import validate_data, create_error_summary

# Validate data
validation_results = validate_data(data, schema)

# Create summary
summary = create_error_summary(validation_results)

# Log summary
if summary['invalid_records'] > 0:
    print(f"Found {summary['invalid_records']} invalid records")
    for error_type, count in summary['error_types'].items():
        print(f"  {error_type}: {count} occurrences")
```

### Custom Naming Convention

```python
from json_normalize.utils import normalize_keys, to_snake_case

# Custom normalization function
def custom_normalize(key):
    # Your custom logic here
    return to_snake_case(key).upper()

# Apply custom normalization
normalized_data = []
for record in data:
    normalized_record = {}
    for key, value in record.items():
        normalized_record[custom_normalize(key)] = value
    normalized_data.append(normalized_record)
```

---

## Best Practices

### Configuration Management

```python
# Create named configurations for different use cases
api_config = JsonNormalizeConfig(
    explode_arrays=True,
    key_convention='camel',
    error_handling='warn'
)

batch_config = JsonNormalizeConfig(
    remove_duplicates=True,
    log_level='ERROR',
    max_depth=5
)
```

### Error Handling Strategy

```python
# Choose appropriate error handling based on use case
# For APIs: 'raise' to fail fast
# For batch processing: 'warn' to continue processing
# For data exploration: 'skip' to ignore problematic records

config = JsonNormalizeConfig(error_handling='warn')
```

### Validation Workflow

```python
# Comprehensive validation workflow
def validate_and_process(data, schema):
    # Step 1: Validate
    validation_results = validate_data(data, schema)
    summary = create_error_summary(validation_results)

    # Step 2: Log issues
    if summary['invalid_records'] > 0:
        log_processing_step("Validation completed", {
            "valid": summary['valid_records'],
            "invalid": summary['invalid_records']
        })

    # Step 3: Filter valid records
    valid_data = filter_valid_records(data, schema)

    # Step 4: Process valid data
    return normalize_json(valid_data[0] if valid_data else {}, schema=schema)
```

### Performance Optimization

```python
# For large datasets
config = JsonNormalizeConfig(
    log_level='WARNING',  # Reduce logging overhead
    remove_duplicates=True,  # Reduce memory usage
    error_handling='skip'  # Skip problematic records
)
```
