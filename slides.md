---
# ============================================================
# Tessera — long talk (~30–35 min) — Slidev deck
#
# Part II of the LtU TSG update (slidev_ltu_tsg) on its own: reaching
# large volumes — composite zooms, the Quijote proof of
# concept and Tessera (pipeline, design, emulation, clustering,
# extensions), closing on the stand-alone Tessera summary slide.
#
# The asset folders under public/ are symlinks into
# ../slidev_ltu_tsg/public (figures, flamels, pptx, data), so
# figures are shared with the LtU deck rather than duplicated.
#
#   npm run dev      -> live-reloading talk at localhost:3030
#   npm run build    -> static site in dist/
#   npm run export   -> PDF
#
# Layout helpers (cols-40-60 etc.) and colours live in style.css.
# ============================================================
theme: default
title: Tessera — composite zoom suites for large volumes
titleTemplate: '%s — C. Lovell'
author: Chris Lovell
conference: Cambridge-LMU Cosmology Meeting
date: 29 September 2026
colorSchema: light
aspectRatio: 16/9
fonts:
  sans: Arial
  provider: none
class: title-slide
---

<!-- title: same cosmic-web strip + zoom callouts as the 15-min deck -->

<img src="/pptx/title_strip.webp" class="title-strip" alt="">

<svg class="title-zooms" viewBox="0 0 1280 720" preserveAspectRatio="none" aria-hidden="true">
  <g>
    <circle class="region" cx="100" cy="120" r="13" />
    <path class="cone" d="M 100 120 L 355 78 L 355 202 Z" />
  </g>
  <g>
    <circle class="region" cx="125" cy="350" r="15" />
    <path class="cone" d="M 125 350 L 395 291 L 395 439 Z" />
  </g>
  <g>
    <circle class="region" cx="90" cy="565" r="12" />
    <path class="cone" d="M 90 565 L 345 527 L 345 643 Z" />
  </g>
</svg>

<div class="zoom-slot" style="left: 22.9%; top: 10.8%; width: 9.7%">
  <img src="/figures/title_zoom_a.webp" class="w-full h-full object-cover" alt="zoom region">
</div>
<div class="zoom-slot" style="left: 25.1%; top: 40.4%; width: 11.6%">
  <img src="/figures/title_zoom_b.webp" class="w-full h-full object-cover" alt="zoom region">
</div>
<div class="zoom-slot" style="left: 22.4%; top: 73.2%; width: 9.1%">
  <img src="/figures/title_zoom_c.webp" class="w-full h-full object-cover" alt="zoom region">
</div>

<div class="ml-[44%] mt-10">

<h1 class="title-main">Efficiently exploring the large volume regime with composite zoom suites</h1>

<div class="mt-8 leading-snug">

**Chris Lovell**  &nbsp;&nbsp; <span class="op75">Research Associate, KICC, Cambridge</span>

</div>

<div class="mt-5 text-sm">

<!--a href="https://christopherlovell.co.uk" class="!border-none">christopherlovell.co.uk</a-->

<div class="op75 mt-1">With Will Roper, Max Lee, Shy Genel, Daniel Anglés-Alcázar, Francisco Villaescusa-Navarro, Claudia Lagos, Ángel Chandro-Gómez, Thomas Bebbington, Carol Cuesta-Lazaro, Shivam Pandey, Yao Zhang, Ben Wandelt, Will Handley and the Tessera team</div>



</div>

<div class="mt-7 flex items-center gap-5">
  <img src="/pptx/image1.webp" class="h-20" alt="University of Cambridge">
  <img src="/pptx/image3.webp" class="h-18" alt="KICC">
  <img src="/pptx/image2.webp" class="h-11" alt="DiRAC">
  <img src="/figures/ltu.webp" class="h-16" alt="Learning the Universe">
</div>

</div>

---

<!-- the resolved halo mass - volume plane, five build-up frames stacked on
     one slide, cross-fading in on clicks (frames are cumulative, so each
     later image simply covers the last). Made by
     cosmo_carta/matplotlib/baryonic_volume_transposed.py talk builds -->

<img src="/figures/baryonic_volume_1_frame.png" class="fig-main" alt="halo mass vs volume: empty plane">

<img v-click="1" src="/figures/baryonic_volume_2_simulations.png" class="fig-main fade-frame" alt="halo mass vs volume: simulations">

<img v-click="2" src="/figures/baryonic_volume_3_tracers.png" class="fig-main fade-frame" alt="halo mass vs volume: + survey tracers">

<img v-click="3" src="/figures/baryonic_volume_4_suites.png" class="fig-main fade-frame" alt="halo mass vs volume: + parameter-variation suites">

<img v-click="4" src="/figures/baryonic_volume_5_question.png" class="fig-main fade-frame" alt="halo mass vs volume: + the gap Tessera aims at">

