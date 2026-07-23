# Official Letter Assistant: Completed Project Plan

**Team:** Mehri Mardoukhi, Siji Jose  
**Course:** SWP: Chat, Search and Summaries  
**Version:** 2026-07-14 - Completed v1.0

## 1. Problem Statement and Vision

### One-sentence pitch

Turn complex German official letters into clear actions, deadlines, risks, and grounded answers in the user's preferred language.

### Problem

Official letters from German public offices, universities, insurers, banks, and service providers are often written in formal administrative language. For international students, immigrants, and other residents who are not confident with formal German, a literal translation is rarely enough. They need to know what the letter means in practice: whether action is required, which deadline matters, what must be paid or submitted, and what may happen if the letter is ignored.

Misunderstanding these details can lead to missed deadlines, additional fees, interrupted services, or administrative consequences. The product therefore focuses on actionable understanding rather than word-for-word translation.

### Vision

Official Letter Assistant is a task-specific web application for understanding and responding to German official letters. Each letter is analyzed independently. A user can paste text or upload a PDF or image. The system extracts or recognizes the text, verifies that the input is a suitable letter, and returns a structured analysis with a concise bottom line, required actions, deadlines, payment details, risks, and supporting information.

After the initial analysis, the user can ask grounded questions, request an editable formal German reply, or translate the analysis into a selected language. The assistant is not a general legal chatbot: its answers remain grounded in the uploaded letter and validated analysis.

### Target users

- International students and researchers living in Germany
- Expats, immigrants, and recent arrivals
- Residents who understand conversational German but find administrative language difficult
- Anyone who needs a fast, structured explanation of an official German letter

### Ethical boundary

The system does not provide legal advice, make decisions for the user, or guarantee legal or administrative outcomes. It identifies uncertainty, includes a clear safety notice, and recommends verifying important decisions with the responsible office or a qualified adviser. Letter content is processed by OpenAI-backed services but is not stored permanently by the application.

## 2. Final Scope

### Completed core capabilities

- Paste German letter text or upload PDF, PNG, or JPEG files
- Extract text from text-based PDFs and use vision-based OCR for scanned PDFs and images
- Reject unsuitable non-letter input with a clear localized response
- Produce a validated structured analysis containing sender, topic, urgency, actions, deadlines, documents, payment information, consequences, unclear points, and a concise bottom line
- Calculate an explainable rule-based confidence level outside the LLM
- Validate exact calendar dates against dates found in the source letter
- Support analysis and grounded chat in 16 output languages, including right-to-left Persian
- Re-translate an existing analysis without repeating the full analysis request
- Stream grounded open-chat answers from the uploaded letter and validated analysis
- Offer quick prompts for common questions
- Generate an editable formal German reply from one of three bounded intents and optional user context
- Keep up to three analyzed letters temporarily in the active browser tab and allow switching between them
- Copy or export the analysis as a PDF
- Provide controlled loading, validation, network, and provider error states
- Support responsive desktop and mobile layouts, plus light and dark themes

### Supporting engineering capabilities

- Separate frontend, API routes, services, schemas, and configuration
- Health and readiness endpoints for deployment checks
- Configurable input limits, timeouts, retries, and output-token budgets
- Automated backend and frontend tests, frontend linting and build checks, and GitHub Actions CI
- Deployed frontend on Vercel and backend on Render

### Future improvements

- Optional anonymization before content is sent to the model provider
- Explicit consent controls for processing real personal letters
- Human-reviewed evaluation with consented, anonymized real-world letters
- Systematic multilingual quality evaluation beyond English scoring
- Usage and cost monitoring for a production deployment
- Broader OCR benchmarking for low-quality photographs and complex layouts

### Out of scope

- Legal advice or guaranteed administrative outcomes
- Automatic submission or sending of generated replies
- User accounts or permanent storage of private letters
- External legal retrieval, a vector database, or a general legal knowledge base
- Automated decisions on behalf of the user

## 3. User Stories

- As a non-native German speaker, I want to paste or upload an official letter so that I can understand its practical meaning without copying every detail manually.
- As a user under time pressure, I want to see the bottom line, urgency, deadlines, and required actions first.
- As a user who needs clarification, I want to ask a question in my selected language and receive an answer grounded only in my letter.
- As a user who must contact the sender, I want an editable formal German reply based on the letter facts and my intended response.
- As a multilingual user, I want to change the explanation language without uploading and analyzing the letter again.
- As a user handling several letters, I want to switch between up to three recent analyses during the current session.
- As a privacy-conscious user, I want the application to avoid persistent letter storage and explain the processing boundary clearly.
- As a user who uploads unsuitable content, I want a clear rejection rather than a confident but irrelevant analysis.

## 4. System Overview

### Basic idea

