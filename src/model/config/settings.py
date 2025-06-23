"""
Simple settings management for the smart document system.
"""

import os
import yaml
import re
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


class Settings:
    """
    Simple settings manager that loads configuration from YAML file with environment variable substitution.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize settings with configuration file.
        
        Args:
            config_path: Path to YAML configuration file (optional)
        """
        # Load environment variables from .env file
        self._load_env_vars()
        
        # Load and process configuration file
        self._load_config_file(config_path)
    
    def _load_env_vars(self):
        """Load environment variables from .env file."""
        # Try to load from project root
        project_root = Path(__file__).parent.parent.parent.parent
        env_file = project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            logger.info(f"Environment variables loaded from: {env_file}")
        else:
            logger.warning("No .env file found")
    
    def _load_config_file(self, config_path: Optional[Path] = None):
        """Load configuration from YAML file with environment variable substitution."""
        if config_path and config_path.exists():
            config_file = config_path
        else:
            # Try to load from project root
            project_root = Path(__file__).parent.parent.parent.parent
            config_file = project_root / "config.yaml"
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        try:
            with open(config_file, 'r') as f:
                content = f.read()
            
            # Substitute environment variables (${VAR_NAME} format)
            content = self._substitute_env_vars(content)
            
            # Load YAML
            self._config_data = yaml.safe_load(content) or {}
            logger.info(f"Configuration loaded from: {config_file}")
            
        except Exception as e:
            logger.error(f"Error loading configuration file: {e}")
            raise
    
    def _substitute_env_vars(self, content: str) -> str:
        """Substitute environment variables in the content."""
        def replace_var(match):
            var_name = match.group(1)
            return os.getenv(var_name, match.group(0))  # Return original if not found
        
        # Replace ${VAR_NAME} patterns
        return re.sub(r'\$\{([^}]+)\}', replace_var, content)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., "llm.api_key", "classifier.model_name")
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def __getattr__(self, name: str) -> Any:
        """Allow direct attribute access to config sections."""
        if name in self._config_data:
            return self._config_data[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access."""
        return self.get(key)
    
    def to_dict(self) -> Dict[str, Any]:
        """Return the entire configuration as a dictionary."""
        return self._config_data.copy()


# Global settings instance
_settings = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def init_settings(config_path: Optional[Path] = None) -> Settings:
    """Initialize settings with a specific config path."""
    global _settings
    _settings = Settings(config_path)
    return _settings 