---
layout: center
clicks: 8
---

<!-- pptx slide 6: the multi-zoom approach — full-slide animated
     build-up (components/CompositeZooms.vue), advanced with
     space/arrow: halo zoom -> patch zoom -> add baryons (HMF morphs
     to GSMF) -> second patch -> overdensity distribution -> regions
     across the full range (each adding its curve) -> composite ->
     closing question (click 8). -->

<CompositeZooms class="w-180 mx-auto" />

<div class="abs-br m-6 text-sm op60">Crain+09, Lovell+21</div>

<div v-click="8" class="absolute bottom-13 left-0 right-0 text-center text-lg font-bold">
Can we do this over large cosmological and astrophysical parameter ranges?
</div>

<!-- final click: a suite of PM parents at different cosmologies streams
     down the left edge (components/ParentStream.vue; CSS-tinted copies
     of the parent render) -->
<div v-click="8" class="absolute left-5 top-4 bottom-12 w-26">
  <div class="text-center text-xs op70 leading-tight mb-1">suite of PM parents<br><i>&theta;<sub>i</sub></i> = {&Omega;<sub>m</sub>, &sigma;<sub>8</sub>, h, &hellip;}</div>
  <ParentStream class="h-[calc(100%-2.4rem)]" />
</div>

---
layout: section
---

<!-- pptx slide 7 -->

<img src="/pptx/image7.webp" class="section-bg" alt="">

# Proof of concept

An emulator for the halo mass function using regions selected from Quijote

<div class="arxiv mt-2">arXiv:2604.17981</div>

---

<!-- pptx slide 8: Quijote + staged density-percentile story.
     Click 0: the Quijote box render fills the right of the slide; the
     global HMF inset rolls in automatically after 2 s. Click 1: the
     green box appears, the render shrinks to the bottom right and the
     overdensity CDF + region insets fade in above it (region A at
     once, region B 2 s later). The story frames are split into
     top/bottom crops in public/quijote_story/ so the two halves can
     be laid out separately (components/AutoStages.vue drives the
     timing; both instances share the same click and delay). -->

<div class="flex items-center gap-4 mt-1">
  <img src="/pptx/image4.webp" class="h-14" alt="Quijote">
  <img src="/pptx/image7.webp" class="h-14" alt="Quijote artwork">
</div>

<div class="text-sm op70 mt-1">Villaescusa-Navarro et al. 2021</div>

<div class="grid grid-cols-[17rem_16rem] gap-4 mt-3 items-start" style="font-size: 0.86rem">

<div class="box-blue" style="padding: 0.8rem 1rem">

- N-body dark-matter-only simulations, $(1\,{\rm Gpc}/h)^3$ each
- Big Sobol Sequence: 32,000 simulations over a Sobol sequence of five ΛCDM parameters

<div style="font-size: 0.8rem; margin-top: -0.4rem">

$$
\begin{aligned}
\Omega_m &\in [0.1,\, 0.5] & \Omega_b &\in [0.03,\, 0.07] \\
h &\in [0.5,\, 0.9] & n_s &\in [0.8,\, 1.2] \\
\sigma_8 &\in [0.6,\, 1.0]
\end{aligned}
$$

</div>

</div>

<div v-click="1" class="box-green" style="padding: 0.8rem 1rem">

- Extract small regions ($50\,{\rm Mpc}/h$ on a side, 0.026 % of the box) from each simulation
- Stratified sample in overdensity, to oversample rare over- and under-dense regions
- Region overdensity from the CIC density field
- Measure the halo mass function in each region

</div>

</div>

<!-- box render: large at click 0, bottom-right at click 1 -->
<div class="absolute fig-anim" :style="$clicks >= 1 ? 'right: 3.5rem; top: 15.4rem; width: 16.8rem; height: 15.19rem' : 'right: 3.5rem; top: 2.5rem; width: 28.8rem; height: 26rem'">
  <AutoStages height="100%" :auto="3" :delay="2000" :srcs="[
    '/quijote_story/A_bottom.png',
    '/quijote_story/B_bottom.png',
    '/quijote_story/C_bottom.png',
    '/quijote_story/D_bottom.png',
    '/quijote_story/E_bottom.png',
  ]" />
</div>

<!-- overdensity CDF + region insets: hidden until click 1 -->
<div class="absolute fig-anim" :style="$clicks >= 1 ? 'right: 3.5rem; top: 2.21rem; width: 16.8rem; height: 13.19rem; opacity: 1' : 'right: 3.5rem; top: 2.21rem; width: 16.8rem; height: 13.19rem; opacity: 0'">
  <AutoStages height="100%" :auto="1" :delay="2000" :srcs="[
    '/quijote_story/blank.png',
    '/quijote_story/D_top.png',
    '/quijote_story/E_top.png',
  ]" />
</div>

