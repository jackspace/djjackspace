import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  root: '.',
  publicDir: 'public',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        software: resolve(__dirname, 'software/index.html'),
        tagforge: resolve(__dirname, 'software/DJTagForge/index.html'),
      },
    },
  },
  server: {
    open: true,
    port: 3000,
  },
});
