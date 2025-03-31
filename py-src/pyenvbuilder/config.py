"""Configuration management for PyEnvBuilder."""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Configuration management for PyEnvBuilder."""
    
    def __init__(self):
        self.default_config = {
            "env_name": "BuildEnv",
            "python_version": "3.6",
            "requirements": [
                "wheel",
                "setuptools",
                "pip-tools",
                "pytest",
                "black",
                "flake8",
                "mypy"
            ],
            "log_level": "INFO",
            "parallel_install": True,
            "no_cache": True,
            "force_cleanup": False
        }
        self.config: Dict[str, Any] = {}
        self.config_file: Optional[Path] = None
        
    def load(self, config_path: Optional[str] = None) -> None:
        """Load configuration from file or use defaults.
        
        Args:
            config_path: Optional path to configuration file
        """
        if config_path:
            self.config_file = Path(config_path)
            if self.config_file.exists():
                try:
                    with open(self.config_file) as f:
                        self.config = json.load(f)
                except json.JSONDecodeError:
                    self.config = self.default_config.copy()
            else:
                self.config = self.default_config.copy()
                self.save()
        else:
            self.config = self.default_config.copy()
            
    def save(self) -> None:
        """Save current configuration to file."""
        if self.config_file:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
                
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, self.default_config.get(key, default))
        
    def set(self, key: str, value: Any) -> None:
        """Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value
        self.save()
        
    def update(self, config_dict: Dict[str, Any]) -> None:
        """Update multiple configuration values.
        
        Args:
            config_dict: Dictionary of configuration values
        """
        self.config.update(config_dict)
        self.save()
        
    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.config = self.default_config.copy()
        self.save()

# Global configuration instance
config = Config() 