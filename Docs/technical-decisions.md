# Technical Decisions

This document records the main technical decisions for the Official Letter Assistant project. The goal is to keep the implementation consistent and make our design choices clear for development, documentation, and presentation.

## 1. Project Direction

Official Letter Assistant is not a generic chatbot. It is a task-specific assistant for understanding German official letters.

The system helps users identify practical information from a letter, such as:

- who sent the letter
- what the letter is about
- how urgent it is
- whether there are deadlines
- whether any action is required
- whether documents are needed
- whether payment information is included
- what consequences are clearly stated
- what should be double-checked

Reason: Users often do not need a word-for-word translation. They need to understand what the letter means in practice and what information matters.

## 2. Backend Structure

We use a modular FastAPI backend with separate folders for schemas, routes, and services.

- `schemas/` defines request and response structures.
- `routes/` defines API endpoints.
- `services/` contains application logic.

Current backend flows:

    POST /analyze-text
    → analysis route
    → analysis_service
    → llm_service
    → structured response

    POST /analyze-pdf
    → analysis route
    → pdf_service
    → analysis_service
    → llm_service
    → structured response

Reason: PDF extraction, prompt construction, LLM communication, response validation, and API handling should not be mixed inside one endpoint. Separating these parts keeps the backend easier to understand, test, and extend.

## 3. API Endpoints

The backend currently provides two main analysis endpoints:

    POST /analyze-text

Used when the user provides pasted letter text.

    POST /analyze-pdf

Used when the user uploads a text-based PDF.

Both endpoints return the same structured response schema.

Reason: The frontend can handle text input and PDF input in a consistent way because both flows produce the same response format.

## 4. LLM Provider Decision

The project currently uses OpenAI as the LLM provider.

Provider-specific logic is kept inside:

    app/services/llm_service.py

Reason: The rest of the backend should not depend directly on one specific LLM provider. If we later change providers, most provider-specific changes should stay inside the LLM service.

## 5. Structured Response Design

The analysis endpoint returns structured JSON instead of a free-form chatbot answer.

The response structure was redesigned after real LLM testing showed that some fields caused repeated or overly chatbot-like output.

Current response fields:

- `sender` / `sender_type` — who sent the letter
- `urgency_level` / `urgency_reason` — how urgent the letter is and why
- `letter_topic` — the main topic
- `tldr` — short bottom-line explanation
- `useful_details` — reference numbers, IDs, submission channels, locations, or other useful context
- `deadlines` — clear deadlines, due dates, response dates, or appointment dates
- `required_actions` — actions explicitly requested in the letter
- `required_documents` — documents explicitly requested in the letter
- `payment_information` — payment amounts, IBAN, BIC, recipients, or payment references
- `possible_consequences` — consequences clearly stated in the letter
- `unclear_or_risky_parts` — unclear, incomplete, or sensitive points
- `safety_note` — fixed AI and legal-advice disclaimer

Main redesign changes:

- `summary` was replaced by `tldr`
- `important_information` / `key_facts` were replaced by `useful_details`
- `next_steps` was removed because it repeated actions, dates, and documents
- `required_documents`, `possible_consequences`, `urgency_level`, and `urgency_reason` were added

The frontend should use user-friendly labels instead of raw backend field names. For example, `tldr` can be shown as “Bottom line”, `required_actions` as “What you need to do”, and `unclear_or_risky_parts` as “Things to double-check.”

Reason: Structured fields help the frontend display results clearly. The redesign removed overlap and kept the output shorter and more practical. Backend names stay stable for development, while UI labels stay natural for users.

## 6. Prompt Design

The prompt is designed specifically for German bureaucratic and administrative letters.

It instructs the model to:

- analyze, not translate
- use only the provided letter text
- avoid unsupported assumptions
- avoid inventing deadlines, payments, actions, senders, or consequences
- return all user-facing content in English
- keep the output short and practical
- separate information into the exact response fields
- avoid legal advice
- include a fixed safety note

Reason: The assistant should behave like a careful document-understanding tool, not a general chatbot that freely discusses the letter.

## 7. Urgency Calculation

The backend injects the current date into the prompt for urgency calculation.

Urgency levels are based on:

