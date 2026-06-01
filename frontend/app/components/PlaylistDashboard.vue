<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import { toast } from 'vue-sonner'
import { usePlaylistApi } from '~/composables/apis/usePlaylistApi'
import { usePlaylistStore } from '~/store/playlist'
import type { Song } from '~/types'

const query = ref('')
const searching = ref(false)
const loading = ref(false)
const csvLoading = ref(false)

const playlistStore = usePlaylistStore()
const data = computed(() => playlistStore.playlist.value)
const totalSongs = computed(() => playlistStore.totalSongs.value)
const currentPage = ref(1)
const pageSize = ref(10)
const isSearchMode = ref(false)
const { fetchAll, fetchPaginated, searchByTitle, updateRating } =
  usePlaylistApi()
const ratingLoadingSongId = ref<string | null>(null)
const hoverSongId = ref<string | null>(null)
const hoverStar = ref(0)
const sortKey = ref<keyof TableRow>('index')
const sortDirection = ref<'asc' | 'desc'>('asc')

type TableRow = {
  index: number
  title: string
  id: string
  rating: number
  danceability: number
  acousticness: number
  energy: number
  mode: number
  tempo: number
  duration_ms: number
  num_sections: number
  num_segments: number
}

const tableData = computed<TableRow[]>(() =>
  data.value.map((song, index) => ({
    index: (currentPage.value - 1) * pageSize.value + index + 1,
    title: song.title,
    id: song.id,
    rating: song.rating,
    danceability: song.danceability,
    acousticness: song.acousticness,
    energy: song.energy,
    mode: song.mode,
    tempo: song.tempo,
    duration_ms: song.duration_ms,
    num_sections: song.num_sections,
    num_segments: song.num_segments
  }))
)

const columns: TableColumn<TableRow>[] = [
  { accessorKey: 'index', header: 'Index' },
  { accessorKey: 'title', header: 'Title' },
  { accessorKey: 'id', header: 'ID' },
  { accessorKey: 'rating', header: 'Rating' },
  { accessorKey: 'danceability', header: 'Danceability' },
  { accessorKey: 'acousticness', header: 'Acousticness' },
  { accessorKey: 'energy', header: 'Energy' },
  { accessorKey: 'mode', header: 'Mode' },
  { accessorKey: 'tempo', header: 'Tempo' },
  { accessorKey: 'duration_ms', header: 'Duration (ms)' },
  { accessorKey: 'num_sections', header: 'Sections' },
  { accessorKey: 'num_segments', header: 'Segments' }
]

const csvColumns: Array<{ key: keyof Song; label: string }> = [
  { key: 'index', label: 'index' },
  { key: 'id', label: 'id' },
  { key: 'title', label: 'title' },
  { key: 'rating', label: 'rating' },
  { key: 'danceability', label: 'danceability' },
  { key: 'acousticness', label: 'acousticness' },
  { key: 'energy', label: 'energy' },
  { key: 'mode', label: 'mode' },
  { key: 'tempo', label: 'tempo' },
  { key: 'duration_ms', label: 'duration_ms' },
  { key: 'num_sections', label: 'num_sections' },
  { key: 'num_segments', label: 'num_segments' }
]

const sortedTableData = computed<TableRow[]>(() => {
  const key = sortKey.value
  const direction = sortDirection.value === 'asc' ? 1 : -1

  return [...tableData.value].sort((a, b) => {
    const left = a[key]
    const right = b[key]

    if (typeof left === 'number' && typeof right === 'number') {
      return (left - right) * direction
    }

    return (
      String(left).localeCompare(String(right), undefined, {
        numeric: true,
        sensitivity: 'base'
      }) * direction
    )
  })
})

async function loadPage(page: number) {
  loading.value = true
  const response = await fetchPaginated({
    page,
    pageSize: pageSize.value
  })
  loading.value = false

  if (!response) return

  playlistStore.setPlaylist(response.items)
  playlistStore.totalSongs.value = response.total
}

onMounted(() => {
  loadPage(currentPage.value)
})

watch(currentPage, (page) => {
  if (isSearchMode.value) return
  loadPage(page)
})

async function handleRate(song: Song, rating: number) {
  if (ratingLoadingSongId.value) return

  const previous = song.rating
  song.rating = rating
  ratingLoadingSongId.value = song.id

  const response = await updateRating({
    songId: song.id,
    rating
  })

  ratingLoadingSongId.value = null

  if (!response) {
    song.rating = previous
    return
  }

  song.rating = response.rating
  toast.success('Rating updated')
}

function displayedRating(row: TableRow) {
  if (hoverSongId.value === row.id && hoverStar.value > 0) {
    return hoverStar.value
  }
  return row.rating
}

function toggleSort(column: keyof TableRow) {
  if (sortKey.value === column) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
    return
  }
  sortKey.value = column
  sortDirection.value = 'asc'
}

function sortIndicator(column: keyof TableRow) {
  if (sortKey.value !== column) return ''
  return sortDirection.value === 'asc' ? '↑' : '↓'
}

function toCsvValue(value: string | number) {
  const text = String(value ?? '')
  if (text.includes(',') || text.includes('"') || text.includes('\n')) {
    return `"${text.replaceAll('"', '""')}"`
  }
  return text
}

function buildCsv(songs: Song[]) {
  const header = csvColumns.map((column) => column.label).join(',')
  const rows = songs.map((song) =>
    csvColumns.map((column) => toCsvValue(song[column.key])).join(',')
  )
  return [header, ...rows].join('\n')
}

