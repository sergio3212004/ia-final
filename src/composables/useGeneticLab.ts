import { computed, onMounted, reactive, ref } from 'vue'
import { checkHealth, completeRun, createRun, stepRun, stopRun } from '../services/api'
import { guideEvents, guidePopulation } from '../data/guidePreset'
import type { GeneticParameters, Phase, RunResponse, RunStatus, WorkspaceView } from '../types/lab'

export const phases: Phase[] = ['Población', 'Ruleta', 'Cruce', 'Mutación', 'Nueva población', 'Resumen']

export function useGeneticLab() {
  const parameters = reactive<GeneticParameters>({
    lower_bound: -5,
    upper_bound: 5,
    precision: 2,
    population_size: 4,
    generations: 20,
    mutation_rate: 0.10,
    crossover_rate: 1,
    seed: 492104,
    initial_population: [1.45, 0.98, -1.25, -0.57],
  })
  const activeView = ref<WorkspaceView>('graph')
  const activePhase = ref<Phase>('Población')
  const selectedIndividual = ref('i4')
  const parametersOpen = ref(false)
  const tableMode = ref<'cards' | 'original'>('cards')
  const runId = ref('')
  const status = ref<RunStatus>('idle')
  const connected = ref(false)
  const error = ref('')
  const generation = ref(0)
  const population = ref([...guidePopulation])
  const events = ref([...guideEvents])
  const convergence = ref([{ generation: 0, best: 0.7548, mean: 0.4994 }])

  const best = computed(() => population.value.reduce((winner, item) => item.fitness > winner.fitness ? item : winner))
  const selected = computed(() => population.value.find((item) => item.id === selectedIndividual.value) ?? best.value)
  const phaseIndex = computed(() => phases.indexOf(activePhase.value))

  function applyResponse(response: RunResponse) {
    runId.value = response.run_id
    status.value = response.status
    generation.value = response.snapshot.generation
    population.value = response.snapshot.population
    events.value = response.snapshot.events
    convergence.value = response.snapshot.convergence
    selectedIndividual.value = response.snapshot.best.id
  }

  async function ensureRun() {
    if (runId.value) return runId.value
    error.value = ''
    const response = await createRun(parameters)
    applyResponse(response)
    return response.run_id
  }

  async function advanceGeneration() {
    try {
      const id = await ensureRun()
      applyResponse(await stepRun(id))
      activePhase.value = 'Resumen'
    } catch (cause) {
      error.value = cause instanceof Error ? cause.message : 'No se pudo avanzar la ejecución.'
      status.value = 'failed'
    }
  }

  function advancePhase() {
    const index = phaseIndex.value
    if (index === phases.length - 1) {
      void advanceGeneration()
    } else {
      activePhase.value = phases[index + 1]
    }
    activeView.value = 'steps'
  }

  async function runToEnd() {
    try {
      const id = await ensureRun()
      status.value = 'running'
      applyResponse(await completeRun(id))
    } catch (cause) {
      error.value = cause instanceof Error ? cause.message : 'No se pudo completar la ejecución.'
      status.value = 'failed'
    }
  }

  async function stop() {
    if (!runId.value) return
    try {
      applyResponse(await stopRun(runId.value))
    } catch (cause) {
      error.value = cause instanceof Error ? cause.message : 'No se pudo detener la ejecución.'
    }
  }

  function resetRun() {
    runId.value = ''
    status.value = 'idle'
    generation.value = 0
    population.value = [...guidePopulation]
    events.value = [...guideEvents]
    convergence.value = [{ generation: 0, best: 0.7548, mean: 0.4994 }]
  }

  onMounted(async () => {
    try {
      connected.value = (await checkHealth()).status === 'ok'
    } catch {
      connected.value = false
    }
  })

  return {
    parameters, activeView, activePhase, selectedIndividual, parametersOpen, tableMode,
    runId, status, connected, error, generation, population, events, convergence,
    best, selected, phaseIndex, advancePhase, advanceGeneration, runToEnd, stop, resetRun,
  }
}