---

<!-- pptx slides 9 + 10 + 11 combined, staged:
     click 0  emulator text + equation
     click 1  region HMF panels fill the right side
     click 2  global-reconstruction text + equation
     click 3  global HMF replaces the region panels
     click 4  fiducial-model text (bottom left) + the error/cosmology
              plots replace the global HMF -->

<div class="absolute left-14 top-8 bottom-4 w-[28%] flex flex-col text-sm">

<div>

Train a small neural emulator to reproduce the binned halo mass function (HMF) as a function of cosmological parameters and overdensity

<div class="eq-flow">

$$
\hat\Phi(m\,|\,\boldsymbol\theta,\delta) \sim \Phi(m\,|\,\boldsymbol\theta,\delta) + \epsilon(m\,|\,\boldsymbol\theta,\delta)
$$

</div>

</div>

<div v-click="2" class="mt-4">

Reconstruct the *global* HMF by integrating the emulator over overdensity of the parent Quijote box

<div class="eq-box mt-3">

$$
\begin{aligned}
\Phi_{\mathrm{global}}(m\,|\,\boldsymbol\theta) &= \int \Phi(m\,|\,\boldsymbol\theta,\delta)\, p(\delta\,|\,\boldsymbol\theta)\,\mathrm{d}\delta \\[1pt]
&\approx \int \hat\Phi(m\,|\,\boldsymbol\theta,\delta)\, p(\delta\,|\,\boldsymbol\theta)\,\mathrm{d}\delta
\end{aligned}
$$

</div>

</div>

<div v-click="4" class="mt-auto text-sm">

Fiducial: **2048** simulations, 2 regions each — <span class="hl">0.026% of the volume</span>

</div>

</div>

<div class="absolute left-[36%] right-6 top-4 bottom-4">
  <!-- print/export (the /print route): the ranged v-clicks below end
       hidden, so lay out all four figures in a static 2x2 grid instead -->
  <div v-if="$route.path === '/print'" class="h-full grid grid-cols-2 grid-rows-2 gap-2 place-items-center">
    <img src="/pptx/image10_top.webp" class="max-h-full max-w-full" alt="emulated region HMFs">
    <img src="/pptx/image16.webp" class="max-h-full max-w-full" alt="global HMF reconstructions">
    <img src="/pptx/image21.webp" class="max-h-full max-w-full" alt="fractional error vs mass">
    <img src="/pptx/image24.webp" class="max-h-full max-w-full" alt="cosmological parameter dependence">
  </div>
  <template v-else>
    <img v-click="[1, 3]" src="/pptx/image10_top.webp" class="abs-fig" alt="emulated region HMFs">
    <img v-click="[3, 4]" src="/pptx/image16.webp" class="abs-fig" alt="global HMF reconstructions">
    <div v-click="4" class="absolute inset-0 flex flex-col items-center justify-center gap-4">
      <img src="/pptx/image21.webp" class="max-h-[42%]" alt="fractional error vs mass">
      <img src="/pptx/image24.webp" class="max-h-[48%]" alt="cosmological parameter dependence">
    </div>
  </template>
</div>

---
layout: section
---

<!-- pptx slide 13: Tessera section -->

<img src="/figures/tessera.png" class="h-40 mx-auto" alt="Tessera">

<div class="op60 mt-4 text-center">A suite of zooms for emulation and inference</div>

<div class="op75 mt-8 text-center text-sm leading-relaxed px-10">Chris Lovell · Will Roper · Max Lee · Shy Genel · Daniel Anglés-Alcázar · Francisco Villaescusa-Navarro · Claudia Lagos · Ángel Chandro-Gómez · Thomas Bebbington · Carol Cuesta-Lazaro · Shivam Pandey · Yao Zhang · Ben Wandelt · Will&nbsp;Handley</div>

---
layout: two-cols
class: cols-30-70
---

<!-- pptx slide 14: text left, pipeline right; each pipeline stage
     fades in together with its bullet point (pmwd immediately, then clicks 1-4):
     pmwd -> region selection -> SWIFT (+specs) -> SHARK -> Synthesizer -->

<div class="mt-6 text-sm pr-4">

<div>

- **pmwd** differentiable particle-mesh parent simulations (Li+22), $V \sim (1.6\,\mathrm{Gpc}/h)^3$

</div>

<div v-click="1">

- Regions selected across the parent overdensity distribution

</div>

<div v-click="2">

- **SWIFT** zoom code, development led by Will Roper, presentation paper in prep.
- DMO suite, $V \sim (50\,\mathrm{Mpc}/h)^3$, $m_p \sim 10^{9}\,\mathrm{M_\odot}/h$
- $\sim 270^3$ particles at median overdensity; $\sim 350^3$ overdense, $\sim 200^3$ underdense

</div>

<div v-click="3">

