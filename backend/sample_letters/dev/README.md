# Development Sample Letters

This folder contains synthetic development sample letters for testing the Official Letter Assistant during backend and LLM development.

These samples are used for prompt tuning, backend testing, and checking whether the system can extract structured information from German official letters.

They are not real user letters and should not be used as final hold-out evaluation samples.

## Privacy Rules

All sample letters in this folder must be fully synthetic.

Do not include:

- real names
- real addresses
- real case numbers
- real student IDs
- real insurance numbers
- real payment references
- real personal or legal information

Synthetic names, fictional cities, fake reference numbers, and fake payment details are used intentionally.

## Sample Overview

| File | Scenario | Main Testing Purpose |
|---|---|---|
| `missing_documents_deadline.txt` | Missing documents for an application | Tests required documents, required actions, a real submission deadline, and no payment hallucination |
| `payment_request.txt` | Semester fee payment request | Tests payment amount, payment deadline, recipient, payment reference, and separation of payment information from general actions |
| `appointment_notice.txt` | Appointment confirmation with cancellation option | Tests appointment date/time, cancellation deadline, location, documents to bring, and multiple-date handling |
| `information_notice_no_clear_deadline.txt` | Information-only notice about document review | Tests no-guessing behavior when no clear deadline, payment, or required action is stated |

## Testing Focus

When testing these samples, we check whether the system:

- follows the MVP response schema
- stays grounded in the letter text
- avoids inventing missing information
- separates deadlines, actions, payments, and unclear/risky parts
- keeps fields empty when information is not clearly stated
- avoids legal advice
- produces short, frontend-friendly result items

## Status

These samples are for development and prompt refinement.  
Demo and evaluation / hold-out samples are kept separate.