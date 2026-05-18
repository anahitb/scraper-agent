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
    "telecommunications",
    "telecom",
    "network-agreement",
    "network_agreement",
    "bulk-internet",
    "bulk_internet",
    "bulk-service",
    "bulk_service",
    "mdu",
    "multi-dwelling",
    "multidwelling",
    "property-agreement",
    "property_agreement",
    "bulk-contract",
    "bulk_contract",
]

# Keywords searched inside PDF text to verify document type
CONTENT_KEYWORDS = [
    "bulk service agreement",
    "bulk internet",
    "bulk telecommunications",
    "telecommunications service agreement",
    "network and service agreement",
    "communications network",
    "bulk agreement",
    "property owner",
    "property manager",
    "multi-dwelling",
    "mdu",
    "exclusive provider",
    "service provider",
    "monthly recurring",
    "term of agreement",
]

# Minimum number of content keywords that must appear to consider a doc valid
MIN_CONTENT_KEYWORD_MATCHES = 3

# Search queries constructed per provider
SEARCH_QUERY_TEMPLATES = [
    '"{provider}" bulk internet agreement filetype:pdf',
    '"{provider}" bulk service agreement telecommunications pdf',
    '"{provider}" bulk contract agreement property internet',
    '"{provider}" network and service agreement bulk filetype:pdf',
    '"{provider}" MDU bulk internet agreement',
]

MAX_RESULTS_PER_QUERY = 10
PDF_DOWNLOAD_TIMEOUT = 30  # seconds
MAX_PDF_PAGES_TO_SCAN = 10  # only read first N pages for speed

OUTPUT_DIR = "output"
REPORT_FILE = "output/report.json"