- **SHARK** semi-analytic model, predicting galaxy properties and full star formation histories (Lagos+18,23)

</div>

<div v-click="4">

- **Synthesizer** forward modelled emission
- All codes open source

</div>

</div>

::right::

<!-- pipeline snake: row 1 left-to-right, down under region selection,
     row 2 right-to-left — arrows trace the dependency chain -->

<div class="flex items-center justify-center gap-1.5">
  <div class="text-center relative">
    <img src="/pptx/image31.webp" class="h-46 mx-auto" alt="PM parent dark matter projection">
    <img src="/pptx/image8.webp" class="absolute top-[42%] left-[42%] -translate-x-1/2 -translate-y-1/2 h-14" alt="pmwd">
    <div class="caption">PM parent (pmwd)<br>Li+22</div>
  </div>
  <div v-click="1" class="collage-arrow">→</div>
  <div v-click="1" class="text-center">
    <img src="/pptx/image11.webp" class="h-50 mx-auto" alt="region selection in the parent">
    <div class="caption">region selection</div>
  </div>
</div>

<div v-click="2" class="flex justify-end pr-40 -my-1">
  <div class="collage-arrow leading-none" style="font-size: 1.6rem">↓</div>
</div>

<div class="flex items-center justify-center gap-1.5">
  <div v-click="4" class="text-center">
    <img src="/figures/synthesizer_logo.png" class="h-28 mx-auto" alt="Synthesizer">
    <div class="caption max-w-32 mx-auto">Synthesizer forward modelled emission<br>Lovell+25, Roper+26</div>
  </div>
  <div v-click="4" class="collage-arrow" style="font-size: 1.8rem">←</div>
  <div v-click="3" class="text-center">
    <img src="/figures/shark.png" class="h-26 mx-auto" alt="SHARK semi-analytic model">
    <div class="caption max-w-32 mx-auto">SHARK semi-analytic model<br>Lagos+18,23</div>
  </div>
  <div v-click="3" class="collage-arrow" style="font-size: 1.8rem">←</div>
  <div v-click="2" class="text-center">
    <img src="/figures/zoom_cutout_P00485.webp" class="h-42 mx-auto" alt="SWIFT zoom re-simulation: dark matter render of one cut-out region">
    <div class="caption">SWIFT zoom<br>Schaller+24</div>
  </div>
  <img v-click="2" src="/pptx/image14.webp" class="h-20" alt="SWIFT">
</div>

---

<!-- pptx slide 16: the design corner plots motivate the zoom grid
     that follows; a one-line status sits over the top -->

<div class="absolute top-4 left-14 right-14 text-center text-sm op80 leading-snug"><b>1,024 zooms run so far</b>, drawn from an 8,192-point Sobol' design over cosmology and galaxy-formation parameters — an extra 8 × galaxy-formation parameter draws per zoom give the full 8,192-point set from the 1,024 zooms</div>

<div class="grid grid-cols-2 gap-2 h-full items-center pt-12">
  <img src="/figures/v0tessera_params_corner_cosmo.png" class="max-h-106 mx-auto" alt="Sobol design: cosmology corner plot">
  <img src="/figures/v0tessera_params_corner_shark_layers.png" class="max-h-106 mx-auto" alt="Sobol design: SHARK parameters corner plot, layered draws">
</div>

---
class: full-bleed
clicks: 2
---

<!-- deep zoom over public/data/deep_zoom — every first-layer zoom
     rendered at 1024px into one 44032x24576 mosaic, served as a tiled
     pyramid through OpenSeadragon (components/DeepZoomMosaic.vue),
     filling the whole slide (class full-bleed drops the layout
     padding). Each stop is a parent label from layout.json (1024 of
     them) and `clicks: 2` must equal (number of stops - 1). Moving
     straight from one region to another flies out to the overview
     first, then in. The tiles are not in the git repo / web build;
     there the slide falls back to the static mosaic_lowres.jpg. -->

<DeepZoomMosaic
  height="100%"
  :tour="['overview', 'P00485', 'overview']"
  fallback="/figures/mosaic_lowres.jpg"
/>

---

<!-- pptx slide 17 -->

<div class="grid grid-cols-[4fr_5fr] gap-x-2 gap-y-2 h-full items-center -mt-6">
  <div class="flex items-center justify-center gap-2">
    <img src="/figures/hmf_suite_z0_z2.png" class="max-h-60" alt="halo mass functions, z=0 and z=2">
    <img src="/pptx/image14.webp" class="h-12" alt="SWIFT">
  </div>
  <div class="flex items-center justify-center gap-1">
    <img src="/figures/gsmf_suite_z0_z2.png" class="max-h-70 max-w-[84%]" alt="galaxy stellar mass functions with SHARK">
    <img src="/figures/shark.png" class="h-11" alt="SHARK">
  </div>
  <div class="col-span-2 flex items-center justify-center gap-3">
    <img src="/figures/lf_g_suite_z0.png" class="max-h-60" alt="g-band luminosity functions">
    <img src="/figures/synthesizer_logo.png" class="h-14" alt="Synthesizer">
    <img src="/figures/colour_gr_suite_z0.png" class="max-h-60" alt="g-r colour distributions">
  </div>
