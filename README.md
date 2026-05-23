# Official Letter Assistant

Official Letter Assistant is a course project that helps users understand German official letters more easily.

The goal is not to translate a letter word-for-word. The goal is to identify the practical meaning of the letter: what it is about, whether something is urgent, what the user needs to do, which documents or payments are mentioned, and what should be double-checked.

## Problem

German official letters can be difficult to understand, especially for people who are not confident with formal German administrative language.

Users may struggle to identify deadlines, required actions, requested documents, payment information, consequences, or unclear parts of the letter.

## Solution

The application analyzes a German official letter and returns a structured English explanation.

Instead of giving a long chatbot-style answer, the system separates the result into clear sections such as:

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

This makes the result easier to display in the frontend and easier for the user to understand.

## MVP Scope

The current MVP supports:

- pasted letter text
- text-based PDF upload
- text extraction from PDFs
- LLM-based structured analysis
- validated JSON response from the backend
- mock response fallback when the API key is not configured
- synthetic sample letters for development and testing

Not included in the current MVP:

- OCR for scanned PDFs
- follow-up Q&A about the letter
- permanent storage of uploaded letters or PDFs

## Architecture Overview

The project is split into frontend and backend parts.

The backend handles:

- API endpoints
- PDF text extraction
- prompt construction
- LLM provider communication
- structured output validation
- mock fallback behavior

The frontend handles:

- user input
- file upload
- displaying the structured analysis result
- user-friendly labels and layout

Basic flow:

    user submits text or a text-based PDF
    → backend extracts/processes the text
    → LLM returns structured analysis
    → backend validates the response
    → frontend displays the result

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