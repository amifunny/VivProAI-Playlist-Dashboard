<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import type { Song } from '~/types'

const props = defineProps<{
  songs: Song[]
}>()

const sortedSongs = computed(() =>
  [...props.songs].sort((a, b) => Number(a.index) - Number(b.index))
)

const chartData = computed(() => ({
  labels: sortedSongs.value.map((song) => song.title),
  datasets: [
    {
      label: 'Tempo',
      data: sortedSongs.value.map((song) => song.tempo),
      backgroundColor: 'rgba(234, 88, 12, 0.75)',
      borderRadius: 2
    }
  ]
}))

const options = {
  indexAxis: 'x' as const,
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: { title: { display: true, text: 'Tempo (BPM)' }, beginAtZero: true },
    y: { ticks: { autoSkip: false, font: { size: 10 } } }
  },
  plugins: { legend: { display: false } }
}
</script>

<template>
  <div class="h-96">
    <Bar :data="chartData" :options="options" />
  </div>
</template>
