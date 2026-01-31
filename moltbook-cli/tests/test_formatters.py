"""Tests for formatters module."""

import pytest
from datetime import datetime

from moltbook_cli.formatters import TableFormatter, JSONFormatter, YAMLFormatter, format_output


class TestTableFormatter:
    """Test table formatter."""
    
    def test_format_post(self):
        """Test formatting a post."""
        formatter = TableFormatter(colors=False)
        
        post = {
            'id': '123',
            'author': 'testuser',
            'created_at': '2024-01-20 10:30:00',
            'content': 'This is a test post',
            'likes': 5,
            'replies': 2,
            'reposts': 1
        }
        
        result = formatter.format_post(post)
        
        assert '[123]' in result
        assert 'testuser' in result
        assert 'This is a test post' in result
        assert '♥ 5' in result
        assert '↩ 2' in result
        assert '↻ 1' in result
    
    def test_format_user(self):
        """Test formatting a user profile."""
        formatter = TableFormatter(colors=False)
        
        user = {
            'username': 'testuser',
            'display_name': 'Test User',
            'bio': 'This is my bio',
            'followers_count': 100,
            'following_count': 50,
            'posts_count': 25
        }
        
        result = formatter.format_user(user)
        
        assert '@testuser' in result
        assert 'Test User' in result
        assert 'This is my bio' in result
        assert '100 followers' in result
        assert '50 following' in result
        assert '25 posts' in result
    
    def test_format_analytics(self):
        """Test formatting analytics data."""
        formatter = TableFormatter(colors=False)
        
        analytics = {
            'posts_created': 10,
            'total_likes': 50,
            'total_replies': 20,
            'total_reposts': 5,
            'engagement_rate': 15.5,
            'top_posts': [
                {'content': 'Popular post 1', 'likes': 25},
                {'content': 'Popular post 2', 'likes': 20}
            ]
        }
        
        result = formatter.format_analytics(analytics)
        
        assert 'Moltbook Analytics' in result
        assert 'Posts Created: 10' in result
        assert 'Total Likes: 50' in result
        assert 'Engagement Rate: 15.50%' in result
        assert 'Top Posts:' in result


class TestJSONFormatter:
    """Test JSON formatter."""
    
    def test_format_dict(self):
        """Test formatting a dictionary as JSON."""
        formatter = JSONFormatter()
        
        data = {'key': 'value', 'number': 42}
        result = formatter.format(data)
        
        assert '"key": "value"' in result
        assert '"number": 42' in result
    
    def test_format_list(self):
        """Test formatting a list as JSON."""
        formatter = JSONFormatter()
        
        data = [{'id': 1}, {'id': 2}]
        result = formatter.format(data)
        
        assert '"id": 1' in result
        assert '"id": 2' in result


class TestYAMLFormatter:
    """Test YAML formatter."""
    
    def test_format_dict(self):
        """Test formatting a dictionary as YAML."""
        formatter = YAMLFormatter()
        
        data = {'key': 'value', 'number': 42}
        result = formatter.format(data)
        
        assert 'key: value' in result
        assert 'number: 42' in result


class TestFormatOutput:
    """Test the format_output function."""
    
    def test_format_output_table(self):
        """Test formatting output as table."""
        post = {
            'id': '123',
            'author': 'testuser',
            'created_at': '2024-01-20 10:30:00',
            'content': 'This is a test post',
            'likes': 5,
            'replies': 2,
            'reposts': 1
        }
        
        result = format_output(post, 'table', colors=False)
        
        assert 'testuser' in result
        assert 'This is a test post' in result
    
    def test_format_output_json(self):
        """Test formatting output as JSON."""
        data = {'key': 'value'}
        result = format_output(data, 'json')
        
        assert '"key": "value"' in result
    
    def test_format_output_yaml(self):
        """Test formatting output as YAML."""
        data = {'key': 'value'}
        result = format_output(data, 'yaml')
        
        assert 'key: value' in result