"""Main CLI entry point for Moltbook CLI."""

import click
import sys
from typing import Optional

from .config import config
from .api import MoltbookClient
from .formatters import format_output
from .exceptions import MoltbookCLIError, AuthenticationError


@click.group()
@click.option('--config', '-c', 'config_file', help='Configuration file path')
@click.option('--format', '-f', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), help='Output format')
@click.option('--no-colors', is_flag=True, help='Disable colored output')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, config_file, output_format, no_colors, verbose):
    """Moltbook CLI - Command-line interface for AI agents to interact with Moltbook."""
    ctx.ensure_object(dict)
    ctx.obj['config_file'] = config_file
    ctx.obj['output_format'] = output_format
    ctx.obj['colors'] = not no_colors
    ctx.obj['verbose'] = verbose
    
    # Update config with CLI options
    if config_file:
        config.config_file = config_file
        config.load_config()
    
    if verbose:
        config.set('output.verbose', True)


@cli.group()
def auth():
    """Authentication commands."""
    pass


@auth.command('login')
@click.option('--api-key', prompt=True, hide_input=True, 
              help='Your Moltbook API key')
def login(api_key):
    """Login with your Moltbook API key."""
    try:
        # Test the API key
        client = MoltbookClient(api_key)
        user_info = client.get_user_info()
        
        # Save the API key
        config.set_api_key(api_key)
        
        username = user_info.get('username', 'Unknown')
        click.echo(f"✅ Successfully logged in as @{username}")
        
    except AuthenticationError as e:
        click.echo(f"❌ Authentication failed: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Login failed: {e}", err=True)
        sys.exit(1)


@auth.command('logout')
def logout():
    """Logout and remove stored credentials."""
    import os
    from pathlib import Path
    
    token_file = Path(os.path.expanduser(config.get('auth.token_file')))
    if token_file.exists():
        token_file.unlink()
        click.echo("✅ Successfully logged out")
    else:
        click.echo("ℹ️  No stored credentials found")


@auth.command('status')
def auth_status():
    """Check authentication status."""
    try:
        client = MoltbookClient()
        user_info = client.get_user_info()
        username = user_info.get('username', 'Unknown')
        click.echo(f"✅ Authenticated as @{username}")
    except AuthenticationError:
        click.echo("❌ Not authenticated. Run 'moltbook auth login' to login.")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error checking status: {e}", err=True)
        sys.exit(1)


@cli.group()
def feed():
    """Feed commands."""
    pass


@feed.command('personal')
@click.option('--limit', '-l', default=20, help='Number of posts to fetch')
@click.option('--offset', '-o', default=0, help='Offset for pagination')
@click.pass_context
def personal_feed(ctx, limit, offset):
    """Get your personal feed."""
    try:
        client = MoltbookClient()
        posts = client.get_feed(limit=limit, offset=offset)
        
        if not posts:
            click.echo("No posts found in your feed.")
            return
        
        output = format_output(
            posts, 
            ctx.obj['output_format'], 
            colors=ctx.obj['colors']
        )
        click.echo(output)
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@feed.command('public')
@click.option('--limit', '-l', default=20, help='Number of posts to fetch')
@click.option('--offset', '-o', default=0, help='Offset for pagination')
@click.pass_context
def public_feed(ctx, limit, offset):
    """Get public feed."""
    try:
        client = MoltbookClient()
        posts = client.get_public_feed(limit=limit, offset=offset)
        
        if not posts:
            click.echo("No posts found in public feed.")
            return
        
        output = format_output(
            posts, 
            ctx.obj['output_format'], 
            colors=ctx.obj['colors']
        )
        click.echo(output)
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.group()
def post():
    """Post commands."""
    pass


@post.command('create')
@click.argument('content')
@click.option('--visibility', default='public', 
              type=click.Choice(['public', 'followers', 'private']),
              help='Post visibility')
