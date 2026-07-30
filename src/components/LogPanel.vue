<script setup lang="ts">
import type { AlgorithmEvent } from '../types/lab'
defineProps<{ events: AlgorithmEvent[]; generation: number; connected: boolean }>()
const tone = (phase: string) => phase === 'evaluation' || phase === 'replacement' ? 'log-green' : phase === 'mutation' || phase === 'selection' ? 'log-amber' : 'log-blue'
</script>
<template>
  <article class="overflow-hidden border border-[#303640] bg-log text-log-text">
    <div class="flex items-center justify-between border-b border-[#303640] px-4 py-3"><div><p class="eyebrow !text-log-muted">Salida estructurada</p><h2 class="font-bold">Logs de ejecución</h2></div><span class="font-mono text-xs" :class="connected ? 'text-positive' : 'text-danger'">● {{ connected ? 'LIVE' : 'LOCAL' }}</span></div>
    <div class="max-h-[560px] space-y-1 overflow-y-auto p-2">
      <div v-for="event in events" :key="event.event_id" class="log-row"><span class="log-index">{{ String(event.event_id).padStart(2,'0') }}</span><span class="min-w-0"><span class="flex gap-2"><b :class="tone(event.phase)">[{{ event.phase.toUpperCase() }}]</b><small class="font-mono text-log-muted">G{{ event.step }}</small></span><strong class="mt-1 block text-xs">{{ event.operation }}</strong><span class="mt-1 block text-xs leading-5 text-log-muted">{{ event.explanation }}</span></span></div>
    </div>
    <div class="border-t border-[#303640] p-3 text-xs text-log-muted">{{ events.length }} eventos · generación {{ generation }}</div>
  </article>
</template>
