# Frontend — Letter Assistant

React frontend for the Letter Assistant application. Communicates with the FastAPI backend to analyze German official letters and present results in a structured, multilingual interface.

---

## Tech Stack

- React 19, Vite, JavaScript
- Custom CSS (no framework)
- jsPDF + html2canvas (PDF export)
- pdfjs-dist (PDF preview)

---

## Setup

```bash
npm install
npm run dev
# → http://localhost:5173
```

The frontend expects the backend at `http://localhost:8000` by default. To use a different URL, set `VITE_API_URL` in a `.env` file:

```
VITE_API_URL=https://your-backend-url
```

---

## Pages

| Page | Route | Description |
|---|---|---|
| Landing Page | `/` | Introduction and entry point |
| Dashboard | `/dashboard` | Main analysis interface |

---

## Features

**Input**
- Paste letter text
- Upload PDF or image (JPEG, PNG)
- Automatic mode detection

**Analysis display**
- Animated typewriter summary
- Accordion sections: urgency, deadlines, required actions, documents, payment, consequences, unclear parts
- Analysis quality label (confidence level)

**Follow-up**
- Four guided question cards: payment, documents, consequences, careful
- Grounded open chat with streaming responses
- Reply draft with three selectable intents

**Language**
- Language selector dropdown (16 languages)
- All analysis fields and chat responses returned in the selected language

**Utilities**
- Copy analysis to clipboard
- Export analysis as PDF
- Dark mode toggle
- Session letter counter

---

## Backend Communication

All API calls use the base URL from `VITE_API_URL` or `http://localhost:8000`.

| Action | Endpoint |
|---|---|
| Analyze text | `POST /analyze-text` |
| Analyze PDF/image | `POST /analyze-pdf` |
| Guided follow-up | `POST /follow-up` |
| Open chat | `POST /chat` |
| Language switch | `POST /translate` |

Full API reference: [../docs/API.md](../docs/API.md)

---

## Deployment

**Frontend:** `<TO_BE_ADDED>`  
**Backend:** `<TO_BE_ADDED>`
