import json
import os
from typing import Any, Dict

from dotenv import load_dotenv
from pydantic import ValidationError

from app.schemas.analysis import AnalyzeTextResponse


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


LETTER_ANALYSIS_PROMPT = """
You are Official Letter Assistant, an assistant that helps people who are not comfortable with formal German official language understand German official letters.

Your task is to analyze the provided German official letter and extract the practical information the user needs to understand it.

Important rules:
- Use only the provided letter text.
- Do not invent deadlines, payments, required actions, sender information, or consequences.
- If information is not clearly stated in the letter, do not guess.
- Do not provide legal advice.
- Do not make decisions for the user.
- Do not guarantee legal or administrative outcomes.
- If something is unclear, incomplete, risky, or should be checked carefully, include it in unclear_or_risky_parts.
- Do not translate the full letter.
- Do not repeat personal data unless it is necessary to understand the letter.
- Use clear, plain English for people who are not comfortable with formal German official language. Do not oversimplify important details.
- Keep each list item short, specific, and useful for a UI card.
- Do not exaggerate risks.

Return only a valid JSON object with exactly these fields:

{
  "sender": "string",
  "letter_topic": "string",
  "summary": "string",
  "important_information": ["string"],
  "deadlines": ["string"],
  "required_actions": ["string"],
  "payment_information": ["string"],
  "unclear_or_risky_parts": ["string"],
  "next_steps": ["string"],
  "safety_note": "string"
}

Field guidance:
- sender: The authority, office, company, university, or organization that sent the letter. If not clear, use "Not clearly identified in the letter."
- letter_topic: A short phrase describing the main topic of the letter.
- summary: A short explanation of the main message of the letter.
- important_information: Important facts the user should understand, such as case/reference numbers, requested information, appointment details, required documents, or important conditions.
- deadlines: Only include dates that are clearly deadlines, due dates, appointment dates, or required response dates. Do not treat the letter date as a deadline unless the letter clearly says so.
- required_actions: Actions the letter asks the user to take.
- payment_information: Only include payment details explicitly mentioned in the letter, such as amount, reason, deadline, IBAN, or payment reference. Do not judge whether the payment request is legitimate.
- unclear_or_risky_parts: Parts that are unclear, incomplete, legally or administratively sensitive, or should be verified carefully.
- next_steps: Simple, safe, non-legal next steps, such as checking requested documents, preparing mentioned information, or contacting the responsible office.
- safety_note: Always include a short note that this is not legal advice and important information should be verified with the responsible office or a qualified advisor.

If a list field has no clearly supported information, return an empty list.

If the letter text seems incomplete, fragmented, or poorly extracted, do not guess. Mention this in unclear_or_risky_parts.

Letter text:
{{LETTER_TEXT}}
"""


def check_llm_config() -> bool:
    return bool(OPENAI_API_KEY) and OPENAI_API_KEY != "your_real_api_key_here"


def build_letter_analysis_prompt(letter_text: str) -> str:
    """
    Build the final prompt for analyzing one German official letter.
    """
    return LETTER_ANALYSIS_PROMPT.replace("{{LETTER_TEXT}}", letter_text)

def get_analysis_response_schema() -> Dict[str, Any]:
    """
    Return the JSON schema for the expected letter analysis response.

    AnalyzeTextResponse is the single source of truth for the backend response
    structure. This schema can later be passed to an LLM provider that supports
    structured output / JSON schema responses.
    """
    return AnalyzeTextResponse.model_json_schema()

def parse_and_validate_llm_response(raw_response: str) -> Dict[str, Any]:
    """
    Parse a raw JSON string returned by the LLM and validate it against
    the backend response schema.

    This prevents invalid or incomplete LLM output from being sent directly
    to the frontend.
    """
    try:
        parsed_response = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM response is not valid JSON.") from exc

    try:
        validated_response = AnalyzeTextResponse(**parsed_response)
    except ValidationError as exc:
        raise ValueError("LLM response does not match the expected schema.") from exc

    return validated_response.model_dump()


def get_mock_letter_analysis() -> Dict[str, Any]:
    """
    Return a temporary structured response for development.

    This is used when the real LLM provider is not connected yet.
    It must follow the same structure as the real LLM response.
    """
    return {
        "sender": "Not clearly identified in this mock response.",
        "letter_topic": "Mock official letter analysis",
        "summary": "This is a temporary structured response used for development before the real LLM call is connected.",
        "important_information": [
            "This mock response follows the planned MVP response structure."
        ],
        "deadlines": [],
        "required_actions": [
            "Connect the real LLM provider once an API key is available."
        ],
        "payment_information": [],
        "unclear_or_risky_parts": [
            "This is not a real analysis of the letter text yet."
        ],
        "next_steps": [
            "Use this response to continue backend and frontend integration."
        ],
        "safety_note": "This is not legal advice. Please verify important information with the responsible office or a qualified advisor."
    }


def analyze_letter_with_llm(letter_text: str) -> Dict[str, Any]:
    """
    Analyze a German official letter with an LLM and return a structured result.

    If the LLM API key is not configured yet, return a mock response so
    development can continue without blocking the project.
    """
    if not check_llm_config():
        return get_mock_letter_analysis()

    # The real LLM call will be added here once the provider/API key is finalized.
    raise NotImplementedError(
        "Real LLM call is not implemented yet. Provider integration will be added in the next step."
    )