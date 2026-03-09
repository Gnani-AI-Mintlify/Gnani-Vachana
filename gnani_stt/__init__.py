"""Gnani STT - Python client for Gnani's multilingual Speech-to-Text API."""

from gnani_stt.client import GnaniSTTClient
from gnani_stt.exceptions import (
    GnaniSTTError,
    AuthenticationError,
    InvalidAudioError,
    APIError,
)

__version__ = "0.1.2"
__all__ = [
    "GnaniSTTClient",
    "GnaniSTTError",
    "AuthenticationError",
    "InvalidAudioError",
    "APIError",
]
