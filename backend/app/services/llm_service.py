import json
import os
from datetime import date
from typing import Any, Dict

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

from app.schemas.analysis import AnalyzeTextResponse, FollowUpResponse


load_dotenv()


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


LETTER_ANALYSIS_PROMPT = """
You are an expert assistant for German bureaucratic and administrative letters.

Your job is not to translate or rewrite the letter. Your job is to read the letter, extract only the supported facts, and return a short, practical, structured JSON response in English.

Think in two steps:
1. Extract structured facts only from the letter.
2. Write the tldr only from those extracted facts.

The user should feel that a knowledgeable, careful helper read the letter and explained what it means for them in simple, everyday English.

Current date for urgency calculation:
{{CURRENT_DATE}}

Rules:
- Use only the provided letter text. Do not assume, add, or invent information.
- Return all user-facing content in English.
- Keep official names, reference numbers, dates, amounts, and document titles unchanged.
- Use the current date only to calculate urgency. Do not use it to invent or change letter information.
- Be brief and selective. Each field should contain only what is necessary for the user to understand the letter or act on it.
- Avoid repetition across fields. Put each piece of information in the most specific field.
- Do not mention the same date, document, payment, or action in multiple fields unless it is necessary for clarity.
- Keep list fields short. Prefer 1-3 items per list. Only include more if the letter clearly contains several separate required items.
- If a list field has no clearly supported information, return an empty list.
- For required string fields with missing information, use: "Not clearly stated in the letter."
- Do not provide legal advice, make decisions for the user, or guarantee outcomes.
- Return only valid JSON. No explanation. No preamble.

Urgency rules:
- Use the current date above to decide whether a deadline is within 14 days.
- High: a serious consequence is clearly stated and the deadline is within 14 days or less.
- Medium: action is required, but the deadline is more than 14 days away, or no serious consequence is clearly stated.
- Low: mainly informational, no required action, or no clear deadline.
- urgency_reason must briefly explain the urgency_level using only the letter text and the current date.

Field guidance:
- sender: The sender of the letter. If unclear, use "Not clearly stated in the letter."
- sender_type: Use one of: "Public office", "University", "Insurance", "Bank", "Employer", "Other", "Unknown".
- urgency_level: Use only one of: "High", "Medium", "Low".
- urgency_reason: A short reason for the urgency level, based only on the letter and the current date. If a deadline is relevant, mention whether it is within 14 days or more than 14 days from the current date. You may mention the approximate number of remaining days if it helps explain the urgency level.
- letter_topic: A short phrase describing the main topic.
- tldr: One short sentence answering: "What does this letter mean for me?" Focus on the practical bottom line, not a general summary of the letter. Write it like a knowledgeable, careful helper giving the bottom line in simple everyday English. Example: "You need to send the missing documents by June 15 so the office can continue processing your application."
- useful_details: Short factual details that help the user identify the case or handle the letter, only if they do not belong in a more specific field. Examples: reference numbers, case IDs, student IDs, submission channels, portal names, office departments, appointment locations, semester names, or relevant conditions. Do not include sender name, letter date, deadlines, required actions, required documents, payment amounts, bank details, payment references, payment recipients, consequences, risks, or anything already covered by another field.
- deadlines: Only dates by which the user must do something, such as payment deadlines, response deadlines, submission deadlines, proof upload deadlines, or appointment dates. Each deadline item must include both the date and the required action or condition, not just the date alone. Good examples: "Payment must be received by 2026-06-14" or "Upload proof of payment by 2026-06-10 if you paid after 2026-05-20". Do not include dates that only describe when a consequence may start, unless the user must act by that date. Do not treat the letter date as a deadline.
- required_actions: Actions explicitly requested by the letter. Do not include general advice or preparation steps.
- required_documents: Documents explicitly requested in the letter.
- payment_information: Payment details explicitly mentioned in the letter, such as amount, IBAN, BIC, recipient, or payment reference. Do not repeat payment deadlines here if they are already listed in deadlines.
- possible_consequences: Only consequences clearly stated in the letter. Do not invent legal or administrative consequences.
- unclear_or_risky_parts: Include unclear, incomplete, risky, sensitive, or easy-to-misunderstand points explicitly present in the letter text. Also include practical traps that could mislead the user, such as conditions, exceptions, or wording where a deadline, payment, document, required action, or consequence could easily be misunderstood. Do not add generic concerns, assumptions, or possible issues that are not grounded in the letter.
- safety_note: Use exactly this sentence: "This is AI-generated help, not legal advice. Please verify important decisions with the responsible office or a qualified advisor."

JSON structure:
{
  "sender": "...",
  "sender_type": "...",
  "urgency_level": "...",
  "urgency_reason": "...",
  "letter_topic": "...",
  "tldr": "...",
  "useful_details": [],
  "deadlines": [],
  "required_actions": [],
  "required_documents": [],
  "payment_information": [],
  "possible_consequences": [],
  "unclear_or_risky_parts": [],
  "safety_note": "..."
}

Letter text:
{{LETTER_TEXT}}
"""


