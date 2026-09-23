import base64
import hashlib
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from sarvamai import SarvamAI

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(
    dotenv_path=ENV_PATH,
    override=True,
)

api_key = os.getenv("SARVAM_API_KEY")

if not api_key:
    raise RuntimeError("SARVAM_API_KEY is not set")

client = SarvamAI(api_subscription_key=api_key)

CACHE_DIR = Path("scripts/audio_outputs/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_MODEL = os.getenv("SARVAM_TTS_MODEL", "bulbul:v3")
DEFAULT_SPEAKER = os.getenv("SARVAM_TTS_SPEAKER", "shubh")
DEFAULT_PACE = float(os.getenv("SARVAM_TTS_PACE", "0.9"))
DEFAULT_TEMPERATURE = float(os.getenv("SARVAM_TTS_TEMPERATURE", "0.2"))
DEFAULT_DICT_ID = os.getenv("SARVAM_PRONUNCIATION_DICT_ID")


def _build_cache_key(
    text: str,
    language_code: str,
    speaker: str,
    model: str,
    pace: float,
    temperature: float,
    dict_id: str | None,
) -> str:
    payload = {
        "text": text,
        "language_code": language_code,
        "speaker": speaker,
        "model": model,
        "pace": pace,
        "temperature": temperature,
        "dict_id": dict_id,
    }

    raw = json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
    ).encode("utf-8")

    return hashlib.sha256(raw).hexdigest()


def _cache_path_from_key(cache_key: str) -> Path:
    return CACHE_DIR / f"{cache_key}.wav"


def _extract_audio_bytes(response) -> bytes:
    if not hasattr(response, "audios") or not response.audios:
        raise RuntimeError(
            f"Sarvam TTS response did not contain audio: {response}"
        )

    audio_base64 = response.audios[0]

    if isinstance(audio_base64, bytes):
        return audio_base64

    if isinstance(audio_base64, str):
        return base64.b64decode(audio_base64)

    raise RuntimeError(
        f"Unsupported audio payload type: {type(audio_base64)}"
    )


def text_to_speech_file(
    text: str,
    filename: str,
    language_code: str = "en-IN",
    speaker: str | None = None,
    use_cache: bool = True,
    model: str | None = None,
    pace: float | None = None,
    temperature: float | None = None,
    dict_id: str | None = None,
    use_pronunciation_dictionary: bool = False,
) -> str:
    if not isinstance(text, str):
        raise TypeError(
            f"text must be a string, got {type(text).__name__}"
        )

    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    resolved_model = model or DEFAULT_MODEL
    resolved_speaker = speaker or DEFAULT_SPEAKER
    resolved_pace = DEFAULT_PACE if pace is None else pace
    resolved_temperature = (
        DEFAULT_TEMPERATURE
        if temperature is None
        else temperature
    )

    resolved_dict_id = (
        (dict_id or DEFAULT_DICT_ID)
        if use_pronunciation_dictionary
        else None
    )

    cache_key = _build_cache_key(
        text=text,
        language_code=language_code,
        speaker=resolved_speaker,
        model=resolved_model,
        pace=resolved_pace,
        temperature=resolved_temperature,
        dict_id=resolved_dict_id,
    )

    cached_file = _cache_path_from_key(cache_key)

    if use_cache and cached_file.exists():
        output_path.write_bytes(cached_file.read_bytes())
        return str(output_path)

    tts_kwargs = {
        "text": text,
        "language_code": language_code,
        "speaker": resolved_speaker,
        "model": resolved_model,
        "pace": resolved_pace,
        "temperature": resolved_temperature,
    }

    if resolved_dict_id:
        tts_kwargs["dict_id"] = resolved_dict_id

    print(
        "Sarvam TTS request:",
        {
            "language_code": language_code,
            "speaker": resolved_speaker,
            "model": resolved_model,
            "pace": resolved_pace,
            "temperature": resolved_temperature,
            "has_dict_id": bool(resolved_dict_id),
        },
    )

    response = client.text_to_speech.convert(**tts_kwargs)

    audio_bytes = _extract_audio_bytes(response)

    cached_file.write_bytes(audio_bytes)
    output_path.write_bytes(audio_bytes)

    return str(output_path)