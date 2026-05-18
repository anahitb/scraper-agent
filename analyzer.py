import logging
import anthropic

logger = logging.getLogger(__name__)

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are an expert analyst specializing in bulk internet and telecommunications service agreements between internet service providers (ISPs) and property owners/managers (MDU — multi-dwelling units, apartment complexes, HOAs, commercial buildings, etc.).

Your job is to:
1. Confirm whether a document is a genuine bulk internet/telecommunications service agreement.
2. Extract and summarize key business terms.

A genuine bulk internet agreement will typically:
- Name an ISP and a property owner/manager as parties
- Cover multiple units or a whole property under one deal
- Include pricing, term length, and service details
- May include exclusivity or revenue share clauses
"""

EXTRACTION_PROMPT = """Below is extracted text from a document. Analyze it and respond in the following JSON format:

{{
  "is_bulk_agreement": true or false,
  "confidence": "high" | "medium" | "low",
  "reason": "one sentence explaining your determination",
  "provider": "name of ISP if identified",
  "property": "name of property or property owner if identified",
  "key_takeaways": {{
    "term_length": "e.g. 5 years, or null",
    "pricing": "summary of pricing structure, or null",
    "exclusivity": "yes / no / partial / unknown",
    "services_covered": ["internet", "cable", "phone", ...],
    "monthly_fee_per_unit": "e.g. $15/unit/month or null",
    "total_units": "number or null",
    "notable_clauses": ["list of any notable clauses like revenue share, early termination, auto-renewal"]
  }}
}}

Document text (first {char_count} characters):
---
{text}
---"""


def analyze(result: dict) -> dict:
    """Run Claude analysis on a successfully downloaded PDF."""
    text = result.get("full_text", "")
    if not text:
        result["analysis"] = {"error": "no text to analyze"}
        return result

    # Trim to stay within token limits (~8k chars ≈ ~2k tokens, safe margin)
    text_sample = text[:8000]

    prompt = EXTRACTION_PROMPT.format(text=text_sample, char_count=len(text_sample))

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()

        # Parse JSON from response
        import json
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            analysis = json.loads(raw[start:end])
        else:
            analysis = {"raw_response": raw}

        result["analysis"] = analysis
        logger.info(
            f"Analysis complete for {result['url']}: "
            f"is_bulk={analysis.get('is_bulk_agreement')}, "
            f"confidence={analysis.get('confidence')}"
        )
    except Exception as e:
        logger.error(f"Analysis failed for {result['url']}: {e}")
        result["analysis"] = {"error": str(e)}

    return result
