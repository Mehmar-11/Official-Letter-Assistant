# Official Letter Assistant

Official Letter Assistant is an LLM-based web application that helps non-native German speakers understand German official letters through clear, structured explanations.

## Project Structure

Official-Letter-Assistant/
├── frontend/   # React frontend
├── backend/    # FastAPI backend
└── README.md

## Responsibilities

- Frontend work should be done inside `frontend/`.
- Backend work should be done inside `backend/`.
- Shared files, such as this README, should be changed after team coordination.

## Current Status

- GitHub repository is set up.
- Basic `frontend/` and `backend/` folders are created.
- Backend has an initial FastAPI structure with schemas, routes, and services.
- Test endpoints are available: `GET /` and `GET /health`.
- First analysis endpoint is available: `POST /analyze-text`.
- The MVP response schema for letter analysis is defined.
- The backend includes an `llm_service` with:
  - the first version of the letter-analysis prompt
  - environment-based API key configuration
  - a mock fallback response for development
- Real LLM provider integration is not connected yet.
- Frontend work is being developed separately and will be connected to the backend in a later step.

## Backend API

### `POST /analyze-text`

Receives German official letter text and returns a structured analysis response.

Request body:

{
  "letter_text": "Sehr geehrte Frau Müller..."
}

Response fields:

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

Current behavior:

- The endpoint accepts `letter_text` as input.
- The request is handled through the backend service layer.
- The analysis flow currently uses a mock structured response if no real LLM API key/provider is configured.
- The mock response follows the planned MVP response schema.
- Real LLM-based analysis will be added after the provider/API key decision is finalized.

## Planned Tech Stack

- Frontend: React
- Backend: FastAPI
- PDF processing: pdfplumber
- LLM: API-based model with structured output
- Deployment: simple cloud hosting, such as Vercel for frontend and Render for backend

## Course

SWP: Chat, Search and Summaries
