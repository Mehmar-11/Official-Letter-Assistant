# Frontend — Letter Assistant

React frontend for the Letter Assistant application. Communicates with the FastAPI backend to analyze German official letters and present results in a structured, multilingual interface.

---

## Tech Stack

- React 19, Vite, JavaScript
- Custom CSS (no framework)
- jsPDF + html2canvas (PDF export)

---

## Setup

```bash
npm install
npm run dev
# → http://localhost:5173
```

The frontend expects the backend at `http://localhost:8000` by default. Copy
`.env.example` to an untracked `.env` file when a different local URL is
needed:

```
VITE_API_URL=https://your-backend-url
```

For Vercel, configure `VITE_API_URL` in the project environment variables.
Do not commit the real `.env` file.

---

## Application Structure

The application is a single-page workflow at `/`. Users can paste or upload a
letter, inspect its analysis, switch languages, ask grounded questions, and
create a reply without moving between routes. Product details, privacy, and
limitations are available from the **About** dialog.

---

## Features

**Input**
- Paste letter text
- Upload PDF or image (JPEG, PNG)
- Explicit text or file input mode
- File upload is the default input mode; pasted text remains one click away

**Analysis display**
- Animated typewriter summary
- Sender, topic, urgency, payment, and analysis-quality indicators
- Accordion sections for required actions, payment, documents, consequences, and careful points
- Analysis quality label (confidence level)

**Follow-up**
- Four quick prompts routed through grounded open chat
- Grounded open chat with streaming responses
- Reply draft with three selectable intents, optional details, and an editable result

**Language**
- Language selector dropdown (16 languages)
- All analysis fields and chat responses returned in the selected language
- Chat history is kept separately per language, so switching languages does not translate or discard earlier conversations
- Temporary-history controls are localized for all 16 supported interface languages

**Utilities**
- Copy analysis to clipboard
- Export analysis as PDF
- Dark mode by default with a persistent manual theme toggle
- Temporary history for the three most recently analyzed letters
- Switch between recent letters without another analysis call
- Remove one letter or clear the complete temporary history

**Temporary history and privacy**
- Recent letters are held only in the memory of the current browser tab
- No letter content is written to local storage, session storage, or a database; only the theme preference is persisted
- Refreshing or closing the tab clears the history
- Each saved letter keeps its own analysis, language, translations, and chat state

**Error handling**
- Network, upload validation, model availability, analysis, translation, chat, and reply-draft failures have distinct user-facing messages
- Analysis and translation errors appear in the result area; chat and reply-draft errors appear in the chat panel
- Error messages are localized in English, German, and Persian, with English as the fallback for other interface languages
- Raw backend and browser error wording is not shown directly to users

---

## Backend Communication

All API calls use the base URL from `VITE_API_URL` or `http://localhost:8000`.

| Action | Endpoint |
|---|---|
| Analyze text | `POST /analyze-text` |
| Analyze PDF/image | `POST /analyze-pdf` |
| Open chat | `POST /chat` |
| Generate reply draft | `POST /reply-draft` |
| Language switch | `POST /translate` |

Full API reference: [../docs/API.md](../docs/API.md)

The backend also exposes `POST /follow-up` for four bounded guided question
types. The current frontend uses quick prompts through `/chat` instead of
calling that endpoint directly.

## Verification

```bash
npm test
npm run lint
npm run build
```

---

## Deployment

- **Frontend:** https://official-letter-assistant.vercel.app
- **Backend:** https://official-letter-assistant-backend.onrender.com
