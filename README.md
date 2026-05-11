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
- Backend has an initial FastAPI skeleton.
- Test endpoints are available: `GET /` and `GET /health`.
- First analysis endpoint is available: `POST /analyze-text`.
- The analysis endpoint currently returns a temporary structured response based on the MVP response schema.
- LLM-based analysis will be added in the next implementation step.

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
- It returns a temporary structured response for testing.
- The response format is the planned MVP structure for letter analysis.
- Real LLM-based analysis is not connected yet.

## Planned Tech Stack

- Frontend: React
- Backend: FastAPI
- PDF processing: pdfplumber
- LLM: API-based model with structured output
- Deployment: simple cloud hosting, such as Vercel for frontend and Render for backend

## Course

SWP: Chat, Search and Summaries
