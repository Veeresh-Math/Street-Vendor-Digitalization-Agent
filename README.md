# Street Vendor Digitalization Agent
## AICTE-IBM SkillsBuild Internship 2026 — Problem Statement No. 29

---

### Tech Stack
| Layer | Technology |
|---|---|
| Backend | Python 3.11 · FastAPI · Uvicorn |
| AI — Generation | `ibm/granite-4-h-small` via `ibm-watsonx-ai` SDK |
| AI — Embeddings | `ibm/granite-embedding-278m-multilingual` via `ibm-watsonx-ai` SDK |
| Vector Store | ChromaDB (local persistent) |
| QR / Business Card | `qrcode` + `Pillow` (non-AI) |
| Geocoding | OpenStreetMap Nominatim (free, no key) |
| Frontend | Pure HTML5 + CSS3 + Vanilla JS (no React, no Streamlit) |

---

### Project Structure
```
├── backend/
│   ├── main.py            FastAPI app — all routes + static file serving
│   ├── ibm_client.py      IBM watsonx-ai SDK wrapper (token, embed, generate)
│   ├── rag_pipeline.py    ChromaDB index + cosine retrieval + prompt builder
│   ├── knowledge_base.py  20+ real-world documents (schemes, UPI, SEO, cities)
│   ├── qr_generator.py    QR PNG + business card generator (Pillow)
│   ├── geocoder.py        OpenStreetMap Nominatim geocoding
│   └── models.py          Pydantic request/response schemas
├── vector_store/          ChromaDB persistent storage (auto-created)
├── frontend/
│   ├── index.html         Landing page (Indian street-market aesthetic)
│   ├── agent.html         Live AI chat + torn-receipt digital kit
│   ├── css/
│   │   ├── theme.css      Colour vars, typography, kraft-paper texture
│   │   ├── layout.css     Nav, grid, stats band, footer
│   │   └── components.css Cards, chat bubbles, torn receipt, pipeline steps
│   └── js/
│       ├── chat.js        Chat UI → POST /api/query
│       ├── kit.js         Digital kit → POST /api/generate-kit + receipt render
│       └── geo.js         Browser geolocation → /api/geocode
├── static/generated/      Generated QR PNGs and business card images
├── requirements.txt
└── README.md
```

---

### Setup & Run

#### 1. Install dependencies
- **API Docs:**     http://localhost:8000/docs

---

## Deploy (GitHub Container + Docker)
This repo is a **FastAPI** server (not static-only), so GitHub Actions builds a Docker image and pushes it to **GHCR**.

### 1) GitHub secret
In your GitHub repo settings → **Secrets and variables → Actions** add:
- `GHCR_PAT` : a GitHub token with permission to write packages (GHCR).

### 2) Push to GitHub
- Ensure your default branch is `main`.
- Any push to `main` triggers `.github/workflows/build-and-push.yml`.

### 3) Run the image (example)
After pushing, you can run the container on any Docker-capable host:
```bash
docker run -p 8000:8000 \
  -e IBM_PROJECT_ID="..." \
  -e IBM_REGION="..." \
  -e IBM_API_KEY="..." \
  ghcr.io/<your-username>/<your-repo>:<tag>
```

> Note: Your backend may read credentials from environment variables (or `.env` during local runs). Do not commit secrets.


---

### API Endpoints
| Method | Path | Description |
|---|---|---|
| GET | `/` | Landing page |
| GET | `/agent` | Live agent chat + digital kit page |
| POST | `/api/query` | RAG query → answer + sources |
| POST | `/api/generate-kit` | Full digital kit + QR business card |
| POST | `/api/qr` | Generate UPI QR PNG |
| GET | `/api/geocode?q=Camp+Pune` | Nominatim geocoding |
| POST | `/api/build-index` | (Re)build ChromaDB index |
| GET | `/api/health` | IBM connection + index status |

---

### IBM Models Used
- **Generation:** `ibm/granite-4-h-small`
- **Embeddings:** `ibm/granite-embedding-278m-multilingual`
- **Project ID:** `59f569dc-3371-40a4-a6dc-0d6242c0745e`
- **Region:** US-South (Dallas)

---

### Knowledge Base Coverage
20+ real-world documents:
- PM SVANidhi, Mudra Yojana, MSME Udyam, FSSAI, e-Shram, Digital India
- PhonePe, Paytm, Google Pay, BHIM UPI setup
- Swiggy Instamart, Blinkit, Zomato, Meesho, GlowRoad, WhatsApp Business
- Hyperlocal SEO strategy, seasonal pricing, QR/branding
- City data: Pune, Mumbai, Chennai, Bangalore, Surat, Delhi
