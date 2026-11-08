#!/usr/bin/env python3
"""Export Hashnode (hn.dh6k.vip, no Pro) -> Astro Content Collections.
Source of truth: RSS for metadata (title/date/tags/cover) + .md endpoint for body.
No API key, no Pro needed.
"""
import re, os, sys, json, html, urllib.request, urllib.parse
from pathlib import Path
from email.utils import parsedate_to_datetime
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent.parent
OUT_BLOG = BASE / "src" / "content" / "blog"
OUT_IMG = BASE / "src" / "assets" / "blog"
RAW_DIR = BASE / "export" / "raw"
for d in (OUT_BLOG, OUT_IMG, RAW_DIR):
    d.mkdir(parents=True, exist_ok=True)

NS = {"content": "http://purl.org/rss/1.0/modules/content/"}
tree = ET.parse(BASE / "rss.xml")
report = {"posts": [], "failed_images": [], "total_images": 0}

def fetch(url, dest=None):
    # urllib hits IncompleteRead on cdn.hashnode.com (truncated chunked bodies);
    # curl handles it fine. Strip #fragment for the download.
    clean = url.split("#", 1)[0]
    import subprocess
    if dest:
        r = subprocess.run(["curl", "-sL", "--retry", "3", "--retry-all-errors",
                            "-A", "Mozilla/5.0 (X11; Linux x86_64) dh6k-hashnode-export",
                            "-o", str(dest), clean],
                           capture_output=True, timeout=120)
        if r.returncode != 0 or not dest.exists() or dest.stat().st_size == 0:
            raise RuntimeError(f"curl exit {r.returncode}: {r.stderr.decode()[:200]}")
        data = dest.read_bytes()
        # guess content-type from extension
        ext = dest.suffix.lower()
        ctype = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                 ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml"}.get(ext, "image/png")
        return data, ctype
    r = subprocess.run(["curl", "-sL", "--retry", "3", "--retry-all-errors",
                        "-A", "Mozilla/5.0 (X11; Linux x86_64) dh6k-hashnode-export", clean],
                       capture_output=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"curl exit {r.returncode}: {r.stderr.decode()[:200]}")
    return r.stdout, "text/markdown"

def safe_ext(url, ctype):
    path = urllib.parse.urlparse(url).path
    ext = Path(path).suffix.lower()
    if ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif"):
        return ext
    return { "image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif",
             "image/webp": ".webp", "image/svg+xml": ".svg" }.get(ctype, ".png")

def yaml_str(s):
    # double-quoted YAML string, escape backslash + quote
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'

def clean_text(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return re.sub(r"\s+", " ", s).strip()

items = tree.getroot().iter("item")
for item in items:
    title = item.findtext("title") or ""
    link = item.findtext("link") or ""
    slug = link.rstrip("/").rsplit("/", 1)[-1]
    pub = item.findtext("pubDate") or ""
    try:
        pubdate = parsedate_to_datetime(pub).strftime("%Y-%m-%d")
    except Exception:
        pubdate = ""
    desc = clean_text(item.findtext("description") or "")
    if len(desc) > 160:
        desc = desc[:157].rsplit(" ", 1)[0] + "..."
    tags = []
    for c in item.findall("category"):
        if c.text:
            t = c.text.strip().strip("`").strip("#").strip()
            if t:
                tags.append(t)
    enc = item.find("enclosure")
    cover_url = enc.get("url") if enc is not None else None

    # 1. download .md body
    md_url = f"https://hn.dh6k.vip/{slug}.md"
    try:
        raw_bytes, _ = fetch(md_url)
        raw = raw_bytes.decode("utf-8", errors="replace")
    except Exception as e:
        report["posts"].append({"slug": slug, "status": "FAILED_MD", "error": str(e)})
        print(f"FAIL md {slug}: {e}", file=sys.stderr)
        continue
    (RAW_DIR / f"{slug}.md").write_text(raw, encoding="utf-8")

    # 2. collect image urls from body (markdown + html img)
    img_urls = []
    for m in re.finditer(r"!\[[^\]]*\]\(\s*([^\s)]+)", raw):
        img_urls.append(m.group(1))
    for m in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', raw):
        img_urls.append(m.group(1))
    # dedupe, keep order; only http(s)
    seen, uniq = set(), []
    for u in img_urls:
        u = u.strip()
        if u.startswith("http") and u not in seen:
            seen.add(u); uniq.append(u)

    # 3. download body images
    url_to_local = {}
    for i, u in enumerate(uniq, 1):
        try:
            data, ctype = fetch(u)
            ext = safe_ext(u, ctype)
            fname = f"{slug}-{i:02d}{ext}"
            (OUT_IMG / fname).write_bytes(data)
            url_to_local[u] = f"../../assets/blog/{fname}"
            report["total_images"] += 1
        except Exception as e:
            report["failed_images"].append({"slug": slug, "url": u, "error": str(e)})
            print(f"FAIL img {slug} {u}: {e}", file=sys.stderr)

    # 4. cover image (enclosure) -> heroImage, if not already downloaded
    hero_rel = None
    if cover_url:
        if cover_url in url_to_local:
            hero_rel = url_to_local[cover_url]
        else:
            try:
                data, ctype = fetch(cover_url)
                ext = safe_ext(cover_url, ctype)
                fname = f"{slug}-cover{ext}"
                (OUT_IMG / fname).write_bytes(data)
                hero_rel = f"../../assets/blog/{fname}"
                report["total_images"] += 1
            except Exception as e:
                report["failed_images"].append({"slug": slug, "url": cover_url, "error": str(e)})
                print(f"FAIL cover {slug}: {e}", file=sys.stderr)

    # 5. rewrite body: replace urls, strip align="...", strip duplicate H1
    body = raw
    for u, local in url_to_local.items():
        body = body.replace(u, local)
    # ![](local align="center") -> ![](local)
    body = re.sub(r"(!\[[^\]]*\]\([^)\s]+)\s+align=\"[^\"]*\"(\))", r"\1\2", body)
    body = re.sub(r"(!\[[^\]]*\]\([^)\s]+)\s+align='[^']*'(\))", r"\1\2", body)
    lines = body.splitlines()
    # drop leading blank lines + first H1 if it equals title
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].strip() == f"# {title}":
        lines.pop(0)
        while lines and not lines[0].strip():
            lines.pop(0)
    body = "\n".join(lines).rstrip() + "\n"

    # 6. frontmatter
    fm = ["---", f"title: {yaml_str(title)}", f"description: {yaml_str(desc)}",
          f"pubDate: {pubdate}"]
    if hero_rel:
        fm.append(f"heroImage: {yaml_str(hero_rel)}")
    tags_yaml = "[" + ", ".join(yaml_str(t) for t in tags) + "]"
    fm.append(f"tags: {tags_yaml}")
    fm.append("---\n")
    out = "\n".join(fm) + body
    (OUT_BLOG / f"{slug}.md").write_text(out, encoding="utf-8")
    report["posts"].append({"slug": slug, "title": title, "pubDate": pubdate,
        "tags": tags, "images": len(uniq), "cover": bool(hero_rel), "status": "OK"})
    print(f"OK {slug} | {pubdate} | imgs={len(uniq)} cover={bool(hero_rel)} tags={tags}")

(BASE / "export" / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nDone: {len(report['posts'])} posts, {report['total_images']} images, failed={len(report['failed_images'])}")
