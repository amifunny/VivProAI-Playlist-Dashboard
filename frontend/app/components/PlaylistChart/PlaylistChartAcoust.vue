<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import type { Song } from '~/types'

const props = defineProps<{
  songs: Song[]
}>()

const songsByIndex = computed(() =>
  [...props.songs].sort((a, b) => Number(a.index) - Number(b.index))
)

const chartData = computed(() => ({
  labels: songsByIndex.value.map((song) => song.title),
  datasets: [
    {
      label: 'Acousticness',
      data: songsByIndex.value.map((song) => song.acousticness),
      backgroundColor: 'rgba(44, 107, 237, 0.7)',
      borderRadius: 2
    }
  ]
}))

const options = {
  indexAxis: 'x' as const,
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: { title: { display: true, text: 'Acousticness' }, beginAtZero: true },
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
