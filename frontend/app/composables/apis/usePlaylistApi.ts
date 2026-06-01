import type { Song } from '~/types'
import { toast } from 'vue-sonner'

export type PlaylistFetchAllResponse = {
  total: number
  items: Song[]
}

export type PlaylistPaginatedResponse = {
  total: number
  page: number
  page_size: number
  items: Song[]
}

export type PlaylistRatingUpdateResponse = {
  id: string
  rating: number
}

export const usePlaylistApi = () => {
  const base = useRuntimeConfig().public.apiBase as string

  async function fetchAll(): Promise<PlaylistFetchAllResponse | null> {
    let response: PlaylistFetchAllResponse | null = null

    try {
      response = await $fetch<PlaylistFetchAllResponse>(`${base}/api/songs/all`)
    } catch (error) {
      toast.error('Something went wrong!')
    }

    if (!response) {
      return null
    }

    return response
  }

  async function fetchPaginated(params: {
    page: number
    pageSize?: number
  }): Promise<PlaylistPaginatedResponse | null> {
    let response: PlaylistPaginatedResponse | null = null

    try {
      response = await $fetch<PlaylistPaginatedResponse>(`${base}/api/songs`, {
        query: {
          page: params.page,
          page_size: params.pageSize ?? 10
        }
      })
    } catch (error) {
      toast.error('Something went wrong!')
    }

    if (!response) {
      return null
    }

    return response
  }

  async function searchByTitle(params: {
    query: string
  }): Promise<PlaylistPaginatedResponse | null> {
    const query = params.query.trim()
    if (!query) {
      return null
    }

    let response: PlaylistPaginatedResponse | null = null

    try {
      response = await $fetch<PlaylistPaginatedResponse>(
        `${base}/api/songs/search`,
        {
          query: {
            title: query
          }
        }
      )
    } catch (error) {
      console.log('hello ----')
      toast.error('Something went wrong!')
    }

    if (!response) {
      return null
    }

    return response
  }

  async function updateRating(params: {
    songId: string
    rating: number
  }): Promise<PlaylistRatingUpdateResponse | null> {
    let response: PlaylistRatingUpdateResponse | null = null

    try {
      response = await $fetch<PlaylistRatingUpdateResponse>(
        `${base}/api/songs/${params.songId}/rating`,
        {
          method: 'PUT',
          body: {
            rating: params.rating
          }
        }
      )
    } catch (error) {
      toast.error('Something went wrong!')
    }

    if (!response) {
      return null
    }

    return response
  }

  return {
    fetchAll,
    fetchPaginated,
    searchByTitle,
    updateRating
  }
}
