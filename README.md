# Street Vendor Digitalization Agent (SVDA)

> **AICTE-IBM SkillsBuild Internship 2026 — Problem Statement No. 29**
>
> An AI-powered RAG (Retrieval-Augmented Generation) agent that transforms India's 5 crore informal street vendors into digitally visible businesses — UPI, MSME credit, Google listing, QR codes & promotional materials in 22+ Indian languages. Powered by IBM watsonx.ai Granite models.

---

## Live Demo

**[Launch the Agent →](/agent)** | **[View Dashboard →](/dashboard)**

---

## Features

### Core AI Agent
- **RAG-Powered Chat** — Ask anything about going digital in English, Hindi, Marathi, Tamil, Telugu, Kannada, Bengali, or Gujarati
- **Digital Kit Generator** — Get a complete digital transformation plan with UPI setup, government schemes, SEO tips, and a printable QR business card
- **Voice Input** — Speak your query in any Indian language (Web Speech API)
- **PM SVANidhi Eligibility Checker** — Quick eligibility assessment for government loans

### Interactive Tools
- **Vendor Map** — Interactive Leaflet.js map showing registered vendors across India
- **Analytics Dashboard** — Real-time charts: vendors by city, business type, UPI adoption
- **Demand Forecasting** — 7-day demand prediction with seasonal/festival adjustments
- **QR Business Card Generator** — Indian-aesthetic styled QR code and business card PNGs

### Technical
- **ChromaDB Vector Store** — Persistent cosine similarity search for 21+ knowledge documents
- **IBM Granite Models** — granite-4-h-small (generation) + granite-embedding-278m-multilingual (embeddings)
- **PWA Support** — Offline caching via Service Worker + IndexedDB
- **FastAPI Backend** — Async Python with Pydantic validation
- **Docker Ready** — Dockerfile + docker-compose.yml for one-command deployment

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11 + FastAPI |
| AI Generation | IBM Granite 4 H Small (`ibm/granite-4-h-small`) |
| AI Embeddings | IBM Granite Embedding 278M Multilingual |
| Vector Store | ChromaDB (HNSW cosine index) |
| Frontend | HTML5 + CSS3 + Vanilla JavaScript |
| Maps | Leaflet.js + OpenStreetMap |
| Charts | Chart.js |
| Voice | Web Speech API |
| Offline | Service Worker + IndexedDB |
| Deployment | Docker + Render.com / Railway |

---

## Project Structure

```
svda/
├── backend/
│   ├── main.py              # FastAPI app + all routes
│   ├── models.py             # Pydantic request/response schemas
│   ├── ibm_client.py         # IBM watsonx.ai SDK wrapper
│   ├── knowledge_base.py     # 21 structured documents
│   ├── rag_pipeline.py       # ChromaDB RAG pipeline
│   ├── rag_query_cache.py    # LRU+TTL query cache
│   ├── qr_generator.py       # QR + business card generator
│   ├── geocoder.py           # Nominatim geocoding
│   ├── vendor_store.py       # Vendor registry + persistence
│   ├── forecast.py           # Demand forecasting module
│   └── scheme_checker.py     # PM SVANidhi eligibility
├── frontend/
│   ├── index.html            # Landing page (dark theme)
│   ├── agent.html            # AI chat + digital kit UI
│   ├── dashboard.html        # Analytics dashboard
│   ├── css/                  # Design system + components
│   ├── js/                   # Chat, map, voice, offline, etc.
│   ├── manifest.json         # PWA manifest
│   └── service-worker.js     # Offline caching
├── tests/                    # pytest test suite
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Clone & Install

```bash
git clone <repo-url>
cd svda
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your IBM watsonx.ai credentials
```

### 3. Run

```bash
# Development
python run_server.py

# Or directly
uvicorn backend.main:app --reload --port 8000
```

### 4. Docker (One Command)

```bash
docker-compose up --build
```

Open **http://localhost:8000**

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Landing page |
| GET | `/agent` | AI chat interface |
| GET | `/dashboard` | Analytics dashboard |
| POST | `/api/query` | RAG query → answer + sources |
| POST | `/api/generate-kit` | Full digital kit with QR card |
| POST | `/api/qr` | Generate UPI QR code |
| GET | `/api/geocode` | Location geocoding |
| GET | `/api/vendors` | List all vendors |
| POST | `/api/vendors` | Register new vendor |
| GET | `/api/analytics` | Dashboard statistics |
| GET | `/api/forecast` | Demand forecast |
| POST | `/api/scheme-check` | PM SVANidhi eligibility |
| GET | `/api/health` | System health check |
| POST | `/api/build-index` | Rebuild vector index |

---

## Knowledge Base

21 structured documents across 6 categories:
- **Government Schemes** — PM SVANidhi, MSME Udyam, Mudra, FSSAI, Digital India, e-Shram
- **UPI Setup** — PhonePe, Paytm, Google Pay, BHIM step-by-step guides
- **Online Listings** — Google Maps, Swiggy/Zomato, Meesho/GlowRoad, WhatsApp Business
- **Local SEO** — Hyperlocal SEO strategy for Indian vendors
- **Customer Engagement** — Festival pricing, QR branding, loyalty programs
- **City Data** — Pune, Mumbai, Chennai, Bangalore, Surat, Delhi/NCR

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Impact

| Metric | Value |
|--------|-------|
| Street vendors in India | 5 Crore+ |
| Currently undigitized | ~95% |
| Languages supported | 22+ |
| Government schemes covered | 6 |
| Cities with specific data | 6 |

---

## License

AICTE-IBM SkillsBuild Internship 2026

---

*Built with IBM watsonx.ai Granite models + ChromaDB RAG pipeline*
