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


def save_csv(results: list[dict]) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([col for col, _ in CSV_COLUMNS])
        for r in results:
            a = r.get("analysis", {})
            kt = a.get("key_takeaways", {})
            writer.writerow([extractor(a, kt, r) for _, extractor in CSV_COLUMNS])
    logger.info(f"CSV saved to {CSV_FILE}")


def run(providers: list[str]) -> list[dict]:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_results = []

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
        all_results.extend(confirmed)

    return all_results


def save_report(results: list[dict]) -> None:
    report = [{k: v for k, v in r.items() if k not in ("full_text", "pdf_bytes")} for r in results]

    save_csv(report)

    print("\n" + "=" * 60)
    print(f"RESULTS: {len(report)} confirmed bulk agreements found")
    print(f"CSV:     {CSV_FILE}")
    print("=" * 60)
    for r in report:
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
