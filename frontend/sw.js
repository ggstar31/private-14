/**
 * sw.js — Service Worker
 * Caches app shell for offline use. API responses cached separately.
 */

const SHELL_CACHE = 'cafekasol-shell-v1';
const API_CACHE   = 'cafekasol-api-v1';

const SHELL_FILES = [
  '/',
  '/index.html',
  '/style.css',
  '/app.js',
  '/geo.js',
  '/ui.js',
  '/manifest.json',
];

// Install — cache app shell
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(SHELL_CACHE).then(cache => cache.addAll(SHELL_FILES))
  );
  self.skipWaiting();
});

// Activate — clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(k => k !== SHELL_CACHE && k !== API_CACHE)
          .map(k => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

// Fetch — shell: cache-first; API: network-first with cache fallback
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  if (url.pathname.startsWith('/api/')) {
    // Network-first for API
    event.respondWith(
      fetch(event.request)
        .then(res => {
          const clone = res.clone();
          caches.open(API_CACHE).then(cache => cache.put(event.request, clone));
          return res;
        })
        .catch(() => caches.match(event.request))
    );
  } else {
    // Cache-first for shell
    event.respondWith(
      caches.match(event.request).then(cached => cached || fetch(event.request))
    );
  }
});
