# Technical Decisions

This document records engineering and product decisions that shaped the Letter Assistant system. It covers choices about product scope, response design, schema structure, input handling, and operational constraints — not LLM prompting decisions (see [LLM_DECISIONS.md](LLM_DECISIONS.md)) or system architecture (see [ARCHITECTURE.md](ARCHITECTURE.md)).

---

## 1. Task-Specific Assistant, Not a Generic Chatbot

**Decision**: Letter Assistant is scoped to German official letters only. It is not a general-purpose assistant.

**Why**: Generic chatbots produce generic answers. Official letters require specific, structured extraction — deadlines, required actions, payment details, consequences. A task-specific scope allows the system to be optimized for one thing and do it reliably.

**Trade-off**: The system rejects non-letter input (`is_valid_letter: false`). Users cannot ask general questions about German bureaucracy outside the context of an uploaded letter.

---

## 2. Structured Response Fields Over Prose

**Decision**: The analysis response returns separate typed fields (`tldr`, `urgency_level`, `deadlines`, `required_actions`, `payment_information`, etc.) rather than a single chatbot-style answer.

**Why**: Structured fields allow the frontend to present information in a scannable layout — urgency badge, deadline list, payment block — rather than forcing the user to read a long paragraph. They also make validation, testing, and evaluation tractable.

**Trade-off**: Some nuance is lost when compressing a complex letter into flat lists. The `unclear_or_risky_parts` field captures what does not fit cleanly elsewhere.

---

## 3. Focused Context for Guided Follow-up

**Decision**: Each guided question type receives only the relevant subset of the structured analysis, not the full letter text or full analysis object.

| Question type | Fields used |
|---|---|
| `payment` | `payment_information`, `deadlines`, `required_actions` |
| `documents` | `required_documents`, `deadlines` |
| `consequences` | `possible_consequences`, `deadlines`, `required_actions`, `unclear_or_risky_parts` |
| `careful` | `unclear_or_risky_parts`, `possible_consequences` |

**Why**: Focused context produces more controlled, relevant answers. Passing the entire analysis or original letter increases the chance of the model repeating information already visible in the UI.

**Trade-off**: If a relevant detail is in a field not included for a given question type, the follow-up answer may miss it. The open chat endpoint handles edge cases that guided follow-up cannot.

---

## 4. Flat-List Schema with Known Limitation

**Decision**: Deadlines, actions, documents, payments, and consequences are stored as separate flat string lists.

**Why**: Simple, frontend-friendly, and sufficient for the current scope. The frontend can render each list independently without complex object traversal.

**Known limitation**: The schema does not model relationships between fields. For example, a required document may have its own deadline and submission channel, but these are not linked in the current structure.

**Future improvement**: Use structured objects that connect related facts — e.g. a `RequiredDocument` object with `name`, `deadline`, and `submission_channel`.

---

## 5. PDF and Image Input Strategy

**Decision**: Text-based PDFs use `pdfplumber`. Scanned PDFs and images use GPT-4o Vision OCR via PyMuPDF page rendering. OCR fallback triggers automatically when `pdfplumber` extracts fewer than 50 characters.

**Why**: Most official German letters are digital PDFs. `pdfplumber` is fast and accurate for these. GPT-4o Vision handles scanned documents and photos — common for users photographing physical letters. The 50-character threshold is conservative enough to catch truly empty extractions without false-positiving on letters with short headers.

**Trade-off**: GPT-4o Vision OCR is slower and costs more per call than `pdfplumber`. Accuracy may vary for low-quality photographs or handwritten annotations.

---

## 6. Current Date Injection for Urgency

**Decision**: The current date is injected into the analysis prompt at request time.

**Why**: Urgency depends on how close a deadline is. Without the current date, the model cannot determine whether a deadline is tomorrow or six months away. The date is used only for urgency calculation — the model is explicitly instructed not to use it to infer or modify other letter content.

---

## 7. Backend Folder Structure

**Decision**: The backend is organized into `routes/`, `schemas/`, and `services/`.

| Folder | Responsibility |
|---|---|
| `routes/` | FastAPI endpoint definitions, request validation, HTTP error handling |
| `schemas/` | Pydantic request/response models and shared types (`OutputLanguage`) |
| `services/` | All application logic — LLM calls, PDF extraction, analysis, follow-up, translation |

**Why**: Separating concerns at the folder level makes the codebase navigable. A developer reading `routes/analysis.py` sees only HTTP handling. All logic lives in `services/`. Translation was implemented as a dedicated service (`translation_service.py`) to keep analysis and localization responsibilities separate.

---

## 8. Privacy and Safety Constraints

**Decision**:
- Letter content is processed in memory only — no database writes, no log files containing letter text
- Real letters are never committed to the repository; only synthetic letters are used for development and evaluation
- API keys are stored in `.env` and excluded from version control
- Translation operates on the validated structured analysis rather than re-processing the original letter, reducing unnecessary LLM work and keeping translated outputs consistent with the original analysis
- Every analysis response includes a fixed safety note that cannot be omitted by the model

**Why**: Official German letters routinely contain personal identification numbers, financial details, immigration status, and legal references. These constraints are not optional — they are requirements for responsible handling of sensitive documents.