def check_llm_config() -> bool:
    if LLM_PROVIDER != "openai":
        raise RuntimeError(f"Unsupported LLM provider: {LLM_PROVIDER}")

    return bool(OPENAI_API_KEY) and OPENAI_API_KEY != "your_api_key_here"


def build_letter_analysis_prompt(letter_text: str) -> str:
    """
    Build the prompt for analyzing a German official letter.

    The current date is included only for urgency calculation, so the model
    does not need to guess how close a deadline is.
    """
    current_date = date.today().isoformat()

    return (
        LETTER_ANALYSIS_PROMPT
        .replace("{{CURRENT_DATE}}", current_date)
        .replace("{{LETTER_TEXT}}", letter_text)
    )


def get_analysis_response_schema() -> Dict[str, Any]:
    """
    Return the JSON schema for the expected letter analysis response.

    AnalyzeTextResponse is the single source of truth for the backend response
    structure. The schema is made strict for OpenAI structured outputs by
    disallowing additional properties.
    """
    schema = AnalyzeTextResponse.model_json_schema()
    schema["additionalProperties"] = False
    return schema


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


def call_openai_provider(prompt: str) -> Dict[str, Any]:
    """
    Call OpenAI with structured output and validate the response.

    OpenAI-specific logic is kept inside this function so the rest of the
    backend remains provider-independent.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "letter_analysis",
                "schema": get_analysis_response_schema(),
                "strict": True,
            }
        },
    )

    raw_response = response.output_text
    return parse_and_validate_llm_response(raw_response)


def get_mock_letter_analysis() -> Dict[str, Any]:
    """
    Return a mock structured response for development when the real LLM provider
    is not configured.

    This mock follows the same response schema as the real LLM output so the
    frontend can be developed and tested without making API calls.
    """
    return {
        "sender": "Amt für Einwanderung Musterstadt",
        "sender_type": "Public office",
        "urgency_level": "Medium",
        "urgency_reason": "The letter asks the user to submit missing documents by a stated deadline, but the deadline is not within 14 days.",
        "letter_topic": "Missing documents for an application",
        "tldr": "You need to send the missing documents by 15.06.2026 so the office can continue processing your application.",
        "useful_details": [
            "Case reference: ABC-12345",
            "Submission channels: post or online portal",
            "A personal visit is not required"
        ],
        "deadlines": [
            "Submit the missing documents by 15.06.2026"
        ],
        "required_actions": [
            "Submit the missing documents",
            "If you already sent them, inform the office and include the case reference"
        ],
        "required_documents": [
            "Current enrollment certificate",
            "Proof of valid health insurance",
            "Current proof of financing"
        ],
        "payment_information": [],
        "possible_consequences": [
            "The application may not be processed further if the documents are not received on time"
        ],
        "unclear_or_risky_parts": [],
        "safety_note": "This is AI-generated help, not legal advice. Please verify important decisions with the responsible office or a qualified advisor."
    }


def call_llm_provider(prompt: str) -> Dict[str, Any]:
    """
    Call the configured LLM provider and return a structured response.

    Provider-specific implementation should stay inside this function or helper
    functions called from here. This keeps routes and analysis services
    independent from the selected LLM provider.
    """
    if LLM_PROVIDER == "openai":
        return call_openai_provider(prompt)

    raise RuntimeError(f"Unsupported LLM provider: {LLM_PROVIDER}")


def analyze_letter_with_llm(letter_text: str) -> Dict[str, Any]:
    """
    Analyze a German official letter with an LLM and return a structured result.

    If the LLM API key is not configured yet, return a mock response so
    development can continue without blocking the project.
    """
    if not check_llm_config():
        return get_mock_letter_analysis()

    prompt = build_letter_analysis_prompt(letter_text)
    return call_llm_provider(prompt)


FOLLOWUP_PROMPT = """
You answer one guided follow-up question about one already analyzed German official letter.

