PROVIDERS = [
    "Comcast",
    "AT&T",
    "Spectrum",
    "Xfinity",
    "Cox",
    "Verizon",
    "CenturyLink",
    "Lumen",
    "Frontier",
    "Ziply",
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

# Search queries constructed per provider
SEARCH_QUERY_TEMPLATES = [
    '"{provider}" "bulk service agreement" filetype:pdf',
    '"{provider}" "communications network and service agreement" bulk',
    '"{provider}" communities service agreement bulk internet',
    '"{provider}" bulk internet agreement HOA filetype:pdf',
    '"{provider}" "bulk cable" OR "bulk internet" service agreement property',
    '"{provider}" MDU bulk service agreement pdf',
]

MAX_RESULTS_PER_QUERY = 10
PDF_DOWNLOAD_TIMEOUT = 30  # seconds
MAX_PDF_PAGES_TO_SCAN = 10  # only read first N pages for speed

OUTPUT_DIR = "output"
REPORT_FILE = "output/report.json"
