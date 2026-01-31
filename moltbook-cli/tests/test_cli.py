"""Basic CLI tests."""

import pytest
from click.testing import CliRunner

from moltbook_cli.main import cli


class TestCLI:
    """Test CLI commands."""
    
    def test_version_command(self):
        """Test version command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['version'])
        
        assert result.exit_code == 0
        assert 'Moltbook CLI' in result.output
    
    def test_help_command(self):
        """Test help command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert 'Moltbook CLI' in result.output
        assert 'auth' in result.output
        assert 'feed' in result.output
        assert 'post' in result.output
    
    def test_auth_help(self):
        """Test auth subcommand help."""
        runner = CliRunner()
        result = runner.invoke(cli, ['auth', '--help'])
        
        assert result.exit_code == 0
        assert 'login' in result.output
        assert 'logout' in result.output
        assert 'status' in result.output
    
    def test_feed_help(self):
        """Test feed subcommand help."""
        runner = CliRunner()
        result = runner.invoke(cli, ['feed', '--help'])
        
        assert result.exit_code == 0
        assert 'personal' in result.output
        assert 'public' in result.output
    
    def test_post_help(self):
        """Test post subcommand help."""
        runner = CliRunner()
        result = runner.invoke(cli, ['post', '--help'])
        
        assert result.exit_code == 0
        assert 'create' in result.output
        assert 'get' in result.output
        assert 'delete' in result.output
        assert 'like' in result.output