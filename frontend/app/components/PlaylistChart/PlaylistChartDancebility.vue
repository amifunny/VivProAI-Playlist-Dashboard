<script setup lang="ts">
import { Scatter } from 'vue-chartjs'
import type { Song } from '~/types'

const props = defineProps<{
  songs: Song[]
}>()

const chartData = computed(() => ({
  datasets: [
    {
      label: 'Songs',
      data: props.songs.map((song, index) => ({
        x: index + 1,
        y: song.danceability,
        title: song.title
      })),
      backgroundColor: 'rgba(44, 107, 237, 0.65)',
      pointRadius: 4
    }
  ]
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      title: { display: true, text: 'Song index' }
    },
    y: {
      title: { display: true, text: 'Danceability' },
      min: 0,
      max: 1
    }
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (ctx: any) => `${ctx.raw.title}: ${ctx.raw.y}`
      }
    }
  }
}
</script>

<template>
  <div class="h-72">
    <Scatter :data="chartData" :options="options" />
  </div>
</template>
