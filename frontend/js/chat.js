/* chat.js — Chat UI logic, talks to POST /api/query */

const chatMessages = document.getElementById('chatMessages');
const chatEmpty    = document.getElementById('chatEmpty');
const chatInput    = document.getElementById('chatInput');
const sendBtn      = document.getElementById('sendBtn');

function getChatLang() {
  const sel = document.getElementById('langSelectChat') || document.getElementById('langSelect');
  return sel ? sel.value : 'en';
}

// Enter key sends
if (chatInput) {
  chatInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !sendBtn.disabled) sendMessage();
  });
}

function fillQuery(el) {
  if (chatInput) {
    chatInput.value = el.textContent.trim();
    chatInput.focus();
  }
}

function clearChat() {
  if (chatMessages) {
    chatMessages.innerHTML = '';
    chatMessages.appendChild(chatEmpty);
    chatEmpty.style.display = 'flex';
  }
}

async function sendMessage() {
  const query = chatInput.value.trim();
  const lang  = getChatLang();
  if (!query) return;

  chatEmpty.style.display = 'none';
  appendBubble('user', query);
  chatInput.value = '';
  sendBtn.disabled = true;

  const typingEl = appendTyping();

  try {
    const apiBase = window.location.origin || '';
    const res = await fetch(`${apiBase}/api/query`, {
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
    appendBubble('agent', data.answer, data.retrieved_docs);

    // Save to offline cache
    if (typeof saveConversation === 'function') {
      saveConversation(query, data.answer);
    }

    // Render receipt in right panel if form exists
    const fVendorName = document.getElementById('fVendorName');
    if (fVendorName && typeof renderReceipt === 'function') {
      renderReceipt({
        vendor_name   : fVendorName.value || 'Vendor',
        business_type : document.getElementById('fBizType')?.value || 'Street Vendor',
        location      : document.getElementById('fLocation')?.value || '',
        upi_id        : document.getElementById('fUpiId')?.value || null,
        answer        : data.answer,
        retrieved_docs: data.retrieved_docs,
        qr_url        : null,
      });
    }

  } catch(e) {
    typingEl.remove();
    appendBubble('agent', `Sorry, something went wrong. Please try again in a moment.`);
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
    const apiBase = window.location.origin || '';
    const r = await fetch(`${apiBase}/api/health`);
    const d = await r.json();
    const navStatus = document.getElementById('navStatus');
    const indexStatus = document.getElementById('indexStatus');
    const chipIbm = document.getElementById('chipIbm');
    const chipIdx = document.getElementById('chipIdx');
    if (navStatus) navStatus.textContent = d.ibm_status === 'connected' ? 'IBM Connected' : 'Connecting...';
    if (indexStatus) {
      indexStatus.textContent = d.index_ready ? `${d.doc_count} docs` : 'Index building...';
      indexStatus.className = 'ibm-model-chip ' + (d.index_ready ? 'chip-live' : 'chip-gen');
    }
    if (chipIbm) {
      chipIbm.textContent = d.ibm_status === 'connected' ? 'IBM: OK' : 'IBM: Error';
      chipIbm.className = 's-chip ' + (d.ibm_status === 'connected' ? 's-ok' : 's-warn');
    }
    if (chipIdx) {
      chipIdx.textContent = d.index_ready ? `Index: ${d.doc_count} docs` : 'Index: Building';
      chipIdx.className = 's-chip ' + (d.index_ready ? 's-ok' : 's-warn');
    }
  } catch(e) {
    const navStatus = document.getElementById('navStatus');
    if (navStatus) navStatus.textContent = 'Server starting...';
  }
}
checkHealth();
