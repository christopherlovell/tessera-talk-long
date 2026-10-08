# Tessera talk (long version) — Slidev deck

Part II of the LtU TSG update (`../slidev_ltu_tsg`) on its own: the
volume–resolution trade-off, the multi-zoom approach, the Quijote proof
of concept and Tessera (pipeline, design, emulation, clustering,
extensions, cost), closing on the summary slide.
Split out from the LtU deck on 2026-09-29. This folder is one workspace
of the parent `../package.json`, so `node_modules` lives in `..` and is
shared with the other decks — run `npm install` from `..`, not here.

## Assets

`public/` holds real copies of just the figures this deck uses
(`figures`, `flamels`, `pptx` were trimmed from the LtU deck's folders
on 2026-10-08, ~27 MB in all), plus the deck-owned `clustering`,
`hmf_emulator` and `quijote_story` folders. The one exception is the
deep-zoom tile pyramid, `public/data/deep_zoom` (~340 MB): locally it is
a symlink into `../slidev_ltu_tsg/public/data/deep_zoom` and it is
gitignored, so the web build shows a static low-res render of the
mosaic (`figures/mosaic_lowres.jpg`, level 12 of the pyramid) instead
of the OpenSeadragon tour. `vite.config.ts` relaxes Vite's strict fs
check so that symlink works in dev.

`components/` and `style.css` are copies (only the components Part II
uses), so they can drift from the LtU deck independently.

## GitHub Pages

This folder is its own git repo. `.github/workflows/deploy.yml` builds
the deck with `--base /<repo-name>/` and publishes `dist/` on every push
to `main` (repo Settings → Pages → Source: GitHub Actions). To stand it
up the first time:

```bash
gh repo create <repo-name> --public --source . --push
```

## Quick start

```bash
npm install        # from ..
npm run dev        # live-reloading talk at http://localhost:3030
```

Press `p` in the browser for presenter mode, `o` for slide overview.

| command | does |
|---|---|
| `npm run dev` | dev server with hot reload |
| `npm run build` | static site in `dist/` (deployable anywhere) |
| `npm run export:pdf` | PDF export (snap chromium) |
| `npm run data` | regenerate `public/data/*.json` |
