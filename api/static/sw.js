
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open('student-panel').then(function(cache) {
      return cache.addAll([
        '/',
        '/static/',
        '/add_student',
        '/generate_xml'
        // Add other URLs that you want to cache for offline access
      ]);
    })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});
