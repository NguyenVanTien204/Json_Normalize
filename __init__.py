"""
JSON Normalize - A comprehensive library for normalizing complex JSON data structures.

This library provides powerful tools to transform nested JSON into flat, relational formats
with support for type casting, validation, deduplication, and relationship extraction.
"""

__version__ = "1.0.0"
__author__ = "JSON Normalize Team"
__description__ = "Comprehensive JSON normalization library"

# Import main functions for easy access
from .core.flattener import flatten_dict
from .core.null_handler import normalize_nulls
from .core.transformer import normalize_json
from .core.relation import (
    extract_child_table,
    extract_nested_relations,
    extract_junction_table,
    flatten_nested_array
)
from .core.type_cast import apply_type_casting, infer_schema, cast_value
from .core.dedup import (
    deduplicate_records,
    deduplicate_relations,
    find_duplicates,
    merge_duplicates
)

# Import utilities
from .utils.config import JsonNormalizeConfig, get_config, set_config
from .utils.naming import (
    normalize_keys,
    to_snake_case,
    to_camel_case,
    normalize_key,
    clean_special_chars
)
from .utils.validation import (
    validate_data,
    validate_record,
    filter_valid_records
)
from .utils.error_handler import (
    handle_error,
    safe_type_cast,
    validate_nesting_depth,
    log_processing_step,
    create_error_summary,
    JsonNormalizeError,
    SchemaValidationError,
    TypeCastError,
    NestingDepthError
)

# Define public API
__all__ = [
    # Core functions
    "flatten_dict",
    "normalize_nulls",
    "normalize_json",
    "apply_type_casting",
    "infer_schema",
    "cast_value",

    # Relations
    "extract_child_table",
    "extract_nested_relations",
    "extract_junction_table",
    "flatten_nested_array",

    # Deduplication
    "deduplicate_records",
    "deduplicate_relations",
    "find_duplicates",
    "merge_duplicates",

    # Configuration
    "JsonNormalizeConfig",
    "get_config",
    "set_config",

    # Naming
    "normalize_keys",
    "to_snake_case",
    "to_camel_case",
    "normalize_key",
    "clean_special_chars",

    # Validation
    "validate_data",
    "validate_record",
    "filter_valid_records",

    # Error handling
    "handle_error",
    "safe_type_cast",
    "validate_nesting_depth",
    "log_processing_step",
    "create_error_summary",
    "JsonNormalizeError",
    "SchemaValidationError",
    "TypeCastError",
    "NestingDepthError",
]

def __getattr__(name):
    """Lazy import for optional dependencies."""
    if name == "pd":
        try:
            import pandas as pd
            return pd
        except ImportError:
            raise ImportError("pandas is required for DataFrame operations")
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
