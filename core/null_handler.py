import math
from typing import Any

def normalize_nulls(data, replace_null=False, null_value="Null"):
    """
    Normalize null values and handle missing fields.

    Args:
        data (any): Input data (dict, list, or primitive).
        replace_null (bool): If True, replace None/null with `null_value`.
                             If False, keep None.
        null_value (any): Value to replace nulls with (e.g., "Null", float('nan')).

    Returns:
        any: Normalized data.
    """

    if data is None:
        return null_value if replace_null else None

    if isinstance(data, list):
        normalized_list = []
        for item in data:
            normalized = normalize_nulls(item, replace_null, null_value)
            # Bỏ qua dict rỗng hoặc list rỗng để tránh noise
            if normalized != {} and normalized != []:
                normalized_list.append(normalized)
        return normalized_list

    if isinstance(data, dict):
        normalized_dict = {}
        for k, v in data.items():
            normalized = normalize_nulls(v, replace_null, null_value)
            # Nếu là dict rỗng thì thay bằng None/null_value
            if normalized == {} or normalized == []:
                normalized = null_value if replace_null else None
            normalized_dict[k] = normalized
        return normalized_dict

    return data
