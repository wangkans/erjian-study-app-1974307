// Service Worker for 二建备考题库 PWA
var CACHE = 'ejian-v1';
var URLS = ['/', '/index.html'];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE).then(function(cache) {
      return cache.addAll(URLS);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.filter(function(k) { return k !== CACHE; })
            .map(function(k) { return caches.delete(k); })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function(e) {
  // 只处理 GET 请求
  if (e.request.method !== 'GET') return;

  // 对于 Cloudflare Pages 的请求，走网络优先
  e.respondWith(
    fetch(e.request).then(function(response) {
      // 网络成功，缓存副本
      if (response && response.status === 200) {
        var clone = response.clone();
        caches.open(CACHE).then(function(cache) {
          cache.put(e.request, clone);
        });
      }
      return response;
    }).catch(function() {
      // 网络失败，尝试缓存
      return caches.match(e.request).then(function(cached) {
        return cached || new Response('离线模式 - 请联网后刷新', {
          status: 503,
          headers: { 'Content-Type': 'text/plain;charset=utf-8' }
        });
      });
    })
  );
});
