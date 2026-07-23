import unittest
import base64
from io import BytesIO
from unittest.mock import patch

import fitz
from fastapi import HTTPException
from fastapi.testclient import TestClient
from PIL import Image
from pydantic import ValidationError

from app.config import MAX_LETTER_TEXT_CHARS, parse_cors_origins
from app.main import app, readiness_check
from app.routes.analysis import analyze_letter_or_raise_http_error
from app.schemas.analysis import AnalyzeTextRequest
from app.services.llm_service import (
    LLMConfigurationError,
    analyze_letter_with_llm,
    generate_reply_draft,
    require_llm_config,
)
from app.services.pdf_service import (
    MAX_OCR_IMAGE_EDGE,
    extract_text_from_image_bytes,
    extract_text_from_pdf_bytes,
    prepare_image_for_ocr,
)


class RuntimeSafetyTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_default_cors_origins_include_local_and_deployed_frontends(self):
        self.assertEqual(
            parse_cors_origins(None),
            (
                "http://localhost:5173",
                "https://official-letter-assistant.vercel.app",
            ),
        )

    def test_cors_origins_are_trimmed_normalized_and_deduplicated(self):
        self.assertEqual(
            parse_cors_origins(
                " https://example.com/, http://localhost:5173,https://example.com "
            ),
            ("https://example.com", "http://localhost:5173"),
        )

    def test_deployed_frontend_passes_cors_preflight(self):
        response = self.client.options(
            "/health",
            headers={
                "Origin": "https://official-letter-assistant.vercel.app",
                "Access-Control-Request-Method": "GET",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["access-control-allow-origin"],
            "https://official-letter-assistant.vercel.app",
        )

    @patch("app.services.llm_service.OPENAI_API_KEY", None)
    @patch("app.services.llm_service.LLM_PROVIDER", "openai")
    def test_analysis_never_returns_mock_content_without_api_key(self):
        with self.assertRaises(LLMConfigurationError):
            analyze_letter_with_llm("Eine echte Eingabe")

    @patch("app.services.llm_service.OPENAI_API_KEY", None)
    @patch("app.services.llm_service.LLM_PROVIDER", "openai")
    def test_reply_draft_never_returns_mock_content_without_api_key(self):
        with self.assertRaises(LLMConfigurationError):
            generate_reply_draft({}, "I need more time")

    @patch("app.services.llm_service.OPENAI_API_KEY", "your_key_here")
    @patch("app.services.llm_service.LLM_PROVIDER", "openai")
    def test_placeholder_api_key_is_rejected(self):
        with self.assertRaises(LLMConfigurationError):
            require_llm_config()

    @patch("app.routes.analysis.analyze_letter_text")
    def test_missing_llm_configuration_becomes_503(self, analyze_mock):
        analyze_mock.side_effect = LLMConfigurationError("missing key")

        with self.assertRaises(HTTPException) as context:
            analyze_letter_or_raise_http_error("Eine echte Eingabe")

        self.assertEqual(context.exception.status_code, 503)

    @patch("app.main.check_llm_config", return_value=False)
    def test_readiness_fails_when_llm_is_not_configured(self, config_mock):
        with self.assertRaises(HTTPException) as context:
            readiness_check()

        config_mock.assert_called_once_with()
        self.assertEqual(context.exception.status_code, 503)

    def test_analyze_text_rejects_blank_or_oversized_input(self):
        with self.assertRaises(ValidationError):
            AnalyzeTextRequest(letter_text="   ")

        with self.assertRaises(ValidationError):
            AnalyzeTextRequest(letter_text="x" * (MAX_LETTER_TEXT_CHARS + 1))

    def test_upload_rejects_file_larger_than_configured_limit(self):
        with patch("app.routes.analysis.MAX_UPLOAD_BYTES", 4):
            response = self.client.post(
                "/analyze-pdf",
                files={"file": ("letter.pdf", b"%PDF-test", "application/pdf")},
            )

        self.assertEqual(response.status_code, 413)

    def test_upload_rejects_content_type_mismatch(self):
        response = self.client.post(
            "/analyze-pdf",
            files={"file": ("letter.pdf", b"not a pdf", "application/pdf")},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("does not match", response.json()["detail"])

    def test_pdf_page_limit_is_enforced_before_ocr(self):
        document = fitz.open()
        document.new_page()
        document.new_page()
        pdf_bytes = document.tobytes()
        document.close()

        with patch("app.services.pdf_service.MAX_PDF_PAGES", 1):
            with self.assertRaisesRegex(ValueError, "at most 1 pages"):
                extract_text_from_pdf_bytes(pdf_bytes)

    def test_phone_sized_jpeg_is_normalized_before_ocr(self):
        image = Image.new("RGB", (4032, 3024), "white")
        source = BytesIO()
        image.save(source, format="JPEG", quality=95)

        normalized = prepare_image_for_ocr(source.getvalue())

        self.assertTrue(normalized.startswith(b"\xff\xd8\xff"))
        with Image.open(BytesIO(normalized)) as prepared:
            self.assertLessEqual(max(prepared.size), MAX_OCR_IMAGE_EDGE)

    @patch("app.services.pdf_service.extract_text_from_image_with_llm")
    def test_jpeg_upload_uses_matching_media_type(self, extract_mock):
        extract_mock.return_value = "Extracted official letter text"
        image = Image.new("RGB", (1200, 1600), "white")
        source = BytesIO()
        image.save(source, format="JPEG")

        extracted = extract_text_from_image_bytes(source.getvalue())

        self.assertEqual(extracted, "Extracted official letter text")
        encoded_image = extract_mock.call_args.args[0]
        self.assertTrue(base64.b64decode(encoded_image).startswith(b"\xff\xd8\xff"))
        self.assertEqual(
            extract_mock.call_args.kwargs["media_type"],
            "image/jpeg",
        )


if __name__ == "__main__":
    unittest.main()
