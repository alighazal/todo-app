import path from "path"
import tailwindcss from "@tailwindcss/vite"

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    watch: {
      // Required for reliable file watching inside Docker (bind mounts often don't propagate inotify)
      usePolling: true,
    },
    hmr: {
      // So HMR WebSocket works when accessing app from host (e.g. localhost:3000)
      clientPort: 3000,
    },
  },
})
