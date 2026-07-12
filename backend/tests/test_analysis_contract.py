import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.schemas.analysis import (
    AnalyzeTextResponse,
    InvalidLetterResponse,
)
from app.services.analysis_service import (
    CONFIDENCE_REASON_TEXTS,
    analyze_letter_text,
    get_confidence_reason,
    validate_grounded_dates,
)
from app.services.llm_service import (
    build_letter_analysis_prompt,
    extract_calendar_dates,
    get_analysis_response_schema,
    parse_and_validate_llm_response,
)
from app.services.translation_service import translate_analysis_response


def build_llm_payload(**overrides):
    values = {
        "is_valid_letter": True,
        "message": "",
        "letter_involves_payment": False,
        "sender": "Beispielbehörde",
        "sender_type": "Public office",
        "urgency_level": "Medium",
        "urgency_reason": "A response is required by a stated deadline.",
        "letter_topic": "Response request",
        "tldr": "You need to reply by 31.07.2026.",
        "useful_details": [],
        "deadlines": ["Reply by 31.07.2026"],
        "required_actions": ["Send a reply"],
        "required_documents": [],
        "payment_information": [],
        "possible_consequences": [],
        "unclear_or_risky_parts": [],
        "safety_note": "This is AI-generated help, not legal advice.",
    }
    values.update(overrides)
    return values


def build_analysis(**overrides):
    values = {
        "is_valid_letter": True,
        "letter_text": "Sehr geehrte Damen und Herren, bitte antworten Sie bis 31.07.2026.",
        "confidence_level": "medium",
        "confidence_reason": CONFIDENCE_REASON_TEXTS["deadline_missing"]["German"],
        "letter_involves_payment": False,
        "sender": "Beispielbehörde",
        "sender_type": "Public office",
        "urgency_level": "Medium",
        "urgency_reason": "Eine Antwort ist bis zum angegebenen Termin erforderlich.",
        "letter_topic": "Antwortanforderung",
        "tldr": "Sie müssen bis zum 31.07.2026 antworten.",
        "useful_details": [],
        "deadlines": ["Antwort bis zum 31.07.2026"],
        "required_actions": ["Antwort senden"],
        "required_documents": [],
        "payment_information": [],
        "possible_consequences": [],
        "unclear_or_risky_parts": [],
        "safety_note": "Dies ist eine KI-generierte Hilfe und keine Rechtsberatung.",
    }
    values.update(overrides)
    return AnalyzeTextResponse(**values)


class AnalysisContractTests(unittest.TestCase):
    def test_source_dates_are_normalized_and_added_to_the_prompt(self):
        letter_text = "Zahlen Sie bis 30.08.2026. Exmatrikulation am 30.09.2026."

        self.assertEqual(
            extract_calendar_dates(letter_text),
            {"2026-08-30", "2026-09-30"},
        )
        prompt = build_letter_analysis_prompt(letter_text, "English")
        self.assertIn("2026-08-30, 2026-09-30", prompt)
        self.assertIn("Every exact calendar date", prompt)

    def test_analysis_rejects_a_date_not_present_in_the_letter(self):
        letter_text = "Bitte zahlen Sie bis 30.08.2026."
        result = build_llm_payload(
            tldr="Pay by June 30, 2026.",
            deadlines=["Payment is due by 2026-06-30"],
        )

        with self.assertRaisesRegex(ValueError, "2026-06-30"):
            validate_grounded_dates(letter_text, result)

    def test_analysis_accepts_dates_present_in_the_letter(self):
        letter_text = "Zahlen Sie bis 30.08.2026. Folge ab 30.09.2026."
        result = build_llm_payload(
            tldr="Pay by August 30, 2026.",
            deadlines=["Payment is due by 2026-08-30"],
            possible_consequences=["Exmatriculation on 2026-09-30"],
        )

        validate_grounded_dates(letter_text, result)

    def test_model_schema_matches_only_model_generated_fields(self):
        schema = get_analysis_response_schema()
        properties = schema["properties"]

        self.assertIn("is_valid_letter", properties)
        self.assertIn("message", properties)
        self.assertNotIn("letter_text", properties)
        self.assertNotIn("confidence_level", properties)
        self.assertNotIn("confidence_reason", properties)
        self.assertEqual(properties["useful_details"]["maxItems"], 50)
        self.assertEqual(
            properties["urgency_level"]["enum"],
            ["High", "Medium", "Low"],
        )

    def test_invalid_letter_payload_is_validated_and_preserved(self):
        payload = build_llm_payload(
            is_valid_letter=False,
            message="این متن شبیه یک نامه رسمی آلمانی نیست.",
            sender="",
            sender_type="Unknown",
            urgency_level="Low",
            urgency_reason="",
            letter_topic="",
            tldr="",
            deadlines=[],
            required_actions=[],
            safety_note="",
        )

        validated = parse_and_validate_llm_response(
            json.dumps(payload, ensure_ascii=False)
        )

        self.assertFalse(validated["is_valid_letter"])
        self.assertEqual(
            validated["message"],
            "این متن شبیه یک نامه رسمی آلمانی نیست.",
        )

    def test_valid_letter_payload_requires_empty_message(self):
        payload = build_llm_payload(message="Unexpected message")

        with self.assertRaises(ValueError):
            parse_and_validate_llm_response(json.dumps(payload))

    @patch("app.services.analysis_service.analyze_letter_with_llm")
    def test_valid_analysis_does_not_expose_internal_message(self, analyze_mock):
        analyze_mock.return_value = build_llm_payload()
        letter_text = (
            "Sehr geehrte Damen und Herren, "
            "bitte antworten Sie bis 31.07.2026. "
        ) * 5

        response = analyze_letter_text(letter_text, output_language="English")

        self.assertIsInstance(response, AnalyzeTextResponse)
        self.assertFalse(hasattr(response, "message"))

    @patch("app.services.analysis_service.analyze_letter_with_llm")
    def test_analysis_returns_invalid_letter_response(self, analyze_mock):
        analyze_mock.return_value = build_llm_payload(
            is_valid_letter=False,
            message="This doesn't look like an official German letter.",
            sender="",
            sender_type="Unknown",
            urgency_level="Low",
            urgency_reason="",
            letter_topic="",
            tldr="",
            deadlines=[],
            required_actions=[],
            safety_note="",
        )

        response = analyze_letter_text("random text", output_language="English")

        self.assertIsInstance(response, InvalidLetterResponse)
        self.assertFalse(response.is_valid_letter)
        self.assertEqual(
            response.message,
            "This doesn't look like an official German letter.",
        )

    @patch("app.services.translation_service.get_openai_client")
    def test_translation_preserves_the_actual_confidence_reason(self, client_mock):
        analysis = build_analysis()
        translated_payload = analysis.model_dump()
        translated_payload["confidence_reason"] = "Incorrect translated reason"

        provider_response = SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=json.dumps(
                            translated_payload,
                            ensure_ascii=False,
                        )
                    )
                )
            ]
        )
        client_mock.return_value.chat.completions.create.return_value = provider_response

        translated = translate_analysis_response(analysis, "Persian")

        prompt = client_mock.return_value.chat.completions.create.call_args.kwargs[
            "messages"
        ][0]["content"]
        self.assertIn("natural administrative meaning", prompt)
        self.assertIn("مدارک درخواستی", prompt)

        self.assertEqual(
            translated.confidence_reason,
            get_confidence_reason("deadline_missing", "Persian"),
        )
        self.assertNotEqual(
            translated.confidence_reason,
            get_confidence_reason("payment_incomplete", "Persian"),
        )


if __name__ == "__main__":
    unittest.main()
