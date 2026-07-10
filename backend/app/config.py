import os
from typing import Optional, Tuple

from dotenv import load_dotenv


load_dotenv()


def _positive_int(name: str, default: int) -> int:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    try:
        value = int(raw_value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be a positive integer.") from exc

    if value <= 0:
        raise RuntimeError(f"{name} must be a positive integer.")
    return value


def _positive_float(name: str, default: float) -> float:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    try:
        value = float(raw_value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be a positive number.") from exc

    if value <= 0:
        raise RuntimeError(f"{name} must be a positive number.")
    return value


def parse_cors_origins(raw_value: Optional[str]) -> Tuple[str, ...]:
    default_origins = (
        "http://localhost:5173",
        "https://official-letter-assistant.vercel.app",
    )
    if not raw_value:
        return default_origins

    origins = []
    for raw_origin in raw_value.split(","):
        origin = raw_origin.strip().rstrip("/")
        if origin and origin not in origins:
            origins.append(origin)

    if not origins:
        raise RuntimeError("CORS_ORIGINS must contain at least one origin.")
    return tuple(origins)


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").strip().lower()
OPENAI_API_KEY = (os.getenv("OPENAI_API_KEY") or "").strip() or None
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o").strip()
OPENAI_TIMEOUT_SECONDS = _positive_float("OPENAI_TIMEOUT_SECONDS", 60.0)
OPENAI_MAX_RETRIES = _positive_int("OPENAI_MAX_RETRIES", 1)
OPENAI_ANALYSIS_MAX_OUTPUT_TOKENS = _positive_int(
    "OPENAI_ANALYSIS_MAX_OUTPUT_TOKENS", 3_000
)
OPENAI_FOLLOWUP_MAX_OUTPUT_TOKENS = _positive_int(
    "OPENAI_FOLLOWUP_MAX_OUTPUT_TOKENS", 1_000
)
OPENAI_CHAT_MAX_OUTPUT_TOKENS = _positive_int(
    "OPENAI_CHAT_MAX_OUTPUT_TOKENS", 1_000
)
OPENAI_REPLY_MAX_OUTPUT_TOKENS = _positive_int(
    "OPENAI_REPLY_MAX_OUTPUT_TOKENS", 1_500
)

CORS_ORIGINS = parse_cors_origins(os.getenv("CORS_ORIGINS"))

MAX_LETTER_TEXT_CHARS = _positive_int("MAX_LETTER_TEXT_CHARS", 100_000)
MAX_UPLOAD_BYTES = _positive_int("MAX_UPLOAD_BYTES", 10 * 1024 * 1024)
MAX_PDF_PAGES = _positive_int("MAX_PDF_PAGES", 20)
