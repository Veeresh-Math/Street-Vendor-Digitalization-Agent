/* chat.js — Chat UI logic, talks to POST /api/query */

const chatMessages = document.getElementById('chatMessages');
const chatEmpty    = document.getElementById('chatEmpty');
const chatInput    = document.getElementById('chatInput');
const sendBtn      = document.getElementById('sendBtn');
const langSelect   = document.getElementById('langSelect');

// Enter key sends
chatInput.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !sendBtn.disabled) sendMessage();
});

function fillQuery(el) {
  chatInput.value = el.textContent.trim();
  chatInput.focus();
}

function clearChat() {
  chatMessages.innerHTML = '';
  chatMessages.appendChild(chatEmpty);
  chatEmpty.style.display = 'flex';
}

async function sendMessage() {
  const query = chatInput.value.trim();
  const lang  = langSelect.value;
  if (!query) return;

  // Hide empty state
  chatEmpty.style.display = 'none';

  // Add user bubble
  appendBubble('user', query);
  chatInput.value = '';
  sendBtn.disabled = true;

  // Show typing
  const typingEl = appendTyping();

  try {
    const res = await fetch('/api/query', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ query, language: lang, top_k: 3 }),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || `HTTP ${res.status}`);
    }

    const data = await res.json();
    typingEl.remove();

    // Agent bubble
    appendBubble('agent', data.answer, data.retrieved_docs);

    // Render receipt in right panel
    renderReceipt({
      vendor_name   : document.getElementById('fVendorName').value || 'Vendor',
      business_type : document.getElementById('fBizType').value    || 'Street Vendor',
      location      : document.getElementById('fLocation').value   || '—',
      upi_id        : document.getElementById('fUpiId').value      || null,
      answer        : data.answer,
      retrieved_docs: data.retrieved_docs,
      qr_url        : null,
    });

  } catch(e) {
    typingEl.remove();
    appendBubble('agent', `⚠️ Error: ${e.message}\n\nPlease ensure the FastAPI server is running and the vector index is built.`);
  }

  sendBtn.disabled = false;
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function appendBubble(role, text, docs = []) {
  if (role === 'user') {
    const el = document.createElement('div');
    el.className = 'bubble-user';
    el.textContent = text;
    chatMessages.appendChild(el);
  } else {
    const wrap = document.createElement('div');
    wrap.className = 'bubble-agent';

    const lbl = document.createElement('div');
    lbl.className = 'bubble-agent-label';
    lbl.innerHTML = '<span>🔵</span> Street Vendor Digitalization Agent · IBM watsonx.ai';

    const body = document.createElement('div');
    body.className = 'bubble-agent-body';
    body.textContent = text;

    wrap.appendChild(lbl);
    wrap.appendChild(body);

    // Retrieved docs
    if (docs && docs.length) {
      const docsEl = buildDocsPanel(docs);
      wrap.appendChild(docsEl);
    }

    chatMessages.appendChild(wrap);
  }
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function appendTyping() {
  const el = document.createElement('div');
  el.className = 'typing-dots';
  el.innerHTML = '<span></span><span></span><span></span>';
  chatMessages.appendChild(el);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return el;
}

function buildDocsPanel(docs) {
  const panel = document.createElement('div');
  panel.className = 'docs-panel';
  panel.innerHTML = `<div class="docs-panel-title">🔍 RAG Sources (${docs.length} retrieved)</div>`;
  docs.forEach(d => {
    const item = document.createElement('div');
    item.className = 'doc-item';
    item.innerHTML = `
      <span class="doc-score">${d.score.toFixed(3)}</span>
      <div>
        <div class="doc-title">${d.title}</div>
        <div class="doc-cat">${d.category}</div>
      </div>`;
    panel.appendChild(item);
  });
  return panel;
}

// Health check
async function checkHealth() {
  try {
    const r = await fetch('/api/health');
    const d = await r.json();
    document.getElementById('navStatus').textContent =
      d.ibm_status === 'connected' ? 'IBM Connected' : 'Connecting...';
    document.getElementById('indexStatus').textContent =
      d.index_ready ? `✅ ${d.doc_count} docs` : '⚠️ Index not ready';
    document.getElementById('indexStatus').className =
      'ibm-model-chip ' + (d.index_ready ? 'chip-live' : 'chip-gen');
  } catch(e) {
    document.getElementById('navStatus').textContent = 'Server starting...';
  }
}
checkHealth();
