# Letter Assistant

A practical LLM-powered application that helps people living in Germany understand and respond to official German letters more confidently.

---

## The Problem

People living in Germany who are not fluent in German regularly receive official letters from government offices, insurance companies, universities, banks, and employers. These letters are often long, bureaucratic, and full of legal language. Missing a deadline or misunderstanding a required action can have real consequences.

**Letter Assistant** solves this by transforming complex German official letters into clear, structured, actionable information — and then letting users ask follow-up questions in their own language.

---

## Target Users

Anyone living in Germany who receives official German letters but is not fully fluent in German — including international students, expats, and recent immigrants.

---

## Core Features

- **Structured letter analysis** — extracts sender, topic, urgency, deadlines, required actions, documents, payment details, risks, and unclear parts
- **Input verification** — detects non-letter content inside the structured analysis flow and returns a compact rejection response
- **Analysis quality label** — rule-based confidence level (high / medium / low) with a clear reason
- **OCR support** — handles scanned PDFs and image uploads (jpg/png) using GPT-4o Vision
- **Grounded open chat** — users can ask open-ended questions about the letter in their own language; all responses are grounded in the uploaded letter text and structured analysis, not general knowledge
- **Multi-language chat** — replies use the output language explicitly selected by the user
- **Reply draft assistant** — generates a formal German reply letter based on user intent and extracted letter facts
- **Guided follow-up** — four pre-defined question cards (payment, documents, risks, careful points)
- **Privacy by design** — no permanent storage; letter text and analysis are processed in memory only and not written to any database or persistent storage

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| LLM | OpenAI GPT-4o |
| Validation | Pydantic |
| PDF extraction | pdfplumber |
| OCR | GPT-4o Vision (via PyMuPDF) |
| Frontend | React |

---

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- OpenAI API key

### Environment Variables

Create a `.env` file in the `backend/` directory:

```
OPENAI_API_KEY=your_api_key_here
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o
OPENAI_TIMEOUT_SECONDS=60
OPENAI_MAX_RETRIES=1
OPENAI_ANALYSIS_MAX_OUTPUT_TOKENS=3000
OPENAI_FOLLOWUP_MAX_OUTPUT_TOKENS=1000
OPENAI_CHAT_MAX_OUTPUT_TOKENS=1000
OPENAI_REPLY_MAX_OUTPUT_TOKENS=1500
CORS_ORIGINS=http://localhost:5173,https://official-letter-assistant.vercel.app
MAX_LETTER_TEXT_CHARS=100000
MAX_UPLOAD_BYTES=10485760
MAX_PDF_PAGES=20
```

The complete template is available in [`backend/.env.example`](../backend/.env.example).
Missing LLM configuration produces HTTP `503`; the backend never substitutes
sample analysis or reply content.

### Run Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`

### Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## Documentation

- [Architecture & System Design](ARCHITECTURE.md)
- [API Reference](API.md)
- [Technical Decisions](TECHNICAL_DECISIONS.md)
- [LLM Design Decisions](LLM_DECISIONS.md)
- [Evaluation & Golden Set](EVALUATION.md)
- [Demo Narrative](DEMO.md)
- [Limitations & Future Work](LIMITATIONS_AND_FUTURE_WORK.md)

---

## How This Project Addresses the Evaluation Criteria

| Criterion | How We Address It |
|---|---|
| **Core functionality** | End-to-end workflow: upload letter (text, PDF, or image) → structured analysis → guided follow-up → grounded open chat → reply draft. Covered by demo scenarios and golden set evaluation. |
| **LLM integration quality** | Two-layer prompting architecture, Pydantic validation at every LLM boundary, grounding strictly in letter text and structured analysis, rule-based confidence level (not LLM-generated), streaming, safety notes on every response. |
| **Engineering practice** | FastAPI with clear route/service/schema separation, Pydantic schema validation before UI rendering, controlled error handling, bounded uploads and model output, environment-based CORS and provider configuration, and golden set evaluation. |
| **User experience** | Structured result cards, guided question cards, grounded open chat with multi-language support, reply draft with smart placeholders, analysis quality label, clear privacy notice, and dark mode UI. |
| **Documentation** | API reference, architecture diagram, LLM design decisions, golden set evaluation, demo guide — all in the `docs/` folder. |
| **Innovation & ethics** | No permanent storage (session-only), synthetic demo data, input verification to reject non-letter content, safety note on every analysis, rule-based confidence label to prevent over-trust in LLM output. |
