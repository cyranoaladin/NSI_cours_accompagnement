import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      },
      '/ws': {
        target: 'ws://localhost:5000',
        ws: true,
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    chunkSizeWarningLimit: 1500,
    rollupOptions: {
      output: {
        manualChunks: (id) => {
          if (id.includes('node_modules')) {
            if (id.includes('react') || id.includes('react-dom')) {
              return 'vendor';
            }
            if (id.includes('react-router')) {
              return 'router';
            }
            if (id.includes('lucide-react')) {
              return 'ui';
            }
            if (id.includes('recharts')) {
              return 'charts';
            }
            if (id.includes('framer-motion')) {
              return 'motion';
            }
            if (id.includes('react-hook-form') || id.includes('@hookform')) {
              return 'forms';
            }
            if (id.includes('clsx') || id.includes('class-variance-authority')) {
              return 'utils';
            }
            return 'vendor';
          }
        }
      }
    }
  },
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router-dom', 'lucide-react', 'recharts']
  }
})

