# dh6k-blog

Personal blog — Astro static site, migrated from Hashnode (`hn.dh6k.vip`).

## Content

11 posts in `src/content/blog/`, images in `src/assets/blog/`. Export source: Hashnode RSS + `.md` endpoint (no Pro needed). See `MIGRATION-REPORT.md` and `scripts/export.py`.

## Develop

```bash
npm install
npm run dev
npm run build
```

## Stack

- Astro 7 (Content Collections, `src/content.config.ts`)
- Giscus comments (GitHub Discussions) — see `.env.example`
- Buttondown newsletter — see `.env.example`
- Deploy: Vercel (static, `dist/`)
