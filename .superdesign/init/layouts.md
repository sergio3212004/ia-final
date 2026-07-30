# Layouts

## `src/App.vue`

Root application shell. It currently delegates the entire render tree to the starter component and has no navigation, sidebar, header, or footer.

```vue
<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <HelloWorld />
</template>
```

## `src/main.ts`

Application mount and global stylesheet entry.

```ts
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

createApp(App).mount('#app')
```
