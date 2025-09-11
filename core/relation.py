def extract_child_table(parent, field, fk_name, remove_duplicates=False):
    """
    Extract child table from array of objects in parent.

    Args:
        parent (dict): The parent object containing the array field.
        field (str): The field name of the array of objects.
        fk_name (str): The name of the foreign key to add to child records.
        remove_duplicates (bool): Whether to remove duplicate child records.

    Returns:
        dict: {
            "main": dict (parent with field removed),
            "child": list[dict] (child records with fk),
            "child_table_name": str
        }
    """
    if field not in parent or not isinstance(parent[field], list):
        return {
            "main": parent,
            "child": [],
            "child_table_name": f"{field}_table"
        }

    child_records = parent[field]
    if not child_records:
        return {
            "main": {k: v for k, v in parent.items() if k != field},
            "child": [],
            "child_table_name": f"{field}_table"
        }

    # Get parent key value for FK, assume it's the first key or 'id'
    parent_fk_value = parent.get('id', parent.get(list(parent.keys())[0]))

    # Process child records
    processed_children = []
    for child in child_records:
        if isinstance(child, dict):
            new_child = child.copy()
            new_child[fk_name] = parent_fk_value
            processed_children.append(new_child)
        else:
            # If not dict, treat as primitive, but for array of objects, skip
            continue

    # Remove duplicates if requested
    if remove_duplicates:
        seen = set()
        unique_children = []
        for child in processed_children:
            # Use tuple of sorted items as key
            key = tuple(sorted(child.items()))
            if key not in seen:
                seen.add(key)
                unique_children.append(child)
        processed_children = unique_children

    # Remove field from parent
    main = {k: v for k, v in parent.items() if k != field}

    return {
        "main": main,
        "child": processed_children,
        "child_table_name": f"{field}_table"
    }

def extract_nested_relations(obj, fk_name="parent_id", remove_duplicates=False):
    """
    Recursively extract nested relations from object.

    Args:
        obj (dict): The object to process.
        fk_name (str): Foreign key name for relations.
        remove_duplicates (bool): Whether to remove duplicates.

    Returns:
        dict: {
            "main": dict,
            "relations": dict of table_name: list[dict]
        }
    """
    relations = {}
    main = obj.copy()

    def _extract(obj, prefix="", parent_fk=None):
        for key, value in list(obj.items()):
            if isinstance(value, list) and value and isinstance(value[0], dict):
                # Array of objects
                table_name = f"{prefix}{key}_table" if prefix else f"{key}_table"
                if table_name not in relations:
                    relations[table_name] = []
                for i, child in enumerate(value):
                    child_fk = f"{parent_fk}_{i}" if parent_fk else f"{key}_{i}"
                    new_child = child.copy()
                    new_child[fk_name] = child_fk
                    # Recursively extract from child
                    _extract(new_child, f"{prefix}{key}_", child_fk)
                    relations[table_name].append(new_child)

                del obj[key]
        return obj

    _extract(main)

    if remove_duplicates:
        for table in relations:
            seen = set()
            unique = []
            for rec in relations[table]:
                key_tuple = tuple(sorted(rec.items()))
                if key_tuple not in seen:
                    seen.add(key_tuple)
                    unique.append(rec)
            relations[table] = unique

    return {
        "main": main,
        "relations": relations
    }

def extract_junction_table(parent, field, fk_name, ref_name, remove_duplicates=False):
    """
    Extract junction table from array of references (N-N relationship).

    Args:
        parent (dict): The parent object containing the array field.
        field (str): The field name of the array of references.
        fk_name (str): The name of the foreign key for parent.
        ref_name (str): The name of the foreign key for references.
        remove_duplicates (bool): Whether to remove duplicate junction records.

    Returns:
        dict: {
            "main": dict (parent with field removed),
            "junction": list[dict] (junction records),
            "junction_table_name": str
        }
    """
    if field not in parent or not isinstance(parent[field], list):
        return {
            "main": parent,
            "junction": [],
            "junction_table_name": f"{field}_junction"
        }

    refs = parent[field]
    if not refs:
        return {
            "main": {k: v for k, v in parent.items() if k != field},
            "junction": [],
            "junction_table_name": f"{field}_junction"
        }

    # Get parent key value for FK
    parent_fk_value = parent.get('id', parent.get(list(parent.keys())[0]))

    # Process junction records
    junction_records = []
    for ref in refs:
        if not isinstance(ref, (dict, list)):  # Primitive reference
            junction_records.append({
                fk_name: parent_fk_value,
                ref_name: ref
            })
        # If dict or list, skip for now (could be extended)

    # Remove duplicates if requested
    if remove_duplicates:
        seen = set()
        unique_junction = []
        for rec in junction_records:
            key = tuple(sorted(rec.items()))
            if key not in seen:
                seen.add(key)
                unique_junction.append(rec)
        junction_records = unique_junction

    # Remove field from parent
    main = {k: v for k, v in parent.items() if k != field}

    return {
        "main": main,
        "junction": junction_records,
        "junction_table_name": f"{field}_junction"
    }

def flatten_nested_array(arr, flatten_config="flat"):
    """
    Flatten nested array based on config.

    Args:
        arr (list): The nested array to flatten.
        flatten_config (str): "flat" to flatten all, "keep" to keep as is.

    Returns:
        list: Flattened array.
    """
    if flatten_config == "keep":
        return arr

    def _flatten(current):
        result = []
        for item in current:
            if isinstance(item, list):
                result.extend(_flatten(item))
            else:
                result.append(item)
        return result

    return _flatten(arr)
