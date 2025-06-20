"""
Configuration manager for the model package.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

from .default_config import DEFAULT_CONFIG

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Manages configuration for the model package.
    
    Handles loading, saving, and merging of configuration files
    with default settings.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to configuration file (optional)
        """
        self.config = DEFAULT_CONFIG.copy()
        self.config_path = config_path
        
        if config_path and config_path.exists():
            self.load_config(config_path)
    
    def load_config(self, config_path: Path) -> None:
        """
        Load configuration from file.
        
        Args:
            config_path: Path to configuration file
        """
        if not config_path.exists():
            logger.warning(f"Configuration file not found: {config_path}")
            return
        
        try:
            if config_path.suffix.lower() == '.json':
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
            elif config_path.suffix.lower() in ['.yml', '.yaml']:
                with open(config_path, 'r') as f:
                    file_config = yaml.safe_load(f)
            else:
                logger.error(f"Unsupported configuration file format: {config_path.suffix}")
                return
            
            self._merge_config(file_config)
            logger.info(f"Configuration loaded from: {config_path}")
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
    
    def save_config(self, config_path: Path) -> None:
        """
        Save current configuration to file.
        
        Args:
            config_path: Path where to save configuration
        """
        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            if config_path.suffix.lower() == '.json':
                with open(config_path, 'w') as f:
                    json.dump(self.config, f, indent=2)
            elif config_path.suffix.lower() in ['.yml', '.yaml']:
                with open(config_path, 'w') as f:
                    yaml.dump(self.config, f, default_flow_style=False)
            else:
                logger.error(f"Unsupported configuration file format: {config_path.suffix}")
                return
            
            logger.info(f"Configuration saved to: {config_path}")
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def get_config(self, section: Optional[str] = None) -> Dict[str, Any]:
        """
        Get configuration or a specific section.
        
        Args:
            section: Configuration section to retrieve (optional)
            
        Returns:
            Configuration dictionary or section
        """
        if section:
            return self.config.get(section, {})
        return self.config.copy()
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """
        Update configuration with new values.
        
        Args:
            updates: Dictionary of configuration updates
        """
        self._merge_config(updates)
        logger.info("Configuration updated")
    
    def reset_to_defaults(self) -> None:
        """
        Reset configuration to default values.
        """
        self.config = DEFAULT_CONFIG.copy()
        logger.info("Configuration reset to defaults")
    
    def _merge_config(self, new_config: Dict[str, Any]) -> None:
        """
        Merge new configuration with existing configuration.
        
        Args:
            new_config: New configuration to merge
        """
        def merge_dicts(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
            """Recursively merge dictionaries."""
            result = base.copy()
            for key, value in update.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dicts(result[key], value)
                else:
                    result[key] = value
            return result
        
        self.config = merge_dicts(self.config, new_config)
    
    def validate_config(self) -> list:
        """
        Validate current configuration.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Validate classifier configuration
        classifier_config = self.config.get('classifier', {})
        if 'type' not in classifier_config:
            errors.append("Missing classifier type")
        elif classifier_config['type'] not in ['llm', 'ml']:
            errors.append("Invalid classifier type")
        
        # Validate extractor configuration
        extractor_config = self.config.get('extractor', {})
        if 'type' not in extractor_config:
            errors.append("Missing extractor type")
        elif extractor_config['type'] not in ['llm', 'rule']:
            errors.append("Invalid extractor type")
        
        # Validate confidence thresholds
        for section in ['classifier', 'extractor']:
            config = self.config.get(section, {})
            threshold = config.get('confidence_threshold')
            if threshold is not None and (threshold < 0 or threshold > 1):
                errors.append(f"Invalid confidence threshold in {section}")
        
        return errors 