from app.schemas.analysis import AnalyzeTextResponse
from app.services.llm_service import analyze_letter_with_llm


def analyze_letter_text(letter_text: str) -> AnalyzeTextResponse:
    llm_result = analyze_letter_with_llm(letter_text)
    return AnalyzeTextResponse(**llm_result)