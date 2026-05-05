"""
run_evals.py — Automated eval runner for Deal Intelligence Agent.

Loops through 20 companies, generates a battlecard for each,
saves the output as a markdown file in eval-results/, and prints
a summary with latency. Every run is automatically logged to LangSmith.

Run from the project root:
    python run_evals.py

Results saved to:
    eval-results/<company-name>.md
"""

import sys
import os
import time
from pathlib import Path

# Add src/ to the path so we can import agent.py, models.py, tools.py
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from agent import generate_battlecard

# --- Company Test List ---
# Mix of large, mid-size, small, and edge case companies.
# Edit this list to swap in your own choices.
COMPANIES = [
    # Rerun v1.2 — 2 remaining cards below 2.0 from Eval Run 2
    "Loom",
    "Workday",
]

# --- Output Folder ---
OUTPUT_DIR = Path(__file__).parent / "eval-results"
OUTPUT_DIR.mkdir(exist_ok=True)


def run_evals():
    """Loop through all companies, generate battlecards, save to files."""

    print(f"\n Starting eval run — {len(COMPANIES)} companies")
    print(f" Results will be saved to: eval-results/")
    print(f" Every run is logged to LangSmith automatically\n")
    print("-" * 50)

    results_summary = []

    for i, company in enumerate(COMPANIES, start=1):
        print(f"\n[{i}/{len(COMPANIES)}] Generating battlecard for: {company}")

        start_time = time.time()

        try:
            battlecard = generate_battlecard(company)
            latency = round(time.time() - start_time, 1)

            # Save battlecard as markdown file
            filename = company.lower().replace(" ", "-").replace(".", "") + ".md"
            output_path = OUTPUT_DIR / filename

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"# Battlecard: {company}\n")
                f.write(f"**Latency:** {latency} seconds\n\n")
                f.write("---\n\n")
                f.write(battlecard.to_markdown())

            print(f" Done in {latency}s — saved to eval-results/{filename}")
            results_summary.append({"company": company, "status": "success", "latency": latency})

        except Exception as e:
            latency = round(time.time() - start_time, 1)
            print(f" Failed after {latency}s — {str(e)}")
            results_summary.append({"company": company, "status": "failed", "latency": latency, "error": str(e)})

        # Wait between companies to avoid DuckDuckGo rate limiting.
        # Skip the wait after the last company.
        if i < len(COMPANIES):
            print(f" Waiting 10 seconds before next company...")
            time.sleep(10)

    # --- Print Final Summary ---
    print("\n" + "=" * 50)
    print(" EVAL RUN COMPLETE")
    print("=" * 50)

    successful = [r for r in results_summary if r["status"] == "success"]
    failed = [r for r in results_summary if r["status"] == "failed"]

    print(f"\n Successful: {len(successful)}/{len(COMPANIES)}")
    print(f" Failed:     {len(failed)}/{len(COMPANIES)}")

    if successful:
        avg_latency = round(sum(r["latency"] for r in successful) / len(successful), 1)
        max_latency = max(r["latency"] for r in successful)
        min_latency = min(r["latency"] for r in successful)
        print(f"\n Latency:")
        print(f"   Average: {avg_latency}s")
        print(f"   Fastest: {min_latency}s")
        print(f"   Slowest: {max_latency}s")

    if failed:
        print(f"\n Failed companies:")
        for r in failed:
            print(f"   - {r['company']}: {r.get('error', 'unknown error')}")

    print(f"\n Open eval-results/ to review each battlecard")
    print(f" Open LangSmith to see full traces for every run\n")


if __name__ == "__main__":
    run_evals()