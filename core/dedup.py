from typing import Dict, List, Callable
import hashlib

def deduplicate_records(records: List[Dict],
                       key_fields: List[str] = None,
                       keep: str = 'first') -> List[Dict]:
    """
    Remove duplicate records based on specified key fields or entire record.

    Args:
        records: List of records to deduplicate.
        key_fields: List of field names to use as deduplication key.
                   If None, uses entire record.
        keep: Which duplicate to keep ('first', 'last').

    Returns:
        List of deduplicated records.
    """
    if not records:
        return records

    seen = {}
    result = []

    for record in records:
        if key_fields:
            # Use specified key fields
            key_values = []
            for field in key_fields:
                value = record.get(field)
                # Convert to string for hashing if needed
                if isinstance(value, (list, dict)):
                    key_values.append(str(sorted(value.items()) if isinstance(value, dict) else sorted(value)))
                else:
                    key_values.append(str(value))
            key = tuple(key_values)
        else:
            # Use entire record as key
            key = tuple(sorted((k, str(v) if isinstance(v, (list, dict)) else v) for k, v in record.items()))

        if key not in seen:
            seen[key] = len(result)
            result.append(record)
        elif keep == 'last':
            # Replace with the last occurrence
            result[seen[key]] = record

    return result

def deduplicate_by_hash(records: List[Dict], keep: str = 'first') -> List[Dict]:
    """
    Remove duplicates using hash of record content.

    Args:
        records: List of records to deduplicate.
        keep: Which duplicate to keep ('first', 'last').

    Returns:
        List of deduplicated records.
    """
    seen_hashes = {}
    result = []

    for record in records:
        # Create hash of sorted record items
        record_str = str(sorted(record.items()))
        record_hash = hashlib.md5(record_str.encode()).hexdigest()

        if record_hash not in seen_hashes:
            seen_hashes[record_hash] = len(result)
            result.append(record)
        elif keep == 'last':
            result[seen_hashes[record_hash]] = record

    return result

def deduplicate_relations(relations: Dict[str, List[Dict]],
                         dedup_rules: Dict[str, Dict] = None) -> Dict[str, List[Dict]]:
    """
    Deduplicate records in relations based on rules.

    Args:
        relations: Dictionary of table_name -> list of records.
        dedup_rules: Dictionary of table_name -> dedup config.
                    Config format: {'key_fields': [...], 'keep': 'first'}

    Returns:
        Dictionary with deduplicated relations.
    """
    deduped_relations = {}

    for table_name, records in relations.items():
        if dedup_rules and table_name in dedup_rules:
            rule = dedup_rules[table_name]
            key_fields = rule.get('key_fields')
            keep = rule.get('keep', 'first')
            deduped_relations[table_name] = deduplicate_records(records, key_fields, keep)
        else:
            # Default: deduplicate by entire record
            deduped_relations[table_name] = deduplicate_records(records)

    return deduped_relations

def find_duplicates(records: List[Dict], key_fields: List[str] = None) -> Dict[str, List[Dict]]:
    """
    Find and group duplicate records.

    Args:
        records: List of records to analyze.
        key_fields: Fields to use as deduplication key.

    Returns:
        Dictionary of key -> list of duplicate records.
    """
    groups = {}

    for record in records:
        if key_fields:
            key_values = tuple(record.get(field) for field in key_fields)
        else:
            key_values = tuple(sorted(record.items()))

        key_str = str(key_values)
        if key_str not in groups:
            groups[key_str] = []
        groups[key_str].append(record)

    # Only return groups with duplicates
    return {k: v for k, v in groups.items() if len(v) > 1}

def merge_duplicates(records: List[Dict],
                    key_fields: List[str],
                    merge_strategy: Callable[[List[Dict]], Dict] = None) -> List[Dict]:
    """
    Merge duplicate records based on key fields.

    Args:
        records: List of records to merge.
        key_fields: Fields to use as merge key.
        merge_strategy: Function to merge a group of records into one.

    Returns:
        List of merged records.
    """
    if not merge_strategy:
        # Default strategy: keep the first record
        def merge_strategy(group):
            return group[0]

    groups = find_duplicates(records, key_fields)
    merged = []
    processed_keys = set()

    for record in records:
        key_values = tuple(record.get(field) for field in key_fields)
        key_str = str(key_values)

        if key_str in groups and key_str not in processed_keys:
            group = groups[key_str]
            merged_record = merge_strategy(group)
            merged.append(merged_record)
            processed_keys.add(key_str)
        elif key_str not in groups:
            merged.append(record)

    return merged
