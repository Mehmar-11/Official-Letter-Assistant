from typing import Union
from app.schemas.analysis import AnalyzeTextResponse, InvalidLetterResponse
from app.services.llm_service import analyze_letter_with_llm


def analyze_letter_text(letter_text: str) -> Union[AnalyzeTextResponse, InvalidLetterResponse]:
    llm_result = analyze_letter_with_llm(letter_text)

    if not llm_result.get("is_valid_letter", True):
        return InvalidLetterResponse(
            message=llm_result.get("message", "This doesn't look like an official German letter.")
        )

    return AnalyzeTextResponse(**llm_result)