PROVIDERS = [
    "Broadstar",
    "Buzz Broadband",
    "Byte Broadband",
    "DECCA Digital Solutions",
    "SecureVision",
    "Single Digits",
    "Upstream",
    "Comcast",
    "Spectrum",
]

# Keywords that indicate a bulk internet agreement URL or document
URL_KEYWORDS = [
    "bulk",
    "service-agreement",
    "service_agreement",
    "network-and-service",
    "network_and_service",
    "communications-network",
    "communications_network",
    "bulk-internet",
    "bulk_internet",
    "bulk-service",
    "bulk_service",
    "bulk-cable",
    "bulk_cable",
    "communities-service",
    "communities_service",
    "xfinity-communities",
    "mdu",
    "multi-dwelling",
    "multidwelling",
    "bulk-contract",
    "bulk_contract",
    "hoa",
    "homeowner",
    "condo-assoc",
]

# Keywords searched inside PDF text to verify document type.
# Derived from reviewing real agreements: WOW!, Spectrum, Xfinity/Comcast, Fibernow.
CONTENT_KEYWORDS = [
    # Document title phrases (very strong signals)
    "bulk cable television services agreement",
    "communications network and service agreement",
    "xfinity communities service agreement",
    "bulk service agreement",
    "bulk internet service",
    "bulk video service",
    "bulk-billed",
    "bulk billed",
    # Pricing / deal structure (appear in every agreement reviewed)
    "per unit",
    "bulk service fee",
    "service commitment period",
    "door fee",
    "per unit compensation",
    "number of units",
    # Party / property language
    "homeowner",
    "homeowners association",
    "condominium",
    "condo assoc",
    "property owner",
    "property manager",
    # Service / tech terms
    "advanced community wifi",
    "bulk internet",
    "bulk video",
    "operator",
    "service activation date",
    # Common structural terms
    "termination notice",
    "non-exclusive marketing",
    "exclusive marketing",
    "marketing rights",
]

# Minimum number of content keywords that must appear to consider a doc valid
MIN_CONTENT_KEYWORD_MATCHES = 4

# Search queries constructed per provider.
# Mix of tight (quoted) and broad queries to maximise recall.
SEARCH_QUERY_TEMPLATES = [
    # Tight — document title phrases
    '"{provider}" "bulk service agreement" filetype:pdf',
    '"{provider}" "communications network and service agreement" bulk filetype:pdf',
    '"{provider}" "xfinity communities service agreement" filetype:pdf',
    '"{provider}" "bulk cable television services agreement" filetype:pdf',
    # Broad — property type combos
    '"{provider}" bulk internet agreement HOA filetype:pdf',
    '"{provider}" bulk internet agreement "homeowners association" pdf',
    '"{provider}" bulk internet agreement "condo" OR "condominium" pdf',
    '"{provider}" MDU bulk service agreement pdf',
    '"{provider}" bulk internet "per unit" agreement pdf',
    # Public records / government portals often host these
    '"{provider}" bulk agreement "number of units" filetype:pdf',
    '"{provider}" "service commitment period" bulk internet pdf',
    '"{provider}" "door fee" bulk internet agreement pdf',
    # Without filetype constraint to catch HTML-hosted or non-standard URLs
    '"{provider}" "bulk service fee" "per unit" internet agreement',
    '"{provider}" communities bulk internet agreement signed',
]

MAX_RESULTS_PER_QUERY = 20
PDF_DOWNLOAD_TIMEOUT = 30  # seconds
MAX_PDF_PAGES_TO_SCAN = 20  # scan more pages — some agreements bury pricing deeper

OUTPUT_DIR = "output"
REPORT_FILE = "output/report.json"
