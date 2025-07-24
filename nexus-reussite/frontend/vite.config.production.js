import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
import { visualizer } from 'rollup-plugin-visualizer';
import path from 'path';

// Configuration Vite optimisée pour Nexus Réussite
export default defineConfig(({ command, mode }) => {
  // Charger les variables d'environnement
  const env = loadEnv(mode, process.cwd(), '');
  
  return {
    plugins: [
      react({
        // Optimisations React
        babel: {
          plugins: [
            // Plugin pour l'optimisation des re-renders
            mode === 'production' && ['babel-plugin-transform-react-remove-prop-types', { mode: 'remove', removeImport: true }]
          ].filter(Boolean)
        }
      }),
      
      // PWA Plugin pour l'installation comme app
      VitePWA({
        registerType: 'autoUpdate',
        workbox: {
          globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
          runtimeCaching: [
            {
              urlPattern: /^https:\/\/api\.nexus-reussite\.com\/.*/i,
              handler: 'NetworkFirst',
              options: {
                cacheName: 'api-cache',
                expiration: {
                  maxEntries: 100,
                  maxAgeSeconds: 60 * 60 * 24 // 24 heures
                }
              }
            }
          ]
        },
        includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'masked-icon.svg'],
        manifest: {
          name: 'Nexus Réussite',
          short_name: 'Nexus',
          description: 'Plateforme d\'accompagnement scolaire intelligente',
          theme_color: '#2563eb',
          background_color: '#ffffff',
          display: 'standalone',
          orientation: 'portrait',
          scope: '/',
          start_url: '/',
          icons: [
            {
              src: 'pwa-192x192.png',
              sizes: '192x192',
              type: 'image/png'
            },
            {
              src: 'pwa-512x512.png',
              sizes: '512x512',
              type: 'image/png'
            },
            {
              src: 'pwa-512x512.png',
              sizes: '512x512',
              type: 'image/png',
              purpose: 'any maskable'
            }
          ]
        }
      }),
      
      // Analyseur de bundle (seulement en développement)
      mode === 'development' && visualizer({
        filename: 'dist/stats.html',
        open: false,
        gzipSize: true
      })
    ].filter(Boolean),
    
    // Configuration du serveur de développement
    server: {
      host: '0.0.0.0',
      port: 3000,
      open: false,
      cors: true,
      proxy: {
        // Proxy pour l'API backend
        '/api': {
          target: env.VITE_BACKEND_URL || 'http://localhost:5000',
          changeOrigin: true,
          secure: false
        },
        // Proxy pour les WebSockets
        '/ws': {
          target: env.VITE_WS_URL || 'ws://localhost:5000',
          ws: true,
          changeOrigin: true
        }
      }
    },
    
    // Configuration du build
    build: {
      target: 'es2020',
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: mode === 'development',
      minify: mode === 'production' ? 'esbuild' : false,
      
      // Optimisations de build
      rollupOptions: {
        output: {
          manualChunks: {
            // Vendor chunks pour un meilleur caching
            vendor: ['react', 'react-dom'],
            router: ['react-router-dom'],
            ui: ['lucide-react', 'framer-motion'],
            charts: ['recharts'],
            forms: ['react-hook-form', '@hookform/resolvers', 'zod'],
            utils: ['axios', 'date-fns', 'clsx']
          },
          // Noms de fichiers avec hash pour le caching
          chunkFileNames: 'assets/[name]-[hash].js',
          entryFileNames: 'assets/[name]-[hash].js',
          assetFileNames: 'assets/[name]-[hash].[ext]'
        }
      },
      
      // Optimisations de performance
      chunkSizeWarningLimit: 1000,
      
      // Configuration pour la compression
      reportCompressedSize: true
    },
    
    // Résolution des chemins
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        '@components': path.resolve(__dirname, './src/components'),
        '@contexts': path.resolve(__dirname, './src/contexts'),
        '@services': path.resolve(__dirname, './src/services'),
        '@utils': path.resolve(__dirname, './src/lib'),
        '@data': path.resolve(__dirname, './src/data'),
        '@assets': path.resolve(__dirname, './src/assets')
      }
    },
    
    // Variables d'environnement exposées au client
    define: {
      __APP_VERSION__: JSON.stringify(process.env.npm_package_version || '1.0.0'),
      __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
      __MODE__: JSON.stringify(mode)
    },
    
    // Configuration CSS
    css: {
      devSourcemap: mode === 'development',
      postcss: {
        plugins: [
          require('tailwindcss'),
          require('autoprefixer')
        ]
      }
    },
    
    // Optimisations des dépendances
    optimizeDeps: {
      include: [
        'react',
        'react-dom',
        'react-router-dom',
        'axios',
        'date-fns',
        'lucide-react',
        'recharts',
        'socket.io-client'
      ],
      exclude: ['@vite/client', '@vite/env']
    },
    
    // Configuration pour la compatibilité
    esbuild: {
      target: 'es2020',
      logOverride: { 'this-is-undefined-in-esm': 'silent' }
    },
    
    // Configuration de base pour le déploiement
    base: env.VITE_BASE_URL || '/'
  };
});
