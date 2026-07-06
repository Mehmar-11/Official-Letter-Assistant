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
```

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
| `/chat` | POST | Open chat, reply draft, intent selection |
| `/translate` | POST | Re-translate an existing analysis into a different language |
| `/health` | GET | Check backend availability |

All user-facing endpoints accept an optional `output_language` parameter (default: `"English"`). 16 languages supported.

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

---

## Privacy

- Letter content is processed in memory only — no database, no log files
- Never commit real letters, API keys, or `.env` files
- Only synthetic letters are used in `sample_letters/`
