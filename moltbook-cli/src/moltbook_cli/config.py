"""Configuration management for Moltbook CLI."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration manager for Moltbook CLI."""
    
    DEFAULT_CONFIG = {
        'api': {
            'base_url': 'https://moltbook.io/api/v1',
            'timeout': 30,
            'retry_attempts': 3,
            'retry_delay': 1
        },
        'auth': {
            'token_file': '~/.moltbook/token'
        },
        'output': {
            'format': 'table',  # table, json, yaml
            'colors': True,
            'verbose': False
        },
        'cache': {
            'enabled': True,
            'ttl': 300,  # 5 minutes
            'dir': '~/.moltbook/cache'
        }
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration."""
        self.config_file = config_file or os.path.expanduser('~/.moltbook/config.yaml')
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file."""
        config_path = Path(self.config_file)
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = yaml.safe_load(f) or {}
                    self._merge_config(self.config, user_config)
            except Exception as e:
                print(f"Warning: Could not load config file {config_path}: {e}")
    
    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """Recursively merge configuration dictionaries."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'api.base_url')."""
        keys = key_path.split('.')
        value = self.config
        try:
            for key in keys:
                value = value[key]
            return value
        except KeyError:
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """Set configuration value using dot notation."""
        keys = key_path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
    
    def save(self) -> None:
        """Save configuration to file."""
        config_path = Path(self.config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def get_api_key(self) -> Optional[str]:
        """Get Moltbook API key from environment or token file."""
        # Check environment variable first
        api_key = os.getenv('MOLTBOOK_API_KEY')
        if api_key:
            return api_key
        
        # Check token file
        token_file = Path(os.path.expanduser(self.get('auth.token_file')))
        if token_file.exists():
            try:
                with open(token_file, 'r') as f:
                    return f.read().strip()
            except Exception:
                pass
        
        return None
    
    def set_api_key(self, api_key: str) -> None:
        """Save API key to token file."""
        token_file = Path(os.path.expanduser(self.get('auth.token_file')))
        token_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(token_file, 'w') as f:
            f.write(api_key)


# Global configuration instance
config = Config()