</div>

---
clicks: 3
---

<!-- the emulator story rerun on the Tessera zooms — held-out regions,
     the global reconstruction, the fractional error, then the
     parameter sweep. components/ZoomStages.vue; `clicks: 3` = (stages - 1). -->

<img src="/pptx/image14.webp" class="abs-tr m-6 h-12" alt="SWIFT">

<div class="flex items-baseline gap-3">
  <h1 class="!mb-0">Emulating Tessera — <em>halo mass function</em></h1>
</div>

<ZoomStages
  class="mt-3"
  height="25rem"
  :stages="[
    { src: '/figures/hmf_regions_fof_z0.png',
      alt: 'emulated HMFs for held-out Tessera regions' },
    { src: '/figures/hmf_global_fof_z0.png',
      alt: 'global HMF reconstruction against the parent Quijote boxes' },
    { src: '/figures/hmf_fractional_fof_z0.png',
      alt: 'fractional error across 65 held-out regions' },
    { src: '/figures/hmf_sweep_fof_z0.png',
      alt: 'emulated HMF as each parameter is swept' },
  ]"
/>

---
clicks: 3
---

<img src="/figures/shark.png" class="abs-tr m-6 h-12" alt="SHARK">

<div class="flex items-baseline gap-3">
  <h1 class="!mb-0">Emulating Tessera — <em>stellar mass function</em></h1>
</div>

<ZoomStages
  class="mt-3"
  height="25rem"
  :stages="[
    { src: '/figures/smf_regions_shark_z0.png',
      alt: 'emulated SMFs for held-out Tessera regions' },
    { src: '/figures/smf_global_shark_z0.png',
      alt: 'global SMF reconstruction against the parent Quijote boxes' },
    { src: '/figures/smf_fractional_shark_z0.png',
      alt: 'fractional error across held-out regions' },
    { src: '/figures/smf_sweep_shark_z0.png',
      alt: 'emulated SMF as each parameter is swept' },
  ]"
/>

---
clicks: 3
---

<img src="/figures/synthesizer_logo.png" class="abs-tr m-6 h-12" alt="Synthesizer">

<div class="flex items-baseline gap-3">
  <h1 class="!mb-0">Emulating Tessera — <em>g-band luminosity function</em></h1>
</div>

<ZoomStages
  class="mt-3"
  height="25rem"
  :stages="[
    { src: '/figures/lf_regions_shark_g_z0.png',
      alt: 'emulated g-band LFs for held-out Tessera regions' },
    { src: '/figures/lf_global_shark_g_z0.png',
      alt: 'global g-band LF reconstruction against the parent Quijote boxes' },
    { src: '/figures/lf_fractional_shark_g_z0.png',
      alt: 'fractional error across held-out regions' },
    { src: '/figures/lf_sweep_shark_g_z0.png',
      alt: 'emulated g-band LF as each parameter is swept' },
  ]"
/>

---
clicks: 2
---

<img src="/figures/synthesizer_logo.png" class="abs-tr m-6 h-12" alt="Synthesizer">

<div class="flex items-baseline gap-3">
  <h1 class="!mb-0">Emulating Tessera — <em>g-r colour</em></h1>
</div>

<ZoomStages
  class="mt-3"
  height="25rem"
  :stages="[
    { src: '/figures/pdf_regions_shark_g-r_z0.png',
      alt: 'emulated g-r colour distributions for held-out Tessera regions' },
    { src: '/figures/pdf_global_shark_g-r_z0.png',
      alt: 'global g-r colour distribution against the parent Quijote boxes' },
    { src: '/figures/pdf_sweep_shark_g-r_z0.png',
      alt: 'emulated g-r colour distribution as each parameter is swept' },
  ]"
/>

---
clicks: 1
---

<!-- two more emulated distributions: the global reconstruction for
     held-out regions first, replaced on click by the parameter sweeps -->

<div class="abs-tr m-6 flex items-center gap-4">
  <img src="/pptx/image14.webp" class="h-12" alt="SWIFT">
  <img src="/figures/shark.png" class="h-12" alt="SHARK">
</div>

<div class="flex items-baseline gap-3">
  <h1 class="!mb-0 pr-40">Emulating Tessera — <em>c–M relation and main sequence</em></h1>
</div>

<div class="relative mt-3" style="height: 25rem">

