#!/usr/bin/env python3
"""
Test the PDF download + analysis pipeline with known URLs.

Use this to validate the agent works before running the full search loop.

Usage:
    python test_pipeline.py <url1> [url2 ...]
    python test_pipeline.py  # uses built-in test URLs

Requires: ANTHROPIC_API_KEY env var
"""

import sys
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TEST_URLS = [
    # Add known bulk agreement PDF URLs here to test the pipeline
    # e.g. "https://example.com/bulk-internet-agreement.pdf",
]

os.makedirs("output", exist_ok=True)

from pdf_handler import process_url
from analyzer import analyze


def test(urls: list[str], provider: str = "Test Provider") -> None:
    for url in urls:
        print(f"\n{'='*60}")
        print(f"Testing: {url}")
        result = {"url": url, "provider": provider}

        result = process_url(result)
        print(f"Status: {result['status']}")

        if result["status"] == "downloaded":
            print(f"Keyword score: {result.get('content_keyword_score')}")
            print(f"Matched keywords: {result.get('matched_keywords')}")
            result = analyze(result)
            a = result.get("analysis", {})
            print(f"\nAnalysis:")
            print(json.dumps(a, indent=2))
        else:
            print(f"Skipped analysis (status={result['status']})")


if __name__ == "__main__":
    urls = sys.argv[1:] if len(sys.argv) > 1 else TEST_URLS
    if not urls:
        print("No URLs provided. Edit TEST_URLS in this file or pass URLs as arguments.")
        print("Example: python test_pipeline.py https://example.com/bulk-agreement.pdf")
        sys.exit(0)
    test(urls)
