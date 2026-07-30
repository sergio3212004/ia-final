<script setup lang="ts">
import type { RunStatus } from '../types/lab'

defineProps<{ connected: boolean; runId: string; seed: number; status: RunStatus }>()
defineEmits<{ openParameters: [] }>()
</script>

<template>
  <header class="sticky top-0 z-40 flex h-14 items-center justify-between border-b border-line bg-white/95 px-4 backdrop-blur lg:px-6">
    <div class="flex items-center gap-3 lg:hidden">
      <span class="grid size-8 place-items-center bg-accent text-xs font-black text-white">OL</span>
      <div><p class="font-black tracking-tight">OPTILAB</p><p class="text-[10px] text-muted">Algoritmo genético</p></div>
    </div>
    <div class="hidden items-center gap-5 lg:flex">
      <span class="flex items-center gap-2 text-xs font-bold"><span class="size-2" :class="connected ? 'bg-positive' : 'bg-danger'"></span> Python: {{ connected ? 'conectado' : 'sin conexión' }}</span>
      <span class="eyebrow">RUN_ID <b class="ml-1 font-mono text-ink">{{ runId || 'SIN INICIAR' }}</b></span>
      <span class="eyebrow">SEMILLA <b class="ml-1 font-mono text-ink">{{ seed }}</b></span>
    </div>
    <div class="flex items-center gap-2">
      <span class="status-badge" :class="status === 'running' ? 'status-running' : 'status-paused'">{{ status }}</span>
      <button class="icon-button lg:hidden" aria-label="Abrir parámetros" @click="$emit('openParameters')">☰</button>
    </div>
  </header>
</template>