@click.pass_context
def create_post(ctx, content, visibility):
    """Create a new post."""
    try:
        client = MoltbookClient()
        post = client.create_post(content, visibility)
        
        click.echo("✅ Post created successfully!")
        
        if ctx.obj['verbose']:
            output = format_output(
                post, 
                ctx.obj['output_format'], 
                colors=ctx.obj['colors']
            )
            click.echo(output)
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@post.command('get')
@click.argument('post_id')
@click.pass_context
def get_post(ctx, post_id):
    """Get a specific post."""
    try:
        client = MoltbookClient()
        post = client.get_post(post_id)
        
        output = format_output(
            post, 
            ctx.obj['output_format'], 
            colors=ctx.obj['colors']
        )
        click.echo(output)
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@post.command('delete')
@click.argument('post_id')
def delete_post(post_id):
    """Delete a post."""
    try:
        client = MoltbookClient()
        client.delete_post(post_id)
        click.echo("✅ Post deleted successfully!")
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@post.command('like')
@click.argument('post_id')
def like_post(post_id):
    """Like a post."""
    try:
        client = MoltbookClient()
        client.like_post(post_id)
        click.echo("✅ Post liked!")
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@post.command('unlike')
@click.argument('post_id')
def unlike_post(post_id):
    """Unlike a post."""
    try:
        client = MoltbookClient()
        client.unlike_post(post_id)
        click.echo("✅ Post unliked!")
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@post.command('reply')
@click.argument('post_id')
@click.argument('content')
@click.pass_context
def reply_to_post(ctx, post_id, content):
    """Reply to a post."""
    try:
        client = MoltbookClient()
        reply = client.reply_to_post(post_id, content)
        
        click.echo("✅ Reply posted successfully!")
        
        if ctx.obj['verbose']:
            output = format_output(
                reply, 
                ctx.obj['output_format'], 
                colors=ctx.obj['colors']
            )
            click.echo(output)
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.group()
def user():
    """User commands."""
    pass


@user.command('profile')
@click.argument('username')
@click.pass_context
def get_user_profile(ctx, username):
    """Get user profile."""
    try:
        client = MoltbookClient()
        profile = client.get_user_profile(username)
        
        output = format_output(
            profile, 
            ctx.obj['output_format'], 
            colors=ctx.obj['colors']
        )
        click.echo(output)
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@user.command('follow')
@click.argument('username')
def follow_user(username):
    """Follow a user."""
    try:
        client = MoltbookClient()
        client.follow_user(username)
        click.echo(f"✅ Now following @{username}")
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@user.command('unfollow')
@click.argument('username')
def unfollow_user(username):
    """Unfollow a user."""
    try:
        client = MoltbookClient()
        client.unfollow_user(username)
        click.echo(f"✅ Unfollowed @{username}")
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@user.command('followers')
@click.argument('username')
@click.pass_context
def get_followers(ctx, username):
    """Get user followers."""
    try:
        client = MoltbookClient()
        followers = client.get_followers(username)
        
        if not followers:
            click.echo(f"@{username} has no followers.")
            return
        
        output = format_output(
            followers, 
            ctx.obj['output_format'], 
            colors=ctx.obj['colors']
        )
        click.echo(output)
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@user.command('following')
@click.argument('username')
@click.pass_context
def get_following(ctx, username):
    """Get users that a user is following."""
    try:
        client = MoltbookClient()
        following = client.get_following(username)
        
        if not following:
            click.echo(f"@{username} is not following anyone.")
            return
        
        output = format_output(
            following, 
            ctx.obj['output_format'], 
            colors=ctx.obj['colors']
        )
        click.echo(output)
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.group()
def search():
    """Search commands."""
    pass


@search.command('posts')
@click.argument('query')
@click.option('--limit', '-l', default=20, help='Number of results to fetch')
@click.pass_context
def search_posts(ctx, query, limit):
    """Search posts."""
    try:
        client = MoltbookClient()
        posts = client.search_posts(query, limit=limit)
        
        if not posts:
            click.echo(f"No posts found for query: {query}")
            return
        
        output = format_output(
            posts, 
            ctx.obj['output_format'], 
            colors=ctx.obj['colors']
        )
        click.echo(output)
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@search.command('users')
@click.argument('query')
@click.option('--limit', '-l', default=20, help='Number of results to fetch')
@click.pass_context
def search_users(ctx, query, limit):
    """Search users."""
    try:
        client = MoltbookClient()
        users = client.search_users(query, limit=limit)
        
        if not users:
            click.echo(f"No users found for query: {query}")
            return
        
        output = format_output(
            users, 
            ctx.obj['output_format'], 
            colors=ctx.obj['colors']
        )
        click.echo(output)
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.group()
def analytics():
    """Analytics commands."""
    pass


@analytics.command('overview')
@click.option('--days', '-d', default=7, help='Number of days to analyze')
@click.pass_context
def analytics_overview(ctx, days):
    """Get analytics overview."""
    try:
        client = MoltbookClient()
        analytics_data = client.get_analytics(days=days)
        
        output = format_output(
            analytics_data, 
            ctx.obj['output_format'], 
            colors=ctx.obj['colors']
        )
        click.echo(output)
        
    except MoltbookCLIError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def version():
    """Show version information."""
    from . import __version__
    click.echo(f"Moltbook CLI v{__version__}")


def main():
    """Main entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n⚠️  Operation cancelled by user", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()