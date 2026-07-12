# API Reference

Letter Assistant exposes eight endpoints. Most endpoints accept and return JSON. `/analyze-pdf` accepts `multipart/form-data`, and the health endpoints return simple JSON status responses.

Base URL (local): `http://localhost:8000`

---

## POST /analyze-text

Analyzes pasted German letter text and returns a validated structured representation.

### Request

```json
{
  "letter_text": "string",
  "output_language": "English"
}
```

`output_language` is optional and defaults to `"English"`. Supported values: `English`, `German`, `Turkish`, `Arabic`, `French`, `Spanish`, `Italian`, `Portuguese`, `Dutch`, `Polish`, `Russian`, `Japanese`, `Korean`, `Chinese`, `Hindi`, `Persian`.

### Response

**If valid letter (`is_valid_letter: true`):**

```json
{
  "is_valid_letter": true,
  "letter_text": "string",
  "confidence_level": "high | medium | low",
  "confidence_reason": "string",
  "letter_involves_payment": true,
  "sender": "string",
  "sender_type": "Public office | University | Insurance | Bank | Employer | Other | Unknown",
  "urgency_level": "High | Medium | Low",
  "urgency_reason": "string",
  "letter_topic": "string",
  "tldr": "string",
  "useful_details": ["string"],
  "deadlines": ["string"],
  "required_actions": ["string"],
  "required_documents": ["string"],
  "payment_information": ["string"],
  "possible_consequences": ["string"],
  "unclear_or_risky_parts": ["string"],
  "safety_note": "string"
}
```

**If not a valid letter (`is_valid_letter: false`):**

```json
{
  "is_valid_letter": false,
  "message": "This doesn't look like an official German letter."
}
```

The invalid-letter message is generated in the requested `output_language` and
validated by the backend before it is returned. The public response remains a
small two-field object, so the frontend only needs to display `message` when
`is_valid_letter` is `false`.

### Example

```bash
curl -s -X POST http://localhost:8000/analyze-text \
  -H "Content-Type: application/json" \
  -d '{"letter_text": "Sehr geehrte Damen und Herren, wir bitten Sie, die fehlenden Unterlagen bis zum 15.06.2026 einzureichen. Aktenzeichen: ABC-12345.", "output_language": "English"}'
```

### Errors

| Code | Reason |
|---|---|
| 422 | Request body missing or malformed |
| 502 | LLM response failed schema or exact-date grounding validation, or the provider request failed |
| 503 | LLM provider is not configured |

---

## POST /analyze-pdf

Analyzes an uploaded PDF or image file. Accepts text-based PDFs, scanned PDFs, and images (JPEG, PNG).

- Text-based PDFs are processed with `pdfplumber`
- Scanned PDFs and images are processed with GPT-4o Vision
- If `pdfplumber` extracts fewer than 50 characters, OCR fallback triggers automatically
- Uploads are limited to 10 MB and PDFs to 20 pages by default
- Extracted letter text is limited to 100,000 characters by default

### Request

`Content-Type: multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `file` | file | PDF, JPEG, or PNG |
| `output_language` | string | Optional. One of the supported languages. Defaults to `"English"`. |

### Response

Same schema as `/analyze-text`.

### Example

```bash
curl -s -X POST http://localhost:8000/analyze-pdf \
  -F "file=@letter.pdf" \
  -F "output_language=Persian"
```

```bash
curl -s -X POST http://localhost:8000/analyze-pdf \
  -F "file=@letter_scan.png"
