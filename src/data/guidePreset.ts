import type { AlgorithmEvent, Individual } from '../types/lab'

export const guidePopulation: Individual[] = [
  { id: 'i1', x: 1.45, encoded: 645, chromosome: '1010000101', objective: -1.1025, distance: 2.1025, fitness: 0.3223, probability: 0.1614, interval: '[0.0000, 0.1614)' },
  { id: 'i2', x: 0.98, encoded: 598, chromosome: '1001010110', objective: 0.0396, distance: 0.9604, fitness: 0.5101, probability: 0.2554, interval: '[0.1614, 0.4168)' },
  { id: 'i3', x: -1.25, encoded: 375, chromosome: '0101110111', objective: -0.5625, distance: 1.4375, fitness: 0.4103, probability: 0.2054, interval: '[0.4168, 0.6222)' },
  { id: 'i4', x: -0.57, encoded: 443, chromosome: '0110111011', objective: 0.6751, distance: 0.3249, fitness: 0.7548, probability: 0.3779, interval: '[0.6222, 1.0000]' },
]

export const guideEvents: AlgorithmEvent[] = [
  { event_id: 1, timestamp: '', phase: 'population', operation: 'initial_population', step: 0, explanation: 'Población inicial codificada: x × 100 + 500. Se requieren 10 bits.', inputs: {}, outputs: {}, objective_current: null, objective_best: null },
  { event_id: 2, timestamp: '', phase: 'evaluation', operation: 'population_evaluation', step: 0, explanation: 'Aptitud calculada con 1 / (1 + distancia).', inputs: {}, outputs: {}, objective_current: 0.6751, objective_best: 0.7548 },
  { event_id: 3, timestamp: '', phase: 'selection', operation: 'roulette_selection', step: 0, explanation: 'random 0.4789 pertenece a [0.4168, 0.6222): seleccionado i3.', inputs: {}, outputs: {}, objective_current: null, objective_best: null },
  { event_id: 4, timestamp: '', phase: 'crossover', operation: 'one_point_crossover', step: 0, explanation: 'random 0.7124 selecciona el punto de corte 7.', inputs: {}, outputs: {}, objective_current: null, objective_best: null },
  { event_id: 5, timestamp: '', phase: 'mutation', operation: 'bit_flip_mutation', step: 0, explanation: 'Cada bit muta cuando random < 0.10.', inputs: {}, outputs: {}, objective_current: null, objective_best: null },
]
