import logging
from urllib.parse import urlparse
from config import URL_KEYWORDS

logger = logging.getLogger(__name__)

# Domains that never host actual agreements — provider marketing sites, social media, etc.
BLOCKED_DOMAINS = [
    "reddit.com", "youtube.com", "twitter.com", "x.com", "linkedin.com",
    "facebook.com", "instagram.com", "wikipedia.org", "yelp.com",
    # Provider-owned domains (agreements are on third-party HOA/condo sites)
    "spectrum.com", "comcast.com", "xfinity.com", "att.com",
    "bluestreamfiber.com", "bluestream.com", "frontier.com",
    "mediacom.com", "astound.com", "gigafy.com", "gigapointe.com",
    "gigstreem.com", "grucom.com", "ibconnect.com", "juvilex.com",
    "newarkfiber.com", "restech.com", "uprisefiber.com", "zentro.com",
]

# URL path terms that indicate marketing/noise content rather than agreements
BLOCKED_URL_TERMS = [
    "faq", "flyer", "brochure", "marketing", "press-release", "pressrelease",
    "press_release", "announcement", "announce", "news", "blog", "article",
    "forum", "thread", "comment", "review", "complaint", "tweet", "post",
    "signup", "sign-up", "pricing", "promo", "promotion", "offer",
    "terms-of-service", "terms_of_service", "privacy-policy", "privacy_policy",
    "contractbuyout", "business-services-agreement",
]


def is_blocked(url: str, provider: str) -> bool:
    """Return True if the URL should be skipped entirely."""
    parsed = urlparse(url)
    domain = parsed.netloc.lower().replace("www.", "")
    path_lower = parsed.path.lower()

    # Block known bad domains
    if any(blocked in domain for blocked in BLOCKED_DOMAINS):
        return True

    # Block provider's own domain dynamically
    provider_domain = provider.lower().split("(")[0].strip().replace(" ", "")
    if provider_domain in domain.replace("-", "").replace(".", ""):
        return True

    # Block marketing/noise URL paths
    if any(term in path_lower for term in BLOCKED_URL_TERMS):
        return True

    return False


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
    if is_blocked(url, provider):
        logger.debug(f"URL blocked: {url}")
        return False
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