async function downloadCsv() {
  csvLoading.value = true

  let songs: Song[] = []
  if (isSearchMode.value) {
    songs = data.value
  } else {
    const response = await fetchAll()
    songs = response?.items ?? []
  }

  csvLoading.value = false

  if (songs.length === 0) {
    toast.error('No songs available to export')
    return
  }

  const blob = new Blob([buildCsv(songs)], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.setAttribute(
    'download',
    isSearchMode.value ? 'playlist-search.csv' : 'playlist-all.csv'
  )
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

async function searchSong() {
  const keyword = query.value.trim()

  if (!keyword) {
    isSearchMode.value = false
    await loadPage(currentPage.value)
    return
  }

  searching.value = true
  const result = await searchByTitle({ query: keyword })
  searching.value = false

  if (!result) return

  isSearchMode.value = true
  currentPage.value = 1
  playlistStore.setPlaylist(result.items)
  playlistStore.totalSongs.value = result.total
}
</script>
<template>
  <div class="space-y-10">
    <p class="font-semibold text-2xl" id="playlist-table">Table</p>
    <div class="p-4 bg-white rounded shadow-md space-y-4">
      <div class="flex justify-between items-center">
        <div class="space-x-4">
          <input
            class="border border-solid border-gray-400 py-2 px-4 rounded"
            v-model="query"
            type="search"
            placeholder="Search by song title"
            @keyup.enter="searchSong" />
          <button
            :disabled="searching"
            class="bg-primary text-white font-semibold py-[9px] px-4 cursor-pointer rounded"
            @click="searchSong">
            {{ searching ? 'Searching…' : 'Search' }}
          </button>
        </div>
        <button
          :disabled="csvLoading || loading || searching"
          class="bg-primary text-white font-semibold py-[9px] px-4 cursor-pointer rounded"
          @click="downloadCsv">
          {{ csvLoading ? 'Loading CSV…' : 'Download CSV' }}
        </button>
      </div>
      <UTable
        :columns="columns"
        :data="sortedTableData"
        class="flex-1 border border-solid border-gray-400 rounded-md">
        <template #index-header>
          <button
            class="w-[100px] cursor-pointer font-semibold"
            @click="toggleSort('index')"
            >Index {{ sortIndicator('index') }}</button
          >
        </template>
        <template #title-header>
          <button
            class="cursor-pointer font-semibold"
            @click="toggleSort('title')"
            >Title {{ sortIndicator('title') }}</button
          >
        </template>
        <template #id-header>
          <button class="cursor-pointer font-semibold" @click="toggleSort('id')"
            >ID {{ sortIndicator('id') }}</button
          >
        </template>
        <template #rating-header>
          <button
            class="cursor-pointer font-semibold"
            @click="toggleSort('rating')"
            >Rating {{ sortIndicator('rating') }}</button
          >
        </template>
        <template #danceability-header>
          <button
            class="cursor-pointer font-semibold"
            @click="toggleSort('danceability')"
            >Danceability {{ sortIndicator('danceability') }}</button
          >
        </template>
        <template #acousticness-header>
          <button
            class="cursor-pointer font-semibold"
            @click="toggleSort('acousticness')"
            >Acousticness {{ sortIndicator('acousticness') }}</button
          >
        </template>
        <template #energy-header>
          <button
            class="cursor-pointer font-semibold"
            @click="toggleSort('energy')"
            >Energy {{ sortIndicator('energy') }}</button
          >
        </template>
        <template #mode-header>
          <button
            class="cursor-pointer font-semibold"
            @click="toggleSort('mode')"
            >Mode {{ sortIndicator('mode') }}</button
          >
        </template>
        <template #tempo-header>
          <button
            class="cursor-pointer font-semibold"
            @click="toggleSort('tempo')"
            >Tempo {{ sortIndicator('tempo') }}</button
          >
        </template>
        <template #duration_ms-header>
          <button
            class="cursor-pointer font-semibold"
            @click="toggleSort('duration_ms')"
            >Duration (ms) {{ sortIndicator('duration_ms') }}</button
          >
        </template>
        <template #num_sections-header>
          <button
            class="cursor-pointer font-semibold"
            @click="toggleSort('num_sections')"
            >Sections {{ sortIndicator('num_sections') }}</button
          >
        </template>
        <template #num_segments-header>
          <button
            class="cursor-pointer font-semibold"
            @click="toggleSort('num_segments')"
            >Segments {{ sortIndicator('num_segments') }}</button
          >
        </template>
        <template #rating-cell="{ row }">
          <div class="flex items-center gap-1">
            <button
              v-for="star in 5"
              :key="star"
              data-test="`${star}`"
              class="cursor-pointer text-lg leading-none"
              :class="
                star <= displayedRating(row.original)
                  ? 'text-yellow-500'
                  : 'text-gray-300'
              "
              :disabled="ratingLoadingSongId === row.original.id"
              @mouseenter="
                () => {
                  hoverSongId = row.original.id
                  hoverStar = star
                }
              "
              @mouseleave="
                () => {
                  hoverSongId = null
                  hoverStar = 0
                }
              "
              @click="
                handleRate(
                  data.find((song) => song.id === row.original.id)!,
                  star
                )
              ">
              ★
            </button>
          </div>
        </template>
      </UTable>
      <div class="flex justify-end border-t border-default pt-4">
        <UPagination
          :page="currentPage"
          :items-per-page="pageSize"
          :total="totalSongs"
          :disabled="loading || searching || isSearchMode"
          @update:page="(p) => (currentPage = p)" />
      </div>
    </div>
  </div>
</template>
