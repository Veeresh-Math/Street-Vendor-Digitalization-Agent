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
