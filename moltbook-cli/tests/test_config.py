"""Tests for configuration module."""

import pytest
import tempfile
import os
from pathlib import Path

from moltbook_cli.config import Config


class TestConfig:
    """Test configuration management."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        
        assert config.get('api.base_url') == 'https://moltbook.io/api/v1'
        assert config.get('api.timeout') == 30
        assert config.get('output.format') == 'table'
        assert config.get('cache.enabled') is True
    
    def test_load_config_from_file(self):
        """Test loading configuration from file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
api:
  base_url: https://custom.api.com
  timeout: 60
output:
  format: json
""")
            temp_file = f.name
        
        try:
            config = Config(temp_file)
            
            assert config.get('api.base_url') == 'https://custom.api.com'
            assert config.get('api.timeout') == 60
            assert config.get('output.format') == 'json'
            
        finally:
            os.unlink(temp_file)
    
    def test_set_and_get_values(self):
        """Test setting and getting configuration values."""
        config = Config()
        
        config.set('custom.key', 'value')
        assert config.get('custom.key') == 'value'
        
        config.set('nested.deep.key', 42)
        assert config.get('nested.deep.key') == 42
    
    def test_get_with_default(self):
        """Test getting values with default fallback."""
        config = Config()
        
        assert config.get('nonexistent.key', 'default') == 'default'
        assert config.get('nonexistent.key') is None
    
    def test_save_config(self):
        """Test saving configuration to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / 'config.yaml'
            
            config = Config(str(config_file))
            config.set('custom.value', 'test')
            config.save()
            
            assert config_file.exists()
            
            # Load the saved config
            new_config = Config(str(config_file))
            assert new_config.get('custom.value') == 'test'