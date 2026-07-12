# Evaluation

This document describes how we evaluated the Letter Assistant backend. The goal was not to show a high pass rate, but to measure extraction quality, reasoning consistency, and evaluation framework reliability across repeated runs.

---

## Methodology

We designed a **Golden Set** of 10 synthetic German official letters covering diverse real-world scenarios. For each letter, we defined expected outputs and keyword checks, then ran the evaluation script multiple times to assess both accuracy and stability.

Evaluation checks three layers:

1. **Field equality** — Does the system return the correct `urgency_level`, `sender_type`, `confidence_level`?
2. **Field presence** — Are required fields non-empty when they should be?
3. **Content correctness** — Do key facts appear in the right fields? (keyword matching with fuzzy/synonym support)

Each check produces one of:
- **PASS** — all checks passed with no partial matches
- **PARTIAL** — at least 70% of checks were accepted, including semantic partial keyword matches, but the sample did not meet the full PASS condition
- **FAIL** — fewer than 70% of checks were accepted

All 10 saved golden-set requests use the `.txt` fixtures listed in
`backend/evaluation/expected_outputs.json`. Companion PDF and PNG files are
manual upload fixtures and are not guaranteed to contain byte-for-byte
identical wording or dates; they are not inputs to the saved golden-set run.

---

## Golden Set Design

The 10 samples were chosen to cover both domain diversity and edge cases:

| # | Sample | Domain | Primary Test |
|---|--------|--------|--------------|
| 01 | VitaPlus Insurance Reminder | Insurance | Multi-condition, payment, borderline urgency |
| 02 | Ausländerbehörde Musterstadt | Public office | Missing documents, residence risk |
| 03 | Technische Universität | University | Multiple deadlines, exmatriculation threat |
| 04 | Sparkasse Musterstadt | Bank | Amount disambiguation, two alternative actions |
| 05 | Finanzamt Musterstadt-Mitte | Public office | Einspruch ≠ payment suspension |
| 06 | Hausverwaltung Musterstadt | Service provider | Two independent actions and deadlines |
| 07 | Telekom Deutschland | Service provider | No required action — urgency must be Low |
| 08 | Jobcenter Musterstadt | Public office | 4-day deadline, benefit suspension threat |
| 09 | Inkasso Musterstadt | Debt collection | Payment with missing IBAN — confidence=medium |
| 10 | Amt für Bürgerangelegenheiten | Public office | Vague notice — no hallucination |

---

## Evaluation Criteria

### Urgency Rubric

Urgency is not determined by deadline proximity alone. It reflects:

```
Urgency = Required Action + Consequence Severity + Deadline Pressure
```

| Level | Criteria |
|-------|----------|
| High | Action required AND: serious consequence (legal action, benefit suspension, immigration risk, exmatriculation, account disruption) OR deadline within 7 days |
| Medium | Action required, deadline exists, but no serious immediate consequence |
| Low | Informational only, no required action, or only optional actions (e.g. Sonderkündigungsrecht) |

### Confidence Rules

Confidence is calculated by rule-based logic in `analysis_service.py`, not by the LLM:

| Level | Condition |
|-------|-----------|
| low | Text under 200 chars, or required_actions empty with urgency ≠ Low, or both sender and topic unknown |
| medium | Sender or topic unknown, payment letter without a recognizable IBAN or recipient, or non-Low urgency without a deadline |
| high | None of the above |

---

## Results

Because the system uses an LLM, individual runs may differ slightly. The table below shows one representative run, while overall stability is analyzed in the next section.

| Sample | Confidence | Urgency | Checks | Result |
|--------|-----------|---------|--------|--------|
| 01_insurance | high | Medium | 9/11 | PARTIAL |
| 02_immigration | high | High | 11/11 | PASS |
| 03_university | high | High | 11/11 | PARTIAL |
| 04_bank | medium | High | 11/11 | PASS |
| 05_finanzamt | high | High | 11/11 | PARTIAL |
| 06_housing | high | High | 11/11 | PARTIAL |
| 07_informational | high | Low | 9/9 | PASS |
| 08_high_urgency | high | High | 11/11 | PARTIAL |
| 09_incomplete_payment | medium | High | 10/10 | PASS |
| 10_vague_notice | high | Low | 9/9 | PASS |

**PASS: 5 / PARTIAL: 5 / FAIL: 0**

The stored result file reports 101 accepted checks out of 105 and no request
errors. It was generated on 2026-07-06. The deterministic exact-date grounding
guard was added later and is covered by unit and manual regression tests, but
the saved 10-letter result should be rerun if that guard must be included in a
new evaluation claim.

