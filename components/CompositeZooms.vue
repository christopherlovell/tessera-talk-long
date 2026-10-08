<script setup>
// Staged build-up of the composite-zoom idea, driven by Slidev clicks
// (set `clicks: 8` in the slide frontmatter — 7 stages + the closing
// question handled in slides.md):
//   click 1  zoom in on a single halo: spiral galaxy in the zoom circle
//   click 2  the region enlarges to a patch: filamentary structure,
//            and the mass-function panel appears with the patch's HMF
//   click 3  add baryons: patch particles recolour to stars/gas and
//            the HMF morphs into a galaxy stellar mass function
//   click 4  a second patch, different environment + its GSMF
//   click 5  overdensity labels + the P(log(1+delta)) distribution
//   click 6  more regions across the overdensity range, each adding
//            its (noisy, density-truncated) GSMF curve
//   click 7  the composite (abundance-weighted) mass function
// A direction caption at the top rotates through the stages.
//
// Everything is deterministic SVG; GSAP tweens one progress value per
// stage (state.s1..s7) and every element's style is a pure function of
// those, so stepping backwards works too.
// NB: on SVG elements use style bindings, never opacity/font-size
// attributes (UnoCSS attributify hijacks them).
import { computed, onMounted, reactive, watch } from 'vue'
import { useSlideContext } from '@slidev/client'
import gsap from 'gsap'

const { $clicks } = useSlideContext()

// ---- geometry (viewBox 680 x 400) -----------------------------------
const BOX = { x: 15, y: 95, s: 220 }
const A = { cx: 170, cy: 170, t: 0.85, log: 0.5 }          // dense region (halo -> patch)
const B = { cx: 65, cy: 275, r: 20, t: 0.15, log: -0.5 }   // void region
const ZA = { cx: 330, cy: 150 }                            // zoom circles
const ZB = { cx: 330, cy: 275, r: 50 }
const AXIS = { x: 460, top: 95, bot: 325, mid: 210, span: 115 } // log(1+d) in [-0.8, 0.8]
const HMF = { x0: 530, x1: 652, y0: 112, y1: 300 }         // mass-function panel
const logToY = l => AXIS.mid - (l / 0.8) * AXIS.span

// void -> dense colour scale (blue -> grey -> red)
const mix = (a, b, t) => Math.round(a + (b - a) * t)
const pColor = t => `rgb(${mix(50, 170, t)}, ${mix(90, 40, t)}, ${mix(160, 40, t)})`
const lerpRgb = (c0, c1, m) => `rgb(${mix(c0[0], c1[0], m)}, ${mix(c0[1], c1[1], m)}, ${mix(c0[2], c1[2], m)})`
const STAR = [210, 154, 61], GAS = [74, 127, 195], DM = [34, 34, 34]

// ---- deterministic scenery ------------------------------------------
function mulberry32(seed) {
  return () => {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0
    let z = Math.imul(seed ^ (seed >>> 15), 1 | seed)
    z = (z + Math.imul(z ^ (z >>> 7), 61 | z)) ^ z
    return ((z ^ (z >>> 14)) >>> 0) / 4294967296
  }
}
const rand = mulberry32(7)

