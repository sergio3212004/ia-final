<script setup lang="ts">
import type { Individual } from '../types/lab'
defineProps<{ population: Individual[]; bestId: string; selectedId: string; tableMode: 'cards' | 'original' }>()
defineEmits<{ select: [id: string]; toggleMode: [] }>()
</script>
<template>
  <article class="panel overflow-hidden">
    <div class="panel-heading"><div><p class="eyebrow">Datos calculados</p><h2 class="font-bold">Población y evaluación</h2></div><button class="text-xs font-bold text-accent lg:hidden" @click="$emit('toggleMode')">{{ tableMode === 'cards' ? 'Tabla original' : 'Vista tarjetas' }}</button></div>
    <div v-if="tableMode === 'cards'" class="grid gap-3 p-3 sm:grid-cols-2 lg:hidden">
      <button v-for="item in population" :key="item.id" class="data-card text-left" :class="{ 'border-accent ring-1 ring-accent': selectedId === item.id }" @click="$emit('select', item.id)">
        <div class="mb-3 flex justify-between"><strong>{{ item.id }} · x={{ item.x }}</strong><span v-if="item.id === bestId" class="source-badge source-good">Mejor</span></div>
        <dl class="grid grid-cols-2 gap-2 text-xs"><dt>Entero</dt><dd>{{ item.encoded }}</dd><dt>Cromosoma</dt><dd class="font-mono">{{ item.chromosome }}</dd><dt>f(x)</dt><dd>{{ item.objective }}</dd><dt>Aptitud</dt><dd>{{ item.fitness }}</dd><dt>Prob.</dt><dd>{{ item.probability.toFixed(4) }}</dd><dt>Intervalo</dt><dd class="col-span-2 font-mono">{{ item.interval }}</dd></dl>
      </button>
    </div>
    <div :class="tableMode === 'cards' ? 'hidden lg:block' : 'block'" class="overflow-x-auto">
      <table class="data-table min-w-[900px]"><thead><tr><th>Ind.</th><th>x</th><th>Entero</th><th>Cromosoma</th><th>f(x)</th><th>Distancia</th><th>Aptitud</th><th>Prob.</th><th>Intervalo</th></tr></thead><tbody>
        <tr v-for="item in population" :key="item.id" :class="{ 'bg-positive-soft': item.id === bestId }" @click="$emit('select', item.id)"><td class="font-bold">{{ item.id }}</td><td>{{ item.x }}</td><td>{{ item.encoded }}</td><td class="font-mono">{{ item.chromosome }}</td><td>{{ item.objective }}</td><td>{{ item.distance }}</td><td>{{ item.fitness }}</td><td>{{ item.probability.toFixed(4) }}</td><td class="font-mono">{{ item.interval }}</td></tr>
      </tbody></table>
    </div>
  </article>
</template>
