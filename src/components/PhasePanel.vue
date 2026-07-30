<script setup lang="ts">
import { phases } from '../composables/useGeneticLab'
import type { Phase } from '../types/lab'
defineProps<{ activePhase: Phase; mutationRate: number }>()
defineEmits<{ select: [phase: Phase]; advance: [] }>()
</script>
<template>
  <article class="panel">
    <div class="panel-heading"><div><p class="eyebrow">Prueba de escritorio</p><h2 class="font-bold">Fases de la generación</h2></div></div>
    <div class="grid grid-cols-3 border-b border-line sm:grid-cols-6 lg:grid-cols-3 xl:grid-cols-6">
      <button v-for="(phase,index) in phases" :key="phase" class="min-h-12 border-b-2 px-1 text-[10px] font-bold" :class="activePhase === phase ? 'border-accent bg-accent-soft text-accent' : 'border-transparent text-muted'" @click="$emit('select', phase)">{{ index+1 }}. {{ phase }}</button>
    </div>
    <div class="p-4 text-sm">
      <template v-if="activePhase === 'Población'"><p>Se transforma cada valor real en un entero positivo y después en binario.</p><div class="formula mt-3">entero = x × 100 + 500</div></template>
      <template v-else-if="activePhase === 'Ruleta'"><p>El random se ubica en los intervalos acumulados.</p><div class="formula mt-3">r = 0.4789 → i3</div></template>
      <template v-else-if="activePhase === 'Cruce'"><p>Cruce de un punto. Random 0.7124 → corte 7.</p><div class="formula mt-3">0101110 | 111</div></template>
      <template v-else-if="activePhase === 'Mutación'"><p>Cada bit se compara con pm = {{ mutationRate }}.</p><div class="mt-3 flex gap-1"><span v-for="(bit,index) in '1000010111'" :key="index" class="bit" :class="{ 'bit-mutated': index === 3 }">{{ bit }}</span></div></template>
      <template v-else-if="activePhase === 'Nueva población'"><p>Se descodifican los cromosomas y se evalúa la nueva población.</p><div class="formula mt-3">x = (entero − 500) / 100</div></template>
      <template v-else><p>Se registra el mejor individuo, la media y el criterio de terminación.</p></template>
      <button class="button-primary mt-4 w-full" @click="$emit('advance')">Avanzar fase</button>
    </div>
  </article>
</template>
