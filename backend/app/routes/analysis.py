from typing import Union

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.analysis import (
    AnalyzeTextRequest,
    AnalyzeTextResponse,
    InvalidLetterResponse,
    FollowUpRequest,
    FollowUpResponse,
    ChatRequest,
    ChatResponse,
)
from app.services.analysis_service import analyze_letter_text
from app.services.pdf_service import extract_text_from_pdf_bytes
from app.services.pdf_service import extract_text_from_pdf_bytes, extract_text_from_image_bytes
from app.services.followup_service import answer_followup_question
from app.services.llm_service import chat_with_llm_stream, generate_reply_draft



router = APIRouter()

def analyze_letter_or_raise_http_error(letter_text: str) -> Union[AnalyzeTextResponse, InvalidLetterResponse]:
    try:
        return analyze_letter_text(letter_text)
    except ValueError as error:
        raise HTTPException(
            status_code=502,
            detail="LLM response failed backend validation.",
        ) from error


ALLOWED_CONTENT_TYPES = ["application/pdf", "image/jpeg", "image/png"]

@router.post("/analyze-text", response_model=Union[AnalyzeTextResponse, InvalidLetterResponse])
def analyze_text(request: AnalyzeTextRequest):
    return analyze_letter_or_raise_http_error(request.letter_text)


@router.post("/analyze-pdf", response_model=Union[AnalyzeTextResponse, InvalidLetterResponse])
async def analyze_pdf(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPEG, or PNG files are supported.",
        )

    file_bytes = await file.read()

    try:
        if file.content_type == "application/pdf":
            extracted_text = extract_text_from_pdf_bytes(file_bytes)
        else:
            extracted_text = extract_text_from_image_bytes(file_bytes)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return analyze_letter_or_raise_http_error(extracted_text)

@router.post("/follow-up", response_model=FollowUpResponse)
def follow_up(request: FollowUpRequest):
    try:
        return answer_followup_question(
            analysis=request.analysis,
            question_type=request.question_type,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=502,
            detail="LLM follow-up response failed backend validation.",
        ) from error

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        if request.reply_intent:
            draft = generate_reply_draft(
                analysis=request.analysis.model_dump(),
                intent=request.reply_intent,
            )
            return ChatResponse(reply=draft)

        stream = chat_with_llm_stream(
            letter_text=request.letter_text,
            analysis=request.analysis.model_dump(),
            messages=request.messages,
        )

        reply = "".join(stream)

        if reply.strip() == "REPLY_DRAFT_REQUESTED":
            return ChatResponse(
                reply="Sure! What's the purpose of your reply?",
                ui_action="show_reply_options",
                options=[
                    "I already took care of it",
                    "I need more time or have a question",
                    "I disagree with this letter",
                ]
            )

        return ChatResponse(reply=reply)

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Chat request failed.",
        ) from error