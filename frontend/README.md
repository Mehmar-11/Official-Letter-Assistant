# 🎨 Official Letter Assistant (Frontend)

## 📌 Overview
React frontend for an AI tool that helps users understand German official letters by turning them into simple, structured explanations.

Users can paste text or upload a PDF, and the system sends it to a backend API for AI analysis.

---

## 🚀 Features
- ✍️ Paste German official letters
- 📄 Upload PDF (UI ready)
- 🧠 Send data to backend API
- 📊 View AI results:
  - Summary
  - Deadlines
  - Required actions
  - Risky / unclear parts
- 🎨 Modern glassmorphism UI
- 📡 Loading + scanning animation
- ✨ Typewriter effect for summary

---

## ⚙️ Tech Stack
- React (Vite)
- JavaScript
- CSS (custom styling)
- Fetch API

---

## 🔗 Backend Connection
The frontend connects to:

`POST http://localhost:8000/analyze-text`

### Request:
```json id="onepage2"
{
  "letter_text": "German official letter text here..."
}
Response:
{
  "summary": "...",
  "deadlines": [],
  "required_actions": [],
  "unclear_or_risky_parts": []
}
▶️ Run Project
npm install
npm run dev

Open:

http://localhost:5173
📁 Structure
src/
 ├── App.jsx
 ├── main.jsx
 ├── index.css
 └── assets/
🚧 Status
UI complete
Backend integration ready
PDF backend processing pending
Final testing in progress
