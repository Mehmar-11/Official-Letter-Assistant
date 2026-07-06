# Technical Decisions

This document records the main technical decisions for the Official Letter Assistant project. It is meant to explain why the system is designed this way, not to repeat setup or API documentation.

## 1. Product Direction

Official Letter Assistant is a task-specific assistant for German official letters, not a generic chatbot.

The goal is to help users understand the practical meaning of a letter:
- what the letter is about
- whether anything is urgent
- what the user needs to do
- whether documents, payments, deadlines, or consequences are mentioned
- what should be double-checked

Decision: the system focuses on structured understanding and practical guidance, not word-for-word translation.

Reason: users usually need to know what matters and what action may be required, not a literal translation of every sentence.

## 2. Backend Separation

The backend is organized into schemas, routes, and services.

- `schemas/` defines request and response models.
- `routes/` defines API endpoints.
- `services/` contains application logic.

Decision: API handling, PDF extraction, LLM calls, validation, and follow-up logic are kept separate.

Reason: this keeps the backend easier to understand, test, debug, and extend.

## 3. Two-Layer LLM Architecture

The backend uses two main LLM-related layers:

1. **Structured Letter Analysis**
   The letter is analyzed once and converted into validated structured facts.

2. **Guided Follow-up Answering**
   A fixed follow-up question type is answered using selected fields from the structured analysis.

Decision: follow-up is built on top of structured analysis instead of re-analyzing the full letter.

Reason: this reduces cost, avoids unnecessary repeated processing, and keeps follow-up answers grounded in already extracted facts.

## 4. Guided Follow-up Instead of Open Chat

The MVP supports four fixed follow-up question types:

- `payment`
- `documents`
- `consequences`
- `careful`

Decision: the frontend sends a controlled `question_type` instead of free-form user text.

Reason: open-ended chat would increase scope, cost, and hallucination risk. Guided follow-up is easier to test and better fits the MVP goal.

## 5. Structured Output and Validation

The backend uses Pydantic response models as the source of truth.

The LLM response is requested as structured JSON and then validated again before it is returned to the frontend.

Decision: invalid or incomplete LLM output should not be shown directly to the user.

Reason: official letters may contain deadlines, payment amounts, reference numbers, and consequences. These fields must be handled carefully.

## 6. Analysis Response Design

The analysis response is structured into separate fields such as:

- `tldr`
- `urgency_level`
- `urgency_reason`
- `deadlines`
- `required_actions`
- `required_documents`
- `payment_information`
- `possible_consequences`
- `unclear_or_risky_parts`

Decision: the backend returns structured fields instead of one long chatbot-style answer.

Reason: structured fields make the frontend easier to design and help users scan the important parts of the letter quickly.

## 7. Follow-up Response Design

Follow-up answers return only:

```json
{
  "summary": "string",
  "details": ["string"]
}
## 8. Focused Context for Follow-up

Each guided question type receives only selected fields from the structured analysis.

Examples:

- `payment` uses payment information, deadlines, and required actions.
- `documents` uses required documents and deadlines.
- `consequences` uses consequences, deadlines, required actions, and risky parts.
- `careful` uses unclear or risky parts.

Decision: the LLM does not receive the full original letter for follow-up answers.

Reason: focused context keeps answers more controlled and reduces irrelevant or repeated information.

## 9. Current Schema Limitation

The current schema stores deadlines, actions, documents, payments, and consequences as separate flat lists.

Decision: keep the flat-list schema for the MVP.

Reason: it is simple, frontend-friendly, and sufficient for the current demo.

Known limitation: the backend does not always know exactly which deadline belongs to which document, payment, or action.

Future improvement: use more structured objects, for example connecting a required document directly to its condition, deadline, and submission channel.

## 10. PDF Strategy

The MVP supports text-based PDFs using `pdfplumber`.

Decision: scanned PDFs and OCR are not part of the MVP.

Reason: OCR errors in official letters can be risky, especially for dates, amounts, names, and reference numbers.

## 11. Urgency Calculation

The current date is injected into the analysis prompt.

Decision: the model should use the provided current date when deciding urgency.

Reason: urgency depends on how close a deadline is. The model should not guess the current date.

## 12. Privacy and Safety

The MVP uses synthetic sample letters for development and demo.

Decision:

- do not commit real private letters
- do not store uploaded letters permanently
- do not log full letter text
- keep API keys outside the repository
- include a fixed safety note

Reason: official letters can contain sensitive personal, financial, legal, or administrative information.

## 13. Testing Approach

The backend was tested manually with synthetic letters covering:

- payment request
- missing documents
- appointment notice
- informational notice with no action
- the final demo letter

Decision: use synthetic letters with different scenarios instead of testing only one example.

Reason: different letter types reveal different failure modes, such as invented deadlines, missing payment information, or hallucinated required actions.

## 14. Cost Control During LLM Testing

Real API calls are used carefully.

Decision:

- test one sample at a time
- avoid repeated calls without a specific reason
- revise prompts only after observed failures
- use mock mode when real LLM behavior is not needed

Reason: LLM calls cost money and can slow development.
