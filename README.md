# gnani-vachana
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Official Python client for the **[Vachana Speech-to-Text API](https://docs.inya.ai/vachana/introduction/introduction)** by [Gnani.ai](https://gnani.ai). Transcribe audio in 10 Indian languages with a single function call.

> **Vachana** is a production-ready speech-to-text API with automatic language detection and code-switching support for accurate multilingual transcriptions.

## Installation

```bash
pip install gnani-vachana
```

Requires **Python 3.9+**.

## Quick Start

```python
from gnani.stt import GnaniSTTClient

client = GnaniSTTClient(
    organization_id="your-organization-id",
    api_key="your-api-key",
    user_id="your-user-id",
)

result = client.transcribe("audio.wav", language_code="hi-IN")
print(result["transcript"])
```

## Authentication

The Vachana API uses header-based authentication. Every request requires three credentials:

| Parameter          | Header              | Description                        |
|--------------------|---------------------|------------------------------------|
| `organization_id`  | `X-Organization-ID` | Your organisation identifier       |
| `api_key`          | `X-API-Key-ID`      | Secret key for authentication      |
| `user_id`          | `X-API-User-ID`     | Your user / organisation name      |

### Obtaining Credentials

Email **[speechstack@gnani.ai](mailto:speechstack@gnani.ai)** with your name, company, and use case. Credentials are typically provisioned within 1 business day, and all new accounts receive **free credits** -- no credit card required.

### Passing Credentials

**Option 1 -- Constructor arguments:**

```python
client = GnaniSTTClient(
    organization_id="your-organization-id",
    api_key="your-api-key",
    user_id="your-user-id",
)
```

**Option 2 -- Environment variables:**

```bash
export GNANI_ORGANIZATION_ID="your-organization-id"
export GNANI_API_KEY="your-api-key"
export GNANI_USER_ID="your-user-id"
```

```python
client = GnaniSTTClient()
```

## Supported Languages

| Language        | Code          | Native Script |
|-----------------|---------------|---------------|
| Bengali         | `bn-IN`       | বাংলা         |
| English (India) | `en-IN`       | Latin         |
| Gujarati        | `gu-IN`       | ગુજરાતી       |
| Hindi           | `hi-IN`       | हिन्दी         |
| Kannada         | `kn-IN`       | ಕನ್ನಡ          |
| Malayalam       | `ml-IN`       | മലയാളം        |
| Marathi         | `mr-IN`       | मराठी          |
| Punjabi         | `pa-IN`       | ਪੰਜਾਬੀ        |
| Tamil           | `ta-IN`       | தமிழ்          |
| Telugu          | `te-IN`       | తెలుగు         |

For **multilingual / code-switching** audio (e.g. Hindi-English mix), pass a comma-separated code:

```python
result = client.transcribe("meeting.wav", language_code="en-IN,hi-IN")
```

## Usage

### Transcribe a file by path

```python
result = client.transcribe("meeting.wav", language_code="en-IN")
print(result["transcript"])
```

### Transcribe from a file object

```python
with open("meeting.mp3", "rb") as f:
    result = client.transcribe(f, language_code="ta-IN")
```

### Transcribe raw bytes

```python
audio_bytes = download_audio_from_somewhere()
result = client.transcribe_bytes(
    audio_bytes, filename="clip.wav", language_code="kn-IN"
)
```

### Custom request ID

```python
result = client.transcribe(
    "call.flac", language_code="hi-IN", request_id="my-trace-123"
)
```

### List supported languages

```python
for code, name in GnaniSTTClient.supported_languages().items():
    print(f"{code}: {name}")
```

## Audio Requirements

| Constraint       | Value                                      |
|------------------|--------------------------------------------|
| Formats          | WAV, MP3, FLAC, OGG, M4A                  |
| Max duration     | 60 seconds                                 |
| Channels         | Mono or stereo                             |
| Sample rate      | Automatically converted to 16 kHz mono     |

## Response Format

```json
{
  "success": true,
  "request_id": "req_abc123",
  "timestamp": "20251226_143052.123",
  "transcript": "नमस्ते, आप कैसे हैं?"
}
```

## Error Handling

```python
from gnani.stt import AuthenticationError, InvalidAudioError, APIError

try:
    result = client.transcribe("audio.wav", language_code="hi-IN")
except AuthenticationError:
    print("Check your credentials")
except InvalidAudioError as e:
    print(f"Bad audio file: {e}")
except APIError as e:
    print(f"API error {e.status_code}: {e}")
```

## Documentation

Full API reference and guides are available at **[docs.inya.ai/vachana](https://docs.inya.ai/vachana/introduction/introduction)**.

## License

This project is licensed under the MIT License -- see the [LICENSE](LICENSE) file for details.
