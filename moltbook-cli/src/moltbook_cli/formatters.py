"""Output formatters for Moltbook CLI."""

import json
import yaml
from datetime import datetime
from typing import Any, Dict, List, Optional
from colorama import Fore, Back, Style, init

init(autoreset=True)


class BaseFormatter:
    """Base formatter class."""
    
    def format(self, data: Any) -> str:
        """Format data for output."""
        raise NotImplementedError


class TableFormatter(BaseFormatter):
    """Format data as a table."""
    
    def __init__(self, colors: bool = True):
        self.colors = colors
    
    def format_post(self, post: Dict[str, Any]) -> str:
        """Format a single post."""
        lines = []
        
        # Header with author and timestamp
        author = post.get('author', 'Unknown')
        created_at = post.get('created_at', '')
        post_id = post.get('id', '')
        
        if self.colors:
            header = f"{Fore.CYAN}{author}{Style.RESET_ALL} • {Fore.GRAY}{created_at}{Style.RESET_ALL}"
            post_id_colored = f"{Fore.YELLOW}[{post_id}]{Style.RESET_ALL}"
        else:
            header = f"{author} • {created_at}"
            post_id_colored = f"[{post_id}]"
        
        lines.append(f"{post_id_colored} {header}")
        
        # Content
        content = post.get('content', '')
        lines.append(f"  {content}")
        
        # Stats
        likes = post.get('likes', 0)
        replies = post.get('replies', 0)
        reposts = post.get('reposts', 0)
        
        if self.colors:
            stats = f"  {Fore.RED}♥ {likes}{Style.RESET_ALL}  {Fore.BLUE}↩ {replies}{Style.RESET_ALL}  {Fore.GREEN}↻ {reposts}{Style.RESET_ALL}"
        else:
            stats = f"  ♥ {likes}  ↩ {replies}  ↻ {reposts}"
        
        lines.append(stats)
        lines.append("")  # Empty line for separation
        
        return "\n".join(lines)
    
    def format_user(self, user: Dict[str, Any]) -> str:
        """Format a single user."""
        username = user.get('username', 'Unknown')
        display_name = user.get('display_name', '')
        bio = user.get('bio', '')
        followers = user.get('followers_count', 0)
        following = user.get('following_count', 0)
        posts = user.get('posts_count', 0)
        
        if self.colors:
            header = f"{Fore.CYAN}@{username}{Style.RESET_ALL}"
            if display_name:
                header += f" ({Fore.GREEN}{display_name}{Style.RESET_ALL})"
        else:
            header = f"@{username}"
            if display_name:
                header += f" ({display_name})"
        
        lines = [header]
        
        if bio:
            lines.append(f"  {bio}")
        
        if self.colors:
            stats = f"  {Fore.YELLOW}{followers} followers{Style.RESET_ALL} • {Fore.BLUE}{following} following{Style.RESET_ALL} • {Fore.GREEN}{posts} posts{Style.RESET_ALL}"
        else:
            stats = f"  {followers} followers • {following} following • {posts} posts"
        
        lines.append(stats)
        lines.append("")
        
        return "\n".join(lines)
    
    def format_analytics(self, analytics: Dict[str, Any]) -> str:
        """Format analytics data."""
        lines = []
        
        if self.colors:
            title = f"{Fore.MAGENTA}📊 Moltbook Analytics{Style.RESET_ALL}"
        else:
            title = "📊 Moltbook Analytics"
        
        lines.append(title)
        lines.append("=" * 40)
        
        # Posts stats
        posts_created = analytics.get('posts_created', 0)
        total_likes = analytics.get('total_likes', 0)
        total_replies = analytics.get('total_replies', 0)
        total_reposts = analytics.get('total_reposts', 0)
        
        if self.colors:
            lines.append(f"{Fore.CYAN}Posts Created:{Style.RESET_ALL} {posts_created}")
            lines.append(f"{Fore.RED}Total Likes:{Style.RESET_ALL} {total_likes}")
            lines.append(f"{Fore.BLUE}Total Replies:{Style.RESET_ALL} {total_replies}")
            lines.append(f"{Fore.GREEN}Total Reposts:{Style.RESET_ALL} {total_reposts}")
        else:
            lines.append(f"Posts Created: {posts_created}")
            lines.append(f"Total Likes: {total_likes}")
            lines.append(f"Total Replies: {total_replies}")
            lines.append(f"Total Reposts: {total_reposts}")
        
        # Engagement rate
        engagement_rate = analytics.get('engagement_rate', 0)
        lines.append(f"Engagement Rate: {engagement_rate:.2f}%")
        
        # Top posts
        top_posts = analytics.get('top_posts', [])
        if top_posts:
            lines.append("")
            if self.colors:
                lines.append(f"{Fore.YELLOW}🏆 Top Posts:{Style.RESET_ALL}")
            else:
                lines.append("🏆 Top Posts:")
            
            for i, post in enumerate(top_posts[:5], 1):
                content = post.get('content', '')[:50] + "..." if len(post.get('content', '')) > 50 else post.get('content', '')
                likes = post.get('likes', 0)
                if self.colors:
                    lines.append(f"  {i}. {Fore.CYAN}{content}{Style.RESET_ALL} ({Fore.RED}{likes} likes{Style.RESET_ALL})")
                else:
                    lines.append(f"  {i}. {content} ({likes} likes)")
        
        return "\n".join(lines)
    
    def format(self, data: Any) -> str:
        """Format data based on its type."""
        if isinstance(data, dict):
            if 'content' in data and 'author' in data:
                return self.format_post(data)
            elif 'username' in data:
                return self.format_user(data)
            elif 'posts_created' in data:
                return self.format_analytics(data)
            else:
                # Generic dict formatting
                lines = []
                for key, value in data.items():
                    if self.colors:
                        lines.append(f"{Fore.CYAN}{key}:{Style.RESET_ALL} {value}")
                    else:
                        lines.append(f"{key}: {value}")
                return "\n".join(lines)
        elif isinstance(data, list):
            return "\n".join(self.format(item) for item in data)
        else:
            return str(data)


class JSONFormatter(BaseFormatter):
    """Format data as JSON."""
    
    def format(self, data: Any) -> str:
        """Format data as JSON."""
        return json.dumps(data, indent=2, ensure_ascii=False)


class YAMLFormatter(BaseFormatter):
    """Format data as YAML."""
    
    def format(self, data: Any) -> str:
        """Format data as YAML."""
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)


class FormatterFactory:
    """Factory for creating formatters."""
    
    FORMATTERS = {
        'table': TableFormatter,
        'json': JSONFormatter,
        'yaml': YAMLFormatter,
    }
    
    @classmethod
    def create(cls, format_type: str, **kwargs) -> BaseFormatter:
        """Create a formatter instance."""
        formatter_class = cls.FORMATTERS.get(format_type.lower())
        if not formatter_class:
            raise ValueError(f"Unknown format type: {format_type}")
        
        return formatter_class(**kwargs)


def format_output(data: Any, format_type: str = 'table', colors: bool = True) -> str:
    """Format data for output."""
    formatter = FormatterFactory.create(format_type, colors=colors)
    return formatter.format(data)