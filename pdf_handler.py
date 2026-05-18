import io
import os
import re
import logging
import requests
import pdfplumber
from config import PDF_DOWNLOAD_TIMEOUT, MAX_PDF_PAGES_TO_SCAN, CONTENT_KEYWORDS, MIN_CONTENT_KEYWORD_MATCHES, OUTPUT_DIR

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def _safe_filename(url: str, provider: str) -> str:
    name = re.sub(r"[^\w\-]", "_", url.split("/")[-1] or "doc")
    if not name.endswith(".pdf"):
        name += ".pdf"
    provider_slug = re.sub(r"\W+", "_", provider)
    return f"{provider_slug}_{name}"[:200]


def fetch_bytes(url: str) -> bytes | None:
    """Download raw bytes from a URL. Returns None on failure."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=PDF_DOWNLOAD_TIMEOUT, stream=True)
        resp.raise_for_status()
        content_type = resp.headers.get("Content-Type", "")
        # Accept PDF content type or unknown (sometimes servers return wrong type)
        if "pdf" not in content_type and "octet-stream" not in content_type and "application" not in content_type:
            # Try anyway if URL ends in .pdf
            if not url.lower().endswith(".pdf"):
                logger.debug(f"Skipping non-PDF content-type '{content_type}' for {url}")
                return None
        return resp.content
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None


def extract_text(pdf_bytes: bytes) -> str:
    """Extract text from first N pages of a PDF."""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            pages = pdf.pages[:MAX_PDF_PAGES_TO_SCAN]
            return "\n".join(p.extract_text() or "" for p in pages)
    except Exception as e:
        logger.warning(f"PDF text extraction failed: {e}")
        return ""


def content_keyword_score(text: str) -> tuple[int, list[str]]:
    """Count how many content keywords appear in the text."""
    text_lower = text.lower()
    matched = [kw for kw in CONTENT_KEYWORDS if kw in text_lower]
    return len(matched), matched


def save_pdf(pdf_bytes: bytes, provider: str, url: str) -> str:
    """Save PDF bytes to the output directory and return the local path."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = _safe_filename(url, provider)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "wb") as f:
        f.write(pdf_bytes)
    logger.info(f"Saved PDF: {path}")
    return path


def process_url(result: dict) -> dict:
    """
    Download the URL, extract text, verify keyword match, save if valid.
    Returns enriched result dict.
    """
    url = result["url"]
    provider = result["provider"]
    result = dict(result)  # copy

    pdf_bytes = fetch_bytes(url)
    if not pdf_bytes:
        result["status"] = "fetch_failed"
        return result

    text = extract_text(pdf_bytes)
    if not text.strip():
        result["status"] = "no_text_extracted"
        result["pdf_bytes"] = pdf_bytes  # might still be useful
        return result

    score, matched_kws = content_keyword_score(text)
    result["content_keyword_score"] = score
    result["matched_keywords"] = matched_kws
    result["extracted_text_preview"] = text[:500]

    if score < MIN_CONTENT_KEYWORD_MATCHES:
        result["status"] = "content_mismatch"
        logger.info(f"Content mismatch (score={score}): {url}")
        return result

    local_path = save_pdf(pdf_bytes, provider, url)
    result["status"] = "downloaded"
    result["local_path"] = local_path
    result["full_text"] = text
    return result
