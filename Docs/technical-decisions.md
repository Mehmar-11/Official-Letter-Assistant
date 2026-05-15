# Technical Decisions

This document records the main technical decisions for the Official Letter Assistant project.  
The goal is to keep the implementation consistent and to make our design choices clear for development, documentation, and presentation.

## 1. Project Direction

Official Letter Assistant is not designed as a generic chatbot.  
It is a task-specific document-understanding assistant for German official letters.

The system should help users identify practical information from a letter, such as:

- who sent the letter
- what the letter is about
- important information
- deadlines
- required actions
- payment information
- unclear or risky parts
- safe next steps

Reason: Users often do not only need a translation. They need to understand what the letter means in practice and what should be checked or done next.

## 2. Backend Structure

We use a modular FastAPI backend with separate folders for schemas, routes, and services.

- `schemas/` defines request and response structures.
- `routes/` defines API endpoints.
- `services/` contains the application logic.

Current backend flow:

```text
POST /analyze-text
→ analysis route
→ analysis_service
→ llm_service
→ structured response
```

Reason: PDF extraction, prompt construction, LLM communication, response validation, and API handling should not be mixed inside one endpoint. Separating these parts keeps the backend easier to understand, test, and extend.

## 3. MVP Analysis Response Schema

The analysis endpoint returns a structured response instead of a free-form chatbot answer.

Current MVP response fields:

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

Reason: These fields match the main questions a user has when reading an official letter: what is this about, what matters, what needs to be done, whether there is a deadline or payment, and what should be checked carefully.

This structure also helps the frontend display the result in clear sections or cards instead of showing one long answer.

## 4. LLM Service Design

LLM-related logic is separated into `llm_service.py`.

The purpose of this file is to handle:

- LLM configuration
- prompt construction
- provider-specific communication
- future parsing of LLM responses

Reason: The rest of the backend should not depend directly on one specific LLM provider. If we later switch from one provider to another, most provider-specific changes should stay inside `llm_service.py`.

The `analysis_service.py` should focus on the project-specific analysis flow, while `llm_service.py` handles the external model interaction.

## 5. Prompt Design

The first prompt version is designed specifically for German official letters.

The prompt is not a general “summarize this text” instruction. It includes rules for:

- using only the provided letter text
- avoiding unsupported assumptions
- not inventing deadlines, payments, actions, senders, or consequences
- avoiding legal advice
- returning the exact MVP response structure
- keeping the output short and suitable for frontend cards
- not translating the full letter
- marking unclear or risky parts instead of guessing

Reason: The goal is to control the LLM output and reduce generic chatbot behavior. The assistant should extract practical information from the letter, not freely discuss the document.

## 6. Mock Fallback

Until the real LLM provider and API key are finalized, the backend uses a mock structured response.

The mock response follows the same structure as the planned real LLM response.

Reason: This allows backend and frontend development to continue without blocking the project. The frontend can already work with the expected response fields.

Limitation: The mock response is only a development fallback. It is not a real analysis and should not be presented as LLM functionality.

## 7. Secret Management

LLM API keys are stored in a local `.env` file and are not committed to GitHub.

We provide `.env.example` as a safe template for required environment variables.

Reason: API keys are secrets. They should not appear in source code, frontend code, README files, screenshots, or GitHub history.

Current approach:

- `.env` is local only
- `.env.example` is safe to commit
- `.gitignore` prevents `.env` and other local files from being tracked

## 8. Privacy Strategy

Official letters can contain sensitive personal information, such as names, addresses, case numbers, residence information, insurance details, payment references, or university IDs.

For the MVP, we follow these privacy decisions:

- no real private letters in GitHub
- no real personal data in demo screenshots or videos
- no permanent storage of uploaded letters
- no full letter text in backend logs
- synthetic sample letters for testing and demo
- API keys stored outside the repository

Reason: The MVP should process the letter for the current request only. Avoiding permanent storage and real personal data reduces privacy risk and keeps the project manageable.

## 9. Safety Boundary

The system explains the content of a letter but does not provide legal advice.

The assistant should not:

- make decisions for the user
- guarantee legal or administrative outcomes
- invent consequences that are not clearly stated in the letter
- tell the user what legal action to take

Reason: Official letters may have legal or administrative consequences. The system should help users understand the letter, but users should verify important information with the responsible office or a qualified advisor.

## 10. Testing Strategy

We plan to test the system with synthetic sample letters.

The samples should cover different official-letter scenarios, such as:

- missing documents
- payment request
- appointment notice
- no clear deadline
- unclear or risky wording
- university or insurance-related notices

We plan to separate sample letters into:

- development samples for prompt tuning and debugging
- a controlled demo sample for the mid-term video
- evaluation / hold-out samples to check whether the system works beyond the examples used during development

Reason: Testing only with one example would be weak. Using different synthetic samples helps us evaluate whether the system extracts deadlines, actions, payments, and unclear parts consistently while avoiding privacy risks.

## 11. Current Limitations

The current implementation is still in progress.

Current limitations:

- real LLM provider integration is not connected yet
- PDF upload and text extraction are not implemented yet
- the mock response is not a real analysis
- scanned PDFs with OCR are outside the MVP scope for now
- follow-up Q&A will be added only after the main analysis flow is stable

Reason: These limitations are intentional for the current stage. The priority is to build a stable core workflow first, then extend it step by step.

## 12. Mid-term Focus

For the mid-term demo, the main goal is to show a stable core workflow:

```text
user provides a letter
→ backend processes the text
→ LLM-based analysis returns a structured result
→ frontend displays the result clearly
```

The demo should emphasize:

- the user problem
- the structured analysis output
- safety and privacy boundaries
- the difference from a generic chatbot
- next steps toward PDF upload, testing, and follow-up Q&A

Reason: The mid-term video should show real progress and a clear technical direction, not only a concept or a generic LLM wrapper.

