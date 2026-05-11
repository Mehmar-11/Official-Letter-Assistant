from fastapi import APIRouter

from app.schemas.analysis import AnalyzeTextRequest, AnalyzeTextResponse
from app.services.analysis_service import analyze_letter_text


router = APIRouter()


@router.post("/analyze-text", response_model=AnalyzeTextResponse)
def analyze_text(request: AnalyzeTextRequest):
    return analyze_letter_text(request.letter_text)