// cosmic-web filaments [p0, p1, p2]; A on their junction, B in the void
const FILS = [
  [[25, 150], [90, 125], [170, 170]],
  [[170, 170], [200, 145], [232, 155]],
  [[170, 170], [205, 230], [228, 292]],
  [[170, 170], [120, 210], [118, 300]],
  [[45, 112], [40, 170], [100, 208]],
]
const qbez = ([p0, p1, p2], t) => [
  (1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * p1[0] + t * t * p2[0],
  (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * p1[1] + t * t * p2[1],
]
const filD = f => `M ${f[0][0]} ${f[0][1]} Q ${f[1][0]} ${f[1][1]} ${f[2][0]} ${f[2][1]}`

const webDots = []
for (const f of FILS)
  for (let t = 0.04; t < 1; t += 0.055) {
    const [x, y] = qbez(f, t)
    for (let k = 0; k < 2; k++)
      webDots.push({ x: x + (rand() - 0.5) * 13, y: y + (rand() - 0.5) * 13, r: 0.7 + rand() * 0.9 })
  }
for (let k = 0; k < 16; k++) {
  const a = rand() * 6.283, d = rand() * 15
  webDots.push({ x: A.cx + Math.cos(a) * d, y: A.cy + Math.sin(a) * d, r: 0.9 + rand() })
}

// spiral galaxy for the halo zoom: bulge + two trailing arms
const galaxyDots = []
for (let k = 0; k < 24; k++) {
  const a = rand() * 6.283, d = 6 * Math.sqrt(rand())
  galaxyDots.push({ x: ZA.cx + Math.cos(a) * d, y: ZA.cy + Math.sin(a) * d * 0.75,
                    r: 0.8 + rand() * 1.1, c: '#c8a35c' })
}
for (const arm of [0, Math.PI])
  for (let i = 0; i < 48; i++) {
    const t = i / 48
    const ang = arm + t * 3.7 + (rand() - 0.5) * 0.25
    const rad = 5 + t * 36
    galaxyDots.push({ x: ZA.cx + Math.cos(ang) * rad, y: ZA.cy + Math.sin(ang) * rad * 0.72,
                      r: 0.5 + (1 - t) * 1.2, c: '#5a6f9e' })
  }

// patch zoom: mini-filaments through the node, dots sampled along them;
// each dot carries a baryon colour for the add-baryons stage
const PATCH_FILS = [
  [[293, 118], [330, 150], [370, 178]],
  [[303, 188], [330, 150], [354, 110]],
  [[288, 152], [330, 150], [368, 140]],
]
const patchDots = []
const baryonOf = () => (rand() < 0.55 ? STAR : GAS)
for (const f of PATCH_FILS)
  for (let t = 0.05; t < 1; t += 0.07)
    for (let k = 0; k < 2; k++) {
      const [x, y] = qbez(f, t)
      patchDots.push({ x: x + (rand() - 0.5) * 9, y: y + (rand() - 0.5) * 9,
                       r: 0.6 + rand() * 0.9, b: baryonOf() })
    }
for (let k = 0; k < 22; k++) {
  const a = rand() * 6.283, d = rand() * 11
  patchDots.push({ x: ZA.cx + Math.cos(a) * d, y: ZA.cy + Math.sin(a) * d,
                   r: 0.8 + rand() * 1.1, b: baryonOf() })
}

// zoom B appears after baryons are added, so its dots are galaxies
const zoomDotsB = []
for (let k = 0; k < 13; k++) {
  const a = rand() * 6.283, d = (ZB.r - 6) * Math.sqrt(rand())
  zoomDotsB.push({ x: ZB.cx + Math.cos(a) * d, y: ZB.cy + Math.sin(a) * d,
                   r: 0.8 + rand() * 0.8, c: lerpRgb(rand() < 0.55 ? STAR : GAS, DM, 0.15) })
}

// stage-6 extra regions across the overdensity range (kept clear of the
// box edges and of region B)
const EXTRAS = [
  { cx: 214, cy: 279, r: 13, log: 0.65 },
  { cx: 90, cy: 127, r: 13, log: 0.3 },
  { cx: 125, cy: 240, r: 13, log: 0.1 },
  { cx: 205, cy: 115, r: 13, log: -0.15 },
  { cx: 35, cy: 220, r: 13, log: -0.3 },
  { cx: 97, cy: 295, r: 13, log: -0.65 },
].map(e => ({ ...e, t: (e.log + 0.8) / 1.6, y: logToY(e.log) }))

// sideways gaussian in log(1+delta)
const gaussD = (() => {
  const pts = []
  for (let y = AXIS.top; y <= AXIS.bot; y += 5)
    pts.push(`${(AXIS.x + 45 * Math.exp(-((y - AXIS.mid) ** 2) / (2 * 48 ** 2))).toFixed(1)} ${y}`)
  return 'M ' + pts.join(' L ')
})()

// ---- mass-function curves -------------------------------------------
// Fixed-length point arrays so the HMF can morph point-wise into the
// GSMF. Dense regions sit higher and reach larger masses; underdense
// regions truncate earlier. Per-curve seeded noise grows toward the
// sparse high-mass end.
const NPTS = 30
function curvePts(t, kind, seed, noiseAmp = 1) {
  const rnd = mulberry32(seed)
  const uCut = Math.min(1, (kind === 'hmf' ? 0.45 : 0.4) + 0.55 * t)
  const pts = []
  for (let i = 0; i < NPTS; i++) {
    const u = uCut * i / (NPTS - 1)
    const x = HMF.x0 + 5 + u * (HMF.x1 - HMF.x0 - 10)
    let y = kind === 'hmf'
      ? (150 - 28 * t) + (150 - 60 * t) * u + 40 * u * u
      : (172 - 26 * t) + (95 - 45 * t) * u + 105 * u ** 3.2
    y += (rnd() - 0.5) * 2 * (1.2 + 7 * u * u) * noiseAmp
    pts.push([x, Math.min(y, HMF.y1 - 3)])
  }
  return pts
}
const toPath = pts => 'M ' + pts.map(p => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' L ')
const lerpPts = (a, b, m) => a.map((p, i) => [p[0] + (b[i][0] - p[0]) * m, p[1] + (b[i][1] - p[1]) * m])

const hmfA = curvePts(A.t, 'hmf', 101)
const gsmfA = curvePts(A.t, 'gsmf', 101)
const gsmfB = toPath(curvePts(B.t, 'gsmf', 202))
const gsmfExtras = EXTRAS.map((e, i) => toPath(curvePts(e.t, 'gsmf', 301 + i)))
// abundance-weighted composite: smooth, sitting below the densest
// region's curve and truncating at the same highest mass (u = 0.9),
// while staying above the underdense curves
const compositePts = []
for (let i = 0; i < NPTS; i++) {
  const u = 0.9 * i / (NPTS - 1)
  compositePts.push([HMF.x0 + 5 + u * (HMF.x1 - HMF.x0 - 10), 158 + 66 * u + 95 * u ** 3.2])
}
const gsmfComposite = toPath(compositePts)

// ---- animation state -------------------------------------------------
const state = reactive({ s1: 0, s2: 0, s3: 0, s4: 0, s5: 0, s6: 0, s7: 0 })
const N = 7
const DUR = { 1: 1.5, 2: 1.7, 3: 1.5, 4: 1.5, 5: 1.8, 6: 1.6, 7: 1.2 }

function applyInstant(clicks) {
  for (let i = 1; i <= N; i++) state['s' + i] = clicks >= i ? 1 : 0
}
applyInstant($clicks.value)

// Snap to the current click state on mount (navigation may set clicks
// after setup); only animate changes after that.
onMounted(() => {
  applyInstant($clicks.value)
  watch(() => $clicks.value, (now, prev) => {
    const tl = gsap.timeline()
    for (let i = 1; i <= N; i++) {
      if (now >= i && prev < i)
        tl.to(state, { ['s' + i]: 1, duration: DUR[i], ease: 'power2.inOut' }, '>-0.1')
      else if (now < i && prev >= i)
        tl.to(state, { ['s' + i]: 0, duration: 0.35, ease: 'power2.out' }, 0)
    }
  })
})

// window helper: progress p remapped to [a, b] sub-interval
const win = (p, a, b) => Math.min(Math.max((p - a) / (b - a), 0), 1)

const fade = (p, a, b, rise = 6) => ({
  opacity: win(p, a, b),
  transform: `translate(-50%, calc(-50% + ${((1 - win(p, a, b)) * rise).toFixed(1)}px))`,
})
const pos = (x, y) => ({ left: (x / 680 * 100) + '%', top: (y / 400 * 100) + '%' })

// zoom A: halo (stage 1) -> patch (stage 2) -> baryons (stage 3)
const zA = computed(() => {
  const grow = win(state.s2, 0, 0.35)
  return {
    regionR: 9 + 11 * grow,
    zoomR: 42 + 10 * grow,
    circle: 1 - win(state.s1, 0, 0.3),
    coneLine: 1 - win(state.s1, 0.25, 0.55),
    coneFill: win(state.s1, 0.45, 0.7) * 0.05,
    zoom: win(state.s1, 0.55, 0.85),
    galaxy: win(state.s1, 0.7, 1) * (1 - win(state.s2, 0.15, 0.55)),
    patch: win(state.s2, 0.35, 0.8),
    baryon: win(state.s3, 0.2, 0.7),               // dot colour morph
    transform: `translate(${ZA.cx} ${ZA.cy}) scale(${0.6 + 0.4 * win(state.s1, 0.55, 0.85)}) translate(${-ZA.cx} ${-ZA.cy})`,
  }
})
// zoom B: single-phase patch (stage 4)
const zB = computed(() => ({
  circle: 1 - win(state.s4, 0, 0.3),
  coneLine: 1 - win(state.s4, 0.25, 0.55),
  coneFill: win(state.s4, 0.45, 0.7) * 0.05,
  zoom: win(state.s4, 0.55, 0.85),
  dots: win(state.s4, 0.7, 1),
  transform: `translate(${ZB.cx} ${ZB.cy}) scale(${0.6 + 0.4 * win(state.s4, 0.55, 0.85)}) translate(${-ZB.cx} ${-ZB.cy})`,
}))
// overdensity distribution (stage 5)
const dist = computed(() => ({
  axis: 1 - win(state.s5, 0.15, 0.4),
  curve: 1 - win(state.s5, 0.35, 0.7),
  lineA: 1 - win(state.s5, 0.65, 0.9),
  lineB: 1 - win(state.s5, 0.7, 0.95),
  markers: win(state.s5, 0.85, 1),
}))
// stage-6 stagger, one window per extra region
const ex = computed(() => EXTRAS.map((_, i) => win(state.s6, i * 0.13, i * 0.13 + 0.35)))

// mass-function panel: axes with the first patch, HMF -> GSMF morph on
// stage 3, curves accumulating as regions appear
const mf = computed(() => ({
  axes: win(state.s2, 0.5, 0.75),
  curveA: toPath(lerpPts(hmfA, gsmfA, win(state.s3, 0.25, 0.75))),
  curveADash: 1 - win(state.s2, 0.65, 1),
  curveBDash: 1 - win(state.s4, 0.6, 1),
  extras: EXTRAS.map((_, i) => 1 - win(state.s6, i * 0.13 + 0.08, i * 0.13 + 0.43)),
  composite: 1 - win(state.s7, 0.15, 0.85),
  massLabelHalo: win(state.s2, 0.55, 0.8) * (1 - win(state.s3, 0.2, 0.6)),
  massLabelStellar: win(state.s3, 0.3, 0.7),
}))

// rotating direction captions
const caps = computed(() => ({
  c1: win(state.s1, 0.05, 0.35) * (1 - win(state.s2, 0, 0.35)),
  c2: win(state.s2, 0.05, 0.4) * (1 - win(state.s3, 0, 0.35)),
  c3: win(state.s3, 0.05, 0.4) * (1 - win(state.s4, 0, 0.35)),
  c4: win(state.s4, 0.05, 0.4) * (1 - win(state.s7, 0, 0.35)),
  c5: win(state.s7, 0.05, 0.4),
}))
</script>

<template>
  <div class="relative select-none">
    <svg viewBox="0 0 680 400" class="w-full">
      <!-- parent box: pmwd PM parent render (public/figures/pm_parent_render.webp) -->
      <image href="/figures/pm_parent_render.webp" :x="BOX.x" :y="BOX.y" :width="BOX.s" :height="BOX.s" preserveAspectRatio="xMidYMid slice" />
      <rect :x="BOX.x" :y="BOX.y" :width="BOX.s" :height="BOX.s" fill="none" stroke="#333" stroke-width="1.5" />


      <!-- zoom A: halo, then patch, then baryons -->
      <g :style="{ opacity: state.s1 > 0 ? 1 : 0 }">
        <polygon :points="`${A.cx},${A.cy} ${ZA.cx},${ZA.cy - zA.zoomR} ${ZA.cx},${ZA.cy + zA.zoomR}`"
                 :fill="`rgba(0,0,0,${zA.coneFill})`" />
        <line :x1="A.cx" :y1="A.cy" :x2="ZA.cx" :y2="ZA.cy - zA.zoomR" pathLength="1" class="cone-edge"
              :stroke-dashoffset="zA.coneLine" />
        <line :x1="A.cx" :y1="A.cy" :x2="ZA.cx" :y2="ZA.cy + zA.zoomR" pathLength="1" class="cone-edge"
              :stroke-dashoffset="zA.coneLine" />
        <circle :cx="A.cx" :cy="A.cy" :r="zA.regionR" pathLength="1" fill="none"
                :stroke="pColor(A.t)" stroke-width="2.5" stroke-dasharray="1" :stroke-dashoffset="zA.circle" />
        <g :transform="zA.transform" :style="{ opacity: zA.zoom }">
          <circle :cx="ZA.cx" :cy="ZA.cy" :r="zA.zoomR" fill="#fff" :stroke="pColor(A.t)" stroke-width="2.5" />
          <g clip-path="url(#clipA)">
            <!-- halo content: spiral galaxy -->
            <g :style="{ opacity: zA.galaxy }">
              <circle :cx="ZA.cx" :cy="ZA.cy" r="7" fill="#e8cf96" style="opacity: 0.55" />
              <circle :cx="ZA.cx" :cy="ZA.cy" r="3" fill="#f4e6c0" />
              <circle v-for="(d, i) in galaxyDots" :key="'g' + i" :cx="d.x" :cy="d.y" :r="d.r" :fill="d.c"
                      style="opacity: 0.9" />
            </g>
            <!-- patch content: filaments; dots recolour as baryons arrive -->
            <g :style="{ opacity: zA.patch }">
              <path v-for="(f, i) in PATCH_FILS" :key="'pf' + i" :d="filD(f)"
                    fill="none" stroke="#ccc" stroke-width="3.5" stroke-linecap="round" style="opacity: 0.6" />
              <circle v-for="(d, i) in patchDots" :key="'pd' + i" :cx="d.x" :cy="d.y" :r="d.r"
                      :fill="lerpRgb(DM, d.b, zA.baryon)" style="opacity: 0.9" />
            </g>
          </g>
        </g>
      </g>

      <!-- zoom B (void patch, with galaxies) -->
      <g :style="{ opacity: state.s4 > 0 ? 1 : 0 }">
        <polygon :points="`${B.cx},${B.cy} ${ZB.cx},${ZB.cy - ZB.r} ${ZB.cx},${ZB.cy + ZB.r}`"
                 :fill="`rgba(0,0,0,${zB.coneFill})`" />
        <line :x1="B.cx" :y1="B.cy" :x2="ZB.cx" :y2="ZB.cy - ZB.r" pathLength="1" class="cone-edge"
              :stroke-dashoffset="zB.coneLine" />
        <line :x1="B.cx" :y1="B.cy" :x2="ZB.cx" :y2="ZB.cy + ZB.r" pathLength="1" class="cone-edge"
              :stroke-dashoffset="zB.coneLine" />
        <circle :cx="B.cx" :cy="B.cy" :r="B.r" pathLength="1" fill="none"
                :stroke="pColor(B.t)" stroke-width="2.5" stroke-dasharray="1" :stroke-dashoffset="zB.circle" />
        <g :transform="zB.transform" :style="{ opacity: zB.zoom }">
          <circle :cx="ZB.cx" :cy="ZB.cy" :r="ZB.r" fill="#fff" :stroke="pColor(B.t)" stroke-width="2.5" />
          <circle v-for="(d, i) in zoomDotsB" :key="i" :cx="d.x" :cy="d.y" :r="d.r" :fill="d.c"
                  :style="{ opacity: zB.dots }" />
        </g>
      </g>

      <!-- stage 5: overdensity axis, distribution, connectors -->
      <g :style="{ opacity: state.s5 > 0 ? 1 : 0 }">
        <line :x1="AXIS.x" :y1="AXIS.bot" :x2="AXIS.x" :y2="AXIS.top - 8" pathLength="1" class="axis"
              stroke-dasharray="1" :stroke-dashoffset="dist.axis" marker-end="url(#arrow)" />
        <path :d="gaussD" pathLength="1" fill="none" stroke="#666" stroke-width="1.8"
              stroke-dasharray="1" :stroke-dashoffset="dist.curve" />
        <line :x1="ZA.cx + zA.zoomR + 4" :y1="ZA.cy" :x2="AXIS.x - 4" :y2="logToY(A.log)" pathLength="1"
              class="connect" :stroke="pColor(A.t)" :stroke-dashoffset="dist.lineA" />
        <line :x1="ZB.cx + ZB.r + 4" :y1="ZB.cy" :x2="AXIS.x - 4" :y2="logToY(B.log)" pathLength="1"
              class="connect" :stroke="pColor(B.t)" :stroke-dashoffset="dist.lineB" />
        <circle :cx="AXIS.x" :cy="logToY(A.log)" r="4.5" :fill="pColor(A.t)" :style="{ opacity: dist.markers }" />
        <circle :cx="AXIS.x" :cy="logToY(B.log)" r="4.5" :fill="pColor(B.t)" :style="{ opacity: dist.markers }" />
      </g>

      <!-- stage 6: more regions across the overdensity range -->
      <g>
        <template v-for="(e, i) in EXTRAS" :key="'e' + i">
          <circle :cx="e.cx" :cy="e.cy" :r="e.r * (0.7 + 0.3 * ex[i])" fill="none"
                  :stroke="pColor(e.t)" stroke-width="2" :style="{ opacity: ex[i] }" />
          <circle :cx="AXIS.x" :cy="e.y" r="3.5" :fill="pColor(e.t)" :style="{ opacity: ex[i] }" />
        </template>
      </g>

      <!-- mass-function panel: curves accumulate as regions appear -->
      <g :style="{ opacity: mf.axes }">
        <line :x1="HMF.x0" :y1="HMF.y1" :x2="HMF.x1 + 6" :y2="HMF.y1" class="axis" marker-end="url(#arrow)" />
        <line :x1="HMF.x0" :y1="HMF.y1" :x2="HMF.x0" :y2="HMF.y0 - 6" class="axis" marker-end="url(#arrow)" />
      </g>
      <g>
        <path :d="mf.curveA" pathLength="1" fill="none" :stroke="pColor(A.t)" stroke-width="1.6"
              stroke-dasharray="1" :stroke-dashoffset="mf.curveADash" style="opacity: 0.85" />
        <path :d="gsmfB" pathLength="1" fill="none" :stroke="pColor(B.t)" stroke-width="1.6"
              stroke-dasharray="1" :stroke-dashoffset="mf.curveBDash" style="opacity: 0.85" />
        <path v-for="(d, i) in gsmfExtras" :key="'h' + i" :d="d" pathLength="1" fill="none"
              :stroke="pColor(EXTRAS[i].t)" stroke-width="1.3" stroke-dasharray="1"
              :stroke-dashoffset="mf.extras[i]" style="opacity: 0.7" />
        <path :d="gsmfComposite" pathLength="1" fill="none" stroke="#1c1c1c" stroke-width="3"
              stroke-dasharray="1" :stroke-dashoffset="mf.composite" stroke-linecap="round" />
      </g>

      <defs>
        <clipPath id="clipA"><circle :cx="ZA.cx" :cy="ZA.cy" :r="zA.zoomR - 1" /></clipPath>
        <marker id="arrow" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="7" markerHeight="7" orient="auto">
          <path d="M 0 0 L 8 4 L 0 8 z" fill="#555" />
        </marker>
      </defs>
    </svg>

    <!-- text as HTML overlays (Slidev CSS breaks SVG <text> positioning) -->
    <div class="lbl cap" :style="{ ...pos(340, 22), opacity: caps.c1 }">zoom in of an individual halo</div>
    <div class="lbl cap" :style="{ ...pos(340, 22), opacity: caps.c2 }">zoom in of a patch of the universe</div>
    <div class="lbl cap" :style="{ ...pos(340, 22), opacity: caps.c3 }">add baryons to the zoom: measure the galaxy stellar mass function</div>
    <div class="lbl cap" :style="{ ...pos(340, 22), opacity: caps.c4 }">multiple zooms of different patches</div>
    <div class="lbl cap" :style="{ ...pos(340, 22), opacity: caps.c5 }">combine the patches based on their relative abundance in the parent simulation</div>

    <div class="lbl" :style="pos(125, 336)">parent: full volume, low resolution</div>
    <div class="lbl theta" :style="pos(125, 84)">&theta; = {&Omega;<sub>m</sub>, &sigma;<sub>8</sub>, h, &hellip;}</div>
    <div class="lbl" :style="{ ...pos(ZA.cx, 82), color: pColor(A.t), ...fade(state.s5, 0, 0.25) }">
      log(1+&delta;) = {{ A.log }}</div>
    <div class="lbl" :style="{ ...pos(ZB.cx, 212), color: pColor(B.t), ...fade(state.s5, 0.05, 0.3) }">
      log(1+&delta;) = &minus;{{ -B.log }}</div>
    <div class="lbl" :style="{ ...pos(AXIS.x, 78), ...fade(state.s5, 0.2, 0.45) }">log(1+&delta;)</div>
    <div class="lbl phi" :style="{ ...pos(HMF.x0, 95), opacity: mf.axes }">&Phi;</div>
    <div class="lbl" :style="{ ...pos((HMF.x0 + HMF.x1) / 2, 316), opacity: mf.massLabelHalo }">halo mass</div>
    <div class="lbl" :style="{ ...pos((HMF.x0 + HMF.x1) / 2, 316), opacity: mf.massLabelStellar }">stellar mass</div>
  </div>
</template>

<style scoped>
.cone-edge {
  stroke: #aaa;
  stroke-width: 1.2;
  stroke-dasharray: 1;
}
.axis {
  stroke: #555;
  stroke-width: 1.5;
}
.connect {
  stroke-width: 1.3;
  stroke-dasharray: 1;
}
.lbl {
  position: absolute;
  transform: translate(-50%, -50%);
  font-size: 0.68rem;
  line-height: 1.2;
  color: #666;
  text-align: center;
  white-space: nowrap;
}
.cap {
  font-size: 0.85rem;
  font-weight: 600;
  color: #444;
}
.phi {
  font-size: 0.85rem;
  font-style: italic;
}
.theta {
  font-size: 0.75rem;
  font-style: italic;
}
</style>
