<script setup>
// Isometric wireframe cubes drawn to a common scale, side by side:
// boxes = [{ L, label, color, subdivide }], L in the same units. A
// `subdivide: n` box gets a faint n x n x n grid, so eight L25 cubes
// visibly fill an L50 one. Labels are HTML overlays (Slidev's CSS
// interferes with SVG <text>); SVG styling goes through style="",
// never opacity/font-size attributes (UnoCSS attributify).
import { computed } from 'vue'

const props = defineProps({
  boxes: { type: Array, required: true },
  height: { type: String, default: '14rem' },
  gap: { type: Number, default: 0.35 },     // gap between boxes, in units of the largest L
})

// isometric projection of (x, y, z), z up
const C = Math.cos(Math.PI / 6), S = Math.sin(Math.PI / 6)
const proj = (x, y, z) => [(x - y) * C, (x + y) * S - z]

const scene = computed(() => {
  const Lmax = Math.max(...props.boxes.map(b => b.L))
  const items = []
  let dx = 0                                   // screen-space x offset of the next cube
  for (const b of props.boxes) {
    const L = b.L, n = b.subdivide || 1, step = L / n
    // project at the origin, then shift horizontally in screen space so
    // the cubes sit side by side instead of overlapping along the x axis
    const P = (x, y, z) => { const [px, py] = proj(x, y, z); return [px + dx, py] }
    const edge = (a, c) => `M ${a[0].toFixed(2)} ${a[1].toFixed(2)} L ${c[0].toFixed(2)} ${c[1].toFixed(2)}`
    const seg = (x1, y1, z1, x2, y2, z2) => edge(P(x1, y1, z1), P(x2, y2, z2))
    // Viewer is above and in front: the bottom-of-screen corner (L, L, 0)
    // is nearest, so the visible faces are x = L, y = L and the top
    // (z = L). The three edges meeting at the far-bottom corner
    // (0, 0, 0) are hidden and drawn dashed.
    const front = [
      seg(L, L, 0, L, 0, 0), seg(L, L, 0, 0, L, 0), seg(L, L, 0, L, L, L),
      seg(L, 0, 0, L, 0, L), seg(0, L, 0, 0, L, L),
      seg(0, 0, L, L, 0, L), seg(0, 0, L, 0, L, L), seg(L, 0, L, L, L, L), seg(0, L, L, L, L, L),
    ]
    const hidden = [seg(0, 0, 0, L, 0, 0), seg(0, 0, 0, 0, L, 0), seg(0, 0, 0, 0, 0, L)]
    // subdivision grid on the three visible faces
    const grid = []
    for (let i = 1; i < n; i++) {
      const t = i * step
      grid.push(seg(L, t, 0, L, t, L), seg(t, L, 0, t, L, L))        // verticals on the x = L and y = L faces
      grid.push(seg(L, 0, t, L, L, t), seg(0, L, t, L, L, t))        // horizontals on those faces
      grid.push(seg(t, 0, L, t, L, L), seg(0, t, L, L, t, L))        // top face
    }
    const corners = [[0,0,0],[L,0,0],[0,L,0],[L,L,0],[0,0,L],[L,0,L],[0,L,L],[L,L,L]].map(c => P(...c))
    const cx = (P(0, 0, 0)[0] + P(L, L, 0)[0]) / 2
    items.push({ ...b, front, hidden, grid, corners, cx, bottom: P(L, L, 0)[1], top: P(0, 0, L)[1] })
    dx += 2 * L * C + props.gap * Lmax         // projected width of this cube, plus the gap
  }
  const xs = items.flatMap(i => i.corners.map(c => c[0])), ys = items.flatMap(i => i.corners.map(c => c[1]))
  const pad = 0.06 * Lmax
  const minx = Math.min(...xs) - pad, maxx = Math.max(...xs) + pad
  const miny = Math.min(...ys) - pad, maxy = Math.max(...ys) + pad
  return { items, viewBox: `${minx} ${miny} ${maxx - minx} ${maxy - miny}`, minx, miny, w: maxx - minx, h: maxy - miny, Lmax }
})
// label position: centred under each cube, as % of the SVG box
const labelPos = it => ({
  left: ((it.cx - scene.value.minx) / scene.value.w * 100) + '%',
  top: ((it.bottom + 0.04 * scene.value.Lmax - scene.value.miny) / scene.value.h * 100) + '%',
})
</script>

<template>
  <div class="wire relative mx-auto" :style="{ height, aspectRatio: scene.w / scene.h }">
    <svg :viewBox="scene.viewBox" class="w-full h-full">
      <g v-for="(it, k) in scene.items" :key="k" :stroke="it.color || '#444'">
        <path v-for="(d, i) in it.grid" :key="'g' + i" :d="d" fill="none" stroke-width="0.35"
              stroke-dasharray="1.2 1.2" style="opacity: 0.45" />
        <path v-for="(d, i) in it.hidden" :key="'h' + i" :d="d" fill="none" stroke-width="0.6"
              stroke-dasharray="1.5 1.5" style="opacity: 0.6" />
        <path v-for="(d, i) in it.front" :key="'f' + i" :d="d" fill="none" stroke-width="0.9"
              stroke-linecap="round" />
      </g>
    </svg>
    <div v-for="(it, k) in scene.items" :key="'l' + k" class="lbl" :style="{ ...labelPos(it), color: it.color || '#444' }"
         v-html="it.label" />
  </div>
</template>

<style scoped>
.wire { max-width: 100%; }
.lbl {
  position: absolute;
  transform: translate(-50%, 0);
  font-size: 0.72rem;
  line-height: 1.25;
  text-align: center;
  white-space: nowrap;
}
</style>
