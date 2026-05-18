import os
import json
import logging

logger = logging.getLogger(__name__)

# Set LLM_BACKEND=anthropic to use Claude (paid).
# Default is groq (free — sign up at console.groq.com, no credit card needed).
LLM_BACKEND = os.getenv("LLM_BACKEND", "groq")

SYSTEM_PROMPT = """You are an expert analyst specializing in bulk internet and telecommunications service agreements between internet service providers (ISPs) and property owners/managers (MDU — multi-dwelling units, apartment complexes, HOAs, condo associations, commercial buildings, etc.).

Your job is to:
1. Confirm whether a document is a genuine bulk internet/telecommunications service agreement.
2. Extract and summarize all key business terms.

A genuine bulk agreement will have ALL of the following characteristics:
- An ISP (e.g. Spectrum, Xfinity/Comcast, WOW!, Frontier, AT&T, Cox, Fibernow, CenturyLink, etc.) listed as Operator or Company
- A property entity (HOA, Homeowners Association, Condo Association, Apartment complex, property manager) listed as Owner or Customer
- A specific number of units covered under the deal
- A per-unit monthly Bulk Service Fee
- A Service Commitment Period or term length (typically 5-10 years)
- Bulk services covering internet and/or cable TV provided as an amenity

Common document titles you will see:
- "Communications Network and Service Agreement (Bulk)"
- "Bulk Cable Television Services Agreement"
- "Xfinity Communities Service Agreement"
- "[Provider] Bulk Service Agreement"

Key clauses to look for: Door Fee (one-time payment), marketing exclusivity, auto-renewal terms, termination payment, Advanced Community WiFi, capital investment by operator.
"""

EXTRACTION_PROMPT = """Below is extracted text from a document. Analyze it and respond ONLY with valid JSON in the exact format below - no explanation, no markdown, just the JSON object.

{{
  "is_bulk_agreement": true or false,
  "confidence": "high" | "medium" | "low",
  "reason": "one sentence explaining your determination",
  "provider": "ISP name (e.g. Spectrum, Xfinity, WOW!, etc.) or null",
  "property_name": "property or HOA name or null",
  "property_address": "address if found or null",
  "key_takeaways": {{
    "number_of_units": "integer or null",
    "service_commitment_period": "e.g. 60 months / 5 years or null",
    "auto_renewal": "yes with term / no / unknown",
    "monthly_fee_per_unit": "e.g. $55.00/unit or null",
    "total_monthly_billing": "e.g. $38,225/month or null",
    "door_fee_per_unit": "one-time fee e.g. $200/unit or null",
    "internet_speed": "e.g. 500 Mbps x 20 Mbps or null",
    "services_covered": ["internet", "cable tv", "phone", "wifi"],
    "marketing_exclusivity": "exclusive / non-exclusive / partial / unknown",
    "capital_investment_by_operator": "dollar amount or null",
    "annual_rate_increase_cap": "e.g. 4% per year or null",
    "notable_clauses": ["list notable items: termination payment formula, revenue share, fiber rebuild, door fee addendum, etc."]
  }}
}}

Document text (first {char_count} characters):
---
{text}
---"""


def _call_groq(prompt: str) -> str:
    from groq import Groq
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1024,
        temperature=0,
    )
    return response.choices[0].message.content.strip()


def _call_anthropic(prompt: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def _parse_json(raw: str) -> dict:
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start != -1 and end > start:
        return json.loads(raw[start:end])
    return {"raw_response": raw}


def analyze(result: dict) -> dict:
    """Run LLM analysis on a successfully downloaded PDF."""
    text = result.get("full_text", "")
    if not text:
        result["analysis"] = {"error": "no text to analyze"}
        return result

    text_sample = text[:8000]
    prompt = EXTRACTION_PROMPT.format(text=text_sample, char_count=len(text_sample))

    try:
        if LLM_BACKEND == "anthropic":
            raw = _call_anthropic(prompt)
        else:
            raw = _call_groq(prompt)

        analysis = _parse_json(raw)
        result["analysis"] = analysis
        logger.info(
            f"Analysis complete ({LLM_BACKEND}) for {result['url']}: "
            f"is_bulk={analysis.get('is_bulk_agreement')}, "
            f"confidence={analysis.get('confidence')}"
        )
    except Exception as e:
        logger.error(f"Analysis failed for {result['url']}: {e}")
        result["analysis"] = {"error": str(e)}

    return result
