import json
from typing import Iterator, Union

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.config import MAX_LETTER_TEXT_CHARS, MAX_UPLOAD_BYTES
from app.schemas.analysis import (
    AnalyzeTextRequest,
    AnalyzeTextResponse,
    ChatRequest,
    FollowUpRequest,
    FollowUpResponse,
    InvalidLetterResponse,
    ReplyDraftRequest,
    ReplyDraftResponse,
    TranslateRequest,
)
from app.schemas.common import OutputLanguage
from app.services.analysis_service import analyze_letter_text
from app.services.pdf_service import extract_text_from_pdf_bytes, extract_text_from_image_bytes
from app.services.followup_service import answer_followup_question
from app.services.llm_service import (
    LLMConfigurationError,
    chat_with_llm_stream,
    generate_reply_draft,
    require_llm_config,
)

router = APIRouter()

LLM_UNAVAILABLE_DETAIL = "The language model service is not configured."

REPLY_DRAFT_REQUESTED = "REPLY_DRAFT_REQUESTED"
REPLY_OPTIONS = [
    "already_completed",
    "need_more_time_or_question",
    "disagree",
]
REPLY_INTENT_INSTRUCTIONS = {
    "already_completed": "I already took care of it",
    "need_more_time_or_question": "I need more time or have a question",
    "disagree": "I disagree with this letter",
}


class EventStreamResponse(StreamingResponse):
    media_type = "text/event-stream"


def analyze_letter_or_raise_http_error(
    letter_text: str,
    output_language: OutputLanguage = "English",
) -> Union[AnalyzeTextResponse, InvalidLetterResponse]:
    try:
        return analyze_letter_text(
            letter_text=letter_text,
            output_language=output_language,
        )
    except LLMConfigurationError as error:
        raise HTTPException(
            status_code=503,
            detail=LLM_UNAVAILABLE_DETAIL,
        ) from error
    except ValueError as error:
        raise HTTPException(
            status_code=502,
            detail="LLM response failed backend validation.",
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Letter analysis request failed.",
        ) from error


ALLOWED_CONTENT_TYPES = ["application/pdf", "image/jpeg", "image/png"]
FILE_SIGNATURES = {
    "application/pdf": (b"%PDF-",),
    "image/jpeg": (b"\xff\xd8\xff",),
    "image/png": (b"\x89PNG\r\n\x1a\n",),
}


def upload_matches_content_type(content_type: str, file_bytes: bytes) -> bool:
    return any(
        file_bytes.startswith(signature)
        for signature in FILE_SIGNATURES[content_type]
    )


@router.post("/analyze-text", response_model=Union[AnalyzeTextResponse, InvalidLetterResponse])
def analyze_text(request: AnalyzeTextRequest):
    return analyze_letter_or_raise_http_error(
        letter_text=request.letter_text,
        output_language=request.output_language,
    )


@router.post("/analyze-pdf", response_model=Union[AnalyzeTextResponse, InvalidLetterResponse])
async def analyze_pdf(
    file: UploadFile = File(...),
    output_language: OutputLanguage = Form("English"),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPEG, or PNG files are supported.",
        )

    file_bytes = await file.read(MAX_UPLOAD_BYTES + 1)

    if len(file_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail="The uploaded file is too large.",
        )

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if not upload_matches_content_type(file.content_type, file_bytes):
        raise HTTPException(
            status_code=400,
            detail="The file content does not match its declared type.",
        )

    try:
        if file.content_type == "application/pdf":
            extracted_text = extract_text_from_pdf_bytes(file_bytes)
        else:
            extracted_text = extract_text_from_image_bytes(file_bytes)
    except LLMConfigurationError as error:
        raise HTTPException(
            status_code=503,
            detail=LLM_UNAVAILABLE_DETAIL,
        ) from error
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Document processing failed.",
        ) from error

    if len(extracted_text) > MAX_LETTER_TEXT_CHARS:
        raise HTTPException(
            status_code=413,
            detail="The extracted letter text is too long.",
        )

    return analyze_letter_or_raise_http_error(
        letter_text=extracted_text,
        output_language=output_language,
    )


