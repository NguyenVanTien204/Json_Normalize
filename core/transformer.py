from .flattener import flatten_dict
from .null_handler import normalize_nulls
from .type_cast import apply_type_casting

try:
    from ..utils.naming import normalize_keys
except ImportError:
    # Fallback if relative import fails
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.naming import normalize_keys

try:
    from ..utils.config import get_config
    from ..utils.error_handler import log_processing_step, handle_error
    from ..core.dedup import deduplicate_records
except ImportError:
    # Fallback
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.config import get_config
    from utils.error_handler import log_processing_step, handle_error
    from core.dedup import deduplicate_records

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

def normalize_json(obj, sep=".", explode_arrays=False, flatten_nested=False,
                  schema=None, key_convention='snake', output_format="dataframe",
                  config=None, extract_relations=True, fk_name="parent_id", null_value=""):
    """
    Normalize a JSON object with comprehensive options and error handling.

    Args:
        obj (dict): The JSON object to normalize.
        sep (str): Separator for flattened keys.
        explode_arrays (bool): Whether to explode primitive arrays.
        flatten_nested (bool): Whether to flatten nested arrays.
        schema (dict): Schema for type casting and validation.
        key_convention (str): Key naming convention ('snake', 'camel', 'keep').
        output_format (str): "dataframe" for pandas.DataFrame, "relational" for dict with main and relations.
        config: Configuration object or dict.
        extract_relations (bool): Whether to extract nested relations into separate tables.
        fk_name (str): Foreign key name for extracted relations.

    Returns:
        list[dict] or pandas.DataFrame or dict: Normalized data.
    """
    # Get configuration
    if config is None:
        cfg = get_config()
    elif isinstance(config, dict):
        cfg = get_config()
        cfg.update(**config)
    else:
        cfg = config

    log_processing_step("Starting JSON normalization", {"input_type": type(obj).__name__})

    try:
        # Flatten the object
        flattened = flatten_dict(obj, sep=sep, explode_arrays=explode_arrays, flatten_nested=flatten_nested)
        log_processing_step("Flattened object", {"records_count": len(flattened)})

        # Initialize relations dict
        relations = {}

        # Extract nested relations if enabled
        if extract_relations:
            if len(flattened) == 1:  # Single record case
                from .relation import extract_nested_relations
                result = extract_nested_relations(flattened[0], fk_name=fk_name, remove_duplicates=cfg.remove_duplicates)
                flattened = [result["main"]]
                relations = result["relations"]
                log_processing_step("Extracted relations", {"relations_count": len(relations)})
            else:
                # For multiple records, extract relations from each
                all_relations = {}
                for i, record in enumerate(flattened):
                    from .relation import extract_nested_relations
                    result = extract_nested_relations(record, fk_name=fk_name, remove_duplicates=cfg.remove_duplicates)
                    flattened[i] = result["main"]
                    # Merge relations
                    for table_name, records in result["relations"].items():
                        if table_name not in all_relations:
                            all_relations[table_name] = []
                        all_relations[table_name].extend(records)
                relations = all_relations
                log_processing_step("Extracted relations from multiple records", {"relations_count": len(relations)})

        # Normalize nulls
        if null_value != "":
            normalized = normalize_nulls(flattened, replace_null= True, null_value=null_value)
        else:
            normalized = normalize_nulls(flattened)

        # Normalize keys
        if key_convention != 'keep':
            normalized = normalize_keys(normalized, key_convention)

        # Apply type casting if schema provided
        if schema:
            normalized = apply_type_casting(normalized, schema)
            log_processing_step("Applied type casting", {"schema_fields": len(schema)})

        # Global deduplication if configured
        if cfg.remove_duplicates:
            original_count = len(normalized)
            normalized = deduplicate_records(normalized)
            log_processing_step("Removed duplicates", {
                "original_count": original_count,
                "final_count": len(normalized)
            })

        if output_format == "dataframe":
            if not PANDAS_AVAILABLE:
                handle_error(ImportError("pandas is required for DataFrame output"), "output_format")
            else:
                if extract_relations and relations:
                    # Return dict of DataFrames (main + relation tables)
                    result = {"main": pd.DataFrame(normalized)}
                    for table_name, records in relations.items():
                        result[table_name] = pd.DataFrame(records) if records else pd.DataFrame()
                    return result
                else:
                    # Return single DataFrame for main data
                    return pd.DataFrame(normalized)
        elif output_format == "relational":
            # Return both main data and relations
            return {
                "main": normalized,
                "relations": relations if extract_relations else {}
            }
        else:
            raise ValueError(f"Unsupported output format: {output_format} please use 'dataframe' or 'relational' instead.")

    except Exception as e:
        handle_error(e, "JSON normalization")
        return []
