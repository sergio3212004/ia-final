<script setup lang="ts">
import AppHeader from './components/AppHeader.vue'
import AppSidebar from './components/AppSidebar.vue'
import EvaluationTable from './components/EvaluationTable.vue'
import LogPanel from './components/LogPanel.vue'
import MetricStrip from './components/MetricStrip.vue'
import MobileNavigation from './components/MobileNavigation.vue'
import ObjectiveChart from './components/ObjectiveChart.vue'
import ParameterPanel from './components/ParameterPanel.vue'
import PhasePanel from './components/PhasePanel.vue'
import { useGeneticLab } from './composables/useGeneticLab'
import type { WorkspaceView } from './types/lab'

const lab = useGeneticLab()
const views: { id: WorkspaceView; label: string }[] = [
  { id: 'graph', label: 'Gráfico' }, { id: 'table', label: 'Tabla' },
  { id: 'steps', label: 'Pasos' }, { id: 'logs', label: 'Logs' },
]
</script>

<template>
  <div class="min-h-dvh overflow-x-hidden bg-canvas text-ink lg:flex">
    <AppSidebar :connected="lab.connected.value" />
    <div class="min-w-0 flex-1">
      <AppHeader :connected="lab.connected.value" :run-id="lab.runId.value" :seed="lab.parameters.seed" :status="lab.status.value" @open-parameters="lab.parametersOpen.value = true" />
      <main class="mx-auto w-full max-w-[1660px] px-3 pb-28 pt-4 sm:px-5 lg:px-6 lg:pb-8">
        <section class="mb-4 flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
          <div><p class="eyebrow mb-2">Repositorio / Genéticos / Ejecución</p><h1 class="text-2xl font-black tracking-[-0.035em] sm:text-3xl">Prueba de escritorio</h1><p class="mt-1 text-sm text-muted">Maximizar <span class="font-mono font-bold text-ink">f(x) = 1 − x²</span> · Guía AG</p></div>
          <div class="flex flex-wrap gap-2">
            <button class="button-secondary xl:hidden" @click="lab.parametersOpen.value = true">Configurar</button>
            <button class="button-primary" :disabled="!lab.connected.value" @click="lab.runToEnd">{{ lab.status.value === 'running' ? 'Ejecutando…' : 'Ejecutar' }}</button>
            <button class="button-secondary" @click="lab.advancePhase">Avanzar fase</button>
            <button class="button-secondary" :disabled="!lab.connected.value" @click="lab.advanceGeneration">Siguiente generación</button>
            <button v-if="lab.runId.value" class="button-secondary !border-danger !text-danger" @click="lab.stop">Detener</button>
          </div>
        </section>
        <p v-if="lab.error.value" class="mb-4 border border-danger bg-danger-soft p-3 text-sm text-danger">{{ lab.error.value }}</p>
        <MetricStrip :generation="lab.generation.value" :max-generations="lab.parameters.generations" :phase="lab.activePhase.value" :best="lab.best.value" :population-size="lab.parameters.population_size" :mutation-rate="lab.parameters.mutation_rate" />

        <div class="sticky top-14 z-30 -mx-3 mb-4 grid grid-cols-4 border-y border-line bg-surface px-3 sm:-mx-5 sm:px-5 lg:hidden">
          <button v-for="view in views" :key="view.id" class="min-h-12 border-b-2 text-xs font-bold" :class="lab.activeView.value === view.id ? 'border-accent bg-white text-accent' : 'border-transparent text-muted'" @click="lab.activeView.value = view.id">{{ view.label }}</button>
        </div>

        <div class="grid gap-4 lg:grid-cols-12">
          <aside class="hidden lg:col-span-3 lg:block xl:col-span-2">
            <div class="panel sticky top-18"><div class="panel-heading"><div><p class="eyebrow">Parámetros</p><h2 class="font-bold">Configuración</h2></div></div><ParameterPanel :parameters="lab.parameters" @reset="lab.resetRun" /></div>
          </aside>

          <section class="space-y-4 lg:col-span-6 xl:col-span-7" :class="{ 'hidden lg:block': lab.activeView.value === 'logs' || lab.activeView.value === 'steps' }">
            <div v-show="lab.activeView.value === 'graph' || lab.activeView.value === 'table'" :class="{ 'hidden lg:block': lab.activeView.value === 'table' }">
              <ObjectiveChart :population="lab.population.value" :selected-id="lab.selectedIndividual.value" :best="lab.best.value" :convergence="lab.convergence.value" @select="lab.selectedIndividual.value = $event" />
            </div>
            <div v-show="lab.activeView.value === 'table'">
              <EvaluationTable :population="lab.population.value" :best-id="lab.best.value.id" :selected-id="lab.selectedIndividual.value" :table-mode="lab.tableMode.value" @select="lab.selectedIndividual.value = $event" @toggle-mode="lab.tableMode.value = lab.tableMode.value === 'cards' ? 'original' : 'cards'" />
            </div>
          </section>

          <aside class="space-y-4 lg:col-span-3 xl:col-span-3" :class="{ 'hidden lg:block': lab.activeView.value !== 'logs' && lab.activeView.value !== 'steps' }">
            <div v-show="lab.activeView.value !== 'logs'"><PhasePanel :active-phase="lab.activePhase.value" :mutation-rate="lab.parameters.mutation_rate" @select="lab.activePhase.value = $event" @advance="lab.advancePhase" /></div>
            <div v-show="lab.activeView.value !== 'steps'"><LogPanel :events="lab.events.value" :generation="lab.generation.value" :connected="lab.connected.value" /></div>
          </aside>
        </div>
      </main>
    </div>

    <div v-if="lab.parametersOpen.value" class="fixed inset-0 z-50 bg-black/35" @click.self="lab.parametersOpen.value = false">
      <section class="absolute inset-y-0 right-0 w-[min(92vw,420px)] overflow-y-auto bg-surface p-5 shadow-2xl">
        <div class="mb-6 flex items-center justify-between"><div><p class="eyebrow">Algoritmo genético</p><h2 class="text-xl font-black">Parámetros</h2></div><button class="icon-button" @click="lab.parametersOpen.value = false">×</button></div>
        <ParameterPanel :parameters="lab.parameters" compact />
        <button class="button-primary mt-5 w-full" @click="lab.resetRun(); lab.parametersOpen.value = false">Aplicar y reiniciar</button>
      </section>
    </div>
    <MobileNavigation :status="lab.status.value" @run="lab.runToEnd" @logs="lab.activeView.value = 'logs'" @parameters="lab.parametersOpen.value = true" />
  </div>
</template>
