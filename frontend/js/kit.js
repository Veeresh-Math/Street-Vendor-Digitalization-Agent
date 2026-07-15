/* kit.js — Digital Kit Generator + Torn Receipt Renderer */

const receiptContainer = document.getElementById('receiptContainer');
const pipelineDisplay  = document.getElementById('pipelineDisplay');
const pipelineSteps    = document.getElementById('pipelineSteps');
const generateKitBtn   = document.getElementById('generateKitBtn');

/* ── Generate Kit (POST /api/generate-kit) ─────────────── */
async function generateKit() {
  const vendorName  = document.getElementById('fVendorName')?.value.trim() || '';
  const bizType     = document.getElementById('fBizType')?.value.trim() || '';
  const location    = document.getElementById('fLocation')?.value.trim() || '';
  const upiId       = document.getElementById('fUpiId')?.value.trim() || '';
  const lang        = (document.getElementById('langSelectChat') || document.getElementById('langSelect'))?.value || 'en';

  if (!vendorName || !bizType || !location) {
    alert('Please fill in Vendor Name, Business Type, and Location.');
    return;
  }

  if (generateKitBtn) generateKitBtn.disabled = true;
  showPipeline(['Embedding query...', 'Retrieving docs...', 'Generating with llama...', 'Rendering receipt...']);

/* Local API base URL */
  const apiBase = window.__API_BASE__ || window.location.origin || '';

  try {
    const res = await fetch(`${apiBase}/api/generate-kit`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({
        vendor_name   : vendorName,
        business_type : bizType,
        location,
        upi_id        : upiId || null,
        language      : lang,
        top_k         : 3,
      }),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || `HTTP ${res.status}`);
    }

    const data = await res.json();
    updatePipelineDone();
    renderReceipt(data);

    // Also append to chat
    if (typeof appendBubble === 'function') {
      document.getElementById('chatEmpty').style.display = 'none';
      appendBubble('user', `[Digital Kit] ${vendorName} — ${bizType} at ${location}`);
      appendBubble('agent', data.answer, data.retrieved_docs);
    }

  } catch(e) {
    hidePipeline();
    alert(`Error generating kit: ${e.message}`);
  }

  if (generateKitBtn) generateKitBtn.disabled = false;
}

/* ── Render Torn Receipt ────────────────────────────────── */
function renderReceipt(data) {
  if (!receiptContainer) return;
  hidePipeline();

  const qrHtml = data.qr_url
    ? `<img class="receipt-qr-img" src="${data.qr_url}" alt="UPI QR Code"/>`
    : `<div class="receipt-qr-img" style="display:flex;align-items:center;justify-content:center;font-size:11px;color:var(--text-light);text-align:center;padding:8px;">Add UPI ID<br/>for QR</div>`;

  const upiHtml = data.upi_id
    ? `<div class="receipt-upi-id">${data.upi_id}</div>
       <div class="receipt-upi-apps">PhonePe · Paytm · GPay · BHIM</div>`
    : `<div style="font-size:12px;color:var(--text-light);">No UPI ID provided</div>`;

  const sourcesHtml = (data.retrieved_docs || []).map(d => `
    <div class="receipt-source-item">
      <span class="source-score">${d.score.toFixed(3)}</span>
      <span>${d.title}</span>
    </div>`).join('');

  const answerEscaped = (data.answer || '')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

  receiptContainer.innerHTML = `
    <div class="receipt-wrap">
      <div class="receipt-card">
        <div class="receipt-header">
          <div class="receipt-header-accent"></div>
          <div class="receipt-vendor-name">${escHtml(data.vendor_name || 'Vendor')}</div>
          <div class="receipt-type">${escHtml(data.business_type || 'Street Vendor')}</div>
          <div class="receipt-loc">📍 ${escHtml(data.location || '')}</div>
        </div>
        <div class="receipt-body">
          <div class="receipt-qr-row">
            ${qrHtml}
            <div class="receipt-upi-info">
              <h4>💳 Scan & Pay (UPI)</h4>
              ${upiHtml}
            </div>
          </div>
          <hr class="receipt-divider"/>
          <div class="receipt-section-title">📋 AI-Generated Digital Guide</div>
          <div class="receipt-answer">${answerEscaped}</div>
          ${sourcesHtml ? `
            <hr class="receipt-divider"/>
            <div class="receipt-section-title">🔍 RAG Sources</div>
            <div class="receipt-sources">${sourcesHtml}</div>
          ` : ''}
        </div>
        <div class="receipt-footer">
          <div class="receipt-footer-brand">🔵 IBM watsonx.ai · llama-3-3-70b-instruct</div>
          <div class="receipt-actions">
            <button class="btn btn-sm btn-outline" onclick="copyReceipt()" title="Copy text">📋</button>
            ${data.qr_url ? `<a class="btn btn-sm btn-green" href="${data.qr_url}" download="qr-card.png" title="Download QR card">⬇ QR</a>` : ''}
            <button class="btn btn-sm btn-saffron" onclick="shareWhatsApp()" title="WhatsApp">💬</button>
          </div>
        </div>
      </div>
    </div>`;
}

/* ── Copy receipt text ─────────────────────────────────── */
function copyReceipt() {
  const el = receiptContainer.querySelector('.receipt-answer');
  if (el) {
    navigator.clipboard.writeText(el.textContent).then(() => alert('Copied to clipboard!'));
  }
}

/* ── WhatsApp share ────────────────────────────────────── */
function shareWhatsApp() {
  const el    = receiptContainer.querySelector('.receipt-answer');
  const name  = receiptContainer.querySelector('.receipt-vendor-name');
  const text  = `*${name?.textContent || 'Digital Kit'}*\n\n${el?.textContent || ''}`;
  const url   = `https://wa.me/?text=${encodeURIComponent(text)}`;
  window.open(url, '_blank');
}

/* ── Pipeline display helpers ──────────────────────────── */
function showPipeline(steps) {
  if (!pipelineDisplay || !pipelineSteps) return;
  pipelineDisplay.style.display = 'block';
  pipelineSteps.innerHTML = steps.map((s,i) =>
    `<div class="pipeline-step ${i===0?'ps-active':'ps-waiting'}" id="ps-${i}">${s}</div>`
  ).join('');
  let i = 0;
  const interval = setInterval(() => {
    i++;
    if (i >= steps.length) { clearInterval(interval); return; }
    document.getElementById(`ps-${i-1}`)?.classList.replace('ps-active','ps-done');
    document.getElementById(`ps-${i}`)?.classList.replace('ps-waiting','ps-active');
  }, 900);
}
function updatePipelineDone() {
  if (!pipelineSteps) return;
  document.querySelectorAll('.pipeline-step').forEach(el => {
    el.className = 'pipeline-step ps-done';
  });
}
function hidePipeline() {
  if (pipelineDisplay) pipelineDisplay.style.display = 'none';
}

/* ── Utility ───────────────────────────────────────────── */
function escHtml(s) {
  return String(s)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
