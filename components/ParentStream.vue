<script setup>
// A looping stream of PM-parent thumbnails, each the parent render tinted
// as if from a different cosmology (after the URF figure's grid of
// parents), running in from the top and off the bottom. Two columns at
// different speeds; each column holds two copies of its tiles so the
// translateY(-50%) keyframe loops seamlessly.
const props = defineProps({
  src: { type: String, default: '/figures/pm_parent_render.webp' },
  columns: { type: Number, default: 2 },
  perColumn: { type: Number, default: 7 },
})

function mulberry32(seed) {
  return () => {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}
const rand = mulberry32(11)
// tint = hue shift (cosmology "colour"), saturation and brightness
// (washed-out to deep), like the parent grid in the figure
const cols = Array.from({ length: props.columns }, (_, c) => ({
  duration: 26 + c * 9,
  delay: -c * 7,
  tiles: Array.from({ length: props.perColumn }, () => ({
    hue: Math.round(-70 + rand() * 140),
    sat: (0.35 + rand() * 1.2).toFixed(2),
    bright: (0.7 + rand() * 1.2).toFixed(2),
  })),
}))
</script>

<template>
  <div class="stream">
    <div v-for="(c, i) in cols" :key="i" class="col"
         :style="{ animationDuration: c.duration + 's', animationDelay: c.delay + 's' }">
      <template v-for="rep in 2" :key="rep">
        <img v-for="(t, j) in c.tiles" :key="rep + '-' + j" :src="src" alt=""
             :style="{ filter: `hue-rotate(${t.hue}deg) saturate(${t.sat}) brightness(${t.bright})` }">
      </template>
    </div>
  </div>
</template>

<style scoped>
.stream {
  position: relative;
  height: 100%;
  display: flex;
  gap: 0.4rem;
  overflow: hidden;
  /* fade the tiles in at the top and out at the bottom */
  -webkit-mask-image: linear-gradient(to bottom, transparent, #000 12%, #000 88%, transparent);
  mask-image: linear-gradient(to bottom, transparent, #000 12%, #000 88%, transparent);
}
.col {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  flex: 1;
  animation-name: stream-down;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  will-change: transform;
}
.col img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 3px;
  border: 1px solid rgba(0, 0, 0, 0.25);
}
/* start with the second copy showing and slide down to the first: the
   tiles appear to enter from the top and leave at the bottom */
@keyframes stream-down {
  from { transform: translateY(-50%); }
  to   { transform: translateY(0); }
}
</style>
