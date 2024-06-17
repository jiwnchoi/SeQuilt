// vite.config.js
import { defineConfig } from "vite"
import anywidget from "@anywidget/vite"

export default defineConfig({
  plugins: [anywidget()],
  build: {
    outDir: "seq/static",
    lib: {
      entry: "widget/widget.ts",
      formats: ["es"],
    },
  },
})
