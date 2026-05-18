#!/usr/bin/env python3
"""
Bulk Internet Agreement Scraper Agent

Searches for competitor bulk internet/telecommunications service agreements,
downloads PDFs, verifies they are genuine bulk agreements, and summarizes key terms.

Usage:
    python main.py                          # uses PROVIDERS list from config.py
    python main.py "Comcast" "AT&T"        # override with specific providers
"""

import argparse
import json
import logging
import os
import sys
import time
from tqdm import tqdm

from config import PROVIDERS, OUTPUT_DIR, REPORT_FILE
from searcher import search_provider
from url_filter import filter_results
from pdf_handler import process_url
from analyzer import analyze

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("output/scraper.log"),
    ],
)
logger = logging.getLogger(__name__)


def run(providers: list[str]) -> list[dict]:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_results = []

    for provider in providers:
        logger.info(f"=== Processing provider: {provider} ===")

        # Step 1: Search
        raw_results = search_provider(provider)

        # Step 2: Filter by URL keywords
        filtered = filter_results(raw_results)

        if not filtered:
            logger.info(f"No relevant URLs found for {provider}")
            continue

        # Step 3: Download + verify content keywords
        logger.info(f"Processing {len(filtered)} candidate URLs for {provider}...")
        processed = []
        for result in tqdm(filtered, desc=f"{provider} — fetching"):
            processed.append(process_url(result))
            time.sleep(0.5)  # polite delay

        downloaded = [r for r in processed if r.get("status") == "downloaded"]
        logger.info(f"{provider}: {len(downloaded)}/{len(filtered)} URLs passed content verification")

        # Step 4: Analyze with Claude
        analyzed = []
        for result in tqdm(downloaded, desc=f"{provider} — analyzing"):
            analyzed.append(analyze(result))

        # Only keep confirmed bulk agreements
        confirmed = [
            r for r in analyzed
            if r.get("analysis", {}).get("is_bulk_agreement") is True
        ]
        logger.info(f"{provider}: {len(confirmed)} confirmed bulk agreements")
        all_results.extend(confirmed)

        # Also keep high-confidence non-confirmed for review
        uncertain = [
            r for r in analyzed
            if r.get("analysis", {}).get("is_bulk_agreement") is not True
            and r.get("analysis", {}).get("confidence") == "high"
        ]
        if uncertain:
            logger.info(f"{provider}: {len(uncertain)} high-confidence non-matches (skipped)")

    return all_results


def save_report(results: list[dict]) -> None:
    # Strip full_text from report (it's large and already saved in PDF)
    report = []
    for r in results:
        entry = {k: v for k, v in r.items() if k not in ("full_text", "pdf_bytes")}
        report.append(entry)

    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)
    logger.info(f"Report saved to {REPORT_FILE}")

    # Print a human-readable summary
    print("\n" + "=" * 60)
    print(f"RESULTS: {len(report)} confirmed bulk agreements found")
    print("=" * 60)
    for r in report:
        a = r.get("analysis", {})
        kt = a.get("key_takeaways", {})
        print(f"\nProvider : {a.get('provider', r.get('provider'))}")
        print(f"Property : {a.get('property', 'unknown')}")
        print(f"URL      : {r['url']}")
        print(f"Saved to : {r.get('local_path', 'N/A')}")
        print(f"Confidence: {a.get('confidence')}")
        print(f"Term     : {kt.get('term_length', 'unknown')}")
        print(f"Pricing  : {kt.get('pricing', 'unknown')}")
        print(f"Exclusivity: {kt.get('exclusivity', 'unknown')}")
        print(f"Services : {', '.join(kt.get('services_covered', []))}")
        if kt.get("notable_clauses"):
            print(f"Notable  : {'; '.join(kt['notable_clauses'])}")
        print("-" * 40)


def main():
    parser = argparse.ArgumentParser(description="Bulk Internet Agreement Scraper")
    parser.add_argument(
        "providers",
        nargs="*",
        help="Provider names to search (defaults to config.py PROVIDERS list)",
    )
    args = parser.parse_args()

    providers = args.providers if args.providers else PROVIDERS
    logger.info(f"Starting scraper for {len(providers)} providers: {providers}")

    results = run(providers)
    save_report(results)


if __name__ == "__main__":
    main()
