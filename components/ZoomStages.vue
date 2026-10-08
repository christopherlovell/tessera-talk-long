<script setup>
// Figures introduced one at a time: the newest is shown large on the
// right, finished ones shrink into a rail down the left-hand side.
// Stage i is featured on click i, so the slide needs
// `clicks: <stages.length - 1>` in its frontmatter.
//
// A stage marked `overlay: true` lands directly on top of the one
// before it, at the same size and position, instead of pushing it into
// the rail — the two are one group and park together.
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'

const props = defineProps({
  stages: { type: Array, required: true },    // [{ src, alt, overlay }]
  height: { type: String, default: '26rem' },
  parkWidth: { type: Number, default: 18 },   // % of the container: rail width
  railGap: { type: Number, default: 2 },      // % between rail and featured figure
  parkGap: { type: Number, default: 3 },      // % between parked figures
})

const { $clicks } = useSlideContext()
const last = props.stages.length - 1
const current = computed(() => Math.min(Math.max($clicks.value ?? 0, 0), last))

// consecutive `overlay` stages join the group of the stage they cover
const groupOf = []
let groups = 0
props.stages.forEach((s, i) => {
  if (!(s.overlay && i > 0)) groups++
  groupOf[i] = groups - 1
})

const maxParked = Math.max(groups - 1, 1)
const slotH = (100 - (maxParked - 1) * props.parkGap) / maxParked
const featLeft = props.parkWidth + props.railGap

// A stage that has not appeared yet gets the box it is about to be
// featured in, so it fades in already in place rather than sliding.
function box(i) {
  const g = groupOf[i]
  if (g < groupOf[current.value]) {
    return {
      left: '0%', width: `${props.parkWidth}%`,
      top: `${g * (slotH + props.parkGap)}%`, height: `${slotH}%`,
    }
  }
  const left = g === 0 ? 0 : featLeft
  return { left: `${left}%`, width: `${100 - left}%`, top: '0%', height: '100%' }
}

const url = s => (s.startsWith('/') ? import.meta.env.BASE_URL + s.slice(1) : s)
</script>

<template>
  <div class="relative w-full" :style="{ height }">
    <img v-for="(s, i) in stages" :key="s.src" class="zoom-stage"
         :src="url(s.src)" :alt="s.alt || ''"
         :style="{ ...box(i), opacity: i <= current ? 1 : 0 }">
  </div>
</template>

<style scoped>
.zoom-stage {
  position: absolute;
  object-fit: contain;
  transition: left 0.7s ease, top 0.7s ease, width 0.7s ease,
              height 0.7s ease, opacity 0.4s ease;
}
</style>
