<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import type { Song } from '~/types'

const props = defineProps<{
  songs: Song[]
}>()

const BIN_SIZE_SECONDS = 30

const histogram = computed(() => {
  const seconds = props.songs.map((song) => Math.round(song.duration_ms / 1000))
  if (seconds.length === 0) {
    return { labels: [] as string[], counts: [] as number[] }
  }

  const min =
    Math.floor(Math.min(...seconds) / BIN_SIZE_SECONDS) * BIN_SIZE_SECONDS
  const max =
    Math.ceil(Math.max(...seconds) / BIN_SIZE_SECONDS) * BIN_SIZE_SECONDS
  const bucketCount = Math.max(1, (max - min) / BIN_SIZE_SECONDS)

  const counts = new Array(bucketCount).fill(0)
  for (const value of seconds) {
    let idx = Math.floor((value - min) / BIN_SIZE_SECONDS)
    if (idx >= bucketCount) idx = bucketCount - 1
    counts[idx]++
  }

  const labels = counts.map(
    (_, i) =>
      `${min + i * BIN_SIZE_SECONDS}-${min + (i + 1) * BIN_SIZE_SECONDS}s`
  )

  return { labels, counts }
})

const chartData = computed(() => ({
  labels: histogram.value.labels,
  datasets: [
    {
      label: 'Songs',
      data: histogram.value.counts,
      backgroundColor: 'rgba(44, 107, 237, 0.7)',
      borderRadius: 2
    }
  ]
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: { title: { display: true, text: 'Duration (seconds)' } },
    y: { title: { display: true, text: 'Count' }, beginAtZero: true }
  },
  plugins: { legend: { display: false } }
}
</script>

<template>
  <div class="h-72">
    <Bar :data="chartData" :options="options" />
  </div>
</template>