The final system retains a two-layer design. The first layer converts a German official letter into a validated structured analysis. The second layer supports controlled interaction through grounded open chat, quick prompts, translation, and reply drafting. The browser receives stable API models rather than raw model output.

### Main components

| Component | Purpose |
|---|---|
| React frontend | Handles text and file input, renders structured results, manages temporary three-letter history, and provides chat, translation, reply drafting, and export controls. |
| FastAPI backend | Exposes analysis, chat, follow-up, translation, reply-draft, health, and readiness endpoints and applies request limits and controlled errors. |
| Document processing | Uses `pdfplumber` for text-based PDFs and PyMuPDF with GPT-4o Vision for scanned PDFs and images. |
| Analysis and validation | Uses strict structured output, Pydantic validation, rule-based confidence, non-letter detection, and deterministic exact-date grounding. |
| Interaction and language services | Ground open chat and reply drafts in the source letter and validated analysis and provide explicit multilingual output control. |

### Data flow

1. The user pastes text or uploads a PDF or image.
2. The backend validates type, size, page count, and text length.
3. Text is extracted directly or through vision OCR.
4. The LLM returns a strict structured analysis in the selected output language.
5. Pydantic validates the response; backend-owned confidence and exact-date checks are applied.
6. The frontend displays the result and stores it only in active-tab memory.
7. Chat, translation, and reply requests reuse the source letter and/or validated analysis with bounded prompts.

No vector database or RAG layer is used. The task concerns one uploaded letter, so direct grounding is simpler and avoids introducing unrelated external legal information.

## 5. Technology and External Services

- **Frontend:** React 19, Vite, JavaScript, custom CSS
- **Backend:** Python 3.9+, FastAPI, Pydantic
- **Model integration:** OpenAI GPT-4o for structured output, streaming chat, translation, and vision OCR
- **Document processing:** pdfplumber and PyMuPDF
- **Testing:** Python `unittest`, Node test runner, ESLint, Vite production build
- **Automation:** GitHub Actions on pushes and pull requests to `main`
- **Deployment:** Vercel frontend and Render backend
- **Configuration:** environment variables for provider credentials, browser origins, timeouts, retries, token budgets, and input limits

## 6. Project Plan and Timeline

| Stage | Work completed | Deliverable |
|---|---|---|
| 1 | Defined the user problem, ethical boundary, initial scope, repository, and frontend/backend separation. | Shared project direction and working repository |
| 2 | Implemented text and text-based PDF analysis with strict structured output and backend validation. | First reliable structured analysis flow |
| 3 | Built the first result interface, created synthetic development letters, and completed the mid-term architecture and demo video. | Mid-term prototype and presentation |
| 4 | Expanded sample diversity and designed grounded open interaction, informed by mid-term feedback and continued testing. | Stronger test material and interaction design |
| 5 | Added image and scanned-PDF OCR, multilingual output, streaming open chat, quick prompts, and bounded reply drafting. | Expanded input and interaction workflows |
| 6 | Aligned frontend and backend contracts; completed translation, temporary history, responsive layouts, and controlled loading and error states. | Stable end-to-end user experience |
| 7 | Added runtime-safety and API tests, frontend tests, CI, a held-out Golden Set, repeated stability analysis, and final deployments. | Verified and deployable release candidate |
| 8 | Prepared final documentation, presentation slides, the recorded-demo scenario, backup material, and Q&A preparation. | Final submission package |

The final release builds on the same structured-analysis foundation presented at the mid-term. Feedback and continued user-centered testing informed a richer interaction layer, particularly grounded open chat and broader test coverage, while preserving the product's safety boundary and task-specific focus.

## 7. Roles and Responsibilities

| Role | Person | Key responsibilities |
|---|---|---|
| Product planning and coordination | Team | Scope decisions, prioritization, progress review, and alignment with course requirements |
| Backend and LLM lead | Mehri Mardoukhi | FastAPI services, schemas, prompts, structured output, grounding, OCR integration, safety controls, configuration, and backend deployment |
| Evaluation and technical documentation lead | Mehri Mardoukhi, with review support from Siji Jose | Synthetic datasets, Golden Set methodology, repeated evaluation, backend tests, architecture, API, LLM decisions, and final technical documentation |
| Frontend and UI/UX lead | Siji Jose, with design input and acceptance review from Mehri Mardoukhi | Single-page interface, responsive design, multilingual presentation, temporary history, chat and reply UI, and user-facing states |
| Frontend-backend integration | Siji Jose and Mehri Mardoukhi | API client integration, contract alignment, streaming events, translation flow, error handling, and final browser verification |
| Demo and presentation | Team | Demo selection, recording, slide preparation, backup material, and discussion preparation |

Important scope and presentation decisions were made jointly. Backend API contracts acted as the integration source of truth, and final changes were reviewed and tested before deployment.

