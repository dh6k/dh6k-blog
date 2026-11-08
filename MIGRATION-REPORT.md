# Hashnode → Astro — Migration Report

Date: 2026-11-09 02:21 +07. Source: `https://hn.dh6k.vip` (publication `61ed6370e247b2151e61a1e5`, no Pro).

## Export — DONE, verified
- Method: RSS for metadata + `https://hn.dh6k.vip/<slug>.md` for body. No API/Pro needed.
- 11/11 posts exported, 0 failed.
- 36/36 images downloaded to `src/assets/blog/` (18 MB source), 0 failed, 0 remaining `cdn.hashnode` refs in source or built HTML.
- Frontmatter per post: `title`, `description` (from RSS, ≤160 chars), `pubDate` (YYYY-MM-DD from RSS), `heroImage` (only when RSS had an enclosure cover — 5 posts), `tags` (from RSS categories, backticks/`#` stripped).
- 5 posts with cover: Odysseus, Blue Archive gacha, Chrome Enterprise, Arch legacy, Nội quy.
- 6 posts without cover (no enclosure in RSS): OpenCodex, CRX extension, Google 2009, Project KV, Nitro, Userscript reup.
- Raw originals kept in `export/raw/`, RSS snapshot in `rss.xml`, machine report in `export/report.json`. Export script: `scripts/export.py` (curl-based — urllib hits IncompleteRead on cdn.hashnode.com, curl does not).

## Astro project — DONE, build verified
- Astro 7.4.7, template `blog`, Node >=22. `npm run build` PASS 02:21, 14 pages, 9.87s.
- Pages: `/`, `/blog/`, 11 × `/blog/<slug>/`, `/about`, `/rss.xml`, sitemap.
- `src/content.config.ts`: added `tags: z.array(z.string()).default([])` to template schema.
- `src/consts.ts`: SITE_TITLE `dh6k's blog`.
- `astro.config.mjs`: `site: 'https://hn.dh6k.vip'` — TODO, change when custom domain is decided.
- Homepage (`src/pages/index.astro`) replaced template placeholder with post list + Newsletter.
- `src/layouts/BlogPost.astro`: shows tags, `<Newsletter />`, `<Comments />`.
- Images optimized by Astro/Sharp: 42 images, e.g. BA gacha cover 424 kB → 63 kB, BA-01 3.2 MB → 188 kB. `dist/` total 2.7 MB.
- Giscus: `src/components/Comments.astro` — renders nothing until `PUBLIC_GISCUS_REPO/REPO_ID/CATEGORY_ID` are set (needs real repo + Discussions). See `.env.example`.
- Newsletter: `src/components/Newsletter.astro` — Buttondown form, username defaults to `dh6k`, change in `.env` (`PUBLIC_BUTTONDOWN_USERNAME`).

## NOT done yet — needs user
- GitHub repo name + push. Local project is NOT committed/pushed yet (per standing rule: user reviews/commits himself unless he explicitly says push).
- Vercel import + deploy (needs repo).
- Giscus IDs (needs repo + Discussions enabled).
- Buttondown username confirm (defaults to `dh6k`, unverified).
- Custom domain — explicitly deferred by user, ask when it comes up.

## How to run locally
```bash
cd ~/workspace/hashnode-astro-export
npm run dev      # or: npm run build && npm run preview
```
