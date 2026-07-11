"""
Street Vendor Digitalization Agent — Streamlit App
Powered by IBM watsonx.ai (Edunet Internship Project)
  - Generation Model:  ibm/granite-4-h-small
  - Embedding Model:   ibm/granite-embedding-278m-multilingual
"""

import streamlit as st
import time
from rag_pipeline import build_index, answer_query, is_index_ready
from knowledge_base import KNOWLEDGE_BASE

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Street Vendor Digitalization Agent",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Import font */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

  /* Global */
  html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
    background-color: #04050a !important;
    color: #f0f2ff !important;
  }

  /* Hide Streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 2rem 2rem 4rem 2rem !important; max-width: 1200px !important; }

  /* ── HERO BANNER ── */
  .hero-banner {
    background: linear-gradient(135deg, #0d0f1a 0%, #131626 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 48px 48px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
  }
  .hero-banner::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #6c47ff, #00d4aa, #ff6b35);
  }
  .hero-title {
    font-size: 42px; font-weight: 900; letter-spacing: -1.5px;
    line-height: 1.1; margin: 0 0 12px 0;
    background: linear-gradient(135deg, #6c47ff, #00d4aa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }
  .hero-sub {
    font-size: 16px; color: #8b92b8; line-height: 1.7; max-width: 700px; margin: 0;
  }
  .hero-badges {
    display: flex; flex-wrap: wrap; gap: 10px; margin-top: 20px;
  }
  .hbadge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 14px; border-radius: 50px; font-size: 12px; font-weight: 700;
    border: 1px solid;
  }
  .hb-ibm { background: rgba(15,98,254,0.15); border-color: rgba(15,98,254,0.4); color: #74b1ff; }
  .hb-rag { background: rgba(108,71,255,0.15); border-color: rgba(108,71,255,0.4); color: #a78bfa; }
  .hb-edu { background: rgba(0,212,170,0.12); border-color: rgba(0,212,170,0.35); color: #34d399; }

  /* ── STATS ROW ── */
  .stats-row {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 16px; margin-bottom: 28px;
  }
  .stat-card {
    background: #0d0f1a; border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 20px 18px; text-align: center;
  }
  .stat-num {
    font-size: 32px; font-weight: 900; letter-spacing: -1px;
    background: linear-gradient(135deg, #6c47ff, #00d4aa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }
  .stat-lbl { color: #8b92b8; font-size: 12px; margin-top: 4px; }

  /* ── CHAT SECTION ── */
  .chat-header {
    background: #0d0f1a;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px 20px 0 0;
    padding: 16px 24px;
    display: flex; align-items: center; gap: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }
  .chat-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
  .chat-title { font-size: 13px; color: #8b92b8; font-weight: 600; flex: 1; text-align: center; }
  .model-pill {
    padding: 4px 10px; border-radius: 50px; font-size: 11px; font-weight: 700;
    background: rgba(15,98,254,0.15); border: 1px solid rgba(15,98,254,0.4); color: #74b1ff;
  }

  /* ── USER BUBBLE ── */
  .user-bubble {
    background: rgba(108,71,255,0.15);
    border: 1px solid rgba(108,71,255,0.3);
    border-radius: 18px 18px 4px 18px;
    padding: 14px 18px; color: #c4b5fd;
    font-size: 15px; margin: 0 0 16px auto;
    max-width: 80%; display: inline-block; float: right; clear: both;
  }

  /* ── AGENT BUBBLE ── */
  .agent-label {
    font-size: 11px; color: #00d4aa; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 8px; clear: both;
  }
  .agent-bubble {
    background: rgba(0,212,170,0.07);
    border: 1px solid rgba(0,212,170,0.2);
    border-radius: 4px 18px 18px 18px;
    padding: 16px 20px; color: #f0f2ff;
    font-size: 15px; line-height: 1.75;
    margin-bottom: 20px; clear: both;
  }

  /* ── RETRIEVED DOCS ── */
  .retrieved-section {
    margin-top: 16px; padding: 16px 20px;
    background: rgba(108,71,255,0.06);
    border: 1px solid rgba(108,71,255,0.2);
    border-radius: 12px;
  }
  .retrieved-title {
    font-size: 11px; font-weight: 800; color: #a78bfa;
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px;
  }
  .rdoc {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 13px;
  }
  .rdoc:last-child { border-bottom: none; }
  .rdoc-score {
    padding: 2px 8px; border-radius: 50px; font-size: 11px; font-weight: 700;
    background: rgba(0,212,170,0.12); color: #34d399; white-space: nowrap; flex-shrink: 0;
  }
  .rdoc-title { color: #f0f2ff; font-weight: 600; }
  .rdoc-cat { color: #8b92b8; font-size: 11px; }

  /* ── INPUT AREA ── */
  .stTextInput > div > div > input {
    background: #131626 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #f0f2ff !important;
    font-size: 15px !important;
    padding: 14px 16px !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: rgba(108,71,255,0.5) !important;
    box-shadow: 0 0 0 2px rgba(108,71,255,0.12) !important;
  }
  .stButton > button {
    background: linear-gradient(135deg, #6c47ff, #00d4aa) !important;
    color: white !important; font-weight: 700 !important;
    border: none !important; border-radius: 12px !important;
    padding: 14px 28px !important; font-size: 15px !important;
    width: 100% !important;
  }
  .stButton > button:hover { opacity: 0.9 !important; }

  /* ── SIDEBAR ── */
  [data-testid="stSidebar"] {
    background: #0d0f1a !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
  }
  [data-testid="stSidebar"] .stMarkdown { color: #f0f2ff !important; }

  /* ── IBM CONFIG CARD ── */
  .ibm-config-card {
    background: #04050a;
    border: 1px solid rgba(15,98,254,0.35);
    border-radius: 14px; padding: 18px 20px;
    position: relative; overflow: hidden;
    margin-bottom: 16px;
  }
  .ibm-config-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #0f62fe, #6c47ff, #00d4aa);
  }
  .config-label { font-size: 11px; font-weight: 800; letter-spacing: 0.07em; text-transform: uppercase; color: #8b92b8; margin-bottom: 5px; }
  .config-val { font-size: 12px; font-family: 'Courier New', monospace; color: #74b1ff; word-break: break-all; }
  .status-connected {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 12px; border-radius: 50px; font-size: 12px; font-weight: 700;
    background: rgba(0,212,170,0.12); border: 1px solid rgba(0,212,170,0.3); color: #34d399;
    margin-top: 12px;
  }

  /* ── MODEL CARD ── */
  .model-card {
    background: #04050a;
    border: 1px solid rgba(108,71,255,0.3);
    border-radius: 12px; padding: 14px 16px; margin-bottom: 10px;
  }
  .model-role { font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }
  .role-gen { color: #00d4aa; }
  .role-emb { color: #a78bfa; }
  .model-name { font-size: 12px; font-family: 'Courier New', monospace; color: #f0f2ff; font-weight: 700; }
  .model-desc { font-size: 11px; color: #8b92b8; margin-top: 4px; line-height: 1.5; }

  /* ── SAMPLE QUERIES ── */
  .sample-query {
    background: #0d0f1a; border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px; padding: 10px 14px;
    font-size: 13px; color: #8b92b8; cursor: pointer;
    margin-bottom: 8px;
  }

  /* ── PIPELINE DISPLAY ── */
  .pipeline-step {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px; border-radius: 10px;
    margin-bottom: 8px; font-size: 13px;
  }
  .ps-active { background: rgba(0,212,170,0.1); border: 1px solid rgba(0,212,170,0.3); color: #34d399; }
  .ps-done   { background: rgba(108,71,255,0.08); border: 1px solid rgba(108,71,255,0.2); color: #a78bfa; }
  .ps-wait   { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); color: #8b92b8; }

  /* ── EXAMPLE TAGS ── */
  .etag {
    display: inline-block; padding: 5px 12px; border-radius: 50px; font-size: 12px;
    font-weight: 700; border: 1px solid; margin: 3px;
  }
  .et-purple { background: rgba(108,71,255,0.15); border-color: rgba(108,71,255,0.4); color: #a78bfa; }
  .et-teal   { background: rgba(0,212,170,0.12); border-color: rgba(0,212,170,0.4); color: #34d399; }
  .et-orange { background: rgba(255,107,53,0.12); border-color: rgba(255,107,53,0.4); color: #fb923c; }

  /* Expander */
  .streamlit-expanderHeader { color: #8b92b8 !important; font-size: 13px !important; }
  .streamlit-expanderContent { border-color: rgba(255,255,255,0.08) !important; }

  /* Divider */
  hr { border-color: rgba(255,255,255,0.08) !important; }

  /* Spinner */
  .stSpinner > div { border-top-color: #6c47ff !important; }
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "chat_history"   not in st.session_state: st.session_state.chat_history   = []
if "index_built"    not in st.session_state: st.session_state.index_built    = False
if "index_building" not in st.session_state: st.session_state.index_building = False
if "build_log"      not in st.session_state: st.session_state.build_log      = []

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛒 Street Vendor<br/>Digitalization Agent", unsafe_allow_html=True)
    st.markdown("<hr/>", unsafe_allow_html=True)

    # IBM Config Card
    st.markdown("""
    <div class="ibm-config-card">
      <div class="config-label">IBM watsonx.ai</div>
      <div style="margin-bottom:12px;">
        <div class="config-label" style="margin-top:10px;">API Key</div>
        <div class="config-val">36yHNYbA0Yj•••••••olv</div>
      </div>
      <div>
        <div class="config-label">Project ID</div>
        <div class="config-val">59f569dc-3371-40a4-a6dc-0d6242c0745e</div>
      </div>
      <div class="status-connected">
        <span style="width:7px;height:7px;border-radius:50%;background:#00d4aa;display:inline-block;"></span>
        Connected · US-South
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Model Cards
    st.markdown("""
    <div class="model-card">
      <div class="model-role role-gen">⚡ Generation Model</div>
      <div class="model-name">ibm/granite-4-h-small</div>
      <div class="model-desc">Fast instruction-tuned model for real-time vendor guidance generation</div>
    </div>
    <div class="model-card">
      <div class="model-role role-emb">🧩 Embedding Model</div>
      <div class="model-name">ibm/granite-embedding-278m-multilingual</div>
      <div class="model-desc">278M param multilingual embeddings for RAG retrieval in 22+ Indian languages</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Build Index Button
    st.markdown("### 🔧 RAG Index")
    if not st.session_state.index_built:
        st.warning("⚠️ Vector index not built yet. Click below to embed all knowledge base documents.")
        if st.button("🚀 Build Vector Index", key="build_idx"):
            st.session_state.index_building = True
            st.session_state.build_log = []
            log_messages = []

            with st.spinner("Embedding knowledge base with granite-embedding-278m-multilingual..."):
                def log_cb(msg):
                    log_messages.append(msg)

                try:
                    build_index(status_callback=log_cb)
                    st.session_state.index_built    = True
                    st.session_state.index_building = False
                    st.session_state.build_log      = log_messages
                    st.success(f"✅ Index built! {len(KNOWLEDGE_BASE)} documents embedded.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to build index: {e}")
                    st.session_state.index_building = False
    else:
        st.success(f"✅ Index Ready — {len(KNOWLEDGE_BASE)} documents")
        if st.button("🔄 Rebuild Index"):
            st.session_state.index_built = False
            st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Top-K Setting
    top_k = st.slider("📄 Retrieved Documents (top-k)", min_value=1, max_value=5, value=3)

    # Clear Chat
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:11px;color:#8b92b8;text-align:center;line-height:1.8;">
      Edunet Internship Project<br/>
      <strong style="color:#74b1ff;">IBM watsonx.ai</strong> · RAG Pipeline<br/>
      Street Vendor Digitalization Agent
    </div>
    """, unsafe_allow_html=True)


# ── MAIN CONTENT ──────────────────────────────────────────────────────────────

# Hero Banner
st.markdown("""
<div class="hero-banner">
  <div class="hero-title">Street Vendor Digitalization Agent</div>
  <div class="hero-sub">
    An AI-powered RAG agent that helps India's 5 crore+ street vendors go digital —
    business profiles, UPI setup, MSME schemes, local SEO, and credit access.
    Powered by IBM watsonx.ai Granite models.
  </div>
  <div class="hero-badges">
    <span class="hbadge hb-ibm">🔵 IBM watsonx.ai</span>
    <span class="hbadge hb-rag">🔗 RAG Pipeline</span>
    <span class="hbadge hb-edu">🎓 Edunet Internship</span>
    <span class="hbadge hb-ibm">⚡ granite-4-h-small</span>
    <span class="hbadge hb-rag">🧩 granite-embedding-278m-multilingual</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Stats Row
st.markdown("""
<div class="stats-row">
  <div class="stat-card"><div class="stat-num">5Cr+</div><div class="stat-lbl">Street vendors in India</div></div>
  <div class="stat-card"><div class="stat-num">95%</div><div class="stat-lbl">Currently undigitized</div></div>
  <div class="stat-card"><div class="stat-num">22+</div><div class="stat-lbl">Indian languages supported</div></div>
  <div class="stat-card"><div class="stat-num">3×</div><div class="stat-lbl">Average revenue uplift</div></div>
</div>
""", unsafe_allow_html=True)

# ── MAIN LAYOUT ───────────────────────────────────────────────────────────────
col_chat, col_info = st.columns([3, 1.2], gap="large")

with col_chat:
    # Chat Header
    st.markdown("""
    <div class="chat-header">
      <span class="chat-dot" style="background:#ff5f57;"></span>
      <span class="chat-dot" style="background:#febc2e;"></span>
      <span class="chat-dot" style="background:#28c840;"></span>
      <span class="chat-title">Street Vendor Digitalization Agent — Live AI Chat</span>
      <span class="model-pill">🔵 granite-4-h-small</span>
    </div>
    """, unsafe_allow_html=True)

    # Chat History
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
            <div style="text-align:center;padding:40px 20px;color:#8b92b8;">
              <div style="font-size:40px;margin-bottom:12px;">🛒</div>
              <div style="font-size:16px;font-weight:700;color:#f0f2ff;margin-bottom:8px;">Ask anything about going digital!</div>
              <div style="font-size:14px;">Try: "I sell fruit in Pune's Camp area" or "I have a chai stall near Dadar station"</div>
              <div style="margin-top:16px;">
                <span class="etag et-purple">UPI Setup</span>
                <span class="etag et-teal">MSME Schemes</span>
                <span class="etag et-orange">Google Listing</span>
                <span class="etag et-purple">QR Code</span>
                <span class="etag et-teal">PM SVANidhi</span>
                <span class="etag et-orange">Local SEO</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for turn in st.session_state.chat_history:
                # User bubble
                st.markdown(f"""
                <div style="text-align:right;margin-bottom:6px;">
                  <div class="user-bubble">"{turn['query']}"</div>
                </div>
                <div style="clear:both;"></div>
                """, unsafe_allow_html=True)

                # Agent bubble
                st.markdown("""<div class="agent-label">🔵 Street Vendor Digitalization Agent · IBM watsonx.ai</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="agent-bubble">{turn['answer'].replace(chr(10), '<br/>')}</div>""", unsafe_allow_html=True)

                # Retrieved documents
                if turn.get("retrieved_docs"):
                    with st.expander(f"📄 Retrieved {len(turn['retrieved_docs'])} documents from Knowledge Base"):
                        st.markdown('<div class="retrieved-title">🔍 RAG — Documents used to generate this answer</div>', unsafe_allow_html=True)
                        for r in turn["retrieved_docs"]:
                            doc = r["doc"]
                            score = r["sim"]
                            st.markdown(f"""
                            <div class="rdoc">
                              <span class="rdoc-score">{score:.3f}</span>
                              <div>
                                <div class="rdoc-title">{doc['title']}</div>
                                <div class="rdoc-cat">{doc['category']}</div>
                              </div>
                            </div>
                            """, unsafe_allow_html=True)

                st.markdown("<hr/>", unsafe_allow_html=True)

    # Input Area
    st.markdown("<br/>", unsafe_allow_html=True)
    input_col, btn_col = st.columns([4, 1])
    with input_col:
        user_query = st.text_input(
            label="",
            placeholder='E.g. "I sell vegetables in T. Nagar, Chennai. How do I go digital?"',
            key="user_input",
            label_visibility="collapsed",
        )
    with btn_col:
        ask_clicked = st.button("Ask AI ✦", key="ask_btn")

    # Process query
    if (ask_clicked or user_query) and user_query.strip():
        if not st.session_state.index_built:
            st.error("⚠️ Please build the Vector Index first using the sidebar button!")
        else:
            with st.spinner(""):
                # Show pipeline steps
                pipeline_placeholder = st.empty()
                pipeline_placeholder.markdown("""
                <div class="pipeline-step ps-active">🧩 Embedding query with granite-embedding-278m-multilingual...</div>
                <div class="pipeline-step ps-wait">🔍 Searching knowledge base...</div>
                <div class="pipeline-step ps-wait">⚡ Generating with granite-4-h-small...</div>
                """, unsafe_allow_html=True)
                time.sleep(0.5)

                pipeline_placeholder.markdown("""
                <div class="pipeline-step ps-done">✅ Query embedded — vector ready</div>
                <div class="pipeline-step ps-active">🔍 Searching knowledge base (cosine similarity)...</div>
                <div class="pipeline-step ps-wait">⚡ Generating with granite-4-h-small...</div>
                """, unsafe_allow_html=True)

                try:
                    result = answer_query(user_query.strip(), top_k=top_k)
                    pipeline_placeholder.markdown("""
                    <div class="pipeline-step ps-done">✅ Query embedded</div>
                    <div class="pipeline-step ps-done">✅ Top documents retrieved</div>
                    <div class="pipeline-step ps-active">⚡ Generating with granite-4-h-small...</div>
                    """, unsafe_allow_html=True)
                    time.sleep(0.3)
                    pipeline_placeholder.empty()

                    # Add to history
                    st.session_state.chat_history.append({
                        "query":         user_query.strip(),
                        "answer":        result["answer"],
                        "retrieved_docs": result["retrieved_docs"],
                    })
                    st.rerun()

                except Exception as e:
                    pipeline_placeholder.empty()
                    st.error(f"❌ Error: {e}")
                    st.info("💡 Make sure your IBM API Key is valid and the index is built.")


with col_info:
    # RAG Pipeline Visual
    st.markdown("""
    <div style="background:#0d0f1a;border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;">
      <div style="font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#6c47ff;margin-bottom:16px;">RAG Pipeline</div>

      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <span style="font-size:18px;">🧑</span>
        <div>
          <div style="font-size:12px;font-weight:700;">Vendor Query</div>
          <div style="font-size:11px;color:#8b92b8;">Natural language input</div>
        </div>
      </div>
      <div style="text-align:center;color:#6c47ff;font-size:14px;margin:4px 0;">↓</div>

      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;background:rgba(15,98,254,0.08);border:1px solid rgba(15,98,254,0.25);border-radius:10px;padding:8px 10px;">
        <span style="font-size:18px;">🧩</span>
        <div>
          <div style="font-size:11px;font-weight:800;color:#74b1ff;">granite-embedding-278m</div>
          <div style="font-size:10px;color:#8b92b8;">Multilingual vectorization</div>
        </div>
      </div>
      <div style="text-align:center;color:#6c47ff;font-size:14px;margin:4px 0;">↓</div>

      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <span style="font-size:18px;">🔍</span>
        <div>
          <div style="font-size:12px;font-weight:700;">Cosine Search</div>
          <div style="font-size:11px;color:#8b92b8;">Top-{top_k} docs retrieved</div>
        </div>
      </div>
      <div style="text-align:center;color:#6c47ff;font-size:14px;margin:4px 0;">↓</div>

      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;background:rgba(15,98,254,0.08);border:1px solid rgba(15,98,254,0.25);border-radius:10px;padding:8px 10px;">
        <span style="font-size:18px;">⚡</span>
        <div>
          <div style="font-size:11px;font-weight:800;color:#74b1ff;">granite-4-h-small</div>
          <div style="font-size:10px;color:#8b92b8;">Contextual generation</div>
        </div>
      </div>
      <div style="text-align:center;color:#6c47ff;font-size:14px;margin:4px 0;">↓</div>

      <div style="display:flex;align-items:center;gap:8px;">
        <span style="font-size:18px;">📦</span>
        <div>
          <div style="font-size:12px;font-weight:700;">Digital Kit</div>
          <div style="font-size:11px;color:#8b92b8;">UPI + Schemes + SEO</div>
        </div>
      </div>
    </div>
    """.replace("{top_k}", str(top_k)), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Sample Queries
    st.markdown("""
    <div style="font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#6c47ff;margin-bottom:12px;">💡 Sample Queries</div>
    """, unsafe_allow_html=True)

    samples = [
        "I sell fruit in Pune's Camp area",
        "I have an idli-dosa stall near Chennai Central",
        "Vegetable vendor in Dharavi Mumbai",
        "I sell sarees in Surat textile market",
        "Tea stall near Dadar station, Mumbai",
        "Flower vendor near MG Road Bangalore",
    ]
    for s in samples:
        st.markdown(f"""<div class="sample-query">💬 "{s}"</div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # KB Stats
    cats = {}
    for doc in KNOWLEDGE_BASE:
        c = doc["category"]
        cats[c] = cats.get(c, 0) + 1

    st.markdown("""
    <div style="font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#6c47ff;margin-bottom:12px;">📚 Knowledge Base</div>
    """, unsafe_allow_html=True)
    for cat, count in cats.items():
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05);font-size:13px;">
          <span style="color:#8b92b8;">{cat}</span>
          <span style="background:rgba(108,71,255,0.15);border:1px solid rgba(108,71,255,0.3);color:#a78bfa;padding:1px 8px;border-radius:50px;font-size:11px;font-weight:700;">{count}</span>
        </div>
        """, unsafe_allow_html=True)
