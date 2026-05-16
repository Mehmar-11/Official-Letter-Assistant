# Official Letter Assistant

Official Letter Assistant is an LLM-based web application that helps users understand German official letters through clear, structured explanations.

The project focuses on practical information such as deadlines, required actions, payment information, unclear or risky parts, and safe next steps. It is designed as a structured document-understanding assistant, not a generic chatbot.

## Project Structure

```text
Official-Letter-Assistant/
├── frontend/   # React frontend
├── backend/    # FastAPI backend
├── Docs/       # Project and technical documentation
└── README.md
```

## Current Status

- React frontend and FastAPI backend are created.
- Backend has a modular structure with schemas, routes, and services.
- Test endpoints are available: `GET /` and `GET /health`.
- Text analysis endpoint is available: `POST /analyze-text`.
- Text-based PDF analysis endpoint is available: `POST /analyze-pdf`.
- The MVP response schema for structured letter analysis is defined.
- Backend includes:
  - `analysis_service` for the analysis flow
  - `llm_service` for prompt handling, mock fallback, and structured response preparation
  - `pdf_service` for text-based PDF extraction
- Frontend-backend local connection works with the current mock response.
- Synthetic development sample letters are available for testing.
- Real LLM provider integration is not connected yet.

## Backend API

### `POST /analyze-text`

Receives German official letter text and returns a structured analysis response.

Request body:

```json
{
  "letter_text": "Sehr geehrte Frau Müller..."
}
```

### `POST /analyze-pdf`

Receives a text-based PDF file, extracts readable text, and returns the same structured analysis response.

Current PDF support is limited to text-based PDFs. Scanned or image-based PDFs are not processed with OCR in the current MVP.

## MVP Response Fields

Both `/analyze-text` and `/analyze-pdf` return the same response structure:

- `sender`
- `letter_topic`
- `summary`
- `important_information`
- `deadlines`
- `required_actions`
- `payment_information`
- `unclear_or_risky_parts`
- `next_steps`
- `safety_note`

## Privacy and Safety

- No real private letters should be committed to GitHub.
- Synthetic sample letters are used for development and testing.
- Uploaded letter text and PDF files are not permanently stored by the backend.
- API keys are stored locally in `.env` and are not committed to the repository.
- The assistant explains letter content but does not provide legal advice.

## Documentation

Additional documentation is available in:

```text
Docs/technical-decisions.md
backend/sample_letters/README.md
backend/sample_letters/dev/README.md
```

These files document technical decisions, testing strategy, privacy rules, and the purpose of synthetic sample letters.

## Planned Tech Stack

- Frontend: React
- Backend: FastAPI
- PDF processing: pdfplumber
- LLM: API-based model with structured output
- Deployment: simple cloud hosting, such as Vercel for frontend and Render for backend

## Current Limitations

- Real LLM provider integration is not connected yet.
- The current analysis response is still a mock response.
- OCR for scanned or image-based PDFs is not supported in the MVP.
- Demo and hold-out evaluation samples are not finalized yet.
- Follow-up Q&A is planned only after the main analysis flow is stable.

## Course

SWP: Chat, Search and Summaries