# Sample Letters

This folder contains synthetic sample letters for developing and testing the Official Letter Assistant.

The sample letters must not contain real personal data. They should use placeholder names, addresses, case numbers, payment references, and other identifiers.

Some sample letters may also have text-based PDF versions for testing PDF extraction. These PDFs must also be fully synthetic and must not contain real personal data.

## Folder Structure

### `dev/`

Development samples used for prompt tuning, debugging, and checking early backend behavior.

### `demo/`

A controlled sample used for the mid-term demo video.

### `eval/`

Hold-out evaluation samples used to check whether the system works on examples that were not used during prompt tuning.

## Privacy Rules

- Do not add real private letters.
- Do not add real names, addresses, case numbers, insurance numbers, student IDs, or payment details.
- Use synthetic placeholders such as `Frau Beispiel`, `Musterstraße 1`, `ABC-12345`, or fake payment references.
- Do not use `eval/` samples for prompt tuning unless we intentionally move them into `dev/`.

## Purpose

These samples help us test whether the system can extract:

- the sender
- the letter topic
- important information
- deadlines
- required actions
- payment information
- unclear or risky parts
- safe next steps

Using synthetic samples helps us test the system while avoiding privacy risks.

## LLM Testing Checklist

When the real LLM provider is connected, these development samples should be tested in a controlled order.

Suggested test order:

1. `missing_documents_deadline.txt`
2. `payment_request.txt`
3. `appointment_notice.txt`
4. `information_notice_no_clear_deadline.txt`

For each response, check whether the system:

- follows the exact MVP response schema
- keeps all list fields as lists
- extracts only information supported by the letter text
- separates deadlines, actions, payment information, and unclear/risky parts correctly
- keeps unsupported fields empty instead of inventing information
- avoids legal advice
- includes a clear safety note
- produces short, frontend-friendly result items

Cost-control rules:

- test one sample at a time
- avoid repeated calls unless the result shows a specific issue
- do not enable automatic retry in the first implementation
- revise the prompt only based on observed failures

If several samples fail in the same way, stop testing and revise the prompt or validation logic before making more API calls.