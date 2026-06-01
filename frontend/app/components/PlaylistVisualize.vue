<script setup lang="ts">
import { usePlaylistStore } from '~/store/playlist'
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  PointElement,
  Tooltip
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  BarElement,
  Legend,
  Tooltip
)

const playlistStore = usePlaylistStore()
const songs = computed(() => playlistStore.playlist.value)
</script>
<template>
  <div class="space-y-10">
    <p class="font-semibold text-2xl">Charts</p>
    <div class="grid md:grid-cols-2 gap-4">
      <div class="bg-white shadow-md rounded-xl p-4 space-y-4">
        <h2 class="font-semibold">Danceability </h2>
        <PlaylistChartDancebility :songs="songs" />
      </div>
      <div class="bg-white shadow-md rounded-xl p-4 space-y-4">
        <h2 class="font-semibold">Duration (in seconds) </h2>
        <PlaylistChartDuration :songs="songs" />
      </div>
      <div class="bg-white shadow-md rounded-xl p-4 space-y-4">
        <h2 class="font-semibold">Acousticness</h2>
        <PlaylistChartAcoust :songs="songs" />
      </div>
      <div class="bg-white shadow-md rounded-xl p-4 space-y-4">
        <h2 class="font-semibold">Tempo</h2>
        <PlaylistChartTempo :songs="songs" />
      </div>
    </div>
  </div>
</template>
