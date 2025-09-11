from typing import Dict, Any
import logging

class JsonNormalizeConfig:
    """
    Configuration class for JSON normalization.

    Attributes:
        sep (str): Separator for flattened keys.
        explode_arrays (bool): Whether to explode primitive arrays.
        flatten_nested (bool): Whether to flatten nested arrays.
        key_convention (str): Key naming convention ('snake', 'camel', 'keep').
        remove_duplicates (bool): Whether to remove duplicates globally.
        max_depth (int): Maximum nesting depth to prevent infinite recursion.
        error_handling (str): Error handling strategy ('raise', 'warn', 'skip').
        log_level (str): Logging level.
    """

    def __init__(self,
                 sep: str = ".",
                 explode_arrays: bool = False,
                 flatten_nested: bool = False,
                 key_convention: str = 'snake',
                 remove_duplicates: bool = False,
                 max_depth: int = 10,
                 error_handling: str = 'warn',
                 log_level: str = 'INFO'):

        self.sep = sep
        self.explode_arrays = explode_arrays
        self.flatten_nested = flatten_nested
        self.key_convention = key_convention
        self.remove_duplicates = remove_duplicates
        self.max_depth = max_depth
        self.error_handling = error_handling
        self.log_level = log_level

        # Setup logging
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, self.log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('JsonNormalize')

    def update(self, **kwargs):
        """Update configuration parameters."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                if key == 'log_level':
                    self._setup_logging()

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'sep': self.sep,
            'explode_arrays': self.explode_arrays,
            'flatten_nested': self.flatten_nested,
            'key_convention': self.key_convention,
            'remove_duplicates': self.remove_duplicates,
            'max_depth': self.max_depth,
            'error_handling': self.error_handling,
            'log_level': self.log_level
        }

# Global default config
default_config = JsonNormalizeConfig()

def get_config() -> JsonNormalizeConfig:
    """Get the global default configuration."""
    return default_config

def set_config(**kwargs):
    """Update the global default configuration."""
    default_config.update(**kwargs)
