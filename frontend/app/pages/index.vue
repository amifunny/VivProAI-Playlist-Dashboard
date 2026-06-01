<script setup lang="ts">
import { Toaster } from 'vue-sonner'
</script>
<template>
  <div class="bg-neutral">
    <div class="pb-20">
      <WelcomeBanner />
      <div class="max-w-5xl lg:w-5xl my-10 mx-auto space-y-10 px-4 md:px-0">
        <PlaylistDashboard />
        <PlaylistVisualize />
      </div>
    </div>
    <Toaster :close-button="true" position="top-center" :rich-colors="true" />
  </div>
</template>
