import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true
      },
      '/ws': {
        target: 'ws://localhost:3000',
        changeOrigin: true,
        ws: true
      },
      '/auth': {
        target: 'http://localhost:3000',
        changeOrigin: true
      },
      '/family': {
        target: 'http://localhost:3000',
        changeOrigin: true
      },
      '/health': {
        target: 'http://localhost:3000',
        changeOrigin: true
      },
      '/basket': {
        target: 'http://localhost:3000',
        changeOrigin: true
      },
      '/meal-plan': {
        target: 'http://localhost:3000',
        changeOrigin: true
      },
      '/shopping-list': {
        target: 'http://localhost:3000',
        changeOrigin: true
      },
      '/analyze': {
        target: 'http://localhost:3000',
        changeOrigin: true
      },
      '/recipes': {
        target: 'http://localhost:3000',
        changeOrigin: true
      }
    }
  }
})