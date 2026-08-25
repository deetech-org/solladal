// sw.js
// -*- coding: utf-8 -*-
/**
 * Service Worker for "சொல்லாடல்" (Solladal) Tamil Word Game PWA.
 * Enables 100% offline gameplay via Cache-First caching strategy.
 */

const CACHE_NAME = 'solladal-1.3.2-feac1356-sa';

const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './css/style.css',
  './assets/fonts/fonts.css',
  './assets/fonts/MuktaMalar-400-latin.woff2',
  './assets/fonts/MuktaMalar-400-latinext.woff2',
  './assets/fonts/MuktaMalar-400-tamil.woff2',
  './assets/fonts/MuktaMalar-600-latin.woff2',
  './assets/fonts/MuktaMalar-600-latinext.woff2',
  './assets/fonts/MuktaMalar-600-tamil.woff2',
  './assets/fonts/MuktaMalar-700-latin.woff2',
  './assets/fonts/MuktaMalar-700-latinext.woff2',
  './assets/fonts/MuktaMalar-700-tamil.woff2',
  './assets/fonts/MuktaMalar-800-latin.woff2',
  './assets/fonts/MuktaMalar-800-latinext.woff2',
  './assets/fonts/MuktaMalar-800-tamil.woff2',
  './assets/fonts/NotoSansTamil-400-latin.woff2',
  './assets/fonts/NotoSansTamil-400-latinext.woff2',
  './assets/fonts/NotoSansTamil-400-tamil.woff2',
  './js/app.js',
  './js/gameEngine.js',
  './js/tamilUtils.js',
  './js/wordBank.js',
  './js/uiController.js',
  './js/modals.js',
  './js/storage.js',
  './data/words.json',
  './manifest.json',
  './assets/icons/icon-192.svg',
  './assets/icons/icon-512.svg'
];

// Install Event: Cache all core assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] Pre-caching offline assets...');
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

// Activate Event: Cleanup stale caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(
        keyList.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[ServiceWorker] Removing old cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event: Cache-First strategy with network fallback
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then((networkResponse) => {
        // Cache external requests if successful (like Google Fonts)
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      });
    }).catch(() => {
      // Fallback to offline index.html if available
      return caches.match('./index.html');
    })
  );
});