@router.post("/follow-up", response_model=FollowUpResponse)
def follow_up(request: FollowUpRequest):
    try:
        return answer_followup_question(
            analysis=request.analysis,
            question_type=request.question_type,
            output_language=request.output_language,
        )
    except LLMConfigurationError as error:
        raise HTTPException(
            status_code=503,
            detail=LLM_UNAVAILABLE_DETAIL,
        ) from error
    except ValueError as error:
        raise HTTPException(
            status_code=502,
            detail="LLM follow-up response failed backend validation.",
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Follow-up request failed.",
        ) from error


def format_sse_event(event_type: str, **payload) -> str:
    data = {"type": event_type, **payload}
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


def validate_grounded_interaction(
    letter_text: str,
    analysis: AnalyzeTextResponse,
) -> None:
    if not analysis.is_valid_letter:
        raise HTTPException(
            status_code=400,
            detail="Chat requires a valid analyzed letter.",
        )

    if letter_text.strip() != analysis.letter_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Letter text does not match the analyzed letter.",
        )


def stream_chat_events(request: ChatRequest) -> Iterator[str]:
    buffered_prefix = ""
    checking_control_token = True

    try:
        stream = chat_with_llm_stream(
            letter_text=request.letter_text,
            analysis=request.analysis.model_dump(),
            messages=request.messages,
            output_language=request.output_language,
        )

        for chunk in stream:
            if not chunk:
                continue

            if checking_control_token:
                buffered_prefix += chunk
                candidate = buffered_prefix.strip()

                if REPLY_DRAFT_REQUESTED.startswith(candidate):
                    continue

                checking_control_token = False
                yield format_sse_event("token", content=buffered_prefix)
                buffered_prefix = ""
                continue

            yield format_sse_event("token", content=chunk)

        if checking_control_token:
            if buffered_prefix.strip() == REPLY_DRAFT_REQUESTED:
                yield format_sse_event(
                    "reply_options",
                    options=REPLY_OPTIONS,
                )
            elif buffered_prefix.strip():
                yield format_sse_event("token", content=buffered_prefix)
            else:
                yield format_sse_event(
                    "error",
                    message="Chat returned an empty response.",
                )
                return

        yield format_sse_event("done")
    except Exception:
        yield format_sse_event(
            "error",
            message="Chat request failed.",
        )


@router.post("/chat", response_class=EventStreamResponse)
def chat(request: ChatRequest):
    validate_grounded_interaction(request.letter_text, request.analysis)

    try:
        require_llm_config()
    except LLMConfigurationError as error:
        raise HTTPException(
            status_code=503,
            detail=LLM_UNAVAILABLE_DETAIL,
        ) from error

    return EventStreamResponse(
        stream_chat_events(request),
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/reply-draft", response_model=ReplyDraftResponse)
def reply_draft(request: ReplyDraftRequest):
    if not request.analysis.is_valid_letter:
        raise HTTPException(
            status_code=400,
            detail="Reply drafting requires a valid analyzed letter.",
        )

    try:
        draft = generate_reply_draft(
            analysis=request.analysis.model_dump(),
            intent=REPLY_INTENT_INSTRUCTIONS[request.intent],
        )
        return ReplyDraftResponse(reply=draft)
    except LLMConfigurationError as error:
        raise HTTPException(
            status_code=503,
            detail=LLM_UNAVAILABLE_DETAIL,
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Reply draft request failed.",
        ) from error


@router.post("/translate", response_model=AnalyzeTextResponse)
def translate(request: TranslateRequest):
    try:
        from app.services.translation_service import translate_analysis_response
        return translate_analysis_response(request.analysis, request.output_language)
    except LLMConfigurationError as error:
        raise HTTPException(
            status_code=503,
            detail=LLM_UNAVAILABLE_DETAIL,
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Translation request failed.",
        ) from error
