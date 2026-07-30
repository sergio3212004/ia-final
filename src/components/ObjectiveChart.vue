<script setup lang="ts">
import { computed } from 'vue'
import type { ConvergencePoint, Individual } from '../types/lab'

const props = defineProps<{ population: Individual[]; selectedId: string; best: Individual; convergence: ConvergencePoint[] }>()
defineEmits<{ select: [id: string] }>()

const selected = computed(() => props.population.find((item) => item.id === props.selectedId) ?? props.best)
const chartX = (x: number) => 50 + ((x + 5) / 10) * 500
const chartY = (y: number) => 28 + ((1 - Math.max(-10, Math.min(1, y))) / 11) * 230
const objectivePath = computed(() => `M ${Array.from({ length: 101 }, (_, index) => {
  const x = -5 + index / 10
  return `${chartX(x)},${chartY(1 - x * x)}`
}).join(' L ')}`)
const convergencePath = computed(() => props.convergence.map((point, index) => {
  const x = 20 + index * Math.max(20, 360 / Math.max(1, props.convergence.length - 1))
  const y = 100 - point.best * 75
  return `${index === 0 ? 'M' : 'L'} ${x} ${y}`
}).join(' '))
</script>

<template>
  <article class="panel overflow-hidden">
    <div class="panel-heading"><div><p class="eyebrow">Función objetivo</p><h2 class="font-bold">Individuos sobre f(x) = 1 − x²</h2></div></div>
    <div class="p-3 sm:p-5">
      <svg class="min-h-[280px] w-full bg-white" viewBox="0 0 600 300" role="img" aria-label="Función objetivo con población">
        <g stroke="#deddd7" stroke-width="1"><line v-for="x in [50,150,250,350,450,550]" :key="x" :x1="x" y1="20" :x2="x" y2="270"/><line v-for="y in [30,90,150,210,270]" :key="y" x1="50" :y1="y" x2="550" :y2="y"/></g>
        <line x1="50" y1="50" x2="550" y2="50" stroke="#77756f"/><line x1="300" y1="20" x2="300" y2="270" stroke="#77756f"/>
        <path :d="objectivePath" fill="none" stroke="#1351aa" stroke-width="3"/>
        <g v-for="item in population" :key="item.id" class="cursor-pointer" role="button" tabindex="0" @click="$emit('select', item.id)" @keydown.enter="$emit('select', item.id)">
          <circle :cx="chartX(item.x)" :cy="chartY(item.objective)" :r="selectedId === item.id ? 9 : 7" :fill="item.id === best.id ? '#16744a' : '#fff'" :stroke="selectedId === item.id ? '#141414' : '#1351aa'" stroke-width="3"/>
          <text :x="chartX(item.x)+10" :y="chartY(item.objective)-9" class="fill-ink text-[12px] font-bold">{{ item.id }}</text>
        </g>
      </svg>
      <div class="mt-3 grid gap-2 border border-line bg-surface p-3 sm:grid-cols-4">
        <div><p class="eyebrow">Seleccionado</p><p class="font-bold">{{ selected.id }}</p></div>
        <div><p class="eyebrow">Cromosoma</p><p class="font-mono text-xs font-bold">{{ selected.chromosome }}</p></div>
        <div><p class="eyebrow">x / f(x)</p><p class="font-mono text-xs">{{ selected.x }} / {{ selected.objective }}</p></div>
        <div><p class="eyebrow">Aptitud</p><p class="font-mono font-bold text-positive">{{ selected.fitness }}</p></div>
      </div>
    </div>
  </article>
  <article class="panel mt-4">
    <div class="panel-heading"><div><p class="eyebrow">Evolución</p><h2 class="font-bold">Convergencia por generación</h2></div></div>
    <div class="p-4"><svg class="h-32 w-full" viewBox="0 0 410 115"><line x1="20" y1="100" x2="400" y2="100" stroke="#deddd7"/><path :d="convergencePath" fill="none" stroke="#1351aa" stroke-width="3"/></svg></div>
  </article>
</template>
