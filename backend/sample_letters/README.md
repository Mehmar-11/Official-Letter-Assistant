# Sample Letters

This folder contains fully synthetic sample letters for developing, testing, and demoing the Official Letter Assistant.

The samples must not contain real personal data. Use placeholder names, addresses, case numbers, student IDs, payment references, and other identifiers.

Some sample letters may also have text-based PDF versions for testing PDF extraction. These PDFs must also be synthetic.

## Folder Structure

### `dev/`

Development samples used for prompt tuning, debugging, and checking backend behavior.

### `demo/`

Controlled samples used for demo videos and presentation walkthroughs.

### `eval/`

Hold-out evaluation samples used to check whether the system works on examples that were not used during prompt tuning.

Do not use `eval/` samples for prompt tuning unless we intentionally move them into `dev/`.

## Privacy Rules

- Do not add real private letters.
- Do not add real names, addresses, case numbers, insurance numbers, student IDs, or payment details.
- Use synthetic placeholders such as `Frau Beispiel`, `Musterstraße 1`, `ABC-12345`, or fake payment references.
- Do not commit screenshots or PDFs that contain real personal data.

## Current Development Samples

Suggested test order:

1. `missing_documents_deadline.txt`
   - Tests required documents, deadline extraction, required actions, and possible consequences.

2. `payment_request.txt`
   - Tests payment amount, due date, payment reference, recipient, and payment-related consequences.

3. `appointment_notice.txt`
   - Tests appointment date, location, required documents, cancellation deadline, and consequences.

4. `information_notice_no_clear_deadline.txt`
   - Tests no-guessing behavior when there is no clear deadline, payment, or required action.

## Expected Response Fields

The current backend response schema includes:

- `sender`
- `sender_type`
- `urgency_level`
- `urgency_reason`
- `letter_topic`
- `tldr`
- `useful_details`
- `deadlines`
- `required_actions`
- `required_documents`
- `payment_information`
- `possible_consequences`
- `unclear_or_risky_parts`
- `safety_note`

Removed older fields:

- `summary`
- `important_information`
- `key_facts`
- `next_steps`

## LLM Testing Checklist

For each sample response, check whether the system:

- follows the exact current response schema
- keeps all list fields as lists
- extracts only information supported by the letter text
- keeps unsupported fields empty instead of inventing information
- separates actions, documents, payments, deadlines, consequences, and useful details
- does not repeat the same information across multiple fields unless needed for clarity
- keeps payment details inside `payment_information`
- keeps required documents inside `required_documents`
- keeps practical user-facing wording short and frontend-friendly
- assigns urgency based on the letter content and the injected current date
- avoids legal advice
- includes the fixed safety note
- checks guided follow-up answers for the supported question types: `payment`, `documents`, `consequences`, and `careful`

## Cost-Control Rules

- Test one sample at a time.
- Avoid repeated calls unless the result shows a specific issue.
- Do not enable automatic retry in the first implementation.
- Revise the prompt only based on observed failures.
- If several samples fail in the same way, stop testing and revise the prompt or validation logic before making more API calls.

## Demo Note

## Demo Note

The current main demo sample is a synthetic insurance reminder letter with payment, proof-of-payment, deadlines, consequences, and risk points.

Use demo samples that are synthetic, realistic, and easy for the audience to understand.