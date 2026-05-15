# Official Letter Assistant (Frontend)

## Overview

This is the frontend application for the Official Letter Assistant project.  
It is a React-based interface that allows users to input German official letters either by pasting text or uploading PDF files. The input is sent to a backend API for structured AI-based analysis.

The system is designed to help users understand complex official German documents by generating simplified explanations.

---

## Features

- Input German official letters via text or PDF upload
- Send input data to backend API for processing
- Display structured AI-generated results including:
  - Summary of the letter
  - Important deadlines
  - Required actions
  - Unclear or risky sections
- Modern UI with glassmorphism design
- Loading and processing animation
- Typewriter effect for displaying AI-generated summary

---

## Technology Stack

- React (Vite)
- JavaScript (ES6+)
- CSS (custom styling)
- Fetch API for backend communication

---

## Backend Integration

The frontend communicates with the backend using the following endpoint:

POST http://localhost:8000/analyze-text

### Request Format

```json id="doc2"
{
  "letter_text": "German official letter text here..."
}
Response Format
{
  "summary": "...",
  "deadlines": [],
  "required_actions": [],
  "unclear_or_risky_parts": []
}
Setup Instructions

Install dependencies:

npm install

Start development server:

npm run dev

The application will be available at:

http://localhost:5173

Project Structure
src/
├── App.jsx
├── main.jsx
├── index.css
└── assets/
Current Status
Frontend user interface completed
Backend API integration implemented
PDF upload UI implemented (backend processing pending)
Full system integration testing in progress
