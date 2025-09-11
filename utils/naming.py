import re
from typing import Dict, List

def to_snake_case(s: str) -> str:
    """
    Convert string to snake_case.

    Args:
        s: The string to convert.

    Returns:
        String in snake_case.
    """
    # Insert underscore before uppercase letters
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
    # Replace spaces and hyphens with underscores
    s = re.sub(r'[-\s]+', '_', s)
    # Remove special characters except underscores
    s = re.sub(r'[^a-zA-Z0-9_]', '', s)
    # Convert to lowercase
    return s.lower()

def to_camel_case(s: str) -> str:
    """
    Convert string to camelCase.

    Args:
        s: The string to convert.

    Returns:
        String in camelCase.
    """
    # Convert to snake_case first
    s = to_snake_case(s)
    # Split by underscore and capitalize
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def normalize_key(key: str, convention: str = 'snake') -> str:
    """
    Normalize a key based on naming convention.

    Args:
        key: The key to normalize.
        convention: 'snake', 'camel', or 'keep'.

    Returns:
        Normalized key.
    """
    if convention == 'snake':
        return to_snake_case(key)
    elif convention == 'camel':
        return to_camel_case(key)
    else:
        return key

def normalize_keys(data: List[Dict], convention: str = 'snake') -> List[Dict]:
    """
    Normalize all keys in the data according to the convention.

    Args:
        data: List of dictionaries to normalize.
        convention: Naming convention ('snake', 'camel', 'keep').

    Returns:
        List of dictionaries with normalized keys.
    """
    normalized_data = []
    for record in data:
        normalized_record = {}
        for key, value in record.items():
            normalized_key = normalize_key(key, convention)
            normalized_record[normalized_key] = value
        normalized_data.append(normalized_record)
    return normalized_data

def clean_special_chars(s: str) -> str:
    """
    Remove or replace special characters in string.

    Args:
        s: The string to clean.

    Returns:
        Cleaned string.
    """
    # Replace special chars with underscores
    s = re.sub(r'[^a-zA-Z0-9_]', '_', s)
    # Remove multiple underscores
    s = re.sub(r'_+', '_', s)
    # Remove leading/trailing underscores
    return s.strip('_')
