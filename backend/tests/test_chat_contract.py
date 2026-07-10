import json
import unittest
from unittest.mock import patch

from fastapi import HTTPException
from pydantic import ValidationError

from app.routes.analysis import (
    chat,
    reply_draft,
    stream_chat_events,
    validate_grounded_interaction,
)
from app.main import app
from app.schemas.analysis import (
    AnalyzeTextResponse,
    ChatRequest,
    ReplyDraftRequest,
)


LETTER_TEXT = "Sehr geehrte Damen und Herren, bitte antworten Sie bis 31.07.2026."


def build_analysis(**overrides) -> AnalyzeTextResponse:
    values = {
        "is_valid_letter": True,
        "letter_text": LETTER_TEXT,
        "confidence_level": "high",
        "confidence_reason": "The key details were identified.",
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
    return AnalyzeTextResponse(**values)


def build_chat_request(**overrides) -> ChatRequest:
    values = {
        "letter_text": LETTER_TEXT,
        "analysis": build_analysis(),
        "messages": [{"role": "user", "content": "What is the deadline?"}],
        "output_language": "English",
    }
    values.update(overrides)
    return ChatRequest(**values)


def parse_sse(events):
    return [json.loads(event.removeprefix("data: ").strip()) for event in events]


class ChatContractTests(unittest.TestCase):
    @patch("app.routes.analysis.chat_with_llm_stream")
    def test_regular_chat_streams_tokens_and_done_event(self, stream_mock):
        stream_mock.return_value = iter(["The deadline ", "is 31.07.2026."])

        events = parse_sse(list(stream_chat_events(build_chat_request())))

        self.assertEqual(
            events,
            [
                {"type": "token", "content": "The deadline "},
                {"type": "token", "content": "is 31.07.2026."},
                {"type": "done"},
            ],
        )

    @patch("app.routes.analysis.chat_with_llm_stream")
    def test_reply_request_emits_options_without_leaking_control_token(self, stream_mock):
        stream_mock.return_value = iter(["REPLY_DRAFT_", "REQUESTED"])

        events = parse_sse(list(stream_chat_events(build_chat_request())))

        self.assertEqual(events[0]["type"], "reply_options")
        self.assertEqual(
            events[0]["options"],
            ["already_completed", "need_more_time_or_question", "disagree"],
        )
        self.assertNotIn("REPLY_DRAFT_REQUESTED", json.dumps(events))
        self.assertEqual(events[-1], {"type": "done"})

    @patch("app.routes.analysis.chat_with_llm_stream")
    def test_stream_failure_returns_controlled_error_event(self, stream_mock):
        stream_mock.side_effect = RuntimeError("provider failed")

        events = parse_sse(list(stream_chat_events(build_chat_request())))

        self.assertEqual(
            events,
            [{"type": "error", "message": "Chat request failed."}],
        )

    @patch("app.routes.analysis.chat_with_llm_stream")
    def test_empty_provider_response_returns_error_event(self, stream_mock):
        stream_mock.return_value = iter([])

        events = parse_sse(list(stream_chat_events(build_chat_request())))

        self.assertEqual(
            events,
            [{"type": "error", "message": "Chat returned an empty response."}],
        )

    def test_chat_rejects_letter_analysis_mismatch(self):
        with self.assertRaises(HTTPException) as context:
            validate_grounded_interaction("Different letter", build_analysis())

        self.assertEqual(context.exception.status_code, 400)

    def test_chat_rejects_invalid_analysis(self):
        invalid_analysis = build_analysis(is_valid_letter=False)

        with self.assertRaises(HTTPException) as context:
            validate_grounded_interaction(LETTER_TEXT, invalid_analysis)

        self.assertEqual(context.exception.status_code, 400)

    def test_chat_schema_rejects_legacy_reply_intent(self):
        with self.assertRaises(ValidationError):
            build_chat_request(reply_intent="already_completed")

    def test_chat_route_uses_event_stream_media_type(self):
        response = chat(build_chat_request())

        self.assertEqual(response.media_type, "text/event-stream")
        self.assertEqual(response.headers["cache-control"], "no-cache")

    def test_openapi_documents_chat_as_event_stream(self):
        content_types = app.openapi()["paths"]["/chat"]["post"]["responses"]["200"]["content"]

        self.assertEqual(list(content_types), ["text/event-stream"])

    @patch("app.routes.analysis.generate_reply_draft")
    def test_reply_draft_returns_complete_response(self, draft_mock):
        draft_mock.return_value = "Vollständiger Antwortentwurf"
        request = ReplyDraftRequest(
            analysis=build_analysis(),
            intent="need_more_time_or_question",
        )

        response = reply_draft(request)

        self.assertEqual(response.reply, "Vollständiger Antwortentwurf")
        draft_mock.assert_called_once_with(
            analysis=build_analysis().model_dump(),
            intent="I need more time or have a question",
        )

    def test_reply_draft_rejects_unknown_intent(self):
        with self.assertRaises(ValidationError):
            ReplyDraftRequest(
                analysis=build_analysis(),
                intent="Invent a legal argument",
            )


if __name__ == "__main__":
    unittest.main()
