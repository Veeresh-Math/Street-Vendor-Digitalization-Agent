"""
Knowledge Base for Street Vendor Digitalization Agent
Contains real-time structured data about:
  - Government schemes (PM SVANidhi, MSME, Mudra Yojana, FSSAI)
  - UPI / Digital Payment setup guides
  - Online listing platforms
  - Hyperlocal SEO strategies
  - Consumer behavior insights
  - Credit access information
"""

# Each document has: id, category, title, content, tags
KNOWLEDGE_BASE = [

    # ── GOVERNMENT SCHEMES ───────────────────────────────────────────────────
    {
        "id": "gov_01",
        "category": "Government Scheme",
        "title": "PM SVANidhi — Micro Credit for Street Vendors",
        "content": (
            "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi) is a micro-credit scheme for street vendors. "
            "Vendors can avail working capital loans of ₹10,000 (1st loan), ₹20,000 (2nd loan), ₹50,000 (3rd loan). "
            "No collateral required. Apply at pmsvanidhi.mohua.gov.in or nearest bank/MFI. "
            "Eligibility: Street vendors with Certificate of Vending or Letter of Recommendation from ULB. "
            "Interest subsidy: 7% per annum. Digital transaction incentive: ₹1,200/year cashback on UPI transactions. "
            "Required documents: Aadhaar card, Vending certificate/LoR, bank account, mobile number. "
            "Apply online: pmsvanidhi.mohua.gov.in | Helpline: 1800-11-1979"
        ),
        "tags": ["credit", "loan", "government", "street vendor", "PM SVANidhi", "micro credit", "working capital"],
    },
    {
        "id": "gov_02",
        "category": "Government Scheme",
        "title": "MSME Registration & Udyam Certificate",
        "content": (
            "Any micro or small business including street vendors can register as MSME on udyamregistration.gov.in. "
            "MSME registration is FREE and gives access to: Priority sector lending, Collateral-free loans up to ₹10 lakh, "
            "Government tenders, Technology upgradation subsidies, Credit Guarantee Fund Trust (CGTMSE). "
            "Micro enterprise: Investment < ₹1 crore, Turnover < ₹5 crore. "
            "Registration process: Visit udyamregistration.gov.in → Enter Aadhaar → Fill business details → Get Udyam Certificate instantly. "
            "Benefits: 50% subsidy on patent/trademark fees, access to SIDBI loans at lower interest rates."
        ),
        "tags": ["MSME", "Udyam", "registration", "certificate", "micro enterprise", "government", "loan"],
    },
    {
        "id": "gov_03",
        "category": "Government Scheme",
        "title": "Mudra Yojana — Pradhan Mantri Mudra Yojana (PMMY)",
        "content": (
            "PMMY provides loans up to ₹10 lakh to non-corporate, non-farm small/micro enterprises. "
            "Three categories: Shishu (up to ₹50,000), Kishore (₹50,001 to ₹5 lakh), Tarun (₹5 lakh to ₹10 lakh). "
            "Apply at any bank, MFI, or NBFC. No collateral for Shishu and Kishore. "
            "Best for: Vegetable vendors, fruit sellers, food stalls, tailors, repair shops, textile traders. "
            "Website: mudra.org.in | Helpline: 1800-180-1111"
        ),
        "tags": ["Mudra", "PMMY", "loan", "Shishu", "Kishore", "Tarun", "micro business", "credit"],
    },
    {
        "id": "gov_04",
        "category": "Government Scheme",
        "title": "FSSAI Registration for Food Vendors",
        "content": (
            "All food vendors including street food stalls, fruit sellers, and snack shops must register under FSSAI. "
            "Basic registration: Annual turnover below ₹12 lakh — register at foscos.fssai.gov.in. Fee: ₹100/year. "
            "State license: Turnover ₹12 lakh to ₹20 crore. "
            "Required documents: Aadhaar, address proof, food safety training certificate. "
            "Benefits: Legal authorization to sell food, eligibility for Zomato/Swiggy listing, consumer trust. "
            "Apply: foscos.fssai.gov.in | Helpline: 1800-112-100"
        ),
        "tags": ["FSSAI", "food license", "registration", "food safety", "street food", "Zomato", "Swiggy"],
    },
    {
        "id": "gov_05",
        "category": "Government Scheme",
        "title": "Digital India — Free Internet & Digital Literacy",
        "content": (
            "Under Digital India, vendors can access: CSC (Common Service Centre) for digital services, "
            "Free WiFi hotspots in markets and public areas, Digital Saksharta Abhiyan for free digital training. "
            "PM eVIDYA provides free online courses in local languages. "
            "DigiLocker: Store and share documents digitally — Aadhaar, licenses, certificates. "
            "PMGDISHA: Free digital literacy training for rural and semi-urban citizens."
        ),
        "tags": ["Digital India", "internet", "digital literacy", "CSC", "DigiLocker", "training"],
    },

    # ── UPI & DIGITAL PAYMENTS ────────────────────────────────────────────────
    {
        "id": "upi_01",
        "category": "UPI Setup",
        "title": "PhonePe UPI Setup for Street Vendors",
        "content": (
            "PhonePe merchant setup steps: "
            "1. Download PhonePe app from Play Store/App Store. "
            "2. Register with mobile number linked to bank account. "
            "3. Tap 'Business' → 'Register as Merchant'. "
            "4. Enter business name, category (e.g., Fruits & Vegetables, Food Stall). "
            "5. Link bank account (savings account works). "
            "6. Download/print QR code from 'My QR' section. "
            "7. Display QR at your stall. Customers scan and pay instantly. "
            "Features: Free settlements, instant notifications, monthly statements, SmartSpeaker for audio confirmation. "
            "Zero MDR (Merchant Discount Rate) on UPI transactions. "
            "PhonePe for Business helpline: 080-68727374"
        ),
        "tags": ["PhonePe", "UPI", "QR code", "merchant", "digital payment", "setup"],
    },
    {
        "id": "upi_02",
        "category": "UPI Setup",
        "title": "Paytm QR Code & Soundbox for Vendors",
        "content": (
            "Paytm merchant setup: "
            "1. Download Paytm Business app. "
            "2. Register with mobile and Aadhaar/PAN. "
            "3. Select business type — Street Vendor, Food Stall, Grocery, etc. "
            "4. Get your unique Paytm QR code — download and print. "
            "5. Optional: Rent Paytm Soundbox (₹99/month) for audio payment alerts. "
            "Benefits: Accept UPI, cards, wallets. Free next-day settlement. "
            "Paytm loan: Apply for business loan up to ₹5 lakh through Paytm app. "
            "Helpline: 0120-4770770"
        ),
        "tags": ["Paytm", "QR code", "Soundbox", "UPI", "payment", "merchant", "loan"],
    },
    {
        "id": "upi_03",
        "category": "UPI Setup",
        "title": "Google Pay (GPay) Merchant Setup",
        "content": (
            "Google Pay for Business setup: "
            "1. Download Google Pay app. "
            "2. Go to 'Business' tab → 'Start accepting payments'. "
            "3. Add business name, type, and bank account. "
            "4. Generate QR code — can be printed or shown digitally. "
            "5. Share UPI ID (e.g., yourbusiness@okaxis) with customers. "
            "Google Pay works with all UPI apps — customers using PhonePe, Paytm, BHIM can all pay. "
            "Free transaction reports and GST-ready invoices available."
        ),
        "tags": ["Google Pay", "GPay", "UPI", "QR code", "merchant", "payment"],
    },

    # ── ONLINE LISTING PLATFORMS ──────────────────────────────────────────────
    {
        "id": "list_01",
        "category": "Online Listing",
        "title": "Google My Business Listing for Street Vendors",
        "content": (
            "Google My Business (Google Business Profile) helps your stall appear on Google Maps and Search. "
            "Setup steps: "
            "1. Visit business.google.com → Sign in with Google account. "
            "2. Search your business name → Click 'Add your business'. "
            "3. Choose category (Food & Beverage, Retail, etc.). "
            "4. Add address/location — even a street corner or market area. "
            "5. Add phone, working hours, photos of your stall and products. "
            "6. Verify via phone call or postcard. "
            "Benefits: Appear in 'near me' searches, get customer reviews, show on Google Maps. "
            "Free to use. Helps attract 3x more walk-in customers."
        ),
        "tags": ["Google Maps", "Google My Business", "listing", "local SEO", "online visibility"],
    },
    {
        "id": "list_02",
        "category": "Online Listing",
        "title": "Swiggy Instamart & Zepto for Vegetable/Fruit Vendors",
        "content": (
            "Swiggy Instamart and Zepto allow hyperlocal grocery and produce vendors to list on their platforms. "
            "Swiggy Instamart partner registration: partner.swiggy.com → Register as Grocery Partner. "
            "Requirements: FSSAI license (for food items), bank account, GST (optional for small vendors). "
            "Zepto Seller: sell.zepto.com — register as a dark store supplier. "
            "Benefits: Access to thousands of daily orders in your area, Swiggy handles delivery logistics. "
            "Commission: 15-25% per order. Best for fruit, vegetable, and daily grocery vendors."
        ),
        "tags": ["Swiggy", "Instamart", "Zepto", "online selling", "grocery", "fruit", "vegetable", "delivery"],
    },
    {
        "id": "list_03",
        "category": "Online Listing",
        "title": "Meesho & GlowRoad for Textile & Clothing Vendors",
        "content": (
            "Meesho is India's largest social commerce platform for small sellers. "
            "Register: supplier.meesho.com → Upload products → Start selling. "
            "No listing fee, zero commission on first 6 months. "
            "GlowRoad: glowroad.com — another reselling platform for clothing, accessories. "
            "Benefits: Pan-India customer reach, Meesho handles payments and returns. "
            "Best for: Textile vendors, clothing sellers, fashion accessories, saree traders. "
            "Required: Bank account, Aadhaar, product photos."
        ),
        "tags": ["Meesho", "GlowRoad", "textile", "clothing", "reselling", "online selling", "fashion"],
    },
    {
        "id": "list_04",
        "category": "Online Listing",
        "title": "Zomato & Swiggy for Street Food Vendors",
        "content": (
            "Zomato and Swiggy allow street food vendors and small restaurants to list online. "
            "Zomato partner registration: zomato.com/business → Register as Restaurant Partner. "
            "Requirements: FSSAI license (mandatory for food), GST (if turnover > ₹20 lakh), bank account. "
            "Swiggy restaurant partner: partner.swiggy.com. "
            "Commission: 18-25%. Average order value: ₹150-300. "
            "Benefits: Access to 10M+ daily active users, free online menu, delivery partner network. "
            "Best for: Idli-dosa stalls, snack vendors, biryani stalls, chaat shops."
        ),
        "tags": ["Zomato", "Swiggy", "food delivery", "street food", "restaurant", "online order"],
    },

    # ── HYPERLOCAL SEO ────────────────────────────────────────────────────────
    {
        "id": "seo_01",
        "category": "Local SEO",
        "title": "Hyperlocal SEO Strategy for Street Vendors",
        "content": (
            "SEO tips for street vendors to appear in local Google searches: "
            "1. Google Business Profile: Add exact locality (Camp, Pune / T. Nagar, Chennai). "
            "2. Keywords to use: '[product] near me', '[product] in [locality]', '[product] [city]'. "
            "3. Get Google Reviews: Ask customers to leave 5-star reviews — boosts ranking. "
            "4. WhatsApp Business: Create a catalog with product photos and prices. "
            "5. Post regularly on Google Business Profile — seasonal offers, new products. "
            "6. Add photos of stall, products, and happy customers. "
            "7. NAP consistency: Same Name, Address, Phone across all platforms. "
            "Result: Appear in top 3 'near me' searches within 2-4 weeks."
        ),
        "tags": ["SEO", "local search", "Google", "near me", "hyperlocal", "visibility", "ranking"],
    },

    # ── CUSTOMER ENGAGEMENT ────────────────────────────────────────────────────
    {
        "id": "engage_01",
        "category": "Customer Engagement",
        "title": "WhatsApp Business for Customer Engagement",
        "content": (
            "WhatsApp Business is a free app for small vendors to engage customers. "
            "Setup: Download WhatsApp Business → Create profile with business name, address, hours. "
            "Features: Product catalog (add photos + prices), Quick replies, Broadcast messages. "
            "Marketing ideas: "
            "- Send daily specials: 'Today's fresh tomatoes ₹30/kg — order now!' "
            "- Festival offers: 'Diwali special — buy 2kg dry fruits get 200g free!' "
            "- Loyalty: 'Buy 10 times, get 1 free!' "
            "- Location: Share live location so customers find you easily. "
            "WhatsApp Pay: Accept UPI payments directly in chat."
        ),
        "tags": ["WhatsApp", "customer engagement", "marketing", "catalog", "promotion"],
    },
    {
        "id": "engage_02",
        "category": "Customer Engagement",
        "title": "Seasonal Pricing & Festival Strategy for Vendors",
        "content": (
            "Smart pricing strategies for street vendors: "
            "Peak season tips: Increase prices by 10-15% during festival seasons (Diwali, Eid, Christmas, Navratri). "
            "Bundle offers: Combine slow-moving items with popular ones. "
            "Morning vs evening pricing: Reduce prices by 20% in last 2 hours to clear stock. "
            "Festival calendar for vendors: Diwali (dry fruits, sweets), Navratri (sabudana, kuttu), "
            "Makar Sankranti (til, gur), Raksha Bandhan (sweets), Durga Puja (new clothes, flowers). "
            "Loyalty programs: Simple punch card — buy 10, get 1 free — increases repeat customers by 40%."
        ),
        "tags": ["pricing", "festival", "seasonal", "strategy", "loyalty", "promotion", "marketing"],
    },

    # ── CITY-SPECIFIC DATA ────────────────────────────────────────────────────
    {
        "id": "city_pune",
        "category": "City Data",
        "title": "Digital Resources for Vendors in Pune",
        "content": (
            "Pune vendors can access: "
            "PMC (Pune Municipal Corporation) vendor registration portal: pmc.gov.in. "
            "Camp area, FC Road, JM Road, Laxmi Road are high-footfall vendor zones. "
            "Pune has 200+ CSC centers for digital assistance. "
            "NMC ULB registration required for vending certificate to apply PM SVANidhi. "
            "Local delivery apps active in Pune: Swiggy, Zomato, Blinkit, Zepto, Dunzo. "
            "Key local keywords: 'fruit seller Camp Pune', 'sabzi vendor FC Road Pune'."
        ),
        "tags": ["Pune", "PMC", "Camp", "FC Road", "local", "city", "Maharashtra"],
    },
    {
        "id": "city_mumbai",
        "category": "City Data",
        "title": "Digital Resources for Vendors in Mumbai",
        "content": (
            "Mumbai vendors: MCGM (BMC) vendor registration at mcgm.gov.in. "
            "Key vendor zones: Dharavi, Dadar, Crawford Market, Kurla, Andheri. "
            "Mumbai-specific apps: Swiggy, Zomato, Blinkit, Dunzo, BigBasket Now. "
            "Local train station stalls (Dadar, CST, Andheri) — high footfall, SEO keywords valuable. "
            "Dharavi vendors: Access to MSME cluster support and credit facilities."
        ),
        "tags": ["Mumbai", "Dharavi", "Dadar", "MCGM", "BMC", "Maharashtra"],
    },
    {
        "id": "city_chennai",
        "category": "City Data",
        "title": "Digital Resources for Vendors in Chennai",
        "content": (
            "Chennai vendors: GCC (Greater Chennai Corporation) registration at chennaicorporation.gov.in. "
            "Key vendor zones: T. Nagar, Sowcarpet, Koyambedu, Anna Nagar. "
            "Tamil Nadu MSME portal: msmeonline.tn.gov.in. "
            "TIDCO assistance for micro vendors in Tamil Nadu. "
            "Local keywords: 'idli vendor T Nagar', 'saree shop Sowcarpet Chennai'. "
            "Active apps: Swiggy, Zomato, Blinkit, Dunzo."
        ),
        "tags": ["Chennai", "T. Nagar", "Koyambedu", "GCC", "Tamil Nadu", "Tamil"],
    },
]


def get_all_documents() -> list[dict]:
    """Return all documents in the knowledge base."""
    return KNOWLEDGE_BASE


def get_documents_by_category(category: str) -> list[dict]:
    """Filter documents by category."""
    return [doc for doc in KNOWLEDGE_BASE if doc["category"].lower() == category.lower()]


def get_all_text_chunks() -> list[tuple[str, dict]]:
    """
    Returns list of (text_to_embed, doc_metadata) tuples.
    The text is title + content combined for richer embeddings.
    """
    chunks = []
    for doc in KNOWLEDGE_BASE:
        text = f"{doc['title']}. {doc['content']}"
        chunks.append((text, doc))
    return chunks
