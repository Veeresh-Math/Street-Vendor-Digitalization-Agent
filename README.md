# Street Vendor Digitalization Agent

> **AICTE-IBM SkillsBuild Internship 2026 — Problem Statement No. 29**
>
> An AI-powered multilingual agent that transforms India's 5 crore street vendors into digitally visible businesses through intelligent consultation, government scheme navigation, and digital tool generation.

---

## Live Deployment

| Component | Platform | Status |
|-----------|----------|--------|
| Frontend | Netlify | Deployed |
| Backend API | Render | Deployed |
| AI Engine | IBM watsonx.ai (Sydney) | Connected |

**[Launch Application →](/agent)** | **[View Dashboard →](/dashboard)**

---

## What It Does

The Street Vendor Digitalization Agent solves a critical problem: India's 5 crore street vendors are excluded from the digital economy due to language barriers, fragmented information, and complex government processes. Our system provides a single integrated platform addressing all digitalization needs through natural language conversation in 8 Indian languages.

---

## Core Features

### AI-Powered Multilingual Consultation
Ask anything about going digital — UPI setup, government schemes, Google listing, SEO tips — and receive personalized answers in English, Hindi, Marathi, Tamil, Telugu, Kannada, Gujarati, or Bengali. Powered by IBM Llama 3.3 70B Instruct with RAG pipeline ensuring accurate, domain-specific responses.

### Digital Kit Generator
Enter your business details and receive a complete digital transformation package: vendor profile summary, UPI setup guide, applicable government schemes, local SEO recommendations, and a styled QR business card ready for printing.

### Interactive Vendor Map
Leaflet.js-powered map displaying registered vendors across 6 Indian cities (Pune, Mumbai, Chennai, Bangalore, Surat, Delhi) with real-time geolocation, city filtering, and business type filtering.

### PM SVANidhi Eligibility Checker
Quick eligibility assessment for the government's working capital loan scheme based on Certificate of Vending, Letter of Recommendation, and food vendor status.

### Demand Forecasting
7-day demand prediction across product categories with trend analysis and seasonal adjustments for inventory planning.

### Analytics Dashboard
Real-time visualization of vendor statistics — city-wise distribution, business type breakdown, UPI adoption rates, and recent registrations.

### Voice Input
Speak your query in any supported language using Web Speech API — no typing required.

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Frontend      │────▶│    Backend      │────▶│    IBM AI       │
│    (Netlify)     │     │    (Render)     │     │    (watsonx)    │
│                  │     │                  │     │                  │
│  HTML5/CSS3/JS   │     │  FastAPI         │     │  Llama 3.3 70B  │
│  Leaflet.js      │     │  ChromaDB        │     │  e5-large       │
│  Chart.js        │     │  Python 3.11     │     │  Sydney Region  │
│  Service Worker  │     │  Docker          │     │                  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Request Flow

```
User Query → Language Detection → Cache Check → Document Retrieval →
Prompt Construction → AI Generation → Response Caching → User
```

### Token Optimization (3-Tier Caching)

| Tier | Mechanism | Token Cost |
|------|-----------|------------|
| 1 | Demo response cache (pre-computed, 8 languages) | Zero |
| 2 | Query result cache (TTL-based LRU, 1000 entries) | Zero |
| 3 | Fresh RAG pipeline (embed + retrieve + generate) | ~45 tokens |

This hierarchical approach reduces API consumption by 70-80% compared to naive RAG implementations.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | HTML5, CSS3, JavaScript (ES6+) | Zero-framework PWA |
| Mapping | Leaflet.js + OpenStreetMap | Vendor geolocation |
| Charts | Chart.js | Analytics visualization |
| Voice | Web Speech API | Multilingual voice input |
| Backend | Python 3.11 + FastAPI | REST API server |
| Validation | Pydantic 2.x | Request/response schemas |
| Vector DB | ChromaDB (HNSW cosine) | Document retrieval |
| AI Generation | Llama 3.3 70B Instruct | Text generation |
| AI Embeddings | multilingual-e5-large | 384-dim multilingual vectors |
| AI Platform | IBM watsonx.ai (Sydney) | Cloud AI services |
| Geocoding | OpenStreetMap Nominatim | Location services |
| Hosting | Netlify (frontend) | CDN + SSL |
| Hosting | Render (backend) | API server |
| Container | Docker | Deployment consistency |
| Version Control | GitHub | CI/CD with auto-deploy |

---

## Project Structure

