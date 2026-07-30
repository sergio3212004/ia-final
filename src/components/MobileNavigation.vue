<script setup lang="ts">
import type { RunStatus } from '../types/lab'
defineProps<{ status: RunStatus }>()
defineEmits<{ run: []; logs: []; parameters: [] }>()
</script>
<template>
  <nav class="fixed inset-x-0 bottom-0 z-40 grid grid-cols-5 border-t border-line bg-white pb-[env(safe-area-inset-bottom)] lg:hidden">
    <button class="mobile-nav-item"><span>⌂</span>Inicio</button><button class="mobile-nav-item text-accent"><span>⌬</span>Algoritmo</button>
    <button class="mobile-nav-run" @click="$emit('run')"><span>{{ status === 'running' ? 'Ⅱ' : '▶' }}</span>{{ status === 'running' ? 'Pausar' : 'Ejecutar' }}</button>
    <button class="mobile-nav-item" @click="$emit('logs')"><span>&gt;_</span>Logs</button><button class="mobile-nav-item" @click="$emit('parameters')"><span>•••</span>Más</button>
  </nav>
</template>
