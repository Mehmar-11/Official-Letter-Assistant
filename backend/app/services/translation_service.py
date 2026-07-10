import json
from app.schemas.analysis import AnalyzeTextResponse
from openai import OpenAI
from app.services.llm_service import OPENAI_API_KEY, OPENAI_MODEL
from app.services.analysis_service import (
    get_confidence_reason,
    get_confidence_reason_key,
)

TRANSLATE_PROMPT = """You are given a structured analysis of a German official letter.
Translate only the user-facing explanatory fields into {output_language}.

Rules:
- Translate: confidence_reason, tldr, urgency_reason, letter_topic, useful_details, deadlines, required_actions, required_documents, payment_information, possible_consequences, unclear_or_risky_parts, safety_note
- Do NOT translate: sender, sender_type, urgency_level, confidence_level, letter_text
- Do NOT translate: dates, amounts, IBAN, BIC, reference numbers, organization names, legal citations (§ ...)
- For payment_information, translate explanatory labels such as "Amount", "Recipient", "Payment reference", or "Deadline", but keep IBAN, BIC, amounts, recipient names, payment references, and exact dates unchanged.
- Return valid JSON with exactly the same structure as the input

Analysis to translate:
{analysis_json}

Return only the translated JSON. No explanation."""


def translate_analysis_response(
    analysis: AnalyzeTextResponse,
    output_language: str,
) -> AnalyzeTextResponse:
    client = OpenAI(api_key=OPENAI_API_KEY)

    analysis_dict = analysis.model_dump()

    prompt = TRANSLATE_PROMPT.format(
        output_language=output_language,
        analysis_json=json.dumps(analysis_dict, ensure_ascii=False, indent=2),
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
        temperature=0,
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    translated = json.loads(raw)

    reason_key = get_confidence_reason_key(analysis.confidence_reason)
    if reason_key is not None:
        translated["confidence_reason"] = get_confidence_reason(
            reason_key,
            output_language,
        )

    return AnalyzeTextResponse(**translated)
