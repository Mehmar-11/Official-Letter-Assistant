from app.schemas.common import OutputLanguage
from typing import Any, Dict

from app.schemas.analysis import (
    AnalyzeTextResponse,
    FollowUpResponse,
)
from app.services.llm_service import answer_followup_with_llm


def build_focused_context(
    analysis: AnalyzeTextResponse,
    question_type: str,
) -> Dict[str, Any]:
    if question_type == "payment":
        return {
            "payment_information": analysis.payment_information,
            "deadlines": analysis.deadlines,
            "required_actions": analysis.required_actions,
        }

    if question_type == "documents":
        return {
            "required_documents": analysis.required_documents,
            "deadlines": analysis.deadlines,
        }

    if question_type == "consequences":
        return {
            "required_actions": analysis.required_actions,
            "deadlines": analysis.deadlines,
            "possible_consequences": analysis.possible_consequences,
            "unclear_or_risky_parts": analysis.unclear_or_risky_parts,
        }

    if question_type == "careful":
        return {
            "unclear_or_risky_parts": analysis.unclear_or_risky_parts,
        }

    raise ValueError(f"Unsupported follow-up question type: {question_type}")


def answer_followup_question(
    analysis: AnalyzeTextResponse,
    question_type: str,
    output_language: OutputLanguage = "English",
) -> FollowUpResponse:
    focused_context = build_focused_context(analysis, question_type)

    llm_result = answer_followup_with_llm(
        focused_context=focused_context,
        question_type=question_type,
        output_language=output_language,
    )

    return FollowUpResponse(**llm_result)