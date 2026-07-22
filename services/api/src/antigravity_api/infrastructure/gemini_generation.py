import json
from json import JSONDecodeError
from typing import Any, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from pydantic import SecretStr


class GeminiGeneration:
    def __init__(self, *, api_key: Optional[SecretStr], model: str) -> None:
        self._api_key = api_key
        self._model = model

    def generate_json(self, *, prompt: str) -> dict[str, object]:
        if self._api_key is None:
            return {
                "status": "configuration_required",
                "agent_log": [
                    "Gemini API key is not configured, so MadeThis prepared a deterministic draft for local review."
                ],
            }

        endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self._model}:"
            f"generateContent?key={self._api_key.get_secret_value()}"
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "responseMimeType": "application/json",
            },
        }
        request = Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=35) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, JSONDecodeError) as exc:
            return {
                "status": "model_unavailable",
                "agent_log": [f"Gemini request did not complete: {type(exc).__name__}."],
            }

        text = _extract_text(response_payload)
        try:
            parsed = json.loads(text)
        except JSONDecodeError:
            return {
                "status": "model_parse_error",
                "agent_log": ["Gemini returned content that was not valid JSON."],
            }

        if isinstance(parsed, dict):
            return parsed

        return {
            "status": "model_parse_error",
            "agent_log": ["Gemini returned JSON, but not an object."],
        }


def _extract_text(response_payload: dict[str, Any]) -> str:
    candidates = response_payload.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        return "{}"
    first_candidate = candidates[0]
    if not isinstance(first_candidate, dict):
        return "{}"
    content = first_candidate.get("content")
    if not isinstance(content, dict):
        return "{}"
    parts = content.get("parts")
    if not isinstance(parts, list):
        return "{}"
    text_parts = [part.get("text", "") for part in parts if isinstance(part, dict)]
    return "".join(text_parts).strip()