<div v-click.hide="1" class="absolute inset-0 grid grid-cols-2 gap-6 items-center">
  <div>
    <img src="/figures/cM_global_z0.png" class="w-full" alt="global concentration-mass relation for held-out regions: emulated median and 16-84 per cent range against the fiducial">
  </div>
  <div>
    <img src="/figures/sfms_global_z0.png" class="w-full" alt="global star-forming main sequence for held-out regions">
  </div>
</div>

<div v-click="1" class="absolute inset-0 grid grid-cols-[11fr_9fr] gap-4 items-center">
  <div>
    <img src="/figures/cM_sweep_z0.png" class="w-full" alt="emulated concentration-mass relation as each parameter is swept">
  </div>
  <div>
    <img src="/figures/sfms_sweep_z0.png" class="max-h-100 mx-auto" alt="emulated star-forming main sequence as each parameter is swept">
  </div>
</div>

</div>

---

<!-- Clustering paper (~/Documents/papers/tessera_clustering, in prep):
     two-point emulation from zoom regions alone. Figure copied from
     the paper's figures/global.png into public/clustering/. -->

<div class="w-[44%] min-w-0">

<div class="flex items-baseline gap-3">
  <h1 class="!mb-0">Clustering from zooms</h1>
  <span class="prelim-inline">in prep</span>
</div>

<div class="op70 text-sm mt-1 leading-snug">with Carol Cuesta-Lazaro, Yao Zhang, Ben Wandelt,<br>Anik Halder &amp; Lurdes Ondaro-Mallea</div>

<div class="mt-2" style="font-size: 0.74rem; line-height: 1.32">

- Halo / galaxy $\xi(r)$ and $P(k)$ as a function of cosmology $\boldsymbol\theta$ from <span class="hl">small zoom regions alone</span> — no full-volume catalogue needed
- **Small scales ($r \lesssim 20\,{\rm Mpc}/h$):** pairs counted *inside* each region; two neural Poisson emulators — the region's halo count, and its pair counts at fixed count — conditioned on $\boldsymbol\theta$ and the region overdensity $\delta_R$, integrated over $p(\delta_R\,|\,\boldsymbol\theta)$
- **Large scales ($r \gtrsim 20\,{\rm Mpc}/h$):** perturbation-theory matter correlation function × linear bias$^2$, the bias emulated from the <span class="hl">response of the halo abundance to $\delta_R$</span>

<div class="eq-box my-1" style="font-size: 0.72rem; padding: 0.25rem 0.5rem">

$$
\begin{aligned}
1 + \xi_{hh}(r) = {}& w(r)\,[1 + \xi_{\rm small}(r)] \\
&+ [1 - w(r)]\,\big[1 + b(\boldsymbol\theta)^2\,\xi_{mm}^{\rm CLPT}(r;\boldsymbol\theta)\big]
\end{aligned}
$$

</div>

- **Validated on Quijote:** 8 × $(50\,{\rm Mpc}/h)^3$ regions per $(1\,{\rm Gpc}/h)^3$ box — <span class="hl">0.1 % of the volume</span> — from 7168 boxes: $\xi_{hh}$ to <span class="hl">−2 / +3 % at $10\,{\rm Mpc}/h$</span> and at the box's own sample-variance floor above $30\,{\rm Mpc}/h$; abundance bias within 1–3 % of the clustering bias

</div>

</div>

<!-- figure spans the full slide height on the right, outside the
     layout padding -->
<div class="absolute top-2 bottom-7 left-[51%] right-3">
  <img src="/clustering/global.png" class="h-full w-full object-contain" alt="joined correlation-function prediction against the full-box truth for six held-out Quijote cosmologies spanning the error range">
</div>

---

<!-- equivalent cost + SAM outputs (cost numbers from the beamer
     backup slide "what would the zoom suite cost?") -->

# Cost and outputs

<div class="grid grid-cols-2 gap-10 mt-6">

<div>

**Equivalent cost**

- A single equivalent resolution periodic box in the same volume (e.g AbacusSummit) would require $8192^3$ particles, and cost $\sim 9$ million core-hours
- A suite of $\sim 1000$ such simulations would cost <span class="hl">9 billion core-hours</span>
- This zoom suite so far cost <span class="hl">less than 1 million core hours</span>
- Each zoom fits on a single cosma7 node, making scheduling trivial, and easily fills spare capacity on the machine; the PM parents are essentially free
- **Verification**: If a single parent volume at the same resolution as the zooms costs $9 \times$ the cost of the entire zoom suite, how can we efficiently verify the outputs of the global emulation?

</div>

<div>

**Disk and forward-modeling**

- A single AbacusSummit snapshot output is $\sim 3.5$ Tb, outputting the $\sim 140$ snapshots required for building high fidelity merger trees would consume half a Petabyte
- In contrast, each zoom with 140 outputs consumes $\sim 100$ Gb
- Zooms are post-processed *one by one* as they finish - no need to store or process a monolithic box
- Snapshots can be cleaned once trees are constructed, further reducing the footprint to $\sim 17$ Gb, around 17 Tb for a suite of a thousand

