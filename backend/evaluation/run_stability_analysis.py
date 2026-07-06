"""
Stability Analysis — runs golden set N times and reports
urgency/confidence consistency per sample.
"""
import json
import subprocess
import sys
from pathlib import Path
from collections import defaultdict

RUNS = 5
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

def run_once(run_id):
    print(f"\n=== Run {run_id} ===", flush=True)
    subprocess.run(
        [sys.executable, str(Path(__file__).parent / "run_golden_set.py")],
        cwd=Path(__file__).parent.parent,
        check=True,
    )
    return json.loads((RESULTS_DIR / "golden_set_results.json").read_text())

def main():
    urgency_map    = defaultdict(list)
    confidence_map = defaultdict(list)
    result_map     = defaultdict(list)

    for i in range(1, RUNS + 1):
        data = run_once(i)
        for r in data["results"]:
            sid = r["id"]
            urgency_map[sid].append(r.get("actual_urgency", "—"))
            confidence_map[sid].append(r.get("actual_confidence", "—"))
            result_map[sid].append(r["result"])

    print("\n\n" + "=" * 100)
    print(f"{'Sample':<30} {'Urgency (5 runs)':<35} {'Confidence (5 runs)':<35} {'Stable?'}")
    print("-" * 100)

    stability = {}
    for sid in urgency_map:
        u_vals = urgency_map[sid]
        c_vals = confidence_map[sid]
        u_stable = len(set(u_vals)) == 1
        c_stable = len(set(c_vals)) == 1
        stable = "✅" if u_stable and c_stable else ("⚠️ urgency" if not u_stable else "⚠️ confidence")
        stability[sid] = {"urgency": u_vals, "confidence": c_vals, "stable": stable}
        print(f"{sid:<30} {' '.join(u_vals):<35} {' '.join(c_vals):<35} {stable}")

    print("=" * 100)

    # Save
    out = RESULTS_DIR / "stability_analysis.json"
    out.write_text(json.dumps(stability, ensure_ascii=False, indent=2))
    print(f"\nSaved → {out}")

if __name__ == "__main__":
    main()
