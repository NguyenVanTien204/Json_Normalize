import datetime
from typing import Any, Dict, List

def cast_value(value: Any, target_type: str) -> Any:
    """
    Cast a value to the target type.

    Args:
        value: The value to cast.
        target_type: The target type string (e.g., 'int', 'float', 'str', 'bool', 'date').

    Returns:
        The casted value, or original value if casting fails.
    """
    if value is None:
        return None

    try:
        if target_type == 'int':
            return int(value)
        elif target_type == 'float':
            return float(value)
        elif target_type == 'str':
            return str(value)
        elif target_type == 'bool':
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes', 'on')
            return bool(value)
        elif target_type == 'date':
            if isinstance(value, str):
                # Try common date formats
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d %H:%M:%S']:
                    try:
                        return datetime.datetime.strptime(value, fmt).date()
                    except ValueError:
                        continue
            return value
        elif target_type == 'datetime':
            if isinstance(value, str):
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%d/%m/%Y %H:%M:%S']:
                    try:
                        return datetime.datetime.strptime(value, fmt)
                    except ValueError:
                        continue
            return value
        else:
            return value
    except (ValueError, TypeError):
        return value

def apply_type_casting(data: List[Dict], schema: Dict[str, str]) -> List[Dict]:
    """
    Apply type casting to data based on schema.

    Args:
        data: List of dictionaries to cast.
        schema: Dictionary mapping field names to target types.

    Returns:
        List of dictionaries with casted values.
    """
    casted_data = []
    for record in data:
        casted_record = {}
        for key, value in record.items():
            if key in schema:
                casted_record[key] = cast_value(value, schema[key])
            else:
                casted_record[key] = value
        casted_data.append(casted_record)
    return casted_data

def infer_schema(data: List[Dict]) -> Dict[str, str]:
    """
    Infer schema from data by analyzing value types.

    Args:
        data: List of dictionaries to analyze.

    Returns:
        Dictionary mapping field names to inferred types.
    """
    if not data:
        return {}

    schema = {}
    for record in data:
        for key, value in record.items():
            if key not in schema:
                if isinstance(value, int):
                    schema[key] = 'int'
                elif isinstance(value, float):
                    schema[key] = 'float'
                elif isinstance(value, bool):
                    schema[key] = 'bool'
                elif isinstance(value, str):
                    # Try to detect date strings
                    if any(fmt in value for fmt in ['-', '/', ':']):
                        schema[key] = 'date'
                    else:
                        schema[key] = 'str'
                else:
                    schema[key] = 'str'
    return schema
