from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.analysis import AnalyzeTextRequest, AnalyzeTextResponse
from app.services.analysis_service import analyze_letter_text
from app.services.pdf_service import extract_text_from_pdf_bytes


router = APIRouter()


@router.post("/analyze-text", response_model=AnalyzeTextResponse)
def analyze_text(request: AnalyzeTextRequest):
    return analyze_letter_text(request.letter_text)


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

    return analyze_letter_text(extracted_text)