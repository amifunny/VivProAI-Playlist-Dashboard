<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import { toast } from 'vue-sonner'
import { usePlaylistApi } from '~/composables/apis/usePlaylistApi'
import { usePlaylistStore } from '~/store/playlist'
import type { Song } from '~/types'

const query = ref('')
const searching = ref(false)
const loading = ref(false)

const playlistStore = usePlaylistStore()
const data = computed(() => playlistStore.playlist.value)
const totalSongs = computed(() => playlistStore.totalSongs.value)
const currentPage = ref(1)
const pageSize = ref(10)
const isSearchMode = ref(false)
const { fetchPaginated, searchByTitle, updateRating } = usePlaylistApi()
const ratingLoadingSongId = ref<string | null>(null)
const hoverSongId = ref<string | null>(null)
const hoverStar = ref(0)

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
  playlistStore.totalSongs.value = 1
}
</script>
<template>
  <div class="space-y-10">
    <p class="font-semibold text-2xl" id="playlist-table">Table</p>
    <div class="p-4 bg-white rounded shadow-md space-y-4">
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
      <UTable
        :columns="columns"
        :data="tableData"
        class="flex-1 border border-solid border-gray-400 rounded-md">
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
