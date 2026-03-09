"""Core client for the Gnani Speech-to-Text API."""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import BinaryIO, Union

import requests

from gnani.stt.exceptions import (
    AuthenticationError,
    InvalidAudioError,
    APIError,
)

SUPPORTED_LANGUAGES = {
    "en-IN": "English (India)",
    "hi-IN": "Hindi",
    "gu-IN": "Gujarati",
    "ta-IN": "Tamil",
    "kn-IN": "Kannada",
    "te-IN": "Telugu",
    "mr-IN": "Marathi",
    "bn-IN": "Bengali",
    "ml-IN": "Malayalam",
    "pa-IN": "Punjabi",
    "en-IN,hi-IN": "English-Hindi",
}

SUPPORTED_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}

DEFAULT_BASE_URL = "https://api.vachana.ai"
STT_ENDPOINT = "/stt/v3"


class GnaniSTTClient:
    """Client for Gnani's multilingual Speech-to-Text REST API.

    Parameters
    ----------
    organization_id : str
        Your unique organisation identifier (``X-Organization-ID``).
    api_key : str
        Your secret API key (``X-API-Key-ID``).
    user_id : str
        Your user / organisation name (``X-API-User-ID``).
    base_url : str, optional
        Override the default API base URL.
    timeout : int, optional
        Request timeout in seconds. Defaults to 60.
    """

    def __init__(
        self,
        organization_id: str | None = None,
        api_key: str | None = None,
        user_id: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 60,
    ):
        self.organization_id = organization_id or os.getenv("GNANI_ORGANIZATION_ID", "")
        self.api_key = api_key or os.getenv("GNANI_API_KEY", "")
        self.user_id = user_id or os.getenv("GNANI_USER_ID", "")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        if not self.organization_id or not self.api_key or not self.user_id:
            raise AuthenticationError(
                "organization_id, api_key, and user_id are required. "
                "Pass them directly or set GNANI_ORGANIZATION_ID, GNANI_API_KEY, "
                "and GNANI_USER_ID environment variables."
            )

    def _build_headers(self, request_id: str | None = None) -> dict[str, str]:
        return {
            "X-Organization-ID": self.organization_id,
            "X-API-Key-ID": self.api_key,
            "X-API-User-ID": self.user_id,
            "X-API-Request-ID": request_id or f"req_{uuid.uuid4().hex[:12]}",
        }

    def transcribe(
        self,
        audio: Union[str, Path, BinaryIO],
        language_code: str = "en-IN",
        *,
        request_id: str | None = None,
    ) -> dict:
        """Transcribe an audio file using Gnani STT.

        Parameters
        ----------
        audio : str | Path | file-like
            Path to an audio file, or an open file-like object (binary mode).
        language_code : str
            BCP-47 style language code. See ``SUPPORTED_LANGUAGES`` for the
            full list. Defaults to ``"en-IN"``.
        request_id : str, optional
            Custom request ID for tracking. Auto-generated if omitted.

        Returns
        -------
        dict
            The parsed JSON response from the API, containing at minimum
            ``success``, ``request_id``, ``timestamp``, and ``transcript``.

        Raises
        ------
        InvalidAudioError
            If the file extension is not supported or the file cannot be read.
        APIError
            If the API returns a non-200 response.
        """
        if language_code not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language_code '{language_code}'. "
                f"Choose from: {', '.join(sorted(SUPPORTED_LANGUAGES))}"
            )

        headers = self._build_headers(request_id)
        file_handle = None
        should_close = False

        try:
            if isinstance(audio, (str, Path)):
                path = Path(audio)
                if not path.exists():
                    raise InvalidAudioError(f"Audio file not found: {path}")
                if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                    raise InvalidAudioError(
                        f"Unsupported audio format '{path.suffix}'. "
                        f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
                    )
                file_handle = open(path, "rb")
                should_close = True
            else:
                file_handle = audio

            url = f"{self.base_url}{STT_ENDPOINT}"
            files = {"audio_file": file_handle}
            data = {"language_code": language_code}

            response = requests.post(
                url,
                headers=headers,
                files=files,
                data=data,
                timeout=self.timeout,
            )
        finally:
            if should_close and file_handle is not None:
                file_handle.close()

        if response.status_code != 200:
            raise APIError(response.status_code, response.text)

        return response.json()

    def transcribe_bytes(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        language_code: str = "en-IN",
        *,
        request_id: str | None = None,
    ) -> dict:
        """Transcribe raw audio bytes.

        Parameters
        ----------
        audio_bytes : bytes
            Raw audio content.
        filename : str
            Filename hint so the server can infer the format.
        language_code : str
            Target language code.
        request_id : str, optional
            Custom request ID.

        Returns
        -------
        dict
            Parsed JSON response from the API.
        """
        if language_code not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language_code '{language_code}'. "
                f"Choose from: {', '.join(sorted(SUPPORTED_LANGUAGES))}"
            )

        headers = self._build_headers(request_id)
        url = f"{self.base_url}{STT_ENDPOINT}"
        files = {"audio_file": (filename, audio_bytes)}
        data = {"language_code": language_code}

        response = requests.post(
            url,
            headers=headers,
            files=files,
            data=data,
            timeout=self.timeout,
        )

        if response.status_code != 200:
            raise APIError(response.status_code, response.text)

        return response.json()

    @staticmethod
    def supported_languages() -> dict[str, str]:
        """Return a mapping of supported language codes to their names."""
        return dict(SUPPORTED_LANGUAGES)
