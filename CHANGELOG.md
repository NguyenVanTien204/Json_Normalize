# Changelog

All notable changes to JSON Normalize will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-09-10

### Added
- **Core Functionality**
  - `normalize_json()`: Main entry point for comprehensive JSON normalization
  - `flatten_dict()`: Flatten nested dictionaries with configurable separators
  - `normalize_nulls()`: Standardize null values and handle missing fields
  - `apply_type_casting()`: Type casting with schema support
  - `infer_schema()`: Automatic schema inference from data

- **Relationship Extraction**
  - `extract_child_table()`: Extract 1-N relationships
  - `extract_junction_table()`: Extract N-N relationships
  - `extract_nested_relations()`: Recursive relationship extraction
  - `flatten_nested_array()`: Handle nested arrays

- **Configuration System**
  - `JsonNormalizeConfig`: Comprehensive configuration class
  - Global configuration management with `get_config()` and `set_config()`
  - Support for all normalization options

- **Naming Conventions**
  - `normalize_keys()`: Apply naming conventions to keys
  - `to_snake_case()`: Convert to snake_case
  - `to_camel_case()`: Convert to camelCase
  - `clean_special_chars()`: Clean special characters

- **Validation System**
  - `validate_data()`: Validate data against schema
  - `validate_record()`: Validate individual records
  - `filter_valid_records()`: Filter valid records
  - Support for type, range, and choice validation

- **Error Handling**
  - Comprehensive error handling with configurable strategies
  - Custom exceptions: `JsonNormalizeError`, `SchemaValidationError`, etc.
  - Safe operations with fallback behavior
  - Detailed logging and error reporting

- **Deduplication**
  - `deduplicate_records()`: Remove duplicate records
  - `deduplicate_relations()`: Deduplicate extracted relations
  - `find_duplicates()`: Find duplicate records
  - `merge_duplicates()`: Merge duplicate records

- **Array Handling**
  - Explode primitive arrays into multiple rows
  - Flatten nested arrays
  - Handle mixed-type arrays gracefully

- **Output Formats**
  - List of dictionaries (default)
  - Pandas DataFrame support (optional)

- **Documentation**
  - Comprehensive README with examples
  - API reference documentation
  - User guide with best practices
  - Module-specific documentation

- **Examples**
  - Basic usage examples
  - Advanced configuration examples
  - Relationship extraction examples
  - Schema and validation examples
  - Error handling examples

### Features
- **Configurable Separators**: Custom separators for flattened keys
- **Multiple Naming Conventions**: snake_case, camelCase, keep original
- **Type Casting**: Support for int, float, str, bool, date, datetime
- **Schema Validation**: Comprehensive validation with constraints
- **Relationship Mapping**: 1-N and N-N relationship extraction
- **Deduplication**: Global and per-table deduplication
- **Error Recovery**: Graceful error handling with multiple strategies
- **Logging**: Detailed processing logs with configurable levels
- **Performance**: Optimized for large datasets

### Technical Details
- **Python Version**: 3.7+
- **Dependencies**: Minimal (pandas optional)
- **Architecture**: Modular design with clear separation of concerns
- **Testing**: Comprehensive test suite with high coverage
- **Documentation**: Complete API documentation and user guides

### Breaking Changes
- None (initial release)

### Deprecated
- None

### Fixed
- None

### Security
- None

---

## [0.1.0] - 2025-09-01

### Added
- Initial project structure
- Basic flattening functionality
- Core module skeleton
- Basic test setup

### Changed
- None

### Deprecated
- None

### Removed
- None

### Fixed
- None

### Security
- None

---

## Types of changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities

## Versioning
This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

## Migration Guide

### From 0.x to 1.0
No migration needed as this is the initial release.

---

*For older versions, see the commit history.*
