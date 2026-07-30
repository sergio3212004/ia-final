<script setup lang="ts">
import type { Individual, Phase } from '../types/lab'
defineProps<{ generation: number; maxGenerations: number; phase: Phase; best: Individual; populationSize: number; mutationRate: number }>()
</script>
<template>
  <section class="mb-4 grid grid-cols-2 gap-px border border-line bg-line sm:grid-cols-4 xl:grid-cols-6">
    <div class="metric-cell"><span class="eyebrow">Generación</span><strong>{{ generation }} / {{ maxGenerations }}</strong></div>
    <div class="metric-cell"><span class="eyebrow">Fase</span><strong class="truncate">{{ phase }}</strong></div>
    <div class="metric-cell"><span class="eyebrow">Mejor x</span><strong class="font-mono">{{ best.x.toFixed(2) }}</strong></div>
    <div class="metric-cell"><span class="eyebrow">Mejor aptitud</span><strong class="font-mono text-positive">{{ best.fitness.toFixed(4) }}</strong></div>
    <div class="metric-cell hidden sm:flex"><span class="eyebrow">Población</span><strong>{{ populationSize }} individuos</strong></div>
    <div class="metric-cell hidden sm:flex"><span class="eyebrow">Mutación</span><strong>{{ Math.round(mutationRate * 100) }}% por bit</strong></div>
  </section>
</template>