</div>

</div>

---

# Extensions

<div class="grid grid-cols-[11fr_9fr] gap-8 items-center mt-1">

<div class="hydro-list">

- **Tessera-HD**: hydrodynamical zooms at CAMELS resolution, varying <span class="hl">galaxy-formation parameters alongside cosmology</span> — $10^5$ times the effective volume of CAMELS
- Can apply **ILI / SBI** as well as explicit likelihood approaches to these emulated distributions / correlation functions
- Multi-fidelity training using DMO + SAM suite as the cheap level and a few hydro zooms as the expensive one (Saoulis+26, Niall Jeffrey)
- **Self-consistent selection of multiple tracers**: we have a <span class="hl">fully physical, forward-model for galaxies and their emission</span>, and so can select e.g. LRGs and ELGs self-consistently, allowing cross correlation studies naturally

</div>

<div>
<img src="/figures/baryonic_volume_6_tessera.png" class="max-h-104 mx-auto" alt="resolved halo mass vs volume plane with Tessera (dark-matter-only) and Tessera-HD (hydrodynamical) at 2 Gpc/h cubed">
</div>

</div>

---

<!-- pptx slide 18 -->

# Summary

<!-- text left; cosmic-web strip + zoom callouts right, mirroring the
     title slide. The Tessera-region zoom shows from the start;
     next steps + the correlation-function zoom appear on click 1.
     Callout geometry is in the 1280x720 SVG grid; the circular
     insets are HTML .zoom-slot divs positioned in % of the slide. -->

<div class="absolute left-14 top-24 w-[50%]">

- We have demonstrated a new method for <span class="hl">emulating distribution functions from composite zoom simulation suites</span> using neural density estimators — <span class="arxiv">arXiv:2604.17981</span>
- **Tessera** is a new simulation suite allowing the exploration of the <span class="hl">large volume, high fidelity regime</span> with self-consistent forward modelled galaxies and their emission, using open source tools

<div v-click="1" class="next-steps mt-6">

**Future work**

- higher order statistics — early tests emulating the two-point correlation function promising (right), using a similarly small fraction of the box volume
- full hydrodynamic simulations, leveraging multi-fidelity techniques to reduce the training number (Saoulis+26)
- Cross-over with the **DREAMS** simulations (Jonah Rose and Alex Garcia)
- Field level emulation (halo catalogues and baryonification)

</div>

</div>

<img src="/pptx/title_strip.webp" class="title-strip-right" alt="">

<svg class="title-zooms" viewBox="0 0 1280 720" preserveAspectRatio="none" aria-hidden="true">
  <g>
    <circle class="region" cx="1185" cy="110" r="12" />
    <path class="cone" d="M 1185 110 L 935 62 L 935 198 Z" />
  </g>
  <g>
    <circle class="region" cx="1170" cy="300" r="12" />
    <path class="cone" d="M 1170 300 L 905 262 L 905 398 Z" />
  </g>
  <g v-click="1">
    <circle class="region" cx="1160" cy="560" r="14" />
    <path class="cone" d="M 1160 560 L 900 458 L 900 622 Z" />
  </g>
</svg>

<div class="zoom-slot" style="left: 67.7%; top: 8.6%; width: 10.6%">
  <img src="/figures/zoom_region_dense.webp" class="w-full h-full object-cover" alt="Tessera zoom region">
</div>
<!--div class="slot-label" style="left: 73%; top: 30.5%">a Tessera zoom region</div-->

<div class="zoom-slot" style="left: 65.4%; top: 36.1%; width: 10.6%">
  <img src="/figures/arxiv_qr.png" class="w-full h-full object-contain p-[13%] bg-white" alt="arXiv QR code">
</div>
<div class="slot-label" style="left: 70.7%; top: 58%">arXiv:2604.17981</div>

<div v-click="1" class="zoom-slot" style="left: 63.9%; top: 63.6%; width: 12.8%">
  <img src="/clustering/global_inset.webp" class="w-full h-full object-contain bg-white" alt="halo correlation function emulated from zoom regions against the full box">
</div>
<div v-click="1" class="slot-label" style="left: 70.3%; top: 90%">&xi;(r) from zoom regions</div>
---

# How many simulations?

<div class="w-[24rem]" style="font-size: 0.86rem; line-height: 1.35">

- $N_\mathrm{sim}$ is the number of input Quijote simulations
- $N_\mathrm{samp}$ is the number of regions sampled from each simulation
- We find that there is no preferences for greater number of regions or samples; greater diversity in cosmological parameter space does not lead to much better results compared to greater diversity in overdensity space at fixed cosmology

