import { defineConfig } from 'vite'

// public/{figures,flamels,pptx,data} are symlinks into
// ../slidev_ltu_tsg/public. Slidev's slide-import guard realpaths
// public assets and rejects anything outside public/, so it has to be
// switched off (it only runs when server.fs.strict is true). Vite itself
// serves and copies the symlinked files fine.
export default defineConfig({
  server: { fs: { strict: false } },
})