The more meaningful signal is not the PASS count but the complete absence of FAILs and the stability of results across repeated runs.

---

## Stability Analysis

### Summary

| Metric | Value |
|--------|-------|
| Repeated runs | 5 |
| Samples | 10 |
| Stable urgency | 8/10 |
| Stable confidence | 9/10 |
| Overall evaluation FAILs | 0 |

### Per-Sample Stability

We ran the full golden set 5 times to assess LLM output consistency:

| Sample | Urgency (5 runs) | Confidence (5 runs) | Stable? |
|--------|-----------------|---------------------|---------|
| 01_insurance | High High High Medium High | high high high high high | ⚠️ urgency |
| 02_immigration | High High High High High | high high high high high | ✅ |
| 03_university | High High High High High | high high high high high | ✅ |
| 04_bank | High — High High High | high — medium medium medium | ⚠️ timeout/confidence |
| 05_finanzamt | High High High High High | high high high high high | ✅ |
| 06_housing | High High High High High | high high high high high | ✅ |
| 07_informational | Low Low Low Low Low | high high high high high | ✅ |
| 08_high_urgency | High High High High High | high high high high high | ✅ |
| 09_incomplete_payment | High High High High High | medium medium medium medium medium | ✅ |
| 10_vague_notice | Low Low Low Low Low | high high high high high | ✅ |

### Borderline Case: 01_insurance

To investigate the urgency instability in `01_insurance`, we ran this sample 10 times in isolation:

- **High:** 8 runs
- **Medium:** 2 runs

The letter involves a 5 EUR reminder fee as the only stated consequence. The model correctly identifies this as borderline — some runs treat it as a serious consequence (High), others do not (Medium). We retained `High` as the expected label based on repeated empirical observations rather than manual preference: 80% of runs produced High, and the letter does require action with a financial consequence, even if minor. This sample was intentionally retained as an edge case because borderline decisions are expected in real-world administrative letters.

> "Across 10 repeated executions, the model classified the sample as High urgency in 8 runs and Medium in 2 runs, indicating a borderline judgment regarding whether a small reminder fee constitutes a serious consequence."

---

## Limitations

**LLM non-determinism:** Even with identical input, GPT-4o can return slightly different outputs across runs. This is inherent to language models and cannot be fully eliminated. Our stability analysis quantifies this effect rather than ignoring it.

**Keyword sensitivity:** Some PARTIAL results are due to keyword matching rather than extraction errors. For example, the model may write "appeal" instead of "Einspruch", or "withheld" instead of "suspended". We use fuzzy matching and synonym groups to reduce this, but some wording variation remains.

**Synthetic data:** All 10 evaluation samples are synthetically generated. Real German official letters may contain layouts, abbreviations, or phrasing that differs from our test set.

**Single-output-language evaluation:** All source samples are German and the
saved evaluation requests use the default English output. Manual regression
checks covered selected Persian and Chinese outputs, but multilingual quality
is not benchmarked systematically.

**Confidence rule proxy:** Confidence level is calculated by rule-based logic, not by measuring actual extraction quality. It is a proxy for reliability, not a direct measure.

---

## Discussion

The evaluation framework deliberately separates three types of failures:

1. **Reasoning failures** — wrong urgency or confidence level
2. **Extraction failures** — missing or incorrect field content
3. **Evaluation mismatches** — correct extraction but different wording

This distinction matters. A system that extracts the right facts but uses different wording is more useful than one that uses the right words but misses the key information. Our PARTIAL category captures this difference.

The zero FAIL count means no saved sample fell below the evaluation script's
70% acceptance threshold. It does not prove the absence of hallucinations or
establish real-world accuracy. The informational letter (07) and vague notice
(10) are useful positive signals because their stored runs kept urgency Low and
required actions empty.

### Conclusion

Within this synthetic 10-letter set, the results support the claim that the
assistant usually extracts the expected actionable fields and handles the two
no-action cases correctly. The evidence remains limited by synthetic data,
English-only scoring, keyword-based checks, and the small sample size. Future
evaluation should add human review, real anonymized letters with consent, and
systematic multilingual scoring.
---

## How to Reproduce

```bash
cd backend
source venv/bin/activate

# Single run
python3 evaluation/run_golden_set.py

# Stability analysis (5 runs)
python3 evaluation/run_stability_analysis.py
```

Results are saved to `evaluation/results/golden_set_results.json` and `evaluation/results/stability_analysis.json`.
