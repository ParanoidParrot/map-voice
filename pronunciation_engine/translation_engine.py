import os

from dotenv import load_dotenv
from sarvamai import SarvamAI
from pathlib import Path

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

SUPPORTED_NATIVE_LANGUAGES = {
    "kn-IN": "Kannada",
    "te-IN": "Telugu",
    "ta-IN": "Tamil",
    "mr-IN": "Marathi",
    "bn-IN": "Bengali",
    "gu-IN": "Gujarati",
    "hi-IN": "Hindi"
}

DEFAULT_TRANSLATION_MODEL = os.getenv(
    "SARVAM_TRANSLATION_MODEL",
    "sarvam-translate:v1",
)


def translate_navigation_text(
    text: str,
    target_language_code: str,
) -> str:
    """Translate an English navigation instruction into a supported Indian language."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")

    if target_language_code not in SUPPORTED_NATIVE_LANGUAGES:
        raise ValueError(
            f"Unsupported target language: {target_language_code}. "
            f"Supported: {', '.join(SUPPORTED_NATIVE_LANGUAGES)}"
        )

    response = client.text.translate(
        input=text.strip(),
        source_language_code="en-IN",
        target_language_code=target_language_code,
        model=DEFAULT_TRANSLATION_MODEL,
    )

    translated_text = getattr(response, "translated_text", None)

    if not translated_text:
        raise RuntimeError(f"Sarvam translation returned no translated_text: {response}")

    return translated_text.strip()
