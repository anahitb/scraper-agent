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
import csv
import logging
import os
import sys
import time
from tqdm import tqdm

from config import PROVIDERS, OUTPUT_DIR
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

CSV_FILE = "output/bulk_agreements.csv"

CSV_COLUMNS = [
    ("Provider",                lambda a, kt, r: a.get("provider") or r.get("provider")),
    ("Property Name",           lambda a, kt, r: a.get("property_name")),
    ("Address",                 lambda a, kt, r: a.get("property_address")),
    ("Units",                   lambda a, kt, r: kt.get("number_of_units")),
    ("Contract Effective Date", lambda a, kt, r: kt.get("contract_effective_date")),
    ("Term Length",             lambda a, kt, r: kt.get("service_commitment_period")),
    ("Services",                lambda a, kt, r: ", ".join(kt.get("services_covered") or [])),
    ("Bulk Rate",               lambda a, kt, r: kt.get("monthly_fee_per_unit")),
    ("Source URL",              lambda a, kt, r: r.get("url")),
    ("Door Fee",                lambda a, kt, r: kt.get("door_fee_per_unit")),
]


def write_csv_row(result: dict) -> None:
    """Append a single confirmed result to the CSV immediately."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([col for col, _ in CSV_COLUMNS])
        a = result.get("analysis", {})
        kt = a.get("key_takeaways", {})
        writer.writerow([extractor(a, kt, result) for _, extractor in CSV_COLUMNS])


def run(providers: list[str]) -> list[dict]:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_results = []

    # Write CSV header upfront so file exists even if no agreements found
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([col for col, _ in CSV_COLUMNS])

    for provider in providers:
        logger.info(f"=== Processing provider: {provider} ===")

        raw_results = search_provider(provider)
        filtered = filter_results(raw_results)

        if not filtered:
            logger.info(f"No relevant URLs found for {provider}")
            continue

        logger.info(f"Processing {len(filtered)} candidate URLs for {provider}...")
        processed = []
        for result in tqdm(filtered, desc=f"{provider} — fetching"):
            processed.append(process_url(result))
            time.sleep(0.5)

        downloaded = [r for r in processed if r.get("status") == "downloaded"]
        logger.info(f"{provider}: {len(downloaded)}/{len(filtered)} URLs passed content verification")

        analyzed = []
        for result in tqdm(downloaded, desc=f"{provider} — analyzing"):
            analyzed.append(analyze(result))

        confirmed = [
            r for r in analyzed
            if r.get("analysis", {}).get("is_bulk_agreement") is True
        ]
        logger.info(f"{provider}: {len(confirmed)} confirmed bulk agreements")

        # Write each confirmed agreement to CSV immediately
        for r in confirmed:
            entry = {k: v for k, v in r.items() if k not in ("full_text", "pdf_bytes")}
            write_csv_row(entry)

        all_results.extend(confirmed)
        logger.info(f"CSV updated after {provider} — {len(all_results)} total so far")

    return all_results


def save_report(results: list[dict]) -> None:
    print("\n" + "=" * 60)
    print(f"RESULTS: {len(results)} confirmed bulk agreements found")
    print(f"CSV:     {CSV_FILE}")
    print("=" * 60)
    for r in results:
        a = r.get("analysis", {})
        kt = a.get("key_takeaways", {})
        print(f"\nProvider     : {a.get('provider', r.get('provider'))}")
        print(f"Property     : {a.get('property_name', 'unknown')}")
        print(f"Address      : {a.get('property_address', 'unknown')}")
        print(f"Units        : {kt.get('number_of_units', 'unknown')}")
        print(f"Effective    : {kt.get('contract_effective_date', 'unknown')}")
        print(f"Term         : {kt.get('service_commitment_period', 'unknown')}")
        print(f"Services     : {', '.join(kt.get('services_covered') or [])}")
        print(f"Bulk Rate    : {kt.get('monthly_fee_per_unit', 'unknown')}")
        print(f"URL          : {r['url']}")
        print(f"Door Fee     : {kt.get('door_fee_per_unit', 'unknown')}")
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
