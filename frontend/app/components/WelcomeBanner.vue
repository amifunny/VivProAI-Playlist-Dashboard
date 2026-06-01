<script setup lang="ts">
function scrollDown() {
  console.log(document.getElementById('playlist-table'))
  document
    .getElementById('playlist-table')
    ?.scrollIntoView({ behavior: 'smooth' })
}
</script>
<template>
  <section
    class="h-screen items-center flex welcome-banner-bg relative overflow-hidden px-8 md:px-0">
    <div class="m-auto max-w-5xl lg:w-5xl space-y-8 text-white">
      <div
        class="inline-flex rounded-full bg-white/10 px-4 py-2 text-xs font-semibold uppercase tracking-wider text-emerald-100 backdrop-blur-sm">
        Playlist Data Platform
      </div>

      <div class="space-y-6">
        <div class="flex items-center gap-4 text-primary">
          <span class="size-20 animate-disc-spin">
            <svg
              fill="currentColor"
              viewBox="-2 -2 24 24"
              xmlns="http://www.w3.org/2000/svg"
              preserveAspectRatio="xMinYMin"
              class="jam jam-disc">
              <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
              <g
                id="SVGRepo_tracerCarrier"
                stroke-linecap="round"
                stroke-linejoin="round"></g>
              <g id="SVGRepo_iconCarrier">
                <path
                  d="M10 20C4.477 20 0 15.523 0 10S4.477 0 10 0s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16zm7-8a6.99 6.99 0 0 1-2.89 5.666l-.53-.796L13 14a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4l1.2-1.6A6.99 6.99 0 0 1 17 10zm-7 3a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm0-2a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"></path>
              </g>
            </svg>
          </span>
          <h2 class="text-5xl font-bold text-white md:text-6xl">PlayList</h2>
        </div>

        <p
          class="max-w-xl text-base font-medium leading-relaxed text-slate-200 md:text-lg">
          Browse through playlists, songs and give rating. Explore and visualize
          metrics of your favourite songs as well.
        </p>
      </div>

      <button
        type="button"
        class="rounded-lg cursor-pointer bg-white px-5 py-2.5 text-sm font-semibold text-slate-900 hover:bg-emerald-50"
        @click="scrollDown">
        Start exploring
      </button>
    </div>
  </section>
</template>

<style scoped>
.welcome-banner-bg {
  background-image: url('/welcome-banner-green.png');
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}

.animate-disc-spin {
  animation: disc-spin 8s linear infinite;
}

@keyframes disc-spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
