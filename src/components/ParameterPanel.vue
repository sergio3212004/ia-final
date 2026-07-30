<script setup lang="ts">
import type { GeneticParameters } from '../types/lab'
defineProps<{ parameters: GeneticParameters; compact?: boolean }>()
defineEmits<{ reset: [] }>()
</script>
<template>
  <div class="space-y-5 p-4">
    <label class="field"><span>Preset</span><select><option>Guía AG · [-5,5] · 10 bits</option><option>Póster AG · [-1,1] · 8 bits</option></select></label>
    <div class="grid grid-cols-2 gap-3">
      <label class="field"><span>Mínimo</span><input v-model.number="parameters.lower_bound" type="number"></label>
      <label class="field"><span>Máximo</span><input v-model.number="parameters.upper_bound" type="number"></label>
    </div>
    <label class="field"><span>Población</span><input v-model.number="parameters.population_size" min="2" type="number"></label>
    <label class="field"><span>Generaciones</span><input v-model.number="parameters.generations" min="1" type="number"></label>
    <label class="field"><span>Selección</span><select><option>Ruleta</option></select></label>
    <label class="field"><span>Cruce</span><select><option>Un punto</option></select></label>
    <label class="field">
      <span class="flex justify-between">Mutación por bit <b>{{ Math.round(parameters.mutation_rate * 100) }}%</b></span>
      <input v-model.number="parameters.mutation_rate" class="accent-accent" min="0" max="1" step="0.01" type="range">
    </label>
    <label class="field"><span>Semilla</span><input v-model.number="parameters.seed" type="number"></label>
    <button v-if="!compact" class="button-secondary w-full" @click="$emit('reset')">Aplicar como nueva ejecución</button>
  </div>
</template>