Use ONLY the provided focused context.
Do not use outside knowledge.
Do not invent missing information.
Do not summarize the whole letter.
Do not give legal advice or guarantee outcomes.
Do not add extra practical advice that is not supported by the focused context, such as telling the user to keep documents, contact someone, or wait, unless that is clearly stated.
Do not simplify or change consequence conditions, dates, or triggers; if you mention a consequence, keep the condition and timing exactly as provided in the focused context.
Do not make dates, amounts, deadlines, or reference numbers vague. Keep them specific when they are provided in the focused context.

Write in simple, natural everyday English, like a careful helper explaining the letter to a non-German speaker. Avoid bureaucratic or database-like wording.

The answer must be practical and action-oriented:
- summary: one short direct answer to the guided question. Do not include specific amounts, dates, recipients, references, or document names in the summary; put them in details.
- details: short, clear bullet points written for a normal user, not database-style fields.
- Keep specific facts mainly in details.
- Do not repeat the same amount, date, recipient, document, reference, or consequence in both summary and details unless it is necessary for clarity.
- Use labels only when they make the answer easier to scan, such as "Amount:", "Deadline:", or "IBAN:".
- Maximum 5 details.

Question type meanings:
- payment: provide payment-related details if the letter contains a payment request; if no payment is stated, say that no payment is requested.
- documents: provide document-related details if the letter requests documents; if no documents are requested, say that no documents are requested.
- consequences: explain only the consequences clearly stated in the letter if the user ignores or misses the required action.
- careful: explain unclear, risky, conditional, or easy-to-miss points from the letter.

If the focused context does not contain enough information to answer clearly, return:
{
  "summary": "I cannot answer that clearly from this letter.",
  "details": []
}

Guided question type:
{{QUESTION_TYPE}}

Focused context:
{{ANALYSIS}}

Return only valid JSON in this format:
{
  "summary": "One short direct answer.",
  "details": [
    "Short clear detail"
  ]
}
"""

def build_followup_prompt(focused_context: Dict[str, Any], question_type: str) -> str:
    context_json = json.dumps(focused_context, indent=2, ensure_ascii=False)

    return (
        FOLLOWUP_PROMPT
        .replace("{{ANALYSIS}}", context_json)
        .replace("{{QUESTION_TYPE}}", question_type)
    )

def get_followup_response_schema() -> Dict[str, Any]:
    schema = FollowUpResponse.model_json_schema()
    schema["additionalProperties"] = False
    return schema


def parse_and_validate_followup_response(raw_response: str) -> Dict[str, Any]:
    try:
        parsed_response = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM follow-up response is not valid JSON.") from exc

    try:
        validated_response = FollowUpResponse(**parsed_response)
    except ValidationError as exc:
        raise ValueError("LLM follow-up response does not match the expected schema.") from exc

    return validated_response.model_dump()


def call_openai_followup_provider(prompt: str) -> Dict[str, Any]:
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "followup_answer",
                "schema": get_followup_response_schema(),
                "strict": True,
            }
        },
    )

    raw_response = response.output_text
    return parse_and_validate_followup_response(raw_response)


def get_mock_followup_answer() -> Dict[str, Any]:
    return {
        "summary": "This letter may require you to check an action, deadline, payment, document, or risk.",
        "details": []
    }


def answer_followup_with_llm(
    focused_context: Dict[str, Any],
    question_type: str,
) -> Dict[str, Any]:
    if not check_llm_config():
        return get_mock_followup_answer()

    prompt = build_followup_prompt(focused_context, question_type)

    if LLM_PROVIDER == "openai":
        return call_openai_followup_provider(prompt)

    raise RuntimeError(f"Unsupported LLM provider: {LLM_PROVIDER}")