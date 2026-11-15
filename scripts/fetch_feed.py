#!/usr/bin/env python3
"""Pull NDA-relevant headlines from public news feeds into data/current_affairs.json.
Standard library only. Runs daily in GitHub Actions; safe to run locally."""
import json, re, sys, html, urllib.request, urllib.parse
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent.parent / "data" / "current_affairs.json"
KEEP_DAYS, MAX_ITEMS, PER_FEED = 45, 400, 25
GN = "https://news.google.com/rss/search?hl=en-IN&gl=IN&ceid=IN:en&q="
def gn(q): return GN + urllib.parse.quote_plus(q + " when:7d")

SOURCES = [
 ("Defence", gn("Indian Army OR Indian Navy OR Indian Air Force OR DRDO OR Ministry of Defence")),
 ("Defence", gn("site:pib.gov.in defence")),
 ("Science and space", gn("ISRO OR Gaganyaan OR DRDO missile test OR space mission India")),
 ("Awards and events", gn("India Padma OR Arjuna Award OR Khel Ratna OR Olympics India OR Asian Games India")),
 ("International", gn("India bilateral OR G20 OR BRICS OR Quad OR UN India summit")),
 ("Polity and economy", gn("Supreme Court India OR Union Cabinet approves OR RBI policy OR Parliament bill India")),
 ("Environment", gn("India national park OR wildlife sanctuary OR climate India OR Ramsar site")),
 ("Polity and economy", "https://www.thehindu.com/news/national/feeder/default.rss"),
]
UA = {"User-Agent": "Mozilla/5.0 (compatible; GarchaNDACoach/1.0)"}

def clean(t):
    t = html.unescape(re.sub(r"<[^>]+>", "", t or "")).strip()
    return re.sub(r"\s+", " ", t)

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()

def parse(xml_bytes, cat):
    root = ET.fromstring(xml_bytes)
    out = []
    for it in root.iter("item"):
        title = clean(it.findtext("title"))
        link = (it.findtext("link") or "").strip()
        src = clean(it.findtext("source")) if it.find("source") is not None else ""
        if " - " in title and not src:
            title, src = title.rsplit(" - ", 1)
        elif " - " in title and src and title.endswith(" - " + src):
            title = title[: -len(src) - 3]
        try:
            dt = parsedate_to_datetime(it.findtext("pubDate"))
            if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
        except Exception:
            dt = datetime.now(timezone.utc)
        if len(title) < 15 or not link.startswith("http"): continue
        out.append({"d": dt.astimezone(timezone.utc).strftime("%Y-%m-%d"), "c": cat, "h": title, "u": link, "s": src or "The Hindu"})
    return out[:PER_FEED]

def key(h): return re.sub(r"[^a-z0-9]", "", h.lower())[:80]

def main():
    old = []
    if OUT.exists():
        try: old = json.loads(OUT.read_text(encoding="utf-8")).get("items", [])
        except Exception: old = []
    fresh, ok = [], 0
    for cat, url in SOURCES:
        try:
            fresh += parse(fetch(url), cat); ok += 1
        except Exception as e:
            print(f"skip {cat}: {type(e).__name__} {e}", file=sys.stderr)
    if ok == 0:
        print("all sources failed; keeping existing data", file=sys.stderr); sys.exit(1)
    cutoff = (datetime.now(timezone.utc) - timedelta(days=KEEP_DAYS)).strftime("%Y-%m-%d")
    seen, merged = set(), []
    for it in sorted(fresh + old, key=lambda x: x["d"], reverse=True):
        k = key(it["h"])
        if k in seen or it["d"] < cutoff: continue
        seen.add(k); merged.append(it)
    merged = merged[:MAX_ITEMS]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), "items": merged}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(merged)} items from {ok}/{len(SOURCES)} sources")

if __name__ == "__main__": main()
