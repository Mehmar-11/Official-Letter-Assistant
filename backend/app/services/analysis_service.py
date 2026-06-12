from typing import Union

from app.schemas.analysis import AnalyzeTextResponse, InvalidLetterResponse
from app.services.llm_service import analyze_letter_with_llm

def calculate_reliability(llm_result: dict) -> tuple[str, str]:
    """
    Calculate confidence_level and confidence_reason based on
    rule-based checks on the LLM output.
    """
    letter_text = llm_result.get("letter_text", "")
    sender = llm_result.get("sender", "")
    letter_topic = llm_result.get("letter_topic", "")
    required_actions = llm_result.get("required_actions", [])
    deadlines = llm_result.get("deadlines", [])
    payment_information = llm_result.get("payment_information", [])
    urgency_level = llm_result.get("urgency_level", "Low")
    letter_involves_payment = llm_result.get("letter_involves_payment", False)

    not_stated = "Not clearly stated in the letter."

    # Low reliability checks
    if len(letter_text) < 200:
        return "low", "The letter text was too short to analyze reliably."

    if not required_actions:
        return "low", "No clear required actions could be found in the letter."

    if sender == not_stated and letter_topic == not_stated:
        return "low", "The sender and topic of the letter could not be identified."

    # Medium reliability checks
    if sender == not_stated or letter_topic == not_stated:
        return "medium", "The sender or topic of the letter was not clearly identified."

    if letter_involves_payment and not payment_information:
        return "medium", "This letter involves a payment, but the payment details were not clearly stated."

    if urgency_level != "Low" and not deadlines:
        return "medium", "This letter seems to require timely action, but no clear deadline was found."

    # High reliability
    return "high", "The letter text was clear and all key details were identified."


def analyze_letter_text(letter_text: str) -> Union[AnalyzeTextResponse, InvalidLetterResponse]:
    llm_result = analyze_letter_with_llm(letter_text)

    if not llm_result.get("is_valid_letter", True):
        return InvalidLetterResponse(message=llm_result.get("message", "This doesn't look like an official German letter."))

    llm_result["letter_text"] = letter_text

    confidence_level, confidence_reason = calculate_reliability(llm_result)
    llm_result["confidence_level"] = confidence_level
    llm_result["confidence_reason"] = confidence_reason

    return AnalyzeTextResponse(**llm_result)