<script setup>
// Stacked figure stages that reveal themselves: the first `auto` images
// appear automatically (one every `delay` ms), then the next click
// shows the following image immediately and the rest continue on the
// same delay. Stepping back hides the click-gated images again.
// The slide still needs one click registered (a v-click element or
// `clicks: 1` in the frontmatter) for Slidev to hold the slide.
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useSlideContext } from '@slidev/client'

const props = defineProps({
  srcs: { type: Array, required: true },
  auto: { type: Number, default: 3 },      // images shown without a click
  delay: { type: Number, default: 2000 },  // ms between reveals
  height: { type: String, default: '28rem' },
})

const { $clicks } = useSlideContext()
const shown = ref(1)
let timers = []
const clearTimers = () => { timers.forEach(clearTimeout); timers = [] }

// step shown up to `target`, one image per delay (first step also delayed)
function rollTo(target) {
  const step = () => {
    if (shown.value < target) {
      shown.value++
      if (shown.value < target) timers.push(setTimeout(step, props.delay))
    }
  }
  timers.push(setTimeout(step, props.delay))
}

onMounted(() => {
  if ($clicks.value >= 1) {
    shown.value = props.srcs.length          // arrived mid-deck: show all
  } else {
    shown.value = 1
    rollTo(props.auto)
  }
  watch(() => $clicks.value, (now, prev) => {
    clearTimers()
    if (now >= 1 && prev < 1) {
      shown.value = Math.max(shown.value, props.auto) + 1   // next appears at once
      if (shown.value < props.srcs.length) rollTo(props.srcs.length)
    } else if (now < 1 && prev >= 1) {
      shown.value = props.auto                              // stepping back
    }
  })
})
onUnmounted(clearTimers)

const url = s => (s.startsWith('/') ? import.meta.env.BASE_URL + s.slice(1) : s)
</script>

<template>
  <div class="relative" :style="{ height }">
    <img v-for="(src, i) in srcs" :key="src" :src="url(src)" class="abs-fig stage-img"
         :style="{ opacity: i < shown ? 1 : 0 }" alt="">
  </div>
</template>

<style scoped>
.stage-img {
  transition: opacity 0.6s ease;
}
</style>
