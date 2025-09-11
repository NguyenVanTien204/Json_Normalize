from typing import Dict, List, Any
import datetime

def validate_record(record: Dict, schema: Dict[str, Any]) -> Dict:
    """
    Validate a single record against schema.

    Args:
        record: The record to validate.
        schema: Schema dictionary with field types and constraints.

    Returns:
        Dictionary with validation results: {'valid': bool, 'errors': list}
    """
    errors = []

    for field, constraints in schema.items():
        if field not in record:
            if constraints.get('required', False):
                errors.append(f"Missing required field: {field}")
            continue

        value = record[field]
        expected_type = constraints.get('type')

        if expected_type:
            if not _check_type(value, expected_type):
                errors.append(f"Field {field}: expected {expected_type}, got {type(value).__name__}")

        # Check additional constraints
        if 'min' in constraints and isinstance(value, (int, float)):
            if value < constraints['min']:
                errors.append(f"Field {field}: value {value} < minimum {constraints['min']}")

        if 'max' in constraints and isinstance(value, (int, float)):
            if value > constraints['max']:
                errors.append(f"Field {field}: value {value} > maximum {constraints['max']}")

        if 'choices' in constraints:
            if value not in constraints['choices']:
                errors.append(f"Field {field}: value {value} not in allowed choices {constraints['choices']}")

    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def _check_type(value: Any, expected_type: str) -> bool:
    """Check if value matches expected type."""
    if expected_type == 'int':
        return isinstance(value, int)
    elif expected_type == 'float':
        return isinstance(value, (int, float))
    elif expected_type == 'str':
        return isinstance(value, str)
    elif expected_type == 'bool':
        return isinstance(value, bool)
    elif expected_type == 'date':
        return isinstance(value, (datetime.date, datetime.datetime))
    elif expected_type == 'list':
        return isinstance(value, list)
    elif expected_type == 'dict':
        return isinstance(value, dict)
    return True

def validate_data(data: List[Dict], schema: Dict[str, Any]) -> List[Dict]:
    """
    Validate all records in data against schema.

    Args:
        data: List of records to validate.
        schema: Schema dictionary.

    Returns:
        List of validation results for each record.
    """
    results = []
    for record in data:
        result = validate_record(record, schema)
        results.append(result)
    return results

def filter_valid_records(data: List[Dict], schema: Dict[str, Any]) -> List[Dict]:
    """
    Filter only valid records based on schema.

    Args:
        data: List of records.
        schema: Schema dictionary.

    Returns:
        List of valid records.
    """
    valid_records = []
    for record in data:
        if validate_record(record, schema)['valid']:
            valid_records.append(record)
    return valid_records
