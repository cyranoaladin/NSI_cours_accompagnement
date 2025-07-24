// Service Worker pour Nexus Réussite
const CACHE_NAME = 'nexus-reussite-v1';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/nexus-favicon.svg',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap'
];

// Installation du Service Worker
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Cache ouvert');
        return cache.addAll(urlsToCache);
      })
  );
});

// Activation du Service Worker
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            console.log('Suppression du cache obsolète:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Interception des requêtes
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - retourner la réponse
        if (response) {
          return response;
        }

        return fetch(event.request).then(
          function(response) {
            // Vérifier si nous avons reçu une réponse valide
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // IMPORTANT: Cloner la réponse. Une réponse est un stream
            // et parce que nous voulons que le navigateur consomme la réponse
            // ainsi que le cache qui consomme la réponse, nous devons la cloner
            // pour que nous ayons deux streams.
            var responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(function(cache) {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      })
    );
});

// Gestion des notifications push
self.addEventListener('push', function(event) {
  const options = {
    body: event.data ? event.data.text() : 'Nouvelle notification de Nexus Réussite',
    icon: '/nexus-favicon.svg',
    badge: '/nexus-favicon.svg',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: '1'
    },
    actions: [
      {
        action: 'explore',
        title: 'Voir',
        icon: '/images/checkmark.png'
      },
      {
        action: 'close',
        title: 'Fermer',
        icon: '/images/xmark.png'
      },
    ]
  };

  event.waitUntil(
    self.registration.showNotification('Nexus Réussite', options)
  );
});

// Gestion des clics sur les notifications
self.addEventListener('notificationclick', function(event) {
  event.notification.close();

  if (event.action === 'explore') {
    // Ouvrir l'application
    event.waitUntil(
      clients.openWindow('/')
    );
  } else if (event.action === 'close') {
    // Fermer la notification
    event.notification.close();
  } else {
    // Action par défaut
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Synchronisation en arrière-plan
self.addEventListener('sync', function(event) {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

function doBackgroundSync() {
  // Logique de synchronisation en arrière-plan
  return fetch('/api/sync')
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      console.log('Synchronisation réussie:', data);
    })
    .catch(function(error) {
      console.log('Erreur de synchronisation:', error);
    });
}

