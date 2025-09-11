import math
from typing import Any

def normalize_nulls(data: Any):
    """
    Deep-normalize null-like values to None and align keys for nested lists of dicts.

    Behavior:
    - Treats None, NaN, and strings "null", "none", "" (case-insensitive, trimmed) as None.
    - If encountering a list where every element is a dict, it will collect the union
      of keys across those dicts and ensure each dict has all keys (missing -> None).
    - Works for top-level dict or list[dict], and for any nested structure (recursive).
    - Empty lists are preserved as [].

    Args:
        data (Any): The input data to normalize.

    Returns:
        Any: The normalized data.
    """
    def is_null_like(v):
        if v is None:
            return True
        if isinstance(v, float) and math.isnan(v):
            return True
        if isinstance(v, str) and v.strip().lower() in {"null", "none", ""}:
            return True
        return False

    def deep_normalize(v):
        # Null-like -> None
        if is_null_like(v):
            return None
        # Dict -> normalize values recursively
        if isinstance(v, dict):
            return {k: deep_normalize(val) for k, val in v.items()}
        # List -> special handling for list-of-dicts (align keys), otherwise normalize elements
        if isinstance(v, list):
            if not v:
                return []  # preserve empty lists
            if all(isinstance(item, dict) for item in v):
                # collect union keys across all dict items
                all_keys = set()
                for item in v:
                    all_keys.update(item.keys())
                normalized_items = []
                for item in v:
                    new_item = {}
                    for k in all_keys:
                        new_item[k] = deep_normalize(item.get(k, None))
                    normalized_items.append(new_item)
                return normalized_items
            else:
                # mixed list or primitive list -> normalize each element
                return [deep_normalize(item) for item in v]
        # other types -> return as-is
        return v

    # If top-level is list of dicts, align top-level keys across records
    if isinstance(data, list) and all(isinstance(d, dict) for d in data):
        all_keys = set()
        for record in data:
            all_keys.update(record.keys())
        normalized = []
        for record in data:
            new_record = {}
            for key in all_keys:
                new_record[key] = deep_normalize(record.get(key, None))
            normalized.append(new_record)
        return normalized

    # otherwise deep-normalize whatever structure we have
    return deep_normalize(data)
