import hashlib
import hmac
import os
import re
from pathlib import Path

from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import FileResponse

from backend_api.cleanup import cleanup_audio_files
from backend_api.schemas import DemoCompareResponse, Instruction
from pronunciation_engine.normalizer import normalize_instruction
from pronunciation_engine.pronunciation_hints import apply_pronunciation_hints
from pronunciation_engine.translation_engine import (
    SUPPORTED_NATIVE_LANGUAGES,
    translate_navigation_text,
)
from pronunciation_engine.tts_engine import text_to_speech_file

router = APIRouter()

GENERATED_AUDIO_DIR = Path("backend_api/generated_audio")
GENERATED_AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def _slugify(text: str, max_len: int = 40) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text[:max_len] if text else "sample"


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _safe_audio_path(filename: str) -> Path:
    """Prevent path traversal by allowing only direct filenames in the audio dir."""
    requested = (GENERATED_AUDIO_DIR / filename).resolve()
    base_dir = GENERATED_AUDIO_DIR.resolve()

    if not str(requested).startswith(str(base_dir)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid audio filename",
        )

    return requested


def _validate_admin_token(x_admin_token: str | None) -> None:
    expected_token = os.getenv("ADMIN_CLEANUP_TOKEN")

    if not expected_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ADMIN_CLEANUP_TOKEN is not configured",
        )

    if not x_admin_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Admin-Token header",
        )

    if not hmac.compare_digest(x_admin_token, expected_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin token",
        )


@router.post("/normalize")
def normalize(data: Instruction):
    normalized_text = normalize_instruction(data.instruction)
    return {"normalized": normalized_text}


@router.get("/audio/{filename}")
def get_audio(filename: str):
    file_path = _safe_audio_path(filename)

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio file not found",
        )

    return FileResponse(
        path=str(file_path),
        media_type="audio/wav",
        filename=file_path.name,
    )


@router.post("/demo/compare", response_model=DemoCompareResponse)
def compare_audio(data: Instruction):
    cleanup_result_before = None
    cleanup_result_after = None

    try:
        cleanup_result_before = cleanup_audio_files()

        original_text = data.instruction.strip()

        if not original_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Instruction cannot be empty",
            )

        if (
            data.target_language_code
            and data.target_language_code not in SUPPORTED_NATIVE_LANGUAGES
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported target language: {data.target_language_code}",
            )

        normalized_text = normalize_instruction(original_text)
        speech_text = apply_pronunciation_hints(normalized_text)

        raw_slug = _slugify(original_text)
        normalized_slug = _slugify(speech_text)

        raw_hash = _hash_text("raw::" + original_text)
        normalized_hash = _hash_text("normalized::" + speech_text)

        raw_file = GENERATED_AUDIO_DIR / f"raw_{raw_slug}_{raw_hash}.wav"
        normalized_file = (
            GENERATED_AUDIO_DIR
            / f"normalized_{normalized_slug}_{normalized_hash}.wav"
        )

        text_to_speech_file(
            text=original_text,
            filename=str(raw_file),
            language_code="en-IN",
            speaker=None,
            use_cache=True,
        )

        text_to_speech_file(
            text=speech_text,
            filename=str(normalized_file),
            language_code="en-IN",
            speaker=None,
            use_cache=True,
        )

        translated_text = None
        native_audio_url = None
        native_audio_error = None
        target_language_name = None

        if data.target_language_code:
            target_language_name = SUPPORTED_NATIVE_LANGUAGES.get(
                data.target_language_code
            )

            if not target_language_name:
                native_audio_error = (
                    f"Unsupported native language: "
                    f"{data.target_language_code}"
                )

            else:
                try:
                    # Translate the normalized instruction rather than the
                    # raw text so numbers, distances and abbreviations have
                    # already been expanded.
                    translated_text = translate_navigation_text(
                        normalized_text,
                        data.target_language_code,
                    )

                    native_slug = _slugify(
                        f"{target_language_name}_{original_text}",
                        max_len=50,
                    )

                    native_hash = _hash_text(
                        f"native::{data.target_language_code}::{translated_text}"
                    )

                    native_file = (
                        GENERATED_AUDIO_DIR
                        / (
                            f"native_{data.target_language_code}_"
                            f"{native_slug}_{native_hash}.wav"
                        )
                    )

                    # The pronunciation dictionary is currently intended
                    # for the English pronunciation path. Native-script
                    # TTS uses the selected language directly.
                    text_to_speech_file(
                        text=translated_text,
                        filename=str(native_file),
                        language_code=data.target_language_code,
                        speaker=None,
                        use_cache=True,
                        use_pronunciation_dictionary=False,
                    )

                    native_audio_url = f"/audio/{native_file.name}"

                except Exception as native_exc:
                    print(
                        "Native-language generation failed:",
                        {
                            "language": data.target_language_code,
                            "error": str(native_exc),
                        },
                    )

                    native_audio_error = (
                        f"{target_language_name} audio "
                        "could not be generated."
                    )

        return DemoCompareResponse(
            original_text=original_text,
            normalized_text=normalized_text,
            speech_text=speech_text,
            raw_audio_url=f"/audio/{raw_file.name}",
            normalized_audio_url=f"/audio/{normalized_file.name}",
            target_language_code=data.target_language_code,
            target_language_name=target_language_name,
            translated_text=translated_text,
            native_audio_url=native_audio_url,
            native_audio_error=native_audio_error,
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate comparison audio: {str(exc)}",
        )

    finally:
        try:
            cleanup_result_after = cleanup_audio_files()
            print(
                "Audio cleanup complete",
                {
                    "before": cleanup_result_before,
                    "after": cleanup_result_after,
                },
            )
        except Exception as cleanup_exc:
            print(f"Audio cleanup failed: {cleanup_exc}")


@router.post("/admin/cleanup-audio")
def admin_cleanup_audio(x_admin_token: str | None = Header(default=None)):
    _validate_admin_token(x_admin_token)
    return cleanup_audio_files()
