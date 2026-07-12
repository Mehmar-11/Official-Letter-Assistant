# Backend — Letter Assistant

FastAPI backend for analyzing German official letters. Accepts text, PDF, and image input; returns structured multilingual analysis.

---

## Tech Stack

- Python 3.9+, FastAPI, Pydantic
- OpenAI GPT-4o (structured outputs, streaming, vision)
- pdfplumber, PyMuPDF
- python-dotenv, python-multipart

---

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env`:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
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

See [`.env.example`](.env.example) for the complete runtime configuration.
The backend never returns sample LLM content when the provider is missing or
misconfigured; affected endpoints return HTTP `503` instead.

---

## Run

```bash
python3 -m uvicorn app.main:app --reload
# → http://localhost:8000
```

---

## Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/analyze-text` | POST | Analyze pasted letter text |
| `/analyze-pdf` | POST | Analyze uploaded PDF or image (JPEG, PNG) |
| `/follow-up` | POST | Answer one of four guided questions |
| `/chat` | POST | Stream grounded open-chat responses using SSE |
| `/reply-draft` | POST | Generate one formal German reply from a safe intent and optional bounded context |
| `/translate` | POST | Re-translate an existing analysis into a different language |
| `/health` | GET | Check backend availability |
| `/ready` | GET | Check whether the LLM provider is configured |

Analysis, follow-up, and chat accept an optional `output_language` parameter
(default: `"English"`), and `/translate` requires a target language. Sixteen
languages are supported. `/reply-draft` intentionally returns formal German.

Full API reference: [../docs/API.md](../docs/API.md)

---

## Project Structure

```
backend/
├── app/
│   ├── main.py
│   ├── routes/
│   │   └── analysis.py        # All endpoint definitions
│   ├── schemas/
│   │   ├── analysis.py        # Request/response Pydantic models
│   │   └── common.py          # OutputLanguage type
│   └── services/
│       ├── analysis_service.py    # Orchestration + confidence calculation
│       ├── llm_service.py         # All LLM calls and prompts
│       ├── followup_service.py    # Guided follow-up logic
│       ├── pdf_service.py         # PDF/image extraction + OCR
│       └── translation_service.py # Re-translation without re-analysis
├── evaluation/
│   ├── run_golden_set.py
│   ├── run_stability_analysis.py
│   └── expected_outputs.json
├── sample_letters/
│   ├── demo/                  # Demo letter (VitaPlus)
│   ├── dev/                   # Development letters
│   └── eval/                  # Golden set (10 letters, txt/pdf/png)
└── requirements.txt
```

---

## Evaluation

```bash
# Run golden set evaluation
python3 evaluation/run_golden_set.py

# Run stability analysis (5 repeated runs)
python3 evaluation/run_stability_analysis.py
```

Results saved to `evaluation/results/`. See [../docs/EVALUATION.md](../docs/EVALUATION.md) for methodology.

## Tests

```bash
python3 -m unittest discover -s tests -q
```

The backend suite covers API contracts, SSE behavior, input and runtime limits,
provider configuration, CORS, reply drafting, translation confidence reasons,
and deterministic date grounding.

---

## Privacy

- Letter content is processed in memory only — no database, no log files
- Never commit real letters, API keys, or `.env` files
- Only synthetic letters are used in `sample_letters/`

## Runtime Limits

- Letter text: 100,000 characters by default
- PDF/JPEG/PNG upload: 10 MB by default
- PDF length: 20 pages by default
- OpenAI request timeout: 60 seconds with one retry by default

All limits are configurable through environment variables in `.env.example`.
