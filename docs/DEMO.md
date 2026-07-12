# Demo Guide

This document will be finalized after the final presentation demo scenario is selected.

The purpose of this file is to provide a practical runbook for demonstrating Letter Assistant: which sample letter to use, which features to show, and how to present the system flow clearly during the final presentation.

---

## Purpose

The demo should show the full end-to-end workflow of Letter Assistant:

1. Upload or paste a German official letter.
2. Generate a structured analysis.
3. Review urgency, deadlines, required actions, payment details, and safety information.
4. Use a quick prompt or enter a letter-specific question in open chat.
5. Show the streamed, grounded response.
6. Generate a formal German reply draft.
7. Demonstrate multilingual output where appropriate.

---

## Candidate Demo Letters

The final demo letter has not been fixed yet. Possible candidates include:

- `backend/sample_letters/demo/vitaplus_mahnung_demo.pdf`
- one selected letter from `backend/sample_letters/eval/`
- one selected letter from `backend/sample_letters/dev/`

The final choice should be based on which letter best demonstrates the core project features within the available presentation time.

---

## Recommended Demo Flow

The final flow will be adjusted after the presentation plan is finalized.

Suggested structure:

1. Open the single-page analysis workspace.
2. Upload the selected demo letter.
3. Show the structured analysis result.
4. Highlight urgency, deadlines, required actions, and confidence level.
5. Switch output language if relevant.
6. Use one quick prompt in the chat panel.
7. Ask one short open-chat question only if it adds a different fact.
8. Generate one formal German reply draft.
9. Briefly explain that the system is grounded in the uploaded letter and validated structured analysis.

---

## What to Highlight

During the demo, the presenter should emphasize:

- The system is not a general chatbot; it is grounded in the uploaded letter.
- The first layer extracts structured facts from the letter.
- Chat and reply generation reuse the validated analysis; open chat also receives the original letter text for questions that exceed the flat schema.
- The system supports text, PDF, and image input.
- The system supports multilingual explanation output.
- The generated reply remains formal German.
- Confidence level is rule-based and explainable.
- The system includes a safety boundary and does not provide legal advice.

---

## Presenter Notes

To be completed after the final demo scenario is selected.

Possible notes to add later:

- which exact file to upload
- which output language to select
- which quick chat prompt to click
- which chat question to ask
- which reply intent to choose
- expected result screenshots or talking points

---

## Backup Plan

If the deployed version is unavailable during the presentation:

1. Run the frontend locally.
2. Run the backend locally.
3. Use the same demo letter.
4. Show screenshots or exported PDF results if live API access fails.
