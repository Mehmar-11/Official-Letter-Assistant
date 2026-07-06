# Limitations and Future Work

This document describes the known limitations of the current system and
the improvements planned or considered for future versions. Limitations
are documented honestly --- not as failures, but as deliberate
trade-offs made within the scope of this project.

------------------------------------------------------------------------

## Current Limitations

### OCR and Document Quality

The system uses GPT-4o Vision for OCR on scanned PDFs and images. While
this handles most real-world letter photographs, accuracy degrades with
low-resolution scans, poor lighting, handwritten annotations, or heavily
formatted layouts with complex tables or stamps.

The 50-character threshold used to trigger OCR fallback is a heuristic.
It works well for standard PDFs but may misfire on letters with very
short headers or minimal text before the main body.

### LLM Non-determinism

GPT-4o produces slightly different outputs across repeated runs with
identical input. This affects urgency classification in borderline cases
--- for example, whether a minor financial penalty constitutes a
"serious consequence" that warrants High urgency. The stability analysis
in `docs/EVALUATION.md` quantifies this effect: 8 out of 10 evaluation
samples were fully stable across 5 repeated runs, but 2 samples showed
urgency variation.

This is a property of the underlying model, not a fixable bug. The
system mitigates it through explicit prompt rules and a rule-based
confidence label, but cannot eliminate it entirely.

### Supported Document Types

The system is optimized for German official letters --- government
notices, university communications, insurance letters, bank notices,
utility and housing correspondence. It is not designed for contracts,
court documents, multi-page legal agreements, or documents that require
cross-referencing multiple attachments.

Input verification (`is_valid_letter`) rejects clearly non-letter
content, but unusual document formats may pass verification and produce
lower-quality analysis.

### Language Support

Analysis output is available in 16 languages. However, output quality
was primarily evaluated in English. Translation quality for less common
languages (e.g. Polish, Korean, Dutch) has not yet been systematically
evaluated across all supported languages.

The original letter must be in German. Non-German input is rejected by
the letter verification step.

### Privacy Considerations

Letter content is processed in memory only and never stored. However,
the system relies on the OpenAI API, which means letter content is
transmitted to a third-party service. Users handling highly sensitive
documents (immigration decisions, medical letters, legal disputes)
should be aware of this.

The current implementation is stateless and does not include user
accounts or authenticated multi-user sessions. In a shared deployment,
letter isolation relies on the stateless nature of the API rather than
application-level access controls.

------------------------------------------------------------------------

## Future Improvements

### Better OCR

Improve OCR robustness for low-quality scans through preprocessing,
image enhancement, or hybrid OCR approaches where appropriate. This
would improve accuracy for photographs taken in poor lighting or at an
angle, without replacing the current GPT-4o Vision pipeline.

### More Document Categories

Extend the system to handle German contracts, rental agreements, and
court notices. These require additional extraction fields and different
urgency logic --- for example, identifying binding clauses, cancellation
windows, and appeal deadlines that differ from standard administrative
letters.

### Expanded Multilingual Support

Evaluate and benchmark output quality across all 16 supported languages,
not just English. Add language-specific prompt tuning for languages
where output quality is consistently lower.

### Stronger Evaluation

Replace the synthetic golden set with real anonymized letters (with user
consent). Expand evaluation beyond extraction accuracy to include
usability studies, human judgment, TL;DR usefulness, urgency agreement,
and reply quality.

### Deployment Improvements

Add user authentication and session isolation for multi-user
deployments. Implement rate limiting to prevent API abuse. Add a
feedback mechanism so users can flag incorrect analyses.

### User Experience Improvements

-   Connect `required_documents` items directly to their deadlines in
    the UI.
-   Allow users to mark actions as completed.
-   Add push notifications or calendar export for deadlines.
-   Support multi-image upload so users can photograph a multi-page
    letter as separate images and have the system combine them before
    OCR and analysis.

------------------------------------------------------------------------

## Out of Scope

The following were deliberately excluded from this project and are not
planned as short-term additions:

-   **Legal advice**: The system explains what a letter says, not what
    the user should legally do. This boundary is enforced by a fixed
    safety note on every response and explicit prompt rules.
-   **German language input from users**: The chat and follow-up
    interfaces accept input in any language, but the letter itself must
    be in German.
-   **Persistent storage**: The system is designed as a stateless,
    privacy-first tool. Adding a database, user accounts, or letter
    history would require a significant redesign of the privacy model.
-   **Real-time letter fetching**: The system requires the user to
    upload or paste a letter manually. Integration with email providers
    or postal APIs is outside scope.
-   **Multi-document analysis**: The system analyzes one letter at a
    time. Cross-referencing multiple related documents is not supported.
-   **Production deployment**: High-availability infrastructure,
    monitoring, logging, and enterprise security features are outside
    the scope of this academic project.
