export type WorkspaceView = 'graph' | 'table' | 'steps' | 'logs'
export type Phase = 'Población' | 'Ruleta' | 'Cruce' | 'Mutación' | 'Nueva población' | 'Resumen'
export type RunStatus = 'idle' | 'paused' | 'running' | 'completed' | 'stopped' | 'failed'

export interface Individual {
  id: string
  x: number
  encoded: number
  chromosome: string
  objective: number
  distance: number
  fitness: number
  probability: number
  interval: string
}

export interface AlgorithmEvent {
  event_id: number
  timestamp: string
  phase: string
  operation: string
  step: number
  explanation: string
  inputs: Record<string, unknown>
  outputs: Record<string, unknown>
  objective_current: number | null
  objective_best: number | null
}

export interface ConvergencePoint {
  generation: number
  best: number
  mean: number
}

export interface RunSnapshot {
  generation: number
  max_generations: number
  bits: number
  population: Individual[]
  best: Individual
  convergence: ConvergencePoint[]
  event_count: number
  events: AlgorithmEvent[]
}

export interface RunResponse {
  run_id: string
  status: Exclude<RunStatus, 'idle'>
  snapshot: RunSnapshot
}

export interface GeneticParameters {
  lower_bound: number
  upper_bound: number
  precision: number
  population_size: number
  generations: number
  mutation_rate: number
  crossover_rate: number
  seed: number
  initial_population: number[]
}
