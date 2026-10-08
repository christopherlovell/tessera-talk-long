<script setup>
// Rendered on every slide (Slidev global layer), unless the slide's
// frontmatter sets `footer: false` (full-bleed video / mosaic slides).
import { computed } from 'vue'
import { useNav } from '@slidev/client'
const nav = useNav()
const show = computed(() => nav.currentSlideRoute.value?.meta?.slide?.frontmatter?.footer !== false)
</script>

<template>
  <footer v-if="show" class="deck-footer">
    <span>{{ $slidev.configs.author }}</span>
    <span>{{ $slidev.configs.conference }} · {{ $slidev.configs.date }}</span>
    <span>{{ $slidev.nav.currentPage }} / {{ $slidev.nav.total }}</span>
  </footer>
</template>
