# Page dependency trees

## `/` — Starter page

Entry: `src/App.vue`

Dependencies:

- `src/App.vue`
  - `src/components/HelloWorld.vue`
    - `src/assets/vite.svg`
    - `src/assets/vue.svg`
    - `src/assets/hero.png`
- `src/main.ts`
  - `src/style.css`

This is the only rendered page. There are no nested layouts, route-level views, or shared UI primitives.
