import type { Song } from '~/types'

export const usePlaylistStore = () => {
  const playlist = useState<Song[]>('playlist-items', () => [])
  const totalSongs = useState<number>('playlist-total-songs', () => 0)

  function setPlaylist(songs: Song[]) {
    playlist.value = songs
  }

  function reset() {
    playlist.value = []
    totalSongs.value = 0
  }

  return {
    playlist,
    totalSongs,
    setPlaylist,
    reset
  }
}
