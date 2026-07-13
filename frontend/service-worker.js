const CACHE_NAME = 'street-vendor-v8';
const CORE_ASSETS = [
  '/',
  '/index.html',
  '/agent.html',
  '/dashboard.html',
  '/css/theme.css',
  '/css/layout.css',
  '/css/components.css',
  '/js/voice.js',
  '/js/vendor-map.js',
  '/js/scheme-checker.js',
  '/js/offline.js',
  '/js/dashboard.js',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(CORE_ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  if (request.method !== 'GET') return;
  if (url.pathname.startsWith('/api/')) return;

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((c) => c.put(request, clone));
          }
          return networkResponse;
        })
        .catch(() =>
          caches.match(request).then((r) => r || caches.match('/index.html'))
        )
    );
    return;
  }

  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached;
      return fetch(request).then((response) => {
        if (!response || response.status !== 200 || response.type !== 'basic')
          return response;
        const clone = response.clone();
        caches.open(CACHE_NAME).then((c) => c.put(request, clone));
        return response;
      });
    })
  );
});