<!-- figures from ~/Documents/papers/hmf_emulator (Lovell+26), copied
     into public/hmf_emulator/ -->

<img src="/hmf_emulator/realisation_region_grid_massbin_median_abs_frac_error_regions12.png" class="max-h-62 mt-3 mx-auto" alt="median absolute fractional error per mass bin for 1 or 16 regions from each of N_sim simulations">

</div>

<div class="absolute top-2 bottom-8 right-8 w-[21rem] flex flex-col items-center justify-between">
  <img src="/hmf_emulator/realisation_region_grid_comparison.png" class="max-h-[15.2rem]" alt="error vs number of simulations, one line per regions-per-simulation">
  <img src="/hmf_emulator/realisation_region_grid_total_simulations_comparison.png" class="max-h-[15.2rem]" alt="error vs total number of regions">
</div>

---

# What volume for each region?

<div class="w-[24rem]" style="font-size: 0.86rem; line-height: 1.35">

- The overall volume of all combined regions correlates strongly with performance
- There is a slight preference for regions that are large enough to overcome cosmic variance
- At > 70 Mpc/h the performance plateau's

<img src="/hmf_emulator/voxel_total_regions_grid_massbin_median_abs_frac_fixed_num_sims.png" class="max-h-62 mt-3 mx-auto" alt="error per mass bin for region sides from 27 to 102 Mpc/h, one region from 4096 simulations">

</div>

<div class="absolute top-2 bottom-8 right-8 w-[21rem] flex flex-col items-center justify-between">
  <img src="/hmf_emulator/voxel_total_regions_grid_median_abs_frac_vs_num_sims.png" class="max-h-[15.2rem]" alt="error vs number of simulations for each region volume">
  <img src="/hmf_emulator/voxel_total_regions_grid_median_abs_frac_vs_total_volume.png" class="max-h-[15.2rem]" alt="error vs total simulated volume for each region volume">
</div>

---

<!-- FLAMELS meeting deck (Aug 2026), "Parent convergence tests" slides:
     figures in public/flamels/ -->

# Parent convergence tests

<div class="grid grid-cols-[10fr_13fr] gap-3 items-start mt-1">
<img src="/flamels/parent_convergence_pdf.png" class="max-h-70 mx-auto" alt="overdensity PDFs, ratio to the N-body reference and percentile shift for PM 512^3 and 1024^3 parents at three smoothing scales">
<img src="/flamels/parent_convergence_z.png" class="max-h-70 mx-auto" alt="maximum percentile error and 68th-percentile rank shift against redshift for PM 512^3, PM 1024^3 and N-body 512^3 parents">
</div>

<div class="grid grid-cols-2 gap-8 mt-2 text-sm">

<div>

- Overdensity PDFs on $R = 16$, $31$, $57\,h^{-1}$ Mpc spheres at $z = 0, 1, 4$: pmwd at $512^3$ and $1024^3$ vs a $1024^3$ N-body reference
- $512^3$ PM biases $1 + \delta_R$ by up to <span class="hl">±4 %</span> at the smallest scale; $1024^3$ stays within <span class="hl">≈ 0.5 %</span>

</div>

<div>

- Selection only needs the region's percentile: with $1024^3$ the maximum error over $p \in [1, 99]$ and the typical rank shift stay <span class="hl">below one percentile</span> at every redshift
- $512^3$ PM and $512^3$ N-body both drift past one percentile for $z \gtrsim 4$ — resolution-limited, not PM-limited

</div>

</div>

---

<!-- FLAMELS meeting deck (Aug 2026), "PM simulations + Selection" -->

# PM parent simulations and region selection

<div class="grid grid-cols-[3fr_2fr] gap-8 items-center mt-2">

<div class="text-sm">

- **512 parent runs complete**, run in serial on an H100 node on cosma8
- Exploring Google TPU resources (David Yallup); Isambard AI / Isambard 3 also available (Thomas Bebbington, Sotiria Fotopoulou)
- New code, `gridder_gpu`, performs the overdensity calculation in memory on the GPU
- **Selection:** if a FOF halo lies on a region boundary, the region is extended to include the whole halo
- Percentile / quantile tables of the overdensity field stored at every output snapshot for downstream use — the $p(\delta\,|\,\boldsymbol\theta)$ that the global reconstruction integrates over
- The PM parent is only asked for the *environment*: its halo mass function agrees with a full SWIFT N-body run above $\sim 10^{14.5}\,{\rm M_\odot}$ but under-resolves lower-mass haloes (right) — those come from the zooms

</div>

<div>
<img src="/flamels/pm_vs_nbody_hmf.png" class="max-h-96 mx-auto" alt="halo mass function of a pmwd PM parent against a full SWIFT N-body run of the same volume, with the ratio">
<div class="caption">pmwd PM parent vs full SWIFT N-body, same initial conditions</div>
</div>

</div>
