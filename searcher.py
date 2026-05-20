import os
import time
import logging
import requests
from config import SEARCH_QUERY_TEMPLATES, MAX_RESULTS_PER_QUERY

logger = logging.getLogger(__name__)

# SEARCH_BACKEND options:
#   "brave"  — Brave Search API (recommended): set BRAVE_API_KEY env var
#   "google" — Google Custom Search API: set GOOGLE_API_KEY + GOOGLE_CSE_ID env vars
#   "ddgs"   — DuckDuckGo (free, no key needed, but weaker results)
SEARCH_BACKEND = os.getenv("SEARCH_BACKEND", "ddgs")


def _search_brave(query: str, max_results: int) -> list[dict]:
    api_key = os.environ["BRAVE_API_KEY"]
    results = []
    offset = 0
    while len(results) < max_results:
        count = min(20, max_results - len(results))
        resp = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": api_key,
            },
            params={"q": query, "count": count, "offset": offset},
            timeout=10,
        )
        resp.raise_for_status()
        items = resp.json().get("web", {}).get("results", [])
        if not items:
            break
        for item in items:
            results.append({
                "url": item.get("url", ""),
                "title": item.get("title", ""),
                "snippet": item.get("description", ""),
            })
        offset += len(items)
    return results[:max_results]


def _search_ddgs(query: str, max_results: int) -> list[dict]:
    from ddgs import DDGS
    with DDGS() as ddgs:
        hits = list(ddgs.text(query, max_results=max_results))
    return [
        {
            "url": h.get("href") or h.get("url", ""),
            "title": h.get("title", ""),
            "snippet": h.get("body", ""),
        }
        for h in hits
        if h.get("href") or h.get("url")
    ]


def _search_google(query: str, max_results: int) -> list[dict]:
    api_key = os.environ["GOOGLE_API_KEY"]
    cse_id = os.environ["GOOGLE_CSE_ID"]
    results = []
    start = 1
    while len(results) < max_results:
        resp = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={"key": api_key, "cx": cse_id, "q": query, "start": start, "num": min(10, max_results)},
            timeout=10,
        )
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if not items:
            break
        for item in items:
            results.append({
                "url": item.get("link", ""),
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
            })
        start += len(items)
    return results[:max_results]


def _run_query(query: str) -> list[dict]:
    if SEARCH_BACKEND == "brave":
        return _search_brave(query, MAX_RESULTS_PER_QUERY)
    if SEARCH_BACKEND == "google":
        return _search_google(query, MAX_RESULTS_PER_QUERY)
    return _search_ddgs(query, MAX_RESULTS_PER_QUERY)


def search_provider(provider: str) -> list[dict]:
    """Search for bulk agreement URLs for a given provider."""
    seen_urls = set()
    results = []

    for template in SEARCH_QUERY_TEMPLATES:
        query = template.format(provider=provider)
        logger.info(f"Searching ({SEARCH_BACKEND}): {query}")
        try:
            hits = _run_query(query)
            for hit in hits:
                url = hit["url"]
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    results.append({
                        "provider": provider,
                        "query": query,
                        "url": url,
                        "title": hit["title"],
                        "snippet": hit["snippet"],
                    })
            time.sleep(1)
        except Exception as e:
            logger.warning(f"Search failed for query '{query}': {e}")
            time.sleep(3)

    logger.info(f"Found {len(results)} unique URLs for {provider}")
    return results
