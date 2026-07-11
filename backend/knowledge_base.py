"""
Knowledge Base — Street Vendor Digitalization Agent
20+ real-world structured documents covering:
  • Government schemes  (PM SVANidhi, Mudra, MSME/Udyam, FSSAI, Digital India)
  • UPI / payment setup (PhonePe, Paytm, GPay)
  • Online listing      (Google Maps, Swiggy, Zomato, Meesho, GlowRoad)
  • Hyperlocal SEO
  • Customer engagement (WhatsApp Business, seasonal pricing)
  • City-specific data  (Pune, Mumbai, Chennai, Bangalore, Surat, Delhi)
Each doc: id, category, title, content, tags, language_hint
"""

DOCUMENTS: list[dict] = [

    # ── GOVERNMENT SCHEMES ───────────────────────────────────────────────────

    {
        "id": "gov_01",
        "category": "Government Scheme",
        "title": "PM SVANidhi — Micro Credit for Street Vendors",
        "content": (
            "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi) provides working-capital loans to street "
            "vendors without collateral. Loan amounts: ₹10,000 (1st), ₹20,000 (2nd), ₹50,000 (3rd). "
            "Interest subsidy: 7% per annum credited directly to bank account. "
            "Digital transaction incentive: ₹1,200/year cashback for UPI usage. "
            "Eligibility: Street vendor with Certificate of Vending (CoV) or Letter of Recommendation (LoR) "
            "from ULB/Town Vending Committee. "
            "Required documents: Aadhaar card, CoV or LoR, savings bank account, mobile number. "
            "Apply online: pmsvanidhi.mohua.gov.in | Nearest bank / MFI / NBFC. "
            "Helpline: 1800-11-1979 (toll-free). "
            "Key benefit: Repay on time → automatically eligible for higher next loan tier."
        ),
        "tags": ["PM SVANidhi", "micro credit", "loan", "street vendor", "working capital",
                 "collateral free", "hawker", "government scheme"],
        "language_hint": "en",
    },
    {
        "id": "gov_02",
        "category": "Government Scheme",
        "title": "MSME Udyam Registration — Free Certificate for Micro Businesses",
        "content": (
            "Any micro business including street vendors can register free at udyamregistration.gov.in. "
            "Micro enterprise definition: investment < ₹1 crore AND turnover < ₹5 crore. "
            "Registration is instant — enter Aadhaar, fill business details, get Udyam certificate. "
            "Benefits: Priority sector bank loans, collateral-free credit up to ₹10 lakh (CGTMSE), "
            "50% subsidy on patent/trademark fees, government tender participation, "
            "lower electricity tariffs in many states, SIDBI refinance. "
            "Portal: udyamregistration.gov.in | Helpline: 1800-111-956"
        ),
        "tags": ["MSME", "Udyam", "registration", "certificate", "micro enterprise",
                 "collateral free", "CGTMSE", "priority sector"],
        "language_hint": "en",
    },
    {
        "id": "gov_03",
        "category": "Government Scheme",
        "title": "Pradhan Mantri Mudra Yojana (PMMY) — Loans up to ₹10 Lakh",
        "content": (
            "PMMY provides loans to non-corporate non-farm micro/small enterprises via banks, MFIs, NBFCs. "
            "Shishu: up to ₹50,000 — for new/early stage vendors. "
            "Kishore: ₹50,001–₹5 lakh — for established vendors wanting to expand. "
            "Tarun: ₹5 lakh–₹10 lakh — for scaling businesses. "
            "No collateral for Shishu and Kishore. Simple documentation. "
            "Best suited for: fruit/veg vendors, food stalls, textile traders, repair shops, tailors. "
            "Apply at any PSU bank, regional rural bank, cooperative bank, or NBFC. "
            "Portal: mudra.org.in | Helpline: 1800-180-1111"
        ),
        "tags": ["Mudra", "PMMY", "Shishu", "Kishore", "Tarun", "loan", "micro business", "expand"],
        "language_hint": "en",
    },
    {
        "id": "gov_04",
        "category": "Government Scheme",
        "title": "FSSAI Basic Registration for Food Street Vendors",
        "content": (
            "All food vendors (fruit sellers, food stalls, chai stalls, snack carts) must register under FSSAI. "
            "Basic registration: annual turnover < ₹12 lakh. Fee: ₹100/year. Apply: foscos.fssai.gov.in. "
            "State license: turnover ₹12 lakh–₹20 crore. "
            "Documents: Aadhaar, address proof, passport photo, food safety training certificate (optional). "
            "Benefits: Legal right to operate, mandatory for Zomato/Swiggy/Blinkit listing, consumer trust, "
            "eligibility for food business loans. "
            "FSSAI helpline: 1800-112-100 | foscos.fssai.gov.in"
        ),
        "tags": ["FSSAI", "food license", "food stall", "chai", "fruit", "snack", "Zomato", "Swiggy",
                 "food safety", "registration"],
        "language_hint": "en",
    },
    {
        "id": "gov_05",
        "category": "Government Scheme",
        "title": "Digital India — CSC, DigiLocker & Free Digital Training",
        "content": (
            "Under Digital India, vendors can access: "
            "Common Service Centres (CSC): 5 lakh+ across India — get Aadhaar, certificates, govt forms processed. "
            "DigiLocker: Store Aadhaar, licenses, FSSAI certificate digitally — share with apps. digilocker.gov.in. "
            "PMGDISHA: Free 20-hour digital literacy course for rural/semi-urban citizens. "
            "PM eVIDYA: Free online courses in all Indian languages. "
            "Free WiFi: PM-WANI scheme — public WiFi at markets, bus stands, railway stations. "
            "National Career Service Portal: ncs.gov.in — free digital skills training."
        ),
        "tags": ["Digital India", "CSC", "DigiLocker", "digital literacy", "PMGDISHA",
                 "free training", "WiFi", "PM-WANI"],
        "language_hint": "en",
    },
    {
        "id": "gov_06",
        "category": "Government Scheme",
        "title": "e-Shram — National Database of Unorganised Workers",
        "content": (
            "e-Shram is a government portal for unorganised sector workers including street vendors. "
            "Register at eshram.gov.in using Aadhaar + mobile. Free registration. "
            "Get e-Shram card (UAN — Universal Account Number). "
            "Benefits: ₹2 lakh accident insurance (PMSBY), priority in PM SVANidhi, "
            "access to social security schemes, direct benefit transfers. "
            "Eligibility: Age 16–59, not an EPFO/ESIC member, income < ₹10,000/month. "
            "Helpline: 14434"
        ),
        "tags": ["e-Shram", "unorganised worker", "UAN", "accident insurance", "social security",
                 "street vendor registration"],
        "language_hint": "en",
    },

    # ── UPI & DIGITAL PAYMENTS ────────────────────────────────────────────────

    {
        "id": "upi_01",
        "category": "UPI Setup",
        "title": "PhonePe Merchant — UPI QR Setup for Street Vendors",
        "content": (
            "PhonePe merchant setup (step-by-step): "
            "1. Download PhonePe app (Play Store / App Store). "
            "2. Register with mobile number linked to your bank account. "
            "3. Tap Business → Register as Merchant. "
            "4. Enter business name + category (Fruits & Vegetables / Food Stall / Grocery etc.). "
            "5. Link savings/current bank account. "
            "6. Download QR from 'My QR' → print at any stationery shop (A4 or A5). "
            "7. Optional: Order PhonePe SmartSpeaker (₹299 one-time) — announces payment amount aloud. "
            "Features: Instant payment alerts, weekly/monthly settlement reports, zero MDR on UPI. "
            "PhonePe Business helpline: 080-68727374"
        ),
        "tags": ["PhonePe", "UPI", "QR code", "merchant", "digital payment", "SmartSpeaker",
                 "zero MDR", "setup"],
        "language_hint": "en",
    },
    {
        "id": "upi_02",
        "category": "UPI Setup",
        "title": "Paytm QR + Soundbox for Vendors",
        "content": (
            "Paytm merchant setup: "
            "1. Download Paytm Business app. "
            "2. Register with mobile + Aadhaar/PAN. "
            "3. Select business type (Street Vendor / Food Stall / Grocery / Clothing). "
            "4. Get unique Paytm QR — download and print at any shop. "
            "5. Optional: Paytm Soundbox rental ₹99/month — audio payment confirmation. "
            "Accept: UPI, debit/credit cards, wallets, EMI. "
            "Free next-day settlement to bank account. "
            "Paytm business loan: up to ₹5 lakh via Paytm app (no branch visit). "
            "Helpline: 0120-4770770 | paytm.com/business"
        ),
        "tags": ["Paytm", "QR code", "Soundbox", "merchant", "UPI", "loan", "payment", "setup"],
        "language_hint": "en",
    },
    {
        "id": "upi_03",
        "category": "UPI Setup",
        "title": "Google Pay (GPay) Merchant Registration",
        "content": (
            "Google Pay for Business setup: "
            "1. Download Google Pay app. "
            "2. Go to Business tab → Start accepting payments. "
            "3. Add business name, type, and bank account (savings works). "
            "4. Generate QR — print it or show phone screen. "
            "5. Share UPI ID (e.g. yourstall@okaxis) on WhatsApp with customers. "
            "GPay accepts payments from ALL UPI apps — PhonePe, Paytm, BHIM, NEFT, IMPS. "
            "Free GST-ready transaction reports downloadable monthly. "
            "Google Pay for Business helpline: 1800-419-0157"
        ),
        "tags": ["Google Pay", "GPay", "UPI", "QR code", "merchant", "payment", "setup", "BHIM"],
        "language_hint": "en",
    },
    {
        "id": "upi_04",
        "category": "UPI Setup",
        "title": "BHIM UPI — Government UPI App for Vendors",
        "content": (
            "BHIM (Bharat Interface for Money) is the government-backed UPI app by NPCI. "
            "Completely free — no monthly charges ever. "
            "Setup: Download BHIM app → register mobile → link bank account → generate merchant QR. "
            "BHIM merchant QR can be printed at any e-Seva / CSC centre for free. "
            "All UPI payments from any app (PhonePe, Paytm, GPay) are accepted on BHIM QR. "
            "BHIM Aadhaar Pay: Accept payments without smartphone — only Aadhaar biometric needed. "
            "Helpline: 18001201740 | bhimupi.org.in"
        ),
        "tags": ["BHIM", "UPI", "NPCI", "government", "QR", "Aadhaar Pay", "free", "merchant"],
        "language_hint": "en",
    },

    # ── ONLINE LISTING PLATFORMS ──────────────────────────────────────────────

    {
        "id": "list_01",
        "category": "Online Listing",
        "title": "Google Business Profile (Google Maps) for Street Vendors",
        "content": (
            "Google Business Profile (formerly Google My Business) puts your stall on Google Maps and Search. "
            "Setup: business.google.com → Sign in → Add your business → Choose category. "
            "Add exact street/market location (Camp, Pune / Dadar, Mumbai / T. Nagar, Chennai). "
            "Add photos: stall exterior, products, price board, happy customers. "
            "Fill hours, phone, UPI ID in description. "
            "Verify: phone call or postcard (free). "
            "Result: Appear in 'fruit vendor near me', 'chai stall Camp Pune' Google searches. "
            "Pro tip: Post weekly offers/photos → boosts local search ranking significantly. "
            "Free forever. Average 3× increase in walk-in customers within 30 days."
        ),
        "tags": ["Google Maps", "Google Business Profile", "GMB", "local SEO", "near me",
                 "online listing", "visibility", "maps"],
        "language_hint": "en",
    },
    {
        "id": "list_02",
        "category": "Online Listing",
        "title": "Swiggy Instamart & Blinkit for Grocery/Produce Vendors",
        "content": (
            "Swiggy Instamart partner: partner.swiggy.com → Register as Grocery/Produce Partner. "
            "Requirements: FSSAI license (food items), bank account, GST optional below ₹20L turnover. "
            "Blinkit seller: seller.blinkit.com — dark store partner for hyperlocal grocery. "
            "Zepto seller: sell.zepto.com — 10-minute delivery platform. "
            "Commission: 15–25% per order (Swiggy/Blinkit handle delivery). "
            "Best for: fruit, vegetable, daily grocery, dairy, egg vendors. "
            "Average daily orders in Tier-1 cities: 20–80 orders/day after 2 months. "
            "Listing is free — you only pay commission on completed orders."
        ),
        "tags": ["Swiggy", "Instamart", "Blinkit", "Zepto", "grocery", "fruit", "vegetable",
                 "online delivery", "hyperlocal"],
        "language_hint": "en",
    },
    {
        "id": "list_03",
        "category": "Online Listing",
        "title": "Zomato & Swiggy Food for Street Food Stalls",
        "content": (
            "Zomato restaurant partner: zomato.com/business → Add Restaurant. "
            "Swiggy food partner: partner.swiggy.com → Restaurant section. "
            "Mandatory requirements: FSSAI license, bank account, GST if turnover > ₹20L. "
            "Commission: 18–25% per order. Average order: ₹150–₹350. "
            "Best for: idli-dosa stalls, biryani, chaat, vada pav, chai, snack counters. "
            "Both platforms provide free printed menu board and promotional materials. "
            "Zomato Gold: extra visibility for top-rated partners. "
            "Key: Maintain 4+ star rating for algorithm boost."
        ),
        "tags": ["Zomato", "Swiggy", "food delivery", "street food", "restaurant partner",
                 "FSSAI", "online order", "food stall"],
        "language_hint": "en",
    },
    {
        "id": "list_04",
        "category": "Online Listing",
        "title": "Meesho & GlowRoad for Textile, Clothing & Accessories Vendors",
        "content": (
            "Meesho — India's largest social commerce for small sellers. "
            "Register: supplier.meesho.com → Upload product photos → Set price → Go live. "
            "No listing fee. Meesho handles payment collection and returns. "
            "Pan-India reach across 19,000+ pin codes. "
            "GlowRoad: glowroad.com — reselling platform for clothing, accessories, home goods. "
            "Flipkart Seller: seller.flipkart.com — for packaged goods. "
            "Best for: sarees, dress materials, fashion accessories, ethnic wear, handicrafts. "
            "Required: Bank account, Aadhaar, product photos (phone camera OK). "
            "Average seller earns ₹8,000–₹25,000/month within 3 months."
        ),
        "tags": ["Meesho", "GlowRoad", "Flipkart", "textile", "clothing", "saree", "fashion",
                 "reselling", "online selling", "accessories"],
        "language_hint": "en",
    },
    {
        "id": "list_05",
        "category": "Online Listing",
        "title": "WhatsApp Business Catalogue for All Vendors",
        "content": (
            "WhatsApp Business is the most powerful free tool for Indian street vendors. "
            "Setup: Download WhatsApp Business app → Create business profile → Add catalogue. "
            "Catalogue: Add product photos, names, prices, descriptions (free, up to 500 items). "
            "Features: Quick replies, Away message, Broadcast lists (send to 256 customers at once). "
            "WhatsApp Pay: Accept UPI payments directly in chat. "
            "Share catalogue link on visiting card, stall display, and Google profile. "
            "Sample broadcast: 'Aaj ke ताज़े फल: Mango ₹80/kg, Watermelon ₹25/kg — Order karo!' "
            "Tip: Add your stall location pin in profile so customers can navigate directly."
        ),
        "tags": ["WhatsApp", "WhatsApp Business", "catalogue", "broadcast", "UPI", "product listing",
                 "customer", "marketing", "free"],
        "language_hint": "en",
    },

    # ── HYPERLOCAL SEO ────────────────────────────────────────────────────────

    {
        "id": "seo_01",
        "category": "Local SEO",
        "title": "Hyperlocal SEO Strategy for Street Vendors",
        "content": (
            "Top SEO moves for vendors to rank on Google 'near me' searches: "
            "1. Google Business Profile: Use exact locality name — not just city (Camp, Pune / Koramangala, Bangalore). "
            "2. Target keywords: '[product] near me', '[product] in [locality]', '[product] [city]', 'fresh [product] [market name]'. "
            "3. Reviews: Ask every customer to leave a Google review. 10+ reviews = top-3 local pack. "
            "4. Post weekly on Google Business Profile: photos of fresh stock, price updates, festival offers. "
            "5. NAP consistency: Exact same Name, Address, Phone on Google, Zomato, Swiggy, WhatsApp. "
            "6. Add business to Justdial, Sulekha, IndiaMART for extra backlinks. "
            "7. Festival keyword targeting: 'Diwali dry fruits Camp Pune', 'Navratri sabudana vendor'. "
            "Result: Top 3 local results in 3–5 weeks with consistent effort."
        ),
        "tags": ["SEO", "local search", "Google", "near me", "hyperlocal", "reviews", "ranking",
                 "visibility", "keywords"],
        "language_hint": "en",
    },

    # ── CUSTOMER ENGAGEMENT ────────────────────────────────────────────────────

    {
        "id": "engage_01",
        "category": "Customer Engagement",
        "title": "Seasonal Pricing & Festival Strategy for Indian Vendors",
        "content": (
            "Smart pricing for Indian street vendors: "
            "Festival calendar: Diwali (dry fruits +30%, diyas), Navratri (sabudana, kuttu, sendha namak), "
            "Makar Sankranti (til, gur, peanuts), Holi (colours, thandai), Eid (dates, sewai, meat), "
            "Christmas (cakes, decorations), Durga Puja (new clothes, sindoor, flowers). "
            "Bundle strategy: Slow item + popular item at combo price → moves more stock. "
            "Evening discount: Reduce perishable prices by 20% in last 2 hours — zero wastage. "
            "Morning premium: Fresh produce commands 10–15% premium before 9 AM. "
            "Loyalty punch card: Paper card — buy 10 get 1 free. Increases repeat visits by 40%. "
            "Festival pre-orders: Collect WhatsApp orders 3 days before festival — reduces uncertainty."
        ),
        "tags": ["pricing", "festival", "Diwali", "Navratri", "seasonal", "strategy",
                 "loyalty", "discount", "bundle", "marketing"],
        "language_hint": "en",
    },
    {
        "id": "engage_02",
        "category": "Customer Engagement",
        "title": "QR Code Poster & Printed Materials for Stall Branding",
        "content": (
            "Stall branding essentials for street vendors: "
            "QR code poster: Print A4 laminated sheet with UPI QR + vendor name + 'Scan to Pay' in local language. "
            "Cost: ₹20–₹30 at any print shop. Place at eye level, cover with transparent sheet for durability. "
            "Price board: Chalkboard or flex banner with top 5 products and prices — attracts walk-ins. "
            "Visiting card: Simple card with name, stall location, phone, WhatsApp, UPI ID. ₹200 for 100 cards. "
            "Festival banner: Seasonal 'Happy Diwali / Eid Mubarak' banner with your stall name — ₹150–₹300. "
            "Tip: Include your Google Maps link (short URL) on visiting card so customers can find you again."
        ),
        "tags": ["QR code", "poster", "branding", "visiting card", "price board", "print",
                 "stall", "marketing materials"],
        "language_hint": "en",
    },

    # ── CITY-SPECIFIC DATA ────────────────────────────────────────────────────

    {
        "id": "city_pune",
        "category": "City Data",
        "title": "Digital Resources for Street Vendors in Pune",
        "content": (
            "Pune Municipal Corporation (PMC) vendor registration: pmc.gov.in → Street Vendor section. "
            "High-footfall vendor zones: Camp, FC Road, JM Road, Laxmi Road, Deccan Gymkhana, Kothrud, Hadapsar. "
            "ULB for vending certificate: PMC Ward Office (nearest). "
            "Active delivery platforms in Pune: Swiggy, Zomato, Blinkit, Zepto, Dunzo. "
            "Local business communities: Pune Merchants Association, Camp Vyapari Mandal. "
            "Key SEO keywords for Pune vendors: 'sabzi mandi Camp Pune', 'fresh fruit FC Road', "
            "'street food Deccan Pune', 'vendor near me Pune'. "
            "CSC centres in Pune: 50+ across all wards for digital assistance."
        ),
        "tags": ["Pune", "PMC", "Camp", "FC Road", "JM Road", "Laxmi Road", "Maharashtra",
                 "Pune vendor", "Pune market"],
        "language_hint": "en",
    },
    {
        "id": "city_mumbai",
        "category": "City Data",
        "title": "Digital Resources for Street Vendors in Mumbai",
        "content": (
            "MCGM/BMC vendor registration: mcgm.gov.in → Online Services → Street Vendor Registration. "
            "High-footfall zones: Dharavi, Dadar, Crawford Market, Kurla, Andheri, Bandra, Borivali, Thane. "
            "Dharavi: MSME cluster with manufacturing + retail — dedicated credit facilitation centre. "
            "Active platforms: Swiggy, Zomato, Blinkit, BigBasket Now, Dunzo, Zepto. "
            "Key SEO: 'vada pav stall Dadar', 'flower vendor Crawford Market Mumbai', "
            "'sabzi vendor Dharavi Mumbai'. "
            "Local train station zones (high footfall): Dadar, CST, Andheri, Borivali — premium stall spots."
        ),
        "tags": ["Mumbai", "Dharavi", "Dadar", "Crawford Market", "MCGM", "BMC",
                 "Maharashtra", "Mumbai vendor", "Mumbai market"],
        "language_hint": "en",
    },
    {
        "id": "city_chennai",
        "category": "City Data",
        "title": "Digital Resources for Street Vendors in Chennai",
        "content": (
            "GCC (Greater Chennai Corporation) vendor registration: chennaicorporation.gov.in. "
            "High-footfall zones: T. Nagar, Sowcarpet, Koyambedu, Anna Nagar, Mylapore, Triplicane. "
            "Koyambedu wholesale market: largest fruit/vegetable market in South India — vendor support available. "
            "Tamil Nadu MSME portal: msmeonline.tn.gov.in | TIDCO for cluster support. "
            "Active platforms: Swiggy, Zomato, Blinkit, Dunzo, BB Daily. "
            "Key SEO (Tamil): 'T. Nagar கடை', 'Koyambedu காய்கறி', 'Chennai idli vendor near me'. "
            "Language: Tamil support available in PhonePe, Paytm, Google Pay, BHIM."
        ),
        "tags": ["Chennai", "T. Nagar", "Koyambedu", "Sowcarpet", "GCC", "Tamil Nadu",
                 "Tamil", "Chennai vendor", "South India"],
        "language_hint": "ta",
    },
    {
        "id": "city_bangalore",
        "category": "City Data",
        "title": "Digital Resources for Street Vendors in Bangalore",
        "content": (
            "BBMP vendor registration: bbmp.gov.in → Street Vendor Registration. "
            "High-footfall zones: Koramangala, Indiranagar, Jayanagar, Malleshwaram, Chickpet, KR Market. "
            "KR Market (Krishnarajendra): largest wholesale market — 2000+ vendors, strong community. "
            "Active platforms: Swiggy, Zomato, Blinkit, Zepto, Dunzo, BigBasket. "
            "Bangalore tech crowd: Open to online ordering, digital payments, QR codes. "
            "Key SEO (Kannada/English): 'flower vendor MG Road Bangalore', "
            "'Koramangala fruit stall near me', 'KR Market vegetable vendor'. "
            "Kannada language support: PhonePe, Paytm, BHIM all support Kannada."
        ),
        "tags": ["Bangalore", "Bengaluru", "BBMP", "KR Market", "Koramangala", "Indiranagar",
                 "Karnataka", "Kannada", "Bangalore vendor"],
        "language_hint": "kn",
    },
    {
        "id": "city_surat",
        "category": "City Data",
        "title": "Digital Resources for Street Vendors in Surat",
        "content": (
            "SMC (Surat Municipal Corporation) vendor registration: suratmunicipal.org. "
            "Surat is India's textile hub — thousands of cloth/saree/fashion vendors. "
            "High-footfall zones: Ring Road, Rustam Darwaja, Udhna, Varachha, Katargam. "
            "Textile market platforms: Meesho, GlowRoad, IndiaMART, TradeIndia for B2B. "
            "Surat Diamond Bourse area: premium buyer footfall. "
            "Active platforms: Swiggy, Zomato, Blinkit. "
            "Gujarati language support: PhonePe, Paytm, BHIM, Google Pay all support Gujarati. "
            "Key SEO (Gujarati): 'Surat saree vendor', 'Ring Road kapda dukaan', 'Surat textile near me'."
        ),
        "tags": ["Surat", "SMC", "textile", "saree", "Gujarat", "Gujarati", "Ring Road",
                 "cloth market", "Surat vendor"],
        "language_hint": "gu",
    },
    {
        "id": "city_delhi",
        "category": "City Data",
        "title": "Digital Resources for Street Vendors in Delhi / NCR",
        "content": (
            "NDMC / SDMC / EDMC vendor registration: apply at respective zonal offices. "
            "High-footfall zones: Chandni Chowk, Sarojini Nagar, Lajpat Nagar, Karol Bagh, Palika Bazar. "
            "Chandni Chowk: wholesale hub for electronics, clothing, spices, dry fruits — 50,000+ vendors. "
            "Active platforms: Swiggy, Zomato, Blinkit, Zepto, BigBasket Now, Dunzo. "
            "Delhi Govt: 'Dilli Bazaar' app for local vendor discovery (DUSIB). "
            "Key SEO: 'Chandni Chowk dry fruits vendor', 'Sarojini Nagar clothes stall', "
            "'Karol Bagh saree near me'. "
            "Hindi language: All UPI apps fully support Hindi UI."
        ),
        "tags": ["Delhi", "Chandni Chowk", "Sarojini Nagar", "Karol Bagh", "NCR", "Hindi",
                 "NDMC", "SDMC", "Delhi vendor"],
        "language_hint": "hi",
    },
]


def get_all_documents() -> list[dict]:
    return DOCUMENTS


def get_text_for_embedding(doc: dict) -> str:
    """Combine title + content + tags for richer embedding."""
    tag_str = ", ".join(doc.get("tags", []))
    return f"{doc['title']}. {doc['content']} Keywords: {tag_str}"


def get_all_chunks() -> list[tuple[str, dict]]:
    """Returns [(embed_text, doc_metadata), ...] for all documents."""
    return [(get_text_for_embedding(d), d) for d in DOCUMENTS]