- whether action is required
- whether a deadline exists
- whether the deadline is within 14 days
- whether a serious consequence is clearly stated

Reason: The LLM should not guess the current date. Injecting the current date makes urgency classification more reliable and easier to explain.

## 8. Structured Output and Validation

The backend uses `AnalyzeTextResponse` as the single source of truth for the response schema.

The LLM is called with structured JSON schema output, and the returned response is validated again with Pydantic before being sent to the frontend.

Flow:

    letter text
    → prompt with current date
    → OpenAI structured output
    → JSON response
    → Pydantic validation
    → frontend-ready response

Reason: The system should not trust LLM output blindly. Official letters may contain deadlines, payments, and administrative consequences, so malformed or incomplete output should not be passed directly to the user interface.

## 9. Mock Fallback

If the OpenAI API key is not configured, the backend returns a mock structured response.

Reason: This allows backend and frontend development to continue without making API calls.

Limitation: The mock response is only a development fallback. It is not a real letter analysis and should not be used to hide real LLM errors once the provider is configured.

## 10. PDF Processing Strategy

The MVP supports text-based PDF extraction through the `/analyze-pdf` endpoint.

Current PDF flow:

    PDF upload
    → validate file type
    → read file in memory
    → extract text with pdf_service
    → analyze extracted text
    → return AnalyzeTextResponse

Scanned or image-based PDFs are not processed with OCR in the MVP.

If text cannot be extracted from a PDF, the backend returns a clear 400 error message. In the MVP, users should paste the letter text manually instead.

Reason: OCR introduces a separate accuracy problem. In official letters, OCR mistakes can be risky because dates, payment amounts, names, and reference numbers may be misread.

## 11. Privacy Strategy

Official letters can contain sensitive personal information, such as names, addresses, case numbers, residence information, insurance details, payment references, or university IDs.

For the MVP, we follow these privacy decisions:

- no real private letters in GitHub
- no real personal data in demo screenshots or videos
- no permanent storage of uploaded letters or PDFs
- PDF files are read in memory
- no full letter text in backend logs
- synthetic sample letters for testing and demo
- API keys stored outside the repository

Reason: The MVP should process the letter for the current request only. Avoiding permanent storage and real personal data reduces privacy risk.

## 12. Safety Boundary

The system explains the content of a letter but does not provide legal advice.

The assistant should not:

- make decisions for the user
- guarantee legal or administrative outcomes
- invent consequences that are not clearly stated
- tell the user what legal action to take

The structured response includes a fixed `safety_note`.

Reason: Official letters may have legal or administrative consequences. The system should help users understand the letter, but users should verify important information with the responsible office or a qualified advisor.

## 13. Testing Strategy

We use synthetic sample letters for development, demo, and evaluation.

Current development samples cover:

- missing documents with a deadline
- semester fee payment request
- appointment notice
- information-only notice with no clear deadline or required action

Main testing checks:

- no invented deadlines
- no invented payment information
- no invented required actions
- required actions and required documents are separated
- payment details stay in `payment_information`
- urgency uses the injected current date
- unsupported fields stay empty
- safety note is always included

Reason: Testing only one example would be weak. Different synthetic samples help check whether the system works across several common official-letter scenarios while avoiding privacy risks.

## 14. Cost-Control During LLM Testing

Real API calls are used carefully.

Testing rules:

- test one sample at a time
- avoid repeated calls unless there is a specific failure
- revise the prompt only based on observed failures
- stop testing if several samples fail in the same way
- use mock mode when real LLM behavior is not required

Reason: LLM calls cost money and can slow development. Controlled testing helps improve the system without wasting API usage.

## 15. Current Limitations

Current MVP limitations:

- Scanned PDFs: OCR is not supported because misreading dates, amounts, names, or reference numbers in official letters could be risky for users. OCR is planned for a future version after the core workflow is stable.
- Follow-up Q&A: Users cannot ask follow-up questions about the letter in the current version.
- Text extraction quality: Analysis quality depends on the quality of extracted text. Poorly formatted PDFs may produce incomplete or unreliable results.
- No legal advice: The system explains letter content but cannot replace professional legal or administrative advice.

Reason: These limitations are intentional for the current stage. The priority is a stable core workflow for structured analysis of text and text-based PDFs.