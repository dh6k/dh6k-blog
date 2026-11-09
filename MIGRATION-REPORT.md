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

## GitHub — DONE 2026-11-09 02:27
- Repo: https://github.com/dh6k/dh6k-blog (public, branch `main`).
- Commits: `6b254c6` feat migrate + `22be960` Giscus General fix. Author `dh6k` noreply, no AI credit.
- Discussions enabled. Giscus: repo `dh6k/dh6k-blog`, repoId `R_kgDOVnZMNg`, category **General** `DIC_kwDOVnZMNs4DKrfA` — GitHub has no API to create a discussion category (REST + GraphQL both 404/undefined field), so "Comments" could not be created programmatically; General is the fallback. Env vars in `.env.example` match these values.

## Vercel — DEPLOYED LIVE 2026-11-09 02:39
- Connector `connected` 02:34, team `dh6k's projects` (`team_FZqq9pZP5QcaatuUgfkWPq2E`, Hobby), user `dh6k` / `duya-sensei@dh6k.vip`.
- First `create_git_project` failed 400 `repo_not_found` — GitHub App lacked access to the new repo; user granted it in GitHub Settings → Applications → Vercel → Configure (02:39), `search_repo` then found `dh6k-blog` (id 1450593334).
- Project `dh6k-blog` (`prj_8amogBxHlHkCBAljKeOFkSmqs6D3`), linked to `dh6k/dh6k-blog`, production branch `main`.
- Env vars set (production + preview): `PUBLIC_GISCUS_REPO`, `PUBLIC_GISCUS_REPO_ID`, `PUBLIC_GISCUS_CATEGORY_ID`, `PUBLIC_BUTTONDOWN_USERNAME` (= `dh6k`, unverified).
- First production deploy `dpl_9EcvGC7mgZtsGBg8p5BEosSu2Uce` READY from `22be960`. Note: env vars were added after that build started, so a redeploy (`dpl_45dJ...`, READY, target null) + `request_promote` (422, failed) did not put env vars into production. Fix that worked: commit `612c42e` (site URL → `https://dh6k-blog.vercel.app`) pushed → auto production deploy `dpl_BtY8G9NqFsgEenmSre8uU3mU92Fc` READY.
- **Live: https://dh6k-blog.vercel.app/** — verified 02:41: homepage lists 11 posts + newsletter form; BA gacha post renders full content + 6 `_astro/*.webp` images; Giscus `client.js` with correct `data-repo`/`data-repo-id`/`data-category-id` present in live HTML; RSS 11 items, sitemap OK.
- `astro.config.mjs` site now `https://dh6k-blog.vercel.app` (change when custom domain is decided).
- Buttondown username confirm (defaults to `dh6k`, unverified).

## Custom domain — DONE 2026-11-09 03:03
- User chose `blog.dh6k.vip` (was CNAME → `ghs.google.com`, proxied, since 2026-07-14).
- Cloudflare connector `custom.cloudflare` (OAuth2 + DCR, MCP `https://mcp.cloudflare.com/mcp`) connected 02:48; `whoami` = `duyanhhoangquoc@gmail.com`; zone `dh6k.vip` (`069c2f3112b2ff7071e38d546e6b2740`, active). First `list-tools` failed 403 Error 1010 — urllib's default User-Agent banned by WAF; fixed with a browser User-Agent header in `client.py`.
- Added `blog.dh6k.vip` to Vercel project (02:51); Vercel asked for TXT `_vercel.dh6k.vip` = `vc-domain-verify=blog.dh6k.vip,d4786f1dc9eea1e98849`.
- DNS via Cloudflare API: CNAME `blog.dh6k.vip` → `cname.vercel-dns.com` (DNS-only, record `0aa74a0b...`), TXT `_vercel.dh6k.vip` added. Both confirmed propagated via DoH (1.1.1.1).
- Commit `02b4bfe` changed `site` to `https://blog.dh6k.vip` → auto production deploy `dpl_Ezs43JyH8UDTSqfZWs2JoeCwaeyi` READY.
- Vercel stayed `verified: false` ~10 min after DNS went live, curl returned empty reply. Fix: dashboard Refresh (browser, signed in via GitHub dh6k) at 03:02 — status moved to "DNS Change Recommended", and Vercel recommended the new CNAME value `27f95937afd5f18f.vercel-dns-017.com` (IP-range expansion; legacy `cname.vercel-dns.com` still works).
- CNAME updated to `27f95937afd5f18f.vercel-dns-017.com` (DNS-only) 03:03; DoH confirms propagation; Vercel now reports `blog.dh6k.vip` **verified: true**.
- **Live: https://blog.dh6k.vip/** — verified 03:03: homepage HTTP 200, title "dh6k's blog", Odysseus post linked; post page HTTP 200. `hn.dh6k.vip` still points to Hashnode (untouched, no redirect set up).
- `astro.config.mjs` site now `https://blog.dh6k.vip`.

## Theme — synced with dh6k.vip / gh.dh6k.vip, DONE 2026-11-09 09:24
- Restyle commit `ff07b6d` (19 files), deploy `dpl_9wdazvK2yBodYHsYEKeN36AndZuP` READY, verified live 09:24.
- Design tokens shared with both sites: dark bg `#0b0b0f`, surface `#111117`, ink `#f4f1f5`, muted `#aaa5af`, accent pink `#ff3d91`, line `#2b2832`; pink radial glow + dot grid background (from dh6k.vip panels / gh radial glow).
- Fonts self-hosted, downloaded from dh6k.vip `/assets/fonts/` into `src/assets/fonts/`, registered via `fontProviders.local()` in `astro.config.mjs`: Major Mono Display (brand + hero, lowercase), Beth Ellen (handwritten accents), Lexend (display/headings), Maven Pro (headings), Asap (body + italic). Atkinson removed (woff files deleted). Fonts emitted to `dist/_astro/fonts/*.woff2`, verified HTTP 200 live.
- Header (gh style): brand `dh6k's blog` in Major Mono (pink `'s blog`), nav mono uppercase with accent underline on active page; Astro/Mastodon/Twitter links removed, GitHub link added. Footer: © dh6k + links GitHub / dh6k.vip / gh.dh6k.vip / RSS.
- Homepage: hero (eyebrow `blog.dh6k.vip`, mono title, SITE_DESCRIPTION lede) + featured latest post with cover + remaining posts as gh-style row list (title + mono date). `/blog` same row list. Post page: article nav (← all posts + date), eyebrow, Lexend title, description, tag pills, hero image, prose `#cbc7ce`; Newsletter restyled as surface card with pill input + pink handwritten button; Giscus theme `transparent_dark`.
- `src/pages/about.astro` still has template lorem ipsum content — style is synced (renders through BlogPost layout) but the text itself was not rewritten.

## How to run locally
```bash
cd ~/workspace/hashnode-astro-export
npm run dev      # or: npm run build && npm run preview
```
