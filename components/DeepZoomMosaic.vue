<script setup>
// OpenSeadragon deep zoom over public/data/deep_zoom: a mosaic holding
// every first-layer zoom as a 1024px circular render, tiled into a
// 17-level pyramid (currently 44032x24576, 43x24 regions; the size is
// read from mosaic.dzi). layout.json maps a parent label (P00123) to
// its [col, row] in that grid; each panel carries its
// own ID, overdensity percentile and cosmology burnt into the image,
// so zooming in is what reveals the parameters — no captions needed.
//
// `tour` is one stop per click ('overview' fits the whole mosaic), so
// the slide needs `clicks: <tour.length - 1>` in its frontmatter.
// Swap in any label from layout.json to change where the tour goes.
//
// The tile pyramid is ~340 MB and is not shipped with the web build
// (public/data/deep_zoom is gitignored); when it is missing the slide
// shows `fallback`, a static low-res render of the whole mosaic.
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useSlideContext } from '@slidev/client'

const props = defineProps({
  tour: { type: Array, default: () => ['overview'] },
  height: { type: String, default: '27rem' },
  panel: { type: Number, default: 1024 },     // px per region in the mosaic
  // seconds per dive (the flight out to the overview takes 0.7 of it);
  // springStiffness only shapes the user's own scroll-wheel zooms
  animationTime: { type: Number, default: 4.5 },
  springStiffness: { type: Number, default: 3.5 },
  fallback: { type: String, default: '' },   // static image shown when the tiles are absent
})

const { $clicks } = useSlideContext()
const el = ref(null)
const failed = ref(false)
let viewer = null
let layout = {}
let OSD = null
let size = null   // mosaic pixel size, from mosaic.dzi

const base = import.meta.env.BASE_URL + 'data/deep_zoom/'
const fallbackUrl = props.fallback.startsWith('/')
  ? import.meta.env.BASE_URL + props.fallback.slice(1) : props.fallback

// the bundled UMD build, loaded once and shared between slides
let osdLoader
function loadOSD() {
  if (!osdLoader) {
    osdLoader = new Promise((resolve, reject) => {
      if (window.OpenSeadragon) return resolve(window.OpenSeadragon)
      const s = document.createElement('script')
      s.src = base + 'openseadragon.min.js'
      s.onload = () => resolve(window.OpenSeadragon)
      s.onerror = () => reject(new Error('OpenSeadragon failed to load'))
      document.head.appendChild(s)
    })
  }
  return osdLoader
}

// Fly to a stop. OpenSeadragon's own springs start at full speed and
// only slow down, which reads as a lurch on a 37x dive, so the camera
// is driven by hand: log-zoom and centre eased in and out (sine) over
// `animationTime` seconds. Between two regions the camera goes out to
// the overview first and dives in once that flight lands. `flight`
// cancels a flight in progress if another click lands mid-way.
let flight = 0
const ease = u => 0.5 - 0.5 * Math.cos(Math.PI * u)
const lerpLog = (a, b, e) => Math.exp((1 - e) * Math.log(a) + e * Math.log(b))
function rectFor(stop) {
  const pos = layout[stop]
  if (!pos) return viewer.viewport.getHomeBounds()
  return viewer.viewport.imageToViewportRectangle(
    pos[0] * props.panel, pos[1] * props.panel, props.panel, props.panel)
}
function fly(target, seconds, done) {
  const vp = viewer.viewport
  const start = vp.getBounds(true)
  const id = ++flight
  const t0 = performance.now()
  const step = now => {
    if (id !== flight || !viewer) return
    const u = Math.min(1, (now - t0) / (seconds * 1000))
    const e = ease(u)
    const w = lerpLog(start.width, target.width, e)
    const h = lerpLog(start.height, target.height, e)
    const cx = (1 - e) * (start.x + start.width / 2) + e * (target.x + target.width / 2)
    const cy = (1 - e) * (start.y + start.height / 2) + e * (target.y + target.height / 2)
    vp.fitBounds(new OSD.Rect(cx - w / 2, cy - h / 2, w, h), true)
    if (u < 1) requestAnimationFrame(step)
    else done?.()
  }
  requestAnimationFrame(step)
}
function goTo(stop, from) {
  if (!viewer) return
  const target = rectFor(stop)
  if (from === undefined) return viewer.viewport.fitBounds(target, true)   // first show: no flight
  if (from && layout[from] && layout[stop])
    return fly(rectFor('overview'), props.animationTime * 0.7, () => fly(target, props.animationTime))
  fly(target, props.animationTime)
}

const stopFor = c => props.tour[Math.min(Math.max(c ?? 0, 0), props.tour.length - 1)]

onMounted(async () => {
  let OpenSeadragon
  try {
    let dzi
    ;[OpenSeadragon, layout, dzi] = await Promise.all([
      loadOSD(),
      fetch(base + 'layout.json').then(r => r.json()),
      fetch(base + 'mosaic.dzi').then(r => r.text()),
    ])
    const m = dzi.match(/Width="(\d+)"\s+Height="(\d+)"/)
    if (!m) throw new Error('mosaic.dzi has no Size')
    size = { width: +m[1], height: +m[2] }
  } catch (e) {
    failed.value = true
    return
  }
  if (!el.value) return                        // slide left before we were ready
  OSD = OpenSeadragon

  viewer = OpenSeadragon({
    element: el.value, prefixUrl: '', showNavigationControl: false,
    showNavigator: true, navigatorPosition: 'BOTTOM_RIGHT', navigatorSizeRatio: 0.12,
    maxZoomPixelRatio: 2, minZoomImageRatio: 0.9, visibilityRatio: 1,
    constrainDuringPan: true,
    animationTime: props.animationTime, springStiffness: props.springStiffness,
    tileSources: {
      Image: {
        xmlns: 'http://schemas.microsoft.com/deepzoom/2008',
        Url: base + 'mosaic_files/', Format: 'jpg', Overlap: '0', TileSize: '512',
        Size: { Width: String(size.width), Height: String(size.height) },
      },
    },
  })
  // leave space/arrow to the deck, but keep drag and scroll-wheel zoom
  viewer.innerTracker.keyDownHandler = null
  viewer.innerTracker.keyUpHandler = null
  viewer.innerTracker.keyHandler = null

  viewer.addHandler('open', () => goTo(stopFor($clicks.value)))
  watch(() => $clicks.value, (c, prev) => goTo(stopFor(c), stopFor(prev)))
})

onUnmounted(() => { viewer?.destroy(); viewer = null })
</script>

<template>
  <div class="mosaic" :style="{ height }">
    <div ref="el" class="w-full h-full" />
    <img v-if="failed && fallback" :src="fallbackUrl" class="mosaic-fallback" alt="" />
    <div v-else-if="failed" class="mosaic-failed">deep zoom mosaic unavailable</div>
  </div>
</template>

<style scoped>
.mosaic {
  position: relative;
  width: 100%;
  background: #000;
  overflow: hidden;
}
.mosaic-fallback {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.mosaic-failed {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  font-size: 0.8rem;
}
</style>
