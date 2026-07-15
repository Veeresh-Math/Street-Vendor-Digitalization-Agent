/* offline.js — IndexedDB offline-first support */

const DB_NAME = 'svda_offline';
const DB_VERSION = 1;
const STORE_CONVERSATIONS = 'conversations';

let db = null;

function openDB() {
  return new Promise((resolve, reject) => {
    if (db) { resolve(db); return; }
    const request = indexedDB.open(DB_NAME, DB_VERSION);
    request.onupgradeneeded = (e) => {
      const d = e.target.result;
      if (!d.objectStoreNames.contains(STORE_CONVERSATIONS)) {
        d.createObjectStore(STORE_CONVERSATIONS, { keyPath: 'id', autoIncrement: true });
      }
    };
    request.onsuccess = (e) => { db = e.target.result; resolve(db); };
    request.onerror = (e) => reject(e.target.error);
  });
}

async function saveConversation(query, answer) {
  try {
    const d = await openDB();
    const tx = d.transaction(STORE_CONVERSATIONS, 'readwrite');
    tx.objectStore(STORE_CONVERSATIONS).add({
      query, answer, timestamp: Date.now(),
    });
  } catch (e) { /* silent */ }
}

function showConversationHistory() {
  const history = getRecentConversations();
  if (!history || history.length === 0) return;
  
  const panel = document.getElementById('chatHistory');
  if (!panel) return;
  
  panel.innerHTML = '<div style="padding:8px 12px;font-size:11px;font-weight:700;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.5px;">Recent Questions</div>';
  history.slice(-5).reverse().forEach(conv => {
    const item = document.createElement('div');
    item.style.cssText = 'padding:8px 12px;cursor:pointer;border-bottom:1px solid var(--bg4);font-size:12px;color:var(--text-light);transition:background 0.2s;';
    item.textContent = conv.query.length > 60 ? conv.query.substring(0, 60) + '...' : conv.query;
    item.onmouseover = () => item.style.background = 'var(--bg4)';
    item.onmouseout = () => item.style.background = 'transparent';
    item.onclick = () => {
      const chatInput = document.getElementById('chatInput');
      if (chatInput) { chatInput.value = conv.query; chatInput.focus(); }
    };
    panel.appendChild(item);
  });
  panel.style.display = 'block';
}

async function getRecentConversations(limit = 20) {
  try {
    const d = await openDB();
    return new Promise((resolve) => {
      const tx = d.transaction(STORE_CONVERSATIONS, 'readonly');
      const req = tx.objectStore(STORE_CONVERSATIONS).getAll();
      req.onsuccess = () => resolve((req.result || []).slice(-limit));
      req.onerror = () => resolve([]);
    });
  } catch (e) { return []; }
}