## 8. Risk Register

| Risk | Why it matters | Mitigation used |
|---|---|---|
| Incorrect or invented LLM output | Users could misunderstand deadlines, payments, or consequences. | Ground prompts in the letter, require strict structured output, validate schemas and dates, calculate confidence with rules, and preserve uncertainty. |
| Instructions embedded in a letter | Uploaded text could attempt to override the assistant's rules. | Treat letter text and analysis as untrusted prompt data and explicitly ignore embedded instructions. |
| OCR or document-quality errors | Scans may distort dates, amounts, or reference numbers. | Prefer direct text extraction, use vision OCR only when needed, enforce file/page limits, and recommend verification of important details. |
| Legal over-reliance | A fluent explanation could be mistaken for legal advice. | Include a required safety notice, avoid legal recommendations or guarantees, and direct important decisions to the responsible office or an adviser. |
| Privacy exposure | Official letters may contain personal and financial data. | Use synthetic project data, avoid server and persistent browser storage, keep history in active-tab memory, and disclose transmission to OpenAI. |
| Provider latency, cost, or unavailability | Model calls may be slow, costly, or temporarily unavailable. | Bound token output, timeout and retries; reject missing configuration explicitly; maintain local run instructions and recorded backup material. |
| Frontend-backend contract drift | Schema or streaming mismatches can break the end-to-end workflow. | Maintain API documentation and client tests, use typed event contracts, run CI, and complete manual deployment smoke tests. |
| Multilingual variation | A correct English analysis may not guarantee equal quality in every language. | Use explicit language selection, preserve technical values, test representative Persian and Chinese outputs, and document systematic multilingual scoring as future work. |
| Scope and schedule pressure | Uncontrolled additions could reduce reliability before submission. | Prioritize the complete analysis-chat-reply workflow, postpone production-only capabilities, and freeze the final release before presentation preparation. |

## 9. Evaluation and Demo Plan

### Success criteria and evidence

| Success criterion | Final evidence |
|---|---|
| Complete end-to-end workflow | Deployed text, PDF, and image analysis; grounded chat; translation; reply drafting; temporary history; and controlled invalid-input handling were manually verified. |
| Structured extraction quality | The representative held-out run accepted 101 of 105 predefined field-level checks. |
| Robust held-out behavior | Across 10 Golden Set letters: 5 PASS, 5 PARTIAL, 0 FAIL, and 0 request errors. |
| Repeated-output stability | The same 10-letter set was run five times; urgency was stable for 8 of 10 letters and rule-based confidence for 9 of 10. |
| Development separation | Ten development letters supported prompting and debugging; the ten Golden Set letters remained held out. Two additional letters were used for final end-to-end browser checks. |
| Engineering reliability | 33 backend tests and 11 frontend tests pass; CI also runs frontend lint and production build checks. |
| Safe and privacy-aware behavior | Non-letter rejection, no-action cases, exact-date validation, required safety guidance, and non-persistent application storage are implemented and documented. |

### Evaluation approach

All development, evaluation, and demo letters are synthetic and contain no real personal data. The held-out Golden Set covers insurance, immigration, university, banking, tax, housing, telecommunications, benefits, debt collection, and deliberately vague notices. Checks combine exact field values, required-field presence, and expected content keywords with synonym and fuzzy matching.

The saved benchmark uses German source letters and English output scoring. Selected Persian and Chinese flows were checked manually, but systematic multilingual scoring, human review, and real anonymized letters remain future evaluation work. The results are evidence for the current controlled test set, not a claim of production-level real-world accuracy.

### Final demo narrative

1. Open the deployed single-page workspace and upload the first synthetic German official letter.
2. Show the structured analysis, including the bottom line, urgency, actions, deadlines, payment information, and confidence explanation.
3. Open chat and show several letter-specific questions with streamed, grounded answers.
4. Select a bounded reply intent and generate an editable formal German reply draft.
5. Change the output language and briefly show that the full analysis is translated while technical values remain unchanged.
6. Analyze a second letter and use temporary history to switch between the two results, noting that up to three letters can be held during the active tab session.
7. Close by stating the safety and privacy boundary: AI-generated help, no legal advice, and no persistent letter storage.

The recorded final video keeps the complete presentation under four minutes and divides time between the product demonstration and the backend decisions and evaluation evidence.

### Backup

The deployed workflow is tested before recording and discussion. Local startup instructions, synthetic demo files, exported results, and screenshots are retained in case the hosted services or network are unavailable.

## 10. Project References

- Repository and complete technical documentation: <https://github.com/Mehmar-11/Official-Letter-Assistant>
- Live frontend: <https://official-letter-assistant.vercel.app>
- Backend service: <https://official-letter-assistant-backend.onrender.com>
