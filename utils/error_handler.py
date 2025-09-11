from typing import Any, Dict, List
from .config import get_config

class JsonNormalizeError(Exception):
    """Base exception for JSON normalization errors."""
    pass

class SchemaValidationError(JsonNormalizeError):
    """Exception for schema validation errors."""
    pass

class TypeCastError(JsonNormalizeError):
    """Exception for type casting errors."""
    pass

class NestingDepthError(JsonNormalizeError):
    """Exception for excessive nesting depth."""
    pass

def handle_error(error: Exception, context: str = "", strategy: str = None) -> Any:
    """
    Handle errors based on configured strategy.

    Args:
        error: The exception that occurred.
        context: Context information about where the error occurred.
        strategy: Error handling strategy ('raise', 'warn', 'skip').

    Returns:
        None if skip, otherwise raises the error.
    """
    config = get_config()
    strategy = strategy or config.error_handling

    logger = config.logger

    if strategy == 'raise':
        logger.error(f"Error in {context}: {str(error)}")
        raise error
    elif strategy == 'warn':
        logger.warning(f"Error in {context}: {str(error)}")
        return None
    elif strategy == 'skip':
        logger.info(f"Skipping error in {context}: {str(error)}")
        return None
    else:
        logger.error(f"Unknown error strategy: {strategy}")
        raise error

def safe_type_cast(value: Any, target_type: str, context: str = "") -> Any:
    """
    Safely cast value to target type with error handling.

    Args:
        value: Value to cast.
        target_type: Target type.
        context: Context for error reporting.

    Returns:
        Casted value or original value if casting fails.
    """
    try:
        from ..core.type_cast import cast_value
        return cast_value(value, target_type)
    except Exception as e:
        handle_error(TypeCastError(f"Failed to cast {value} to {target_type}: {str(e)}"),
                    context, 'warn')
        return value

def validate_nesting_depth(depth: int, context: str = ""):
    """
    Validate that nesting depth doesn't exceed maximum.

    Args:
        depth: Current nesting depth.
        context: Context for error reporting.

    Raises:
        NestingDepthError: If depth exceeds maximum.
    """
    config = get_config()
    if depth > config.max_depth:
        handle_error(NestingDepthError(f"Nesting depth {depth} exceeds maximum {config.max_depth}"),
                    context, 'raise')

def log_processing_step(step: str, details: Dict = None):
    """
    Log a processing step with optional details.

    Args:
        step: Description of the processing step.
        details: Additional details to log.
    """
    config = get_config()
    logger = config.logger

    message = f"Processing step: {step}"
    if details:
        message += f" - Details: {details}"

    logger.info(message)

def create_error_summary(errors: List[Dict]) -> Dict:
    """
    Create a summary of errors from validation results.

    Args:
        errors: List of error dictionaries.

    Returns:
        Summary dictionary with error counts and details.
    """
    summary = {
        'total_records': len(errors),
        'valid_records': 0,
        'invalid_records': 0,
        'error_types': {},
        'error_details': []
    }

    for error in errors:
        if error.get('valid', False):
            summary['valid_records'] += 1
        else:
            summary['invalid_records'] += 1
            summary['error_details'].extend(error.get('errors', []))

            for err in error.get('errors', []):
                error_type = err.split(':')[0] if ':' in err else 'Unknown'
                summary['error_types'][error_type] = summary['error_types'].get(error_type, 0) + 1

    return summary
