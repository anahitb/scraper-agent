PROVIDERS = [
    "Hotwire Communications",
    "Consolidated Smart Broadband Systems, LLC",
    "ENCO Electronic Systems LLC",
    "West Coast Internet",
    "HOME TOWN CABLE TV, LLC",
    "BLUE STREAM",
    "ResTech Services",
    "Uprise Fiber",
    "Hawaii Dialogix Telecom, LLC",
    "Florida WiFi, LLC",
    "NexGen Connected Communities",
    "Xiber, LLC",
    "Fiber Fast Homes",
    "KC Fiber",
    "IBT Connect",
    "Newark Fiber",
    "Juvilex Communications",
    "Network Tool and Die Company Inc.",
    "FPUAnet Communications",
    "Ethx Internet",
    "Gigafy",
    "Independents Fiber Network",
    "832 Communications",
    "AccessParks",
    "Broadstar",
    "GRUCom (Gator Net)",
    "GigaPointe",
    "Gigstreem",
    "UPN",
    "Zentro",
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
    "internet-agreement",
    "internet_agreement",
    "internet-pdf",
    "internet_pdf",
    "telecom-agreement",
    "telecom_agreement",
    "telecommunications-agreement",
    "telecommunications_agreement",
    "provider-agreement",
    "provider_agreement",
    "signed-agreement",
    "signed_agreement",
    "broadband-agreement",
    "broadband_agreement",
    "broadband-service",
    "broadband_service",
    "fiber-agreement",
    "fiber_agreement",
    "cable-agreement",
    "cable_agreement",
    "residential-agreement",
    "residential_agreement",
    "property-agreement",
    "property_agreement",
]

# Keywords searched inside PDF text to verify document type.
CONTENT_KEYWORDS = [
    # Document title phrases (very strong signals)
    "bulk cable television services agreement",
    "communications network and service agreement",
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
MIN_CONTENT_KEYWORD_MATCHES = 2

# Search queries constructed per provider.
# Note: filetype:pdf removed — Serper returns 400 errors with that operator.
SEARCH_QUERY_TEMPLATES = [
    '"{provider}" MDU agreement pdf',
    '"{provider}" internet pdf',
    '"{provider}" "internet agreement" pdf',
    '"{provider}" "service agreement" pdf',
    '"{provider}" "bulk internet" pdf',
]

MAX_RESULTS_PER_QUERY = 10  # results per page
SEARCH_PAGES = 2            # number of Google pages to fetch per query
PDF_DOWNLOAD_TIMEOUT = 10   # seconds
MAX_PDF_PAGES_TO_SCAN = 20  # scan more pages — some agreements bury pricing deeper

OUTPUT_DIR = "output"
