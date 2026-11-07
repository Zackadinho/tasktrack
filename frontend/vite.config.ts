import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Vite is the dev server and build tool.
// `npm run dev`   -> serves the app on http://localhost:5173 and reloads on every save
// `npm run build` -> compiles everything into plain HTML/JS/CSS files in dist/
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, host: true },
});
