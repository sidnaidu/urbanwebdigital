#!/usr/bin/env python3
"""
Download all external images used in the site into assets/img and keep the site fully local.

Usage:
  python3 download_images.py

Notes:
- Requires internet
- Installs: pip install requests
"""
import json, os, re, sys
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
try:
    import requests
except ImportError:
    print("Missing dependency: requests. Install with: pip install requests")
    sys.exit(1)

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(ROOT, "assets", "images.json")

def ensure_jpg(url: str) -> str:
    # Append fm=jpg and disable auto format to avoid AVIF/WEBP surprises on some CDNs
    parts = urlparse(url)
    q = dict(parse_qsl(parts.query, keep_blank_values=True))
    q["fm"] = "jpg"
    # If auto=format present, keep it (fine), but fm=jpg will force jpeg on Unsplash
    new_query = urlencode(q, doseq=True)
    return urlunparse((parts.scheme, parts.netloc, parts.path, parts.params, new_query, parts.fragment))

def download(url: str, out_path: str) -> bool:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    headers = {
        "User-Agent": "Mozilla/5.0 (UrbanWebDigital Image Fetcher)",
        "Accept": "image/jpeg,image/*;q=0.9,*/*;q=0.1",
    }
    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code != 200:
        return False
    ctype = (r.headers.get("content-type") or "").lower()
    # Save bytes regardless; extension is .jpg in our site.
    with open(out_path, "wb") as f:
        f.write(r.content)
    # Quick sanity check: tiny responses usually mean an error page
    if os.path.getsize(out_path) < 15_000:
        # Keep file but flag as failed
        return False
    return True

def main():
    with open(MANIFEST, "r", encoding="utf-8") as f:
        items = json.load(f)

    ok = 0
    fail = 0
    for it in items:
        local = it["filename"].replace("/", os.sep)
        out_path = os.path.join(ROOT, local)
        raw_url = it["url"]
        url = ensure_jpg(raw_url)
        print(f"- Downloading {os.path.basename(out_path)}")
        if download(url, out_path):
            ok += 1
        else:
            fail += 1
            print(f"  ! Failed: {raw_url}")

    print(f"\nDone. Success: {ok}, Failed: {fail}")
    if fail:
        print("If some images fail due to 403/429, re-run later or swap URLs in assets/images.json.")

if __name__ == "__main__":
    main()
