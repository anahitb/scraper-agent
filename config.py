PROVIDERS = [
    # D
    "DiamondNet",
    "Dickey Rural Telephone Coop",
    "Digitalway Services",
    "Discernity",
    "Dojo Networks",
    "DTS Fiber",
    # E
    "Eastern Shore Communications",
    "Empire Telephone Corp",
    "Ethx",
    # F
    "FastStream Networks",
    "Fiber Communications of Columbus",
    "Fiber Fast Homes",
    "Fiber Stream",
    "Fibernow (Opticaltel)",
    "Fiberspark",
    "First Step Internet",
    "Flume",
    "Fourway Computer Products",
    "FPUAnet Communications",
    "Franklin Telephone Company",
    # G
    "Gigafy",
    "GigaPointe",
    "Gigstreem",
    "Grand Mound Cooperative Telephone",
    "Great Works Internet",
    "Green Mountain Access",
    "GRUCom (Gator Net)",
    # H
    "Harmony Telephone Company",
    "Hawaii Dialogix Telecom, LLC",
    "HDER LINK",
    "Heart of Iowa Communications Cooperative",
    "Heartland Technology",
    "Home Town Cable TV",
    "Horry Telephone Cooperative",
    "Hotwire Communications",
    # I
    "IBT Connect",
    "ICS Advanced Technologies",
    "IFN",
    "InfoWest",
    "Inland Cellular",
    "IPacket Networks",
    "IPV Connect",
    "ISP.Net",
    # J
    "James Valley Cooperative Telephone Company",
    "Juvilex Communications",
    # K
    "KC Fiber",
    "Kwikbit",
    # L
    "Latigo",
    "LR Communications",
    "Luminate Fiber",
    # M
    "Madrone Broadband",
    "Massena Telephone Company",
    "Massivemesh Networks",
    "McDonough Telephone Cooperative",
    "MDU Datacom",
    "MDU Internet Services",
    "MDU Netech",
    "Mereo Networks",
    "Mitchell Telecom",
    "MLGC",
    "MoCoNet",
    "Montana Internet",
    "Mosaic Technologies",
    "Mountain Communications",
    # N
    "National WiFi",
    "Natural Wireless",
    "Nemont",
    "Net Vision Communications",
    "Netblazr",
    "Network Tool and Die Company",
    "New Hampshire Broadband",
    "Newark Fiber",
    "NexGen Connected Communities",
    "North East Fiber",
    "North Texas Fiber",
    "Northland Cable",
    "NUconnect",
    # O
    "OACYS Technology",
    "OptiLink",
    # P
    "PCs for People",
    "Premium Choice Broadband",
    # Q
    "Quad State Internet",
    # R
    "Ralls Technologies, L.L.C",
    "Red Bison",
    "ResTech Services",
    "Router12 Networks",
    "RTC Communications",
    # S
    "Salsgiver",
    "Santel",
    "SecureVision",
    "Single Digits",
    "Smart Grid Fiber",
    "Smartaira",
    "Smithville Communication",
    "Southeastern Indiana REMC",
    "Spencer Municipal Utilities",
    "Stellar Broadband",
    "Stowe Communications",
    "Stupp Fiber",
    "Succeed.Net",
    "Supernet",
    "SVEConnect",
    # T
    "TalusLink",
    "Triangle Communications",
    "Twin Valley Communications",
    # U
    "ULTRAFi",
    "United Wireless Communications",
    "UPN",
    "Uprise Fiber",
    "Upstream",
    "US Internet",
    # V
    "VA Skywire",
    "Vernon Communications",
    # W
    "WATCH TV",
    "Wavefly",
    "West Carolina Rural Telephone Cooperative",
    "West Coast Internet",
    "West River Telecommunications Cooperative",
    "West Texas Rural Telephone Cooperative",
    "West Wisconsin Telcom Cooperative",
    "WideOpen Networks",
    "Wonderlink Communications",
    "WWTELCO",
    # X
    "Xiber",
    # Y
    "yondoo Broadband",
    # Z
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
    # Tight — document title phrases
    '"{provider}" "bulk service agreement" pdf',
    '"{provider}" "communications network and service agreement" bulk pdf',
    '"{provider}" "bulk cable television services agreement" pdf',
    # Broad — property type combos
    '"{provider}" bulk internet agreement HOA pdf',
    '"{provider}" bulk internet agreement "homeowners association" pdf',
    '"{provider}" bulk internet agreement "condo" OR "condominium" pdf',
    '"{provider}" MDU bulk service agreement pdf',
    '"{provider}" bulk internet "per unit" agreement pdf',
    # Public records / government portals often host these
    '"{provider}" bulk agreement "number of units" pdf',
    '"{provider}" "service commitment period" bulk internet pdf',
    '"{provider}" "door fee" bulk internet agreement pdf',
    # Without pdf constraint — catches HTML-hosted or non-standard URLs
    '"{provider}" "bulk service fee" "per unit" internet agreement',
    '"{provider}" communities bulk internet agreement signed',
    # Simple unquoted — catches docs where provider name isn't in exact title
    '{provider} bulk internet agreement pdf',
    '{provider} MDU bulk service agreement pdf',
]

MAX_RESULTS_PER_QUERY = 10  # results per page
SEARCH_PAGES = 5            # number of Google pages to fetch per query
PDF_DOWNLOAD_TIMEOUT = 30   # seconds
MAX_PDF_PAGES_TO_SCAN = 20  # scan more pages — some agreements bury pricing deeper

OUTPUT_DIR = "output"
