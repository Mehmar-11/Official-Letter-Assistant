# Frontend — Official Letter Assistant

The frontend application for **Official Letter Assistant**, a React-based interface that enables users to analyze German official letters, view structured multilingual explanations, ask contextual follow-up questions, and generate reply drafts. The application communicates with a FastAPI backend through a REST API.

---

# Technology Stack

* **React 19**
* **Vite**
* **JavaScript**
* **Custom CSS**
* **jsPDF** & **html2canvas** (PDF export)

---

# Getting Started

## Prerequisites

* Node.js (recommended LTS version)
* npm

## Installation

```bash
npm install
```

## Run the Development Server

```bash
npm run dev
```

The application will be available at:

```
http://localhost:5173
```

---

# Environment Configuration

By default, the frontend communicates with the backend at:

```
http://localhost:8000
```

To use a different backend, create a local `.env` file by copying the provided example:

```bash
cp .env.example .env
```

Then configure the API URL:

```env
VITE_API_URL=https://your-backend-url
```

> **Note:** Never commit your local `.env` file. Only `.env.example` should be tracked in version control.

For Vercel deployments, configure `VITE_API_URL` as an Environment Variable within the project settings.

---

# Application Overview

The application is implemented as a **single-page workflow**, allowing users to complete the entire letter analysis process without navigating between pages.

Users can:

* Upload or paste a German official letter
* Review a structured AI-generated analysis
* Switch between supported languages
* Ask grounded follow-up questions
* Generate editable reply drafts

Additional information regarding privacy, limitations, and product details is available through the **About** dialog.

---

# Features

## Letter Input

* Upload PDF, PNG, or JPEG files
* Paste letter text directly
* Toggle between file upload and text input modes
* File upload is the default workflow

---

## Letter Analysis

The analysis interface includes:

* Animated typewriter summary
* Sender identification
* Topic classification
* Urgency indicator
* Payment information
* Analysis confidence indicator

Additional information is organized into expandable sections:

* Required actions
* Payment details
* Required documents
* Potential consequences
* Important considerations

---

## Follow-up Assistance

Users can continue interacting with the analyzed letter through:

* Four predefined quick prompts
* Streaming grounded chat responses
* Context-aware conversation based on the current analysis

---

## Reply Draft Generation

Generate professional reply drafts with:

* Three selectable response intents
* Optional custom instructions
* Fully editable generated responses

---

## Multilingual Support

The application supports **16 interface and output languages**.

Features include:

* Localized analysis results
* Localized chat responses
* Localized temporary history controls
* Independent chat history for each language

Switching languages preserves existing conversations rather than translating or overwriting them.

---

## Productivity Features

* Copy analysis to the clipboard
* Export analysis as PDF
* Persistent dark mode with manual theme toggle
* Temporary history for the three most recently analyzed letters
* Switch between recent analyses without reprocessing
* Remove individual history entries or clear the entire session

---

## Privacy

User privacy is a core design consideration.

* Letter content is stored only in the current browser tab's memory.
* No analysis data is written to Local Storage, Session Storage, or a database.
* Closing or refreshing the browser tab permanently clears temporary history.
* Each stored letter maintains its own analysis, translations, selected language, and chat history.
* Only the user's theme preference is persisted between sessions.

---

## Error Handling

The application provides user-friendly, localized error messages for:

* Network failures
* Invalid uploads
* Model availability
* Analysis failures
* Translation failures
* Chat failures
* Reply generation failures

Supported localized error messages include:

* English
* German
* Persian

English is used as the default fallback language.

Raw backend or browser error messages are intentionally hidden from end users.

---

# Backend Integration

The frontend communicates with the backend using the base URL defined by:

```
VITE_API_URL
```

or

```
http://localhost:8000
```

## API Endpoints

| Feature            | Endpoint             |
| ------------------ | -------------------- |
| Analyze text       | `POST /analyze-text` |
| Analyze PDF/Image  | `POST /analyze-pdf`  |
| Chat               | `POST /chat`         |
| Reply Draft        | `POST /reply-draft`  |
| Translate Analysis | `POST /translate`    |

Although the backend also provides:

```
POST /follow-up
```

the current frontend routes predefined quick prompts through the `/chat` endpoint instead.

For the complete API specification, refer to:

```
docs/API.md
```

---

# Verification

Run the following commands before submitting changes:

```bash
npm test
npm run lint
npm run build
```

---

# Deployment

## Production Frontend

https://official-letter-assistant.vercel.app

## Production Backend

https://official-letter-assistant-backend.onrender.com
