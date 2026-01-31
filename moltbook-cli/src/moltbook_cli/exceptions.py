"""Custom exceptions for Moltbook CLI."""


class MoltbookCLIError(Exception):
    """Base exception for Moltbook CLI errors."""
    pass


class MoltbookAPIError(MoltbookCLIError):
    """Exception raised for API-related errors."""
    pass


class AuthenticationError(MoltbookAPIError):
    """Exception raised for authentication errors."""
    pass


class RateLimitError(MoltbookAPIError):
    """Exception raised when rate limit is exceeded."""
    pass


class ConfigurationError(MoltbookCLIError):
    """Exception raised for configuration errors."""
    pass


class ValidationError(MoltbookCLIError):
    """Exception raised for validation errors."""
    pass