```

### Errors

| Code | Reason |
|---|---|
| 400 | Unsupported, empty, unreadable, or mismatched file content |
| 413 | File or extracted text exceeds the configured limit |
| 502 | Document processing or LLM analysis failed, including schema or exact-date grounding validation |
| 503 | LLM provider is not configured |

---

## POST /follow-up

Answers one of four predefined guided questions about an already-analyzed letter. Uses only the relevant fields from the structured analysis — not the full letter text.

### Question Types

| Type | What it answers |
|---|---|
| `payment` | Payment amount, IBAN, BIC, reference, and deadlines |
| `documents` | Documents explicitly requested in the letter |
| `consequences` | What happens if the user ignores or misses the required action |
| `careful` | Unclear, risky, or easy-to-miss parts of the letter |

### Request

```json
{
  "analysis": { },
  "question_type": "payment | documents | consequences | careful",
  "output_language": "English"
}
```

The `analysis` field is the full `AnalyzeTextResponse` object returned by `/analyze-text` or `/analyze-pdf`.

### Response

```json
{
  "summary": "string",
  "details": ["string"]
}
```

- `summary`: one short direct answer
- `details`: up to five bullet points with specific facts (dates, amounts, references)

### Example

```bash
curl -s -X POST http://localhost:8000/follow-up \
  -H "Content-Type: application/json" \
  -d '{
    "analysis": { ...full analysis object... },
    "question_type": "payment",
    "output_language": "English"
  }'
```

### Errors

| Code | Reason |
|---|---|
| 422 | Missing or invalid `question_type` |
| 502 | LLM follow-up response failed Pydantic validation |
| 503 | LLM provider is not configured |

---

## POST /chat

Streams grounded open-chat responses using Server-Sent Events (SSE). The
endpoint accepts only open-chat requests. Reply drafts use `/reply-draft`.

The supplied `letter_text` must exactly match `analysis.letter_text`, and the
analysis must represent a valid letter.

### Request

```json
{
  "letter_text": "string",
  "analysis": { },
  "messages": [
    { "role": "user", "content": "string" },
    { "role": "assistant", "content": "string" }
  ],
  "output_language": "English"
}
```

| Field | Description |
|---|---|
| `letter_text` | Full extracted letter text (returned by `/analyze-text` or `/analyze-pdf`) |
| `analysis` | Full `AnalyzeTextResponse` object |
| `messages` | Conversation history in order. The latest message must be from the user. Maximum 50 messages. |
| `output_language` | Optional. Language for the chat response. Defaults to `"English"`. |

### Response Stream

The response content type is `text/event-stream`. Each event is one JSON object
prefixed with `data:` and terminated by a blank line.

```text
data: {"type":"token","content":"The deadline "}

data: {"type":"token","content":"is 31.07.2026."}

data: {"type":"done"}
```

Event types:

| Type | Fields | Meaning |
|---|---|---|
| `token` | `content` | Append this text to the current assistant message |
| `reply_options` | `options` | Three stable reply-intent identifiers; the frontend localizes their labels |
| `done` | none | The stream completed successfully |
| `error` | `message` | Generation failed after the stream started |

If the user asks for a reply draft, no control token is exposed to the client.
The stream returns a `reply_options` event followed by `done`.

```text
data: {"type":"reply_options","options":["already_completed","need_more_time_or_question","disagree"]}

data: {"type":"done"}
```

### Example

```bash
curl -N -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "letter_text": "...",
    "analysis": { ...full analysis object... },
    "messages": [
      { "role": "user", "content": "What documents do I need to send?" }
    ],
    "output_language": "English"
  }'
```

### Errors

| Code or event | Reason |
|---|---|
| HTTP 400 | Invalid analysis or letter/analysis mismatch |
| HTTP 422 | Missing fields, malformed request, or latest message is not from the user |
| HTTP 503 | LLM provider is not configured before streaming starts |
| `error` event | The provider failed after streaming began |

---

## POST /reply-draft

Generates one complete formal German reply. This endpoint does not stream.
The intent must be one of the three supported values. The optional
`additional_context` field lets the user provide a short question, reason, or
requested extension without replacing facts extracted from the letter.

### Request

```json
{
  "analysis": { },
  "intent": "need_more_time_or_question",
  "additional_context": "Please request an extension until 31 July 2026."
}
```

| Field | Description |
|---|---|
| `analysis` | Full validated `AnalyzeTextResponse` object |
| `intent` | One of the three stable reply intent identifiers |
| `additional_context` | Optional, trimmed user context between 1 and 1,000 characters |

### Reply Intent Values

| Intent | When to use |
|---|---|
| `"already_completed"` | User has already paid, submitted documents, or completed the required action |
| `"need_more_time_or_question"` | User cannot meet the deadline or needs clarification |
| `"disagree"` | User disputes the amount, decision, or content of the letter |

The intent values are stable API identifiers. The frontend should display a
localized label for each identifier.

### Response

```json
{
  "reply": "--- Bitte vor dem Absenden prüfen. Platzhalter in eckigen Klammern ausfüllen. ---\n\n[ORT, DATUM]\n\nSehr geehrte Damen und Herren,\n\nbezugnehmend auf Ihr Schreiben...\n\nMit freundlichen Grüßen\n[IHR VOLLSTÄNDIGER NAME]"
}
```

### Example

```bash
curl -s -X POST http://localhost:8000/reply-draft \
  -H "Content-Type: application/json" \
  -d '{
    "analysis": { ...full analysis object... },
    "intent": "need_more_time_or_question",
    "additional_context": "Please request an extension until 31 July 2026."
  }'
