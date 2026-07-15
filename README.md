<div align="center">

# 🇮🇳 Street Vendor Digitalization Agent

### *Empowering 5 Crore Street Vendors with AI*

**AICTE-IBM SkillsBuild Internship 2026 — Problem Statement No. 29**
*In association with Edunet Foundation*

An AI-powered multilingual agent that transforms India's street vendors into digitally visible businesses through intelligent consultation, government scheme navigation, and digital tool generation.

---

[![Frontend](https://img.shields.io/badge/Frontend-Netlify-00C7B7?style=for-the-badge&logo=netlify&logoColor=white)](https://street-vendor-agent.netlify.app)
[![Backend](https://img.shields.io/badge/Backend-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://street-vendor-digitalization-agent-isog.onrender.com)
[![AI](https://img.shields.io/badge/AI-IBM%20watsonx.ai-054ADA?style=for-the-badge&logo=ibm&logoColor=white)](https://cloud.ibm.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

---

## 🚀 [Launch Application](https://street-vendor-agent.netlify.app/agent) | 📊 [View Dashboard](https://street-vendor-agent.netlify.app/dashboard)

</div>

---

## 📋 Table of Contents

- [What It Does](#-what-it-does)
- [Core Features](#-core-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Knowledge Base](#-knowledge-base)
- [Languages Supported](#-languages-supported)
- [Quick Start](#-quick-start)
- [Security](#-security)
- [Token Economics](#-token-economics)
- [Impact](#-impact)

---

## 🎯 What It Does

India's **5 crore street vendors** are excluded from the digital economy due to:
- 🗣️ **Language barriers** — Limited English proficiency
- 📚 **Fragmented information** — Scattered across multiple sources
- 🏛️ **Complex government processes** — Difficult scheme navigation

**Our solution:** A single integrated platform addressing all digitalization needs through natural conversation in **8 Indian languages**.

---

## ✨ Core Features

<table>
<tr>
<td width="50%">

### 🤖 AI-Powered Multilingual Consultation
Ask anything about going digital — UPI setup, government schemes, Google listing, SEO tips — and receive personalized answers in your language.

**Powered by:** IBM Llama 3.3 70B Instruct with RAG pipeline

</td>
<td width="50%">

### 📦 Digital Kit Generator
Get a complete digital transformation package: vendor profile, UPI guide, government schemes, SEO tips, and a styled QR business card ready for printing.

</td>
</tr>
<tr>
<td>

### 🗺️ Interactive Vendor Map
Leaflet.js-powered map showing registered vendors across 6 Indian cities with geolocation, city filtering, and business type filtering.

</td>
<td>

### ✅ PM SVANidhi Eligibility Checker
Quick eligibility assessment for government working capital loans based on CoV, LoR, and vendor status.

</td>
</tr>
<tr>
<td>

### 📈 Demand Forecasting
7-day demand prediction across product categories with trend analysis and seasonal adjustments.

</td>
<td>

### 📊 Analytics Dashboard
Real-time charts: city-wise distribution, business type breakdown, UPI adoption rates.

</td>
</tr>
<tr>
<td>

### 🎤 Voice Input
Speak your query in any supported language using Web Speech API — no typing required.

</td>
<td>

### 🔒 Enterprise Security
Rate limiting, XSS protection, input sanitization, CORS configuration, security headers.

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Frontend      │────▶│    Backend      │────▶│    IBM AI       │
│    (Netlify)     │     │    (Render)     │     │    (watsonx)    │
│                  │     │                  │     │                  │
│  🎨 HTML5/CSS3   │     │  ⚡ FastAPI      │     │  🧠 Llama 3.3   │
│  🗺️ Leaflet.js   │     │  💾 ChromaDB     │     │  📐 e5-large    │
│  📊 Chart.js     │     │  🐍 Python 3.11  │     │  🌏 Sydney      │
│  📱 PWA Ready    │     │  🐳 Docker       │     │                  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 🔄 Request Flow

```
👤 User Query
    │
    ▼
🔍 Language Detection ──▶ 📋 Cache Check ──▶ ✅ Return Cached (0 tokens)
    │ MISS
    ▼
📄 Document Retrieval ──▶ ✍️ Prompt Construction ──▶ 🤖 AI Generation
    │
    ▼
💾 Cache & Return ──▶ 👤 Response
```

### ⚡ Token Optimization (3-Tier Caching)

| Tier | Mechanism | Token Cost | Savings |
|------|-----------|------------|---------|
| 🥇 | Demo response cache (pre-computed, 8 languages) | **Zero** | 100% |
| 🥈 | Query result cache (TTL-based LRU, 1000 entries) | **Zero** | 100% |
| 🥉 | Fresh RAG pipeline (embed + retrieve + generate) | **~45 tokens** | Baseline |

> 💡 **Result:** 70-80% reduction in API consumption vs naive RAG implementations

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| 🎨 **Frontend** | HTML5, CSS3, JavaScript (ES6+) | Zero-framework PWA |
| 🗺️ **Mapping** | Leaflet.js + OpenStreetMap | Vendor geolocation |
| 📊 **Charts** | Chart.js | Analytics visualization |
| 🎤 **Voice** | Web Speech API | Multilingual voice input |
| ⚡ **Backend** | Python 3.11 + FastAPI | REST API server |
| ✅ **Validation** | Pydantic 2.x | Request/response schemas |
| 💾 **Vector DB** | ChromaDB (HNSW cosine) | Document retrieval |
| 🧠 **AI Generation** | Llama 3.3 70B Instruct | Text generation |
| 📐 **AI Embeddings** | multilingual-e5-large | 384-dim multilingual vectors |
| ☁️ **AI Platform** | IBM watsonx.ai (Sydney) | Cloud AI services |
| 🌍 **Geocoding** | OpenStreetMap Nominatim | Location services |
| 🌐 **Frontend Host** | Netlify | CDN + SSL |
| ⚙️ **Backend Host** | Render | API server |
| 🐳 **Container** | Docker | Deployment consistency |
| 🔄 **CI/CD** | GitHub | Auto-deploy on push |

---

## 📁 Project Structure

```
street-vendor-digitalization-agent/
├── 🐍 backend/
│   ├── main.py              # FastAPI app + 27 API routes
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
├── 🎨 frontend/
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
├── 🧪 tests/                # 62 unit tests (pytest)
├── 📁 static/generated/     # QR code output directory
├── 💾 vector_store/         # ChromaDB persistent storage
├── 🐳 Dockerfile            # Python 3.11-slim container
├── 🐳 docker-compose.yml    # One-command deployment
├── ⚙️ render.yaml           # Render deployment config
├── 🌐 netlify.toml          # Netlify deployment config
├── 📋 requirements.txt      # Python dependencies
└── 📖 README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| 🟢 | `POST /api/query` | RAG-based multilingual Q&A |
| 🟢 | `POST /api/generate-kit` | Digital kit with QR business card |
| 🟢 | `POST /api/qr` | UPI QR code generation |
| 🔵 | `GET /api/vendors` | List registered vendors |
| 🟢 | `POST /api/vendors` | Register new vendor |
| 🔵 | `GET /api/analytics` | Dashboard statistics |
| 🔵 | `GET /api/forecast` | 7-day demand forecast |
| 🟢 | `POST /api/scheme-check` | PM SVANidhi eligibility |
| 🔵 | `GET /api/schemes` | Government schemes list |
| 🔵 | `GET /api/geocode` | Location geocoding |
| 🔵 | `GET /api/cities` | Supported cities |
| 🔵 | `GET /api/recommendations` | Personalized recommendations |
| 🔵 | `GET /api/health` | System health status |
| 🔵 | `GET /api/monitoring/tokens` | Token usage statistics |
| 🟢 | `POST /api/build-index` | Rebuild vector index |

> 🟢 = POST | 🔵 = GET

---

## 📚 Knowledge Base

**24 curated documents** across 6 categories:

| Category | 📄 Docs | Coverage |
|----------|---------|----------|
| 🏛️ Government Schemes | 6 | PM SVANidhi, MSME Udyam, Mudra, FSSAI, e-Shram, Digital India |
| 💳 UPI Setup | 4 | PhonePe, Paytm, Google Pay, BHIM step-by-step guides |
| 🌐 Online Listing | 5 | Google Business, Swiggy/Zomato, Meesho/GlowRoad, WhatsApp Business |
| 🔍 Local SEO | 1 | Hyperlocal SEO strategy for Indian vendors |
| 🤝 Customer Engagement | 2 | Festival pricing, QR branding, loyalty programs |
| 🏙️ City Data | 6 | Pune, Mumbai, Chennai, Bangalore, Surat, Delhi |

---

## 🗣️ Languages Supported

| Language | Code | Script |
|----------|------|--------|
| 🇬🇧 English | `en` | Latin |
| 🇮🇳 Hindi | `hi` | Devanagari |
| 🇮🇳 Marathi | `mr` | Devanagari |
| 🇮🇳 Tamil | `ta` | Tamil |
| 🇮🇳 Telugu | `te` | Telugu |
| 🇮🇳 Kannada | `kn` | Kannada |
| 🇮🇳 Gujarati | `gu` | Gujarati |
| 🇮🇳 Bengali | `bn` | Bengali |

---

## 🚀 Quick Start

### 📦 Local Development

```bash
# Clone the repository
git clone https://github.com/Veeresh-Math/Street-Vendor-Digitalization-Agent.git
cd Street-Vendor-Digitalization-Agent

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your IBM watsonx.ai credentials

# Run the application
uvicorn backend.main:app --reload --port 8000
```

### 🐳 Docker Deployment

```bash
docker-compose up --build
```

Open **https://street-vendor-agent.netlify.app** 🎉

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

✅ **62 unit tests** covering:
- API endpoints
- RAG pipeline
- QR generation
- Vendor management
- Forecasting
- Scheme checker
- Geocoding
- Monitoring

---

## 🔒 Security

| Feature | Implementation |
|---------|---------------|
| 🚦 Rate Limiting | 30 requests/minute per IP |
| 🛡️ XSS Protection | HTML entity escaping on all inputs |
| ✅ Input Sanitization | Pydantic validators + regex UPI validation |
| 🔐 CORS | Controlled cross-origin access |
| 📋 Security Headers | X-Frame-Options, X-Content-Type-Options, X-XSS-Protection |

---

## 💰 Token Economics

| Metric | Value |
|--------|-------|
| 📊 Daily embed limit | 5,000 tokens |
| 📊 Daily generation limit | 10,000 tokens |
| 💵 Embed cost per query | ~15 tokens |
| 💵 Generation cost per query | ~30 tokens |
| 🔄 Index rebuild cost | ~2,400 tokens |
| 📈 Queries per day | ~170 |

---

## 📊 Impact

<div align="center">

| 🏷️ Metric | 📈 Value |
|-----------|----------|
| 🏪 Street vendors in India | **5 Crore+** |
| 🗣️ Languages supported | **8** |
| 🏛️ Government schemes covered | **6** |
| 🏙️ Cities with specific data | **6** |
| 📚 Knowledge documents | **24** |
| 🔌 API endpoints | **27** |
| 🧪 Unit tests | **62** |

</div>

---

## 🏆 Key Achievements

- ✅ **70-80% token savings** through 3-tier caching strategy
- ✅ **8 Indian languages** with native script support
- ✅ **Zero-framework frontend** — loads on 3G connections
- ✅ **Self-healing index** — auto-rebuilds on dimension mismatch
- ✅ **Production-ready security** at prototype stage
- ✅ **Split-deployment** optimizing cost across cloud platforms

---

## 📄 License

**AICTE-IBM SkillsBuild Internship 2026**

---

<div align="center">

### 🙏 Built with ❤️ for India's Street Vendors

**Powered by:** IBM watsonx.ai Llama 3.3 70B + multilingual-e5-large + ChromaDB RAG pipeline

![Built with Python](https://img.shields.io/badge/Built%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Powered by IBM](https://img.shields.io/badge/Powered%20by-IBM%20watsonx-054ADA?style=for-the-badge&logo=ibm&logoColor=white)

</div>
