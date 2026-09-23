from pydantic import BaseModel


class Instruction(BaseModel):
    instruction: str
    target_language_code: str | None = None


class DemoCompareResponse(BaseModel):
    original_text: str
    normalized_text: str
    speech_text: str
    raw_audio_url: str
    normalized_audio_url: str
    
    target_language_code: str | None = None
    target_language_name: str | None = None
    translated_text: str | None = None
    native_audio_url: str | None = None
    native_audio_error: str | None = None
