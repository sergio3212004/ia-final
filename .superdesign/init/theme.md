# Theme

## Compact token summary

- Framework: Vue 3 + Vite 8.
- CSS approach: one global `src/style.css`; Tailwind CSS 4 is installed through the Vite plugin but is not used in the current templates.
- Light colors: background `#fff`, primary text `#08060d`, secondary text `#6b6375`, border `#e5e4e7`, code surface `#f4f3ec`, accent `#aa3bff`.
- Dark colors: background `#16171d`, primary text `#f3f4f6`, secondary text `#9ca3af`, border `#2e303a`, code surface `#1f2028`, accent `#c084fc`.
- Font families: system UI for body and headings; `ui-monospace, Consolas, monospace` for logs/code.
- Base typography: `18px/145%`; `16px` at widths up to `1024px`. H1 `56px` desktop / `36px` compact. H2 `24px` desktop / `20px` compact.
- Radius: code `4px`, counter `5px`, resource links `6px`.
- Shadow: `0 10px 15px -3px` plus `0 4px 6px -2px`.
- Main breakpoint: `1024px`.
- Current app width: `1126px`, centered, full viewport height.
- Theme mode: automatic via `prefers-color-scheme`.

## Raw source: `vite.config.ts`

```ts
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [vue(), tailwindcss()],
});
```

## Raw source: `src/style.css`

```css
:root {
  --text: #6b6375;
  --text-h: #08060d;
  --bg: #fff;
  --border: #e5e4e7;
  --code-bg: #f4f3ec;
  --accent: #aa3bff;
  --accent-bg: rgba(170, 59, 255, 0.1);
  --accent-border: rgba(170, 59, 255, 0.5);
  --social-bg: rgba(244, 243, 236, 0.5);
  --shadow:
    rgba(0, 0, 0, 0.1) 0 10px 15px -3px, rgba(0, 0, 0, 0.05) 0 4px 6px -2px;
  --sans: system-ui, 'Segoe UI', Roboto, sans-serif;
  --heading: system-ui, 'Segoe UI', Roboto, sans-serif;
  --mono: ui-monospace, Consolas, monospace;
  font: 18px/145% var(--sans);
  letter-spacing: 0.18px;
  color-scheme: light dark;
  color: var(--text);
  background: var(--bg);
}

@media (prefers-color-scheme: dark) {
  :root {
    --text: #9ca3af;
    --text-h: #f3f4f6;
    --bg: #16171d;
    --border: #2e303a;
    --code-bg: #1f2028;
    --accent: #c084fc;
    --accent-bg: rgba(192, 132, 252, 0.15);
    --accent-border: rgba(192, 132, 252, 0.5);
    --social-bg: rgba(47, 48, 58, 0.5);
  }
}

body { margin: 0; }

#app {
  width: 1126px;
  max-width: 100%;
  margin: 0 auto;
  min-height: 100svh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

@media (max-width: 1024px) {
  :root { font-size: 16px; }
}
```

The full stylesheet remains in `src/style.css` (296 lines); the compact raw block above captures the reusable token and shell portions relevant to new-page generation.
