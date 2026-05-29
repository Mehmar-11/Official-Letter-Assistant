# Official Letter Assistant

Official Letter Assistant is a course project that helps users understand German official letters more easily.

The goal is not to translate a letter word-for-word. The goal is to identify the practical meaning of the letter: what it is about, whether something is urgent, what the user needs to do, which documents or payments are mentioned, and what should be double-checked.

## Problem

German official letters can be difficult to understand, especially for people who are not confident with formal German administrative language.

Users may struggle to identify deadlines, required actions, requested documents, payment information, consequences, or unclear parts of the letter.

## Solution

The application analyzes a German official letter and returns a structured English explanation.

Instead of generating loose, chatbot-style text, the backend enforces a strict JSON schema using **OpenAI Structured Outputs** paired with **Pydantic** validation. This strongly constrains the LLM response to match the backend schema and keeps it aligned with the frontend data contract.

The system separates the result into clear, scannable sections:

- Bottom line
- Urgency
- Sender
- Topic
- Useful details
- Dates and deadlines
- What the user needs to do
- Documents needed
- Payment details
- Possible consequences
- Things to double-check
- Safety note



## MVP Scope

The current MVP supports:

- pasted letter text
- text-based PDF upload
- text extraction from PDFs
- LLM-based structured analysis
- validated JSON response from the backend
- guided follow-up questions for payment, documents, consequences, and important risks
- mock response fallback when the API key is not configured
- synthetic sample letters for development and testing

Not included in the current MVP:

- OCR for scanned PDFs
- open-ended multi-turn chat about the letter
- permanent storage of uploaded letters or PDFs

## Architecture Overview

The project is split into a FastAPI backend and a React/TypeScript frontend.

### Backend Pipeline:
1. **Text Ingestion:** Extracts raw text from user input or text-based PDFs via `pdfplumber`.
2. **Strict LLM Querying:** Constructs the prompt and calls the OpenAI API utilizing native `response_format` (JSON Schema derived directly from Pydantic models).
3. **Type-Safe Validation:** Validates the structured JSON through Pydantic before sending it to the frontend. If validation fails, the backend rejects the response and returns a controlled error instead of showing incomplete output to the user.
4. **API Response:** Dispatches the validated, structured JSON payload to the frontend.
5. **Guided Follow-up:** Answers fixed follow-up question types using selected fields from the structured analysis instead of re-analyzing the full letter.

### Frontend Pipeline:
1. Captures user input and file uploads.
2. Renders the structured JSON analysis into typed, user-friendly UI components and status cards.
3. Shows guided follow-up options for common user concerns such as payment, documents, consequences, and important risks.


## Tech Stack

Backend:

- FastAPI
- Python
- OpenAI API
- Pydantic
- python-dotenv
- pdfplumber

Frontend:

- React
- TypeScript

## Run the Project

To run the full project, set up the backend first, then the frontend. See the README files below for details.

Backend setup and API usage are documented in:

    backend/README.md

Frontend setup is documented in:

    frontend/README.md

## Documentation

Important project documentation:

- `backend/README.md` — backend setup, API usage, response structure, and validation
- `frontend/README.md` — frontend setup and UI details
- `backend/sample_letters/README.md` — synthetic sample letter strategy and testing checklist
- `Docs/technical-decisions.md` — main technical decisions and design reasoning