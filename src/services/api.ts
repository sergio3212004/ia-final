import type { GeneticParameters, RunResponse } from '../types/lab'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...init?.headers },
  })
  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: 'Error de conexión con Python.' }))
    throw new Error(payload.detail ?? `Error HTTP ${response.status}`)
  }
  return response.json() as Promise<T>
}

export function checkHealth() {
  return request<{ status: string }>('/health')
}

export function createRun(parameters: GeneticParameters) {
  return request<RunResponse>('/api/runs', {
    method: 'POST',
    body: JSON.stringify({ ...parameters, auto_run: false }),
  })
}

export function stepRun(runId: string) {
  return request<RunResponse>(`/api/runs/${runId}/step`, { method: 'POST' })
}

export function completeRun(runId: string) {
  return request<RunResponse>(`/api/runs/${runId}/run`, { method: 'POST' })
}

export function stopRun(runId: string) {
  return request<RunResponse>(`/api/runs/${runId}/stop`, { method: 'POST' })
}