```

### Errors

| Code | Reason |
|---|---|
| 400 | Analysis does not represent a valid letter |
| 422 | Missing fields, unsupported intent, or invalid additional context |
| 502 | Reply draft generation failed |
| 503 | LLM provider is not configured |

---

## POST /translate

Re-translates an existing analysis into a different language without re-analyzing the letter. Use this when the user switches language after the initial analysis.

### Request

```json
{
  "analysis": { },
  "output_language": "Persian"
}
```

| Field | Description |
|---|---|
| `analysis` | Full `AnalyzeTextResponse` object returned by `/analyze-text` or `/analyze-pdf` |
| `output_language` | Target language. One of the 16 supported languages. |

### Response

Same schema as `AnalyzeTextResponse`. The following fields are never translated:

- `sender`, `sender_type`, `urgency_level`, `confidence_level`, `letter_text`
- Dates, amounts, IBAN, BIC, reference numbers, organization names, legal citations

`confidence_reason` is translated from the actual backend rule that produced the
current reason. It is not inferred from `confidence_level`, because different
rules can produce the same level.

### Example

```bash
curl -s -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{
    "analysis": { ...full analysis object... },
    "output_language": "Persian"
  }'
```

### Errors

| Code | Reason |
|---|---|
| 422 | Invalid `output_language` value |
| 502 | Translation request failed |
| 503 | LLM provider is not configured |

---

## GET /health

Returns backend availability status.

### Response

```json
{
  "status": "ok"
}
```

### Example

```bash
curl -s http://localhost:8000/health
```

---

## GET /ready

Returns `200` only when the configured LLM provider and API key are available
to the backend process. It does not send a test request to the provider.

### Response

```json
{
  "status": "ready"
}
```

### Errors

| Code | Reason |
|---|---|
| 503 | LLM provider or API key is not configured |

---

## Grounding Summary

Grounding differs by endpoint:

- `/chat` receives the original letter text, validated structured analysis, and bounded conversation history.
- `/follow-up` receives only the relevant subset of the validated analysis.
- `/reply-draft` receives the validated analysis, one fixed intent, and optional bounded user context.
- `/translate` receives the validated analysis and does not reprocess the original letter.

No external retrieval, vector database, or external knowledge base is used.

---

## Common Notes

**Safety note**: Every valid analysis response includes a required localized
safety note. Wording may vary, but it must state that the output is
AI-generated help rather than legal advice and recommend verification of
important decisions.

**Confidence level**: Not generated by the LLM. Calculated using rule-based logic in the backend based on the validated structured output. See [ARCHITECTURE.md](ARCHITECTURE.md) for the full ruleset.

**Multi-language**: Analysis, follow-up, and chat accept `output_language`, and
`/translate` accepts a target language. Supported values are `English`,
`German`, `Turkish`, `Arabic`, `French`, `Spanish`, `Italian`, `Portuguese`,
`Dutch`, `Polish`, `Russian`, `Japanese`, `Korean`, `Chinese`, `Hindi`, and
`Persian`. Technical values such as sender names, IBAN, amounts, references,
and legal citations are preserved. Reply drafts are always formal German.
