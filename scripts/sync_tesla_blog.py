#!/usr/bin/env python3
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

BLOG_URL = "https://www.atesla.rs/blog"
RSS_URLS = [
    "https://www.atesla.rs/blog-feed.xml",
    "https://www.atesla.rs/feed.xml",
]
UA = "Mozilla/5.0 (compatible; GoBigBlogSync/1.0; +https://www.atesla.rs/blog)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, text/html;q=0.9,*/*;q=0.8"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()


def clean_html(value):
    value = re.sub(r"<script.*?</script>|<style.*?</style>", " ", value or "", flags=re.S | re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def image_from_html(value):
    m = re.search(r'<img[^>]+src=["\']([^"\']+)', value or "", flags=re.I)
    return unescape(m.group(1)) if m else ""


def parse_rss(data):
    root = ET.fromstring(data)
    items = []
    for item in root.findall(".//item"):
        title = clean_html(item.findtext("title"))
        link = (item.findtext("link") or "").strip()
        if not title or "/post/" not in link:
            continue
        desc_raw = item.findtext("description") or ""
        desc = clean_html(desc_raw)
        pub = (item.findtext("pubDate") or "").strip()
        date_display = pub
        if pub:
            try:
                date_display = parsedate_to_datetime(pub).strftime("%b %-d, %Y")
            except Exception:
                pass
        image = ""
        enclosure = item.find("enclosure")
        if enclosure is not None and enclosure.attrib.get("url"):
            image = enclosure.attrib["url"]
        if not image:
            for child in item:
                tag = child.tag.lower()
                if tag.endswith("content") or tag.endswith("thumbnail"):
                    if child.attrib.get("url"):
                        image = child.attrib["url"]
                        break
        if not image:
            image = image_from_html(desc_raw)
        items.append({
            "title": title,
            "url": link,
            "date": date_display,
            "summary": desc[:260],
            "image": image,
            "source": "TESLA Alliance"
        })
    return items


class BlogParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []
        self.current = None
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "/post/" in attrs.get("href", ""):
            href = attrs["href"]
            if href.startswith("/"):
                href = "https://www.atesla.rs" + href
            self.current = {"title_parts": [], "url": href, "image": ""}
            self.depth = 1
        elif self.current:
            self.depth += 1
            if tag == "img" and not self.current["image"]:
                self.current["image"] = attrs.get("src", "") or attrs.get("data-src", "")

    def handle_data(self, data):
        if self.current:
            text = re.sub(r"\s+", " ", data).strip()
            if text:
                self.current["title_parts"].append(text)

    def handle_endtag(self, tag):
        if self.current:
            self.depth -= 1
            if tag == "a" and self.depth <= 0:
                title = " ".join(self.current["title_parts"]).strip()
                if len(title) > 8:
                    self.items.append({
                        "title": title,
                        "url": self.current["url"],
                        "date": "",
                        "summary": "",
                        "image": self.current["image"],
                        "source": "TESLA Alliance"
                    })
                self.current = None
                self.depth = 0


def parse_blog_html(data):
    parser = BlogParser()
    parser.feed(data.decode("utf-8", errors="ignore"))
    unique = []
    seen = set()
    for item in parser.items:
        url = item["url"].split("?")[0]
        if url in seen:
            continue
        seen.add(url)
        item["url"] = url
        unique.append(item)
    return unique


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "dist/blog-data.json")
    items = []
    method = ""
    for url in RSS_URLS:
        try:
            candidate = parse_rss(fetch(url))
            if candidate:
                items = candidate
                method = "rss"
                break
        except Exception as exc:
            print(f"RSS unavailable: {url}: {exc}")
    if not items:
        try:
            items = parse_blog_html(fetch(BLOG_URL))
            method = "html"
        except Exception as exc:
            print(f"Blog page unavailable: {exc}")

    if not items:
        print("No live TESLA posts fetched; keeping existing fallback data.")
        return 0

    payload = {
        "source": "TESLA Alliance",
        "source_url": BLOG_URL,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "sync_method": method,
        "items": items[:24],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Synced {len(payload['items'])} TESLA blog posts via {method} -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
