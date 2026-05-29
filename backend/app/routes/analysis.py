from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.analysis import (
    AnalyzeTextRequest,
    AnalyzeTextResponse,
    FollowUpRequest,
    FollowUpResponse,
)
from app.services.analysis_service import analyze_letter_text
from app.services.pdf_service import extract_text_from_pdf_bytes
from app.services.followup_service import answer_followup_question


router = APIRouter()


def analyze_letter_or_raise_http_error(letter_text: str) -> AnalyzeTextResponse:
    """
    Analyze letter text and convert backend validation failures into a
    controlled HTTP error instead of returning invalid output to the frontend.
    """
    try:
        return analyze_letter_text(letter_text)
    except ValueError as error:
        raise HTTPException(
            status_code=502,
            detail="LLM response failed backend validation.",
        ) from error


@router.post("/analyze-text", response_model=AnalyzeTextResponse)
def analyze_text(request: AnalyzeTextRequest):
    return analyze_letter_or_raise_http_error(request.letter_text)


@router.post("/analyze-pdf", response_model=AnalyzeTextResponse)
async def analyze_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    pdf_bytes = await file.read()

    try:
        extracted_text = extract_text_from_pdf_bytes(pdf_bytes)
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