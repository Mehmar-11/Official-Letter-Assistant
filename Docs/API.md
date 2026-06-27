# API Reference

Letter Assistant exposes four endpoints. All endpoints accept and return JSON. The `/analyze-pdf` endpoint accepts `multipart/form-data`.

Base URL (local): `http://localhost:8000`

---

## POST /analyze-text

Analyzes pasted German letter text and returns a validated structured representation.

### Request

```json
{
  "letter_text": "string"
}
```

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

### Example

```bash
curl -s -X POST http://localhost:8000/analyze-text \
  -H "Content-Type: application/json" \
  -d '{"letter_text": "Sehr geehrte Damen und Herren, wir bitten Sie, die fehlenden Unterlagen bis zum 15.06.2026 einzureichen. Aktenzeichen: ABC-12345."}'
```

### Errors

| Code | Reason |
|---|---|
| 422 | Request body missing or malformed |
| 502 | LLM response failed Pydantic validation |

---

## POST /analyze-pdf

Analyzes an uploaded PDF or image file. Accepts text-based PDFs, scanned PDFs, and images (JPEG, PNG).

- Text-based PDFs are processed with `pdfplumber`
- Scanned PDFs and images are processed with GPT-4o Vision
- If `pdfplumber` extracts fewer than 50 characters, OCR fallback triggers automatically

### Request

`Content-Type: multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `file` | file | PDF, JPEG, or PNG |

### Response

Same schema as `/analyze-text`.

### Example

```bash
curl -s -X POST http://localhost:8000/analyze-pdf \
  -F "file=@letter.pdf"
```

```bash
curl -s -X POST http://localhost:8000/analyze-pdf \
  -F "file=@letter_scan.png"
```

### Errors

| Code | Reason |
|---|---|
| 400 | Unsupported file type, empty file, or unreadable content |
| 502 | LLM response failed Pydantic validation |

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
  "question_type": "payment | documents | consequences | careful"
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
    "question_type": "payment"
  }'
```

### Errors

| Code | Reason |
|---|---|
| 422 | Missing or invalid `question_type` |
| 502 | LLM follow-up response failed Pydantic validation |

---

## POST /chat

Handles three interaction modes in a single endpoint: open chat, reply intent selection, and reply draft generation.

The chat endpoint is grounded in the uploaded letter text and validated analysis.

### Interaction Modes

| Mode | Trigger |
|---|---|
| Regular chat | `reply_intent` is `null` |
| Intent selection | Backend detects a reply request in the message |
| Reply draft | `reply_intent` is one of the three intent strings |

### Request

```json
{
  "letter_text": "string",
  "analysis": { },
  "messages": [
    { "role": "user", "content": "string" },
    { "role": "assistant", "content": "string" }
  ],
  "reply_intent": "string | null"
}
```

| Field | Description |
|---|---|
| `letter_text` | Full extracted letter text (returned by `/analyze-text` or `/analyze-pdf`) |
| `analysis` | Full `AnalyzeTextResponse` object |
| `messages` | Complete conversation history in order |
| `reply_intent` | One of three intent strings, or `null` for regular chat |

### Response

```json
{
  "reply": "string",
  "ui_action": "show_reply_options | null",
  "options": ["string"] | null
}
```

### Mode 1 — Regular Chat Reply

```json
{
  "reply": "You need to send three documents: enrollment certificate, proof of health insurance, and proof of financing.",
  "ui_action": null,
  "options": null
}
```

### Mode 2 — Intent Selection

User asks to draft a reply. Backend returns three options for the frontend to display as buttons.

```json
{
  "reply": "Sure! What's the purpose of your reply?",
  "ui_action": "show_reply_options",
  "options": [
    "I already took care of it",
    "I need more time or have a question",
    "I disagree with this letter"
  ]
}
```

### Mode 3 — Reply Draft

`reply_intent` is set. Backend generates a formal German reply using the validated analysis and the selected intent. Placeholders mark fields the system does not have.

```json
{
  "reply": "--- Bitte vor dem Absenden prüfen. Platzhalter in eckigen Klammern ausfüllen. ---\n\n[ORT, DATUM]\n\nSehr geehrte Damen und Herren,\n\nbezugnehmend auf Ihr Schreiben mit dem Aktenzeichen ABC-12345...\n\nMit freundlichen Grüßen\n[IHR VOLLSTÄNDIGER NAME]",
  "ui_action": null,
  "options": null
}
```

### Reply Intent Values

| Intent | When to use |
|---|---|
| `"I already took care of it"` | User has already paid, submitted documents, or completed the required action |
| `"I need more time or have a question"` | User cannot meet the deadline or needs clarification |
| `"I disagree with this letter"` | User disputes the amount, decision, or content of the letter |

### Example — Regular Chat

```bash
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "letter_text": "...",
    "analysis": { ...full analysis object... },
    "messages": [
      { "role": "user", "content": "What documents do I need to send?" }
    ],
    "reply_intent": null
  }'
```

### Example — Reply Draft

```bash
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "letter_text": "...",
    "analysis": { ...full analysis object... },
    "messages": [],
    "reply_intent": "I already took care of it"
  }'
```

### Errors

| Code | Reason |
|---|---|
| 422 | Missing required fields or malformed request |
| 502 | Chat or reply draft generation failed |

---

## Grounding Summary

Chat, follow-up answers, and reply drafts are grounded in:

- the uploaded letter text
- the validated structured analysis
- the current conversation history

No external retrieval, vector database, or external knowledge base is used.

---

## Common Notes

**Safety note**: Every analysis response includes a fixed safety note:
`"This is AI-generated help, not legal advice. Please verify important decisions with the responsible office or a qualified advisor."`

**Confidence level**: **Not generated by the LLM.** Calculated using rule-based logic in the backend based on the validated structured output. See [ARCHITECTURE.md](ARCHITECTURE.md) for the full ruleset.

**Multi-language**: The `/chat` endpoint automatically replies in the language the user writes in. No language parameter is needed or accepted.
