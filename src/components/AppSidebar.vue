<script setup lang="ts">
defineProps<{ connected: boolean }>()
</script>

<template>
  <aside class="hidden min-h-dvh w-56 shrink-0 border-r border-line bg-surface lg:flex lg:flex-col">
    <div class="flex h-18 items-center gap-3 border-b border-line px-6">
      <span class="grid size-8 place-items-center bg-accent text-sm font-black text-white">OL</span>
      <div><p class="text-lg font-black tracking-[-0.04em]">OPTILAB</p><p class="eyebrow">Metaheurísticas</p></div>
    </div>
    <nav class="flex-1 py-5 text-sm">
      <a class="nav-item" href="#"><span>⌂</span> Dashboard</a>
      <p class="eyebrow mb-2 mt-6 px-6">Algoritmos</p>
      <a class="nav-item nav-item-active" href="#"><span>⌬</span> Genéticos</a>
      <a class="nav-item" href="#"><span>▤</span> Búsqueda Tabú</a>
      <a class="nav-item" href="#"><span>♟</span> Colonia de hormigas</a>
      <p class="eyebrow mb-2 mt-7 px-6">Laboratorio</p>
      <a class="nav-item" href="#"><span>↺</span> Historial</a>
      <a class="nav-item" href="#"><span>?</span> Guía</a>
    </nav>
    <div class="border-t border-line p-4 text-xs text-muted">
      <span class="mr-2 inline-block size-2" :class="connected ? 'bg-positive' : 'bg-danger'"></span>
      Python {{ connected ? 'conectado' : 'desconectado' }}
    </div>
  </aside>
</template>