```
street-vendor-digitalization-agent/
├── backend/
│   ├── main.py              # FastAPI app + 15 API endpoints
│   ├── models.py            # Pydantic request/response schemas
│   ├── ibm_client.py        # IBM watsonx.ai SDK client
│   ├── rag_pipeline.py      # RAG pipeline with 3-tier caching
│   ├── rag_query_cache.py   # TTL-based LRU query cache
│   ├── knowledge_base.py    # 24 structured domain documents
│   ├── demo_responses.py    # Pre-computed responses (8 languages)
│   ├── qr_generator.py      # QR code + business card generator
│   ├── geocoder.py          # OpenStreetMap geocoding
│   ├── vendor_store.py      # Vendor registry + JSON persistence
│   ├── forecast.py          # Demand forecasting module
│   ├── scheme_checker.py    # PM SVANidhi eligibility logic
│   ├── monitoring.py        # Request logging middleware
│   └── .env                 # IBM credentials (gitignored)
├── frontend/
│   ├── index.html           # Landing page
│   ├── agent.html           # AI chat + digital kit interface
│   ├── dashboard.html       # Analytics dashboard
│   ├── css/                 # Design system + responsive styles
│   ├── js/
│   │   ├── chat.js          # Chat interface logic
│   │   ├── kit.js           # Digital kit generator
│   │   ├── vendor-map.js    # Leaflet.js vendor map
│   │   ├── dashboard.js     # Chart.js analytics
│   │   ├── voice.js         # Web Speech API voice input
│   │   ├── offline.js       # IndexedDB offline support
│   │   ├── scheme-checker.js # Eligibility checker
│   │   └── geo.js           # Geolocation helper
│   ├── manifest.json        # PWA manifest
│   └── service-worker.js    # Offline caching
├── tests/                   # 62 unit tests (pytest)
├── static/generated/        # QR code output directory
├── vector_store/            # ChromaDB persistent storage
├── Dockerfile               # Python 3.11-slim container
├── docker-compose.yml       # One-command deployment
├── render.yaml              # Render deployment config
├── netlify.toml             # Netlify deployment config
├── requirements.txt         # Python dependencies
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/query` | RAG-based multilingual Q&A |
| POST | `/api/generate-kit` | Digital kit with QR business card |
| POST | `/api/qr` | UPI QR code generation |
| GET | `/api/vendors` | List registered vendors |
| POST | `/api/vendors` | Register new vendor |
| GET | `/api/analytics` | Dashboard statistics |
| GET | `/api/forecast` | 7-day demand forecast |
| POST | `/api/scheme-check` | PM SVANidhi eligibility |
| GET | `/api/schemes` | Government schemes list |
| GET | `/api/geocode` | Location geocoding |
| GET | `/api/cities` | Supported cities |
| GET | `/api/recommendations` | Personalized recommendations |
| GET | `/api/health` | System health status |
| GET | `/api/monitoring/tokens` | Token usage statistics |
| POST | `/api/build-index` | Rebuild vector index |

---

## Knowledge Base

24 curated documents across 6 categories:

| Category | Documents | Coverage |
|----------|-----------|----------|
| Government Schemes | 6 | PM SVANidhi, MSME Udyam, Mudra, FSSAI, e-Shram, Digital India |
| UPI Setup | 4 | PhonePe, Paytm, Google Pay, BHIM step-by-step guides |
| Online Listing | 5 | Google Business, Swiggy/Zomato, Meesho/GlowRoad, WhatsApp Business |
| Local SEO | 1 | Hyperlocal SEO strategy for Indian vendors |
| Customer Engagement | 2 | Festival pricing, QR branding, loyalty programs |
| City Data | 6 | Pune, Mumbai, Chennai, Bangalore, Surat, Delhi |

---

## Languages Supported

| Language | Code | Status |
|----------|------|--------|
| English | en | Supported |
| Hindi | hi | Supported |
| Marathi | mr | Supported |
| Tamil | ta | Supported |
| Telugu | te | Supported |
| Kannada | kn | Supported |
| Gujarati | gu | Supported |
| Bengali | bn | Supported |

---

## Quick Start

### Local Development

```bash
git clone https://github.com/Veeresh-Math/Street-Vendor-Digitalization-Agent.git
cd Street-Vendor-Digitalization-Agent
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your IBM watsonx.ai credentials
uvicorn backend.main:app --reload --port 8000
```

### Docker Deployment

```bash
docker-compose up --build
```

Open **http://localhost:8000**

---

## Running Tests

```bash
pytest tests/ -v
```

**62 unit tests** covering API endpoints, RAG pipeline, QR generation, vendor management, and system health.

---

## Security

- **Rate Limiting**: 30 requests per minute per IP
- **XSS Protection**: HTML entity escaping on all inputs
- **Input Sanitization**: Pydantic validators with regex UPI validation
- **CORS**: Controlled cross-origin access
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection

---

## Token Economics

| Metric | Value |
|--------|-------|
| Daily embed limit | 5,000 tokens |
| Daily generation limit | 10,000 tokens |
| Embed cost per query | ~15 tokens |
| Generation cost per query | ~30 tokens |
| Index rebuild cost | ~2,400 tokens |
| Queries per day (after rebuild) | ~170 |

---

## Impact

| Metric | Value |
|--------|-------|
| Street vendors in India | 5 Crore+ |
| Languages supported | 8 |
| Government schemes covered | 6 |
| Cities with specific data | 6 |
| Knowledge documents | 24 |
| API endpoints | 15 |
| Unit tests | 62 |

---

## License

AICTE-IBM SkillsBuild Internship 2026

---

*Built with IBM watsonx.ai Llama 3.3 70B + multilingual-e5-large + ChromaDB RAG pipeline*
