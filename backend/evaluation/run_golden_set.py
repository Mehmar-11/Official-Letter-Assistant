"""
Golden Set Evaluation Script
Letter Assistant — Backend Evaluation

Usage:
    python3 evaluation/run_golden_set.py

Requirements:
    - Backend running at http://localhost:8000
    - Sample letters in backend/sample_letters/
    - expected_outputs.json in backend/evaluation/

Output:
    - Terminal table with pass/fail per sample
    - evaluation/results/golden_set_results.json
"""

import json
import requests
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8000"
SCRIPT_DIR = Path(__file__).parent
BACKEND_DIR = SCRIPT_DIR.parent
EXPECTED_FILE = SCRIPT_DIR / "expected_outputs.json"
RESULTS_DIR = SCRIPT_DIR / "results"
RESULTS_FILE = RESULTS_DIR / "golden_set_results.json"

RESULTS_DIR.mkdir(exist_ok=True)

# Synonym groups for flexible keyword matching
SYNONYMS = {
    "cancel": ["cancel", "terminat", "kündigung", "kündig", "widerruf"],
    "suspend": ["suspend", "einst", "stopp", "ausset"],
    "iban": ["iban"],
    "recipient": ["recipient", "empfänger", "zahlungsempfänger"],
    "auftraggeber": ["auftraggeber", "creditor", "client", "origin"],
    "einspruch": ["einspruch", "objection", "appeal", "contest"],
    "payment": ["payment", "zahlung", "pay", "überweisu"],
    "exmatri": ["exmatri", "deregistr", "disenroll", "unenroll"],
    "interest": ["interest", "zinssatz", "zins", "14.75"],
}


def expand_keyword(keyword: str) -> list:
    kw = keyword.lower()
    for key, synonyms in SYNONYMS.items():
        if kw in synonyms or kw == key:
            return synonyms
    return [kw]


def keyword_found(keyword: str, text: str) -> bool:
    text_lower = text.lower()
    for variant in expand_keyword(keyword):
        if variant in text_lower:
            return True
    return False


