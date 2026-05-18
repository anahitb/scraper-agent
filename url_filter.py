import logging
from urllib.parse import urlparse
from config import URL_KEYWORDS

logger = logging.getLogger(__name__)


def score_url(url: str, provider: str) -> int:
    """
    Score a URL based on how many bulk-agreement keywords it contains.
    Higher score = more likely to be a relevant agreement document.
    """
    url_lower = url.lower()
    provider_lower = provider.lower().replace(" ", "")
    score = 0

    for kw in URL_KEYWORDS:
        if kw in url_lower:
            score += 1

    # Bonus: provider name appears in URL
    if provider_lower in url_lower.replace("-", "").replace("_", ""):
        score += 1

    # Bonus: URL ends in .pdf
    parsed = urlparse(url)
    if parsed.path.lower().endswith(".pdf"):
        score += 2

    return score


def is_url_relevant(url: str, provider: str, min_score: int = 1) -> bool:
    """Return True if the URL is likely a bulk agreement document."""
    score = score_url(url, provider)
    relevant = score >= min_score
    if relevant:
        logger.debug(f"URL accepted (score={score}): {url}")
    else:
        logger.debug(f"URL rejected (score={score}): {url}")
    return relevant


def filter_results(results: list[dict]) -> list[dict]:
    """Filter a list of search results to those with relevant URLs."""
    filtered = [
        r for r in results
        if is_url_relevant(r["url"], r["provider"])
    ]
    logger.info(f"URL filter: {len(filtered)}/{len(results)} results passed")
    return filtered
