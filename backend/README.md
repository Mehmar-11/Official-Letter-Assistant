# Backend — Official Letter Assistant

This backend provides the API for analyzing German official letters. It accepts pasted text or text extracted from a text-based PDF and returns a structured English analysis.

The goal is not word-for-word translation. The goal is to help users quickly understand what the letter means, what matters, and whether they need to take action.

## Tech Stack

- FastAPI
- Python
- OpenAI API
- Pydantic
- python-dotenv
- pdfplumber

## Setup

Create and activate a virtual environment:

    python3 -m venv venv
    source venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Create a local `.env` file based on `.env.example`:

    LLM_PROVIDER=openai
    OPENAI_API_KEY=your_api_key_here
    OPENAI_MODEL=gpt-4.1-mini

Do not commit `.env` to GitHub.

## Run

From the `backend` directory:

    python3 -m uvicorn app.main:app --reload

Local backend URL:

    http://127.0.0.1:8000

## API Usage

### Analyze pasted text

Endpoint:

    POST /analyze-text

Example request:

    curl -X POST http://127.0.0.1:8000/analyze-text \
      -H "Content-Type: application/json" \
      -d '{
        "letter_text": "Sehr geehrte Damen und Herren, bitte reichen Sie die fehlenden Unterlagen bis zum 15.06.2026 ein."
      }'

Example response shape:

    {
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

### Analyze a PDF

Endpoint:

    POST /analyze-pdf

Example request:

    curl -X POST http://127.0.0.1:8000/analyze-pdf \
      -F "file=@sample_letters/dev/example.pdf"

Notes:

- Only PDF files are accepted.
- The MVP supports text-based PDFs.
- Scanned PDFs are not supported yet.
- If text cannot be extracted from a PDF, the backend returns a clear 400 error message. In the MVP, users should paste the letter text manually instead.

## Main Features

- Analyze pasted official-letter text
- Extract text from text-based PDFs
- Call the configured LLM provider
- Return structured JSON
- Validate LLM output with Pydantic
- Use mock mode when the API key is not configured

OCR is not part of the MVP because OCR mistakes can be risky for dates, payment amounts, reference numbers, and deadlines.

## LLM Analysis Design

The backend uses an LLM to analyze the letter, not to translate it word-for-word.

The response structure was redesigned to avoid long chatbot-style answers and repeated information. The backend now returns:

- one short user-friendly bottom line
- structured fields for deadlines, actions, documents, payments, consequences, risks, and useful details

The backend injects the current date into the prompt so urgency can be calculated more reliably.

## Response Fields

| Field | Purpose |
|---|---|
| `sender` | Organization or office that sent the letter. |
| `sender_type` | Type of sender, such as public office, university, insurance, bank, employer, other, or unknown. |
| `urgency_level` | Overall urgency: `High`, `Medium`, or `Low`. |
| `urgency_reason` | Short reason for the urgency level. |
| `letter_topic` | Main topic of the letter. |
| `tldr` | Short bottom-line explanation for the user. |
| `useful_details` | Useful reference/context details, such as case numbers, student IDs, submission channels, portal names, appointment locations, or relevant conditions. |
| `deadlines` | Clear deadlines, due dates, appointment dates, or response dates. |
| `required_actions` | Actions explicitly requested in the letter. |
| `required_documents` | Documents explicitly requested in the letter. |
| `payment_information` | Payment details such as amount, due date, IBAN, BIC, recipient, or payment reference. |
| `possible_consequences` | Consequences clearly stated in the letter. |
| `unclear_or_risky_parts` | Unclear, incomplete, risky, or sensitive points explicitly present in the letter. |
| `safety_note` | Fixed reminder that the response is AI-generated and not legal advice. |

## Important Response Design Changes

The current response structure replaced older, broader fields:

- `summary` was replaced by `tldr`
- `important_information` / `key_facts` were replaced by `useful_details`
- `next_steps` was removed because it repeated actions, dates, and documents
- `required_documents`, `possible_consequences`, `urgency_level`, and `urgency_reason` were added

The frontend should use user-friendly labels instead of raw backend field names.

Suggested UI labels:

| Backend field | Suggested UI label |
|---|---|
| `tldr` | Bottom line |
| `urgency_level` / `urgency_reason` | Urgency |
| `required_actions` | What you need to do |
| `required_documents` | Documents needed |
| `payment_information` | Payment details |
| `deadlines` | Dates & deadlines |
| `useful_details` | Useful details |
| `possible_consequences` | What could happen |
| `unclear_or_risky_parts` | Things to double-check |
| `safety_note` | Safety note |

## Validation and Mock Mode

LLM output is validated against `AnalyzeTextResponse` before being returned to the frontend.

Relevant files:

- `app/schemas/analysis.py`
- `app/services/llm_service.py`

If the API key is not configured, the backend returns a mock response. This allows backend and frontend development to continue without making API calls.

## Testing Notes

The current response design was tested with sample letters covering:

- Missing documents with a deadline
- Payment request
- Appointment notice
- Information-only notice with no clear deadline

Main checks:

- No invented deadlines, payments, or actions
- Required actions and required documents are separated
- Payment details stay in `payment_information`
- Urgency uses the injected current date
- Safety note is always included

## Privacy and Safety

Use synthetic or anonymized letters for development and demo.

Do not commit:

- real private letters
- API keys
- `.env` files
- screenshots containing personal data

The assistant does not provide legal advice. Important decisions should be verified with the responsible office or a qualified advisor.