def analyze_text(letter_text: str) -> dict:
    response = requests.post(
        f"{BASE_URL}/analyze-text",
        json={"letter_text": letter_text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def analyze_pdf(file_path: Path) -> dict:
    with open(file_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/analyze-pdf",
            files={"file": (file_path.name, f, "application/pdf")},
            timeout=60,
        )
    response.raise_for_status()
    return response.json()


def check_field(actual: dict, field: str, expected_value) -> tuple:
    if field.endswith("_empty"):
        real_field = field.replace("_empty", "")
        actual_value = actual.get(real_field, [])
        is_empty = not actual_value
        passed = is_empty == expected_value
        note = f"{real_field}: {'empty' if is_empty else 'not empty'} (expected {'empty' if expected_value else 'not empty'})"
        return passed, note
    else:
        actual_value = actual.get(field)
        passed = str(actual_value).lower() == str(expected_value).lower()
        note = f"{field}: '{actual_value}' (expected '{expected_value}')"
        return passed, note


def check_must_contain(actual: dict, must_contain: dict) -> list:
    checks = []
    for field, keywords in must_contain.items():
        field_value = actual.get(field, [])
        field_text = " ".join(field_value).lower() if isinstance(field_value, list) else str(field_value).lower()

        found_count = sum(1 for kw in keywords if keyword_found(kw, field_text))
        total = len(keywords)

        if found_count == total:
            result = "pass"
        elif found_count >= total * 0.5:
            result = "partial"
        else:
            result = "fail"

        checks.append({
            "field": f"must_contain in {field}",
            "passed": result in ("pass", "partial"),
            "partial": result == "partial",
            "note": f"{found_count}/{total} keywords found in {field}",
        })
    return checks


def check_must_not_contain(actual: dict, must_not_contain: dict) -> list:
    checks = []
    for field, keywords in must_not_contain.items():
        field_value = actual.get(field, [])
        field_text = " ".join(field_value).lower() if isinstance(field_value, list) else str(field_value).lower()

        hallucinated = [kw for kw in keywords if keyword_found(kw, field_text)]
        passed = len(hallucinated) == 0

        checks.append({
            "field": f"must_not_contain in {field}",
            "passed": passed,
            "partial": False,
            "note": "no hallucination detected" if passed else f"possible hallucination: {hallucinated}",
        })
    return checks


def compute_result(checks: list) -> str:
    total = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    partial = sum(1 for c in checks if c.get("partial", False))

    if passed == total and partial == 0:
        return "PASS"
    elif passed >= total * 0.7:
        return "PARTIAL"
    else:
        return "FAIL"


def evaluate_sample(sample: dict) -> dict:
    sample_id = sample["id"]
    file_path = BACKEND_DIR / sample["file"]
    input_type = sample["input_type"]
    expected = sample["expected"]
    must_contain = sample.get("must_contain", {})
    must_not_contain = sample.get("must_not_contain", {})

    print(f"  {sample_id:<35}", end=" ", flush=True)

    try:
        if input_type == "pdf":
            actual = analyze_pdf(file_path)
        else:
            letter_text = file_path.read_text(encoding="utf-8")
            actual = analyze_text(letter_text)

        if not actual.get("is_valid_letter", False):
            print("SKIP")
            return {
                "id": sample_id,
                "description": sample["description"],
                "result": "SKIP",
                "reason": actual.get("message", "Rejected by input verification"),
                "checks": [],
            }

        checks = []
        for field, expected_value in expected.items():
            passed, note = check_field(actual, field, expected_value)
            checks.append({"field": field, "passed": passed, "partial": False, "note": note})

        checks += check_must_contain(actual, must_contain)
        checks += check_must_not_contain(actual, must_not_contain)

        passed_count = sum(1 for c in checks if c["passed"])
        total_count = len(checks)
        result = compute_result(checks)
        partial_count = sum(1 for c in checks if c.get("partial", False))
        failed_count = total_count - passed_count

        print(
            f"{actual.get('confidence_level', '—'):<10} "
            f"{actual.get('urgency_level', '—'):<10} "
            f"{passed_count}/{total_count} "
            f"({partial_count} partial, {failed_count} failed)   "
            f"{result}"
            )

        return {
            "id": sample_id,
            "description": sample["description"],
            "result": result,
            "passed": passed_count,
            "total": total_count,
            "checks": checks,
            "actual_confidence": actual.get("confidence_level"),
            "actual_confidence_reason": actual.get("confidence_reason", ""),
            "actual_urgency": actual.get("urgency_level"),
            "actual_sender_type": actual.get("sender_type"),
            "actual_letter_topic": actual.get("letter_topic", ""),
            "actual_tldr": actual.get("tldr", "")[:150],
            "partial_matches": partial_count,
            "failed_checks": failed_count,
        }

    except Exception as e:
        print(f"ERROR: {e}")
        return {
            "id": sample_id,
            "description": sample["description"],
            "result": "ERROR",
            "error": str(e),
            "checks": [],
        }


def print_summary(results: list):
    print("\n" + "=" * 95)
    print(f"  {'Sample':<33} {'Confidence':<10} {'Urgency':<10} {'Checks':<18} Result")
    print("  " + "-" * 85)
    for r in results:
        if r["result"] in ("ERROR", "SKIP"):
            print(f"  {r['id']:<33} {'—':<10} {'—':<10} {'—':<10} {r['result']}")
            continue
        print(
            f"  {r['id']:<33}"
            f"{r.get('actual_confidence', '—'):<10}"
            f"{r.get('actual_urgency', '—'):<10}"
            f"{r['passed']}/{r['total']} "
            f"({r.get('partial_matches', 0)} partial, "
            f"{r.get('failed_checks', 0)} failed)   "
            f"{r['result']}"
        )

    print("=" * 95)
    total = len(results)
    passed = sum(1 for r in results if r["result"] == "PASS")
    partial = sum(1 for r in results if r["result"] == "PARTIAL")
    failed = sum(1 for r in results if r["result"] == "FAIL")
    errors = sum(1 for r in results if r["result"] in ("ERROR", "SKIP"))
    print(f"\n  Total: {total}  |  PASS: {passed}  |  PARTIAL: {partial}  |  FAIL: {failed}  |  ERROR/SKIP: {errors}\n")


def main():
    print("\nLetter Assistant — Golden Set Evaluation")
    print(f"Backend:   {BASE_URL}")
    print(f"Time:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    with open(EXPECTED_FILE, encoding="utf-8") as f:
        data = json.load(f)

    samples = data["samples"]
    print(f"Running {len(samples)} samples...\n")
    print(f"  {'Sample':<35} {'Confidence':<10} {'Urgency':<10} {'Checks':<10} Result")
    print("  " + "-" * 85)

    results = [evaluate_sample(s) for s in samples]
    print_summary(results)

    output = {
        "timestamp": datetime.now().isoformat(),
        "backend_url": BASE_URL,
        "total_samples": len(results),
        "passed": sum(1 for r in results if r["result"] == "PASS"),
        "partial": sum(1 for r in results if r["result"] == "PARTIAL"),
        "failed": sum(1 for r in results if r["result"] == "FAIL"),
        "errors": sum(1 for r in results if r["result"] in ("ERROR", "SKIP")),
        "results": results,
    }

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"  Results saved → {RESULTS_FILE}\n")


if __name__ == "__main__":
    main()
