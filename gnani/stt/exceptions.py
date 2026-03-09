"""Custom exceptions for the Gnani STT client."""


class GnaniSTTError(Exception):
    """Base exception for all Gnani STT errors."""


class AuthenticationError(GnaniSTTError):
    """Raised when API authentication fails (missing or invalid credentials)."""


class InvalidAudioError(GnaniSTTError):
    """Raised when the provided audio file is invalid or unsupported."""


class APIError(GnaniSTTError):
    """Raised when the Gnani API returns a non-success response."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}: {message}")
