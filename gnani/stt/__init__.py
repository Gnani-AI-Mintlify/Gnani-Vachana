"""Gnani STT - Python client for Gnani's multilingual Speech-to-Text API."""

from gnani.stt.client import GnaniSTTClient
from gnani.stt.exceptions import (
    GnaniSTTError,
    AuthenticationError,
    InvalidAudioError,
    APIError,
)

__version__ = "0.1.3"
__all__ = [
    "GnaniSTTClient",
    "GnaniSTTError",
    "AuthenticationError",
    "InvalidAudioError",
    "APIError",
]
