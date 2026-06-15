#!/usr/bin/env python3
"""
BuyZOXS x /e/OS Compatibility Crawler
=======================================
Fetches all devices from buyzoxs.de (via sitemap) and cross-references them
with the known /e/OS supported devices list. Fetches live prices and conditions
via internal APIs using cloudscraper to bypass Cloudflare protection.

Includes SQLite tracking to report price drops, new conditions, and stock changes.

Usage:
    py eos_buyzoxs_crawler.py                    # full run, print report
    py eos_buyzoxs_crawler.py --json             # also dump results to eos_results.json
    py eos_buyzoxs_crawler.py --ods              # also create eos_results.ods spreadsheet
    py eos_buyzoxs_crawler.py --ods --json       # both exports
    py eos_buyzoxs_crawler.py --min-score 70     # adjust fuzzy-match threshold (default 80)

Dependencies:
    pip install cloudscraper requests beautifulsoup4 thefuzz odfpy
"""

import argparse
import json
import re
import sqlite3
import time
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional, List, Dict

import requests
import cloudscraper
from bs4 import BeautifulSoup
from thefuzz import fuzz

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SITEMAP_URL = "https://www.buyzoxs.de/sitemap.xml"
DB_PATH = "eos_buyzoxs.db"

# Initialize cloudscraper to bypass Cloudflare 403 Forbidden errors
scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
}
REQUEST_TIMEOUT = 15

# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class EosDevice:
    brand: str
    model: str
    codename: str
    status: str          # "official" | "community" | "test"
    keywords: list[str] = field(default_factory=list)
    android_versions: str = ""

    def search_text(self) -> str:
        return f"{self.brand} {self.model}".lower()

@dataclass
class Variant:
    zustand: str
    price: str

@dataclass
class MatchResult:
    slug: str
    display_name: str
    eos_device: EosDevice
    brand: str
    variants: List[Variant] = field(default_factory=list)

# ---------------------------------------------------------------------------
# /e/OS known supported devices
# ---------------------------------------------------------------------------

EOS_DEVICES: list[EosDevice] = [
    # ---- BQ ----
    EosDevice("BQ", "Aquaris X",     "bardock",    "community", ["bq-aquaris-x"]),
    EosDevice("BQ", "Aquaris X Pro", "bardockpro", "community", ["bq-aquaris-x-pro"]),

    # ---- Fairphone ----
    EosDevice("Fairphone", "Fairphone 3",  "FP3",  "official",  ["fairphone/fairphone-3"]),
    EosDevice("Fairphone", "Fairphone 4",  "FP4",  "official",  ["fairphone/fairphone-4"]),
    EosDevice("Fairphone", "Fairphone 5",  "FP5",  "official",  ["fairphone/fairphone-5"]),

    # ---- Gigaset ----
    EosDevice("Gigaset", "GS290", "GS290", "official", ["gigaset/gigaset-gs290"]),
    EosDevice("Gigaset", "GS6 / GS6 PRO", "GS6_Venus", "official", ["gigaset/gigaset-gs6"]),

    # ---- Google Pixel ----
    EosDevice("Google", "Pixel 4a 5G",    "bramble",  "community", ["google-pixel-4a-5g"]),
    EosDevice("Google", "Pixel 6a",       "bluejay",  "community", ["google-pixel-6a"]),
    EosDevice("Google", "Pixel 7a",       "lynx",     "community", ["google-pixel-7a"]),
    EosDevice("Google", "Pixel 6",        "oriole",   "official",  ["google/pixel-6"]),
    EosDevice("Google", "Pixel 6 Pro",    "raven",    "official",  ["google/pixel-6-pro"]),
    EosDevice("Google", "Pixel 7",        "panther",  "official",  ["google/pixel-7"]),
    EosDevice("Google", "Pixel 7 Pro",    "cheetah",  "official",  ["google/pixel-7-pro"]),
    EosDevice("Google", "Pixel 8",        "shiba",    "official",  ["google/pixel-8"]),
    EosDevice("Google", "Pixel 8 Pro",    "husky",    "official",  ["google/pixel-8-pro"]),
    EosDevice("Google", "Pixel 9",        "tokay",    "official",  ["google/pixel-9"]),
    EosDevice("Google", "Pixel 9 Pro",    "caiman",   "official",  ["google/pixel-9-pro"]),
    EosDevice("Google", "Pixel 9 Pro XL", "komodo",   "official",  ["google/pixel-9-pro-xl"]),
    EosDevice("Google", "Pixel 9 Pro Fold","comet",   "official",  ["google/pixel-9-pro-fold"]),

    # ---- Samsung Galaxy S ----
    EosDevice("Samsung", "Galaxy S7",     "herolte",    "community", ["samsung-galaxy-s7"]),
    EosDevice("Samsung", "Galaxy S7 Edge","hero2lte",   "community", ["samsung-galaxy-s7-edge"]),
    EosDevice("Samsung", "Galaxy S8",     "dreamlte",   "community", ["samsung-galaxy-s8"]),
    EosDevice("Samsung", "Galaxy S8+",    "dream2lte",  "community", ["samsung-galaxy-s8-plus"]),
    EosDevice("Samsung", "Galaxy S9",     "starlte",    "official",  ["samsung-galaxy-s9"]),
    EosDevice("Samsung", "Galaxy S9+",    "star2lte",   "official",  ["samsung-galaxy-s9-plus"]),
    EosDevice("Samsung", "Galaxy S10e",   "beyond0lte", "community", ["samsung-galaxy-s10e"]),
    EosDevice("Samsung", "Galaxy S10",    "beyond1lte", "community", ["samsung-galaxy-s10"]),
    EosDevice("Samsung", "Galaxy S10+",   "beyond2lte", "community", ["samsung-galaxy-s10-plus"]),
    EosDevice("Samsung", "Galaxy S10 Lite","beyondxq",  "community", ["samsung-galaxy-s10-lite"]),
    EosDevice("Samsung", "Galaxy S20 FE", "r8q",        "community", ["samsung-galaxy-s20-fe"]),
    EosDevice("Samsung", "Galaxy S20+",   "y2s",        "community", ["samsung-galaxy-s20-plus"]),
    EosDevice("Samsung", "Galaxy S20 Ultra","z3q",      "community", ["samsung-galaxy-s20-ultra"]),
    
    # ---- Samsung Galaxy A ----
    EosDevice("Samsung", "Galaxy A21s",   "a21s",       "community", ["samsung-galaxy-a21"]),
    EosDevice("Samsung", "Galaxy A52s 5G","a52sxq",     "community", ["samsung-galaxy-a52"]),
    EosDevice("Samsung", "Galaxy A53 5G", "a53x",       "community", ["samsung-galaxy-a53"]),
    
    # ---- Samsung Galaxy Note ----
    EosDevice("Samsung", "Galaxy Note 9", "crownlte",   "community", ["samsung-galaxy-note-9"]),
    EosDevice("Samsung", "Galaxy Note 10","d1",         "community", ["samsung-galaxy-note-10"]),
    EosDevice("Samsung", "Galaxy Note 20","c1s",        "community", ["samsung-galaxy-note-20"]),

    # ---- OnePlus ----
    EosDevice("OnePlus", "OnePlus Nord", "avicii",       "official",  ["oneplus-nord"]),
    EosDevice("OnePlus", "OnePlus 3",  "oneplus3",       "community", ["oneplus-3"]),
    EosDevice("OnePlus", "OnePlus 5",  "cheeseburger",   "community", ["oneplus-5"]),
    EosDevice("OnePlus", "OnePlus 6",  "enchilada",      "community", ["oneplus-6"]),
    EosDevice("OnePlus", "OnePlus 7",  "guacamoleb",     "community", ["oneplus-7"]),
    EosDevice("OnePlus", "OnePlus 8",  "instantnoodle",  "official",  ["oneplus-8"]),
    EosDevice("OnePlus", "OnePlus 9",  "lemonade",       "official",  ["oneplus-9"]),

    # ---- Sony Xperia ----
    EosDevice("Sony", "Xperia 1 III / IV", "pdx215", "community", ["sony-xperia-1"]),
    EosDevice("Sony", "Xperia 5 III / V",  "pdx214", "community", ["sony-xperia-5"]),
    EosDevice("Sony", "Xperia 10 IV / V",  "pdx225", "official",  ["sony-xperia-10"]),

    # ---- Xiaomi / Redmi / POCO ----
    EosDevice("Xiaomi", "Mi A1",        "tissot",         "official",  ["mi-a1"]),
    EosDevice("Xiaomi", "Mi A2",        "jasmine_sprout", "official",  ["mi-a2"]),
    EosDevice("Xiaomi", "Mi A3",        "laurel_sprout",  "official",  ["mi-a3"]),
    EosDevice("Xiaomi", "Mi 8",         "dipper",         "community", ["mi-8"]),
    EosDevice("Xiaomi", "Mi 9",         "cepheus",        "community", ["mi-9"]),
    EosDevice("Xiaomi", "Mi 10",        "umi",            "community", ["mi-10"]),
    EosDevice("Xiaomi", "Mi 11",        "venus",          "community", ["mi-11", "xiaomi-11"]),
    EosDevice("Xiaomi", "Xiaomi 12",    "cupid",          "community", ["xiaomi-12"]),
    EosDevice("Xiaomi", "POCO F5",      "marble",         "community", ["xiaomi-poco-f5", "poco-f5"]),
    EosDevice("Xiaomi", "POCO X3 Pro",    "vayu",           "community", ["xiaomi-poco-x3-pro"]),
    EosDevice("Xiaomi", "Redmi Note 9S",  "miatoll",        "community", ["redmi-note-9"]),
    EosDevice("Xiaomi", "Redmi Note 10 Pro","sweet",         "community", ["redmi-note-10"]),
    EosDevice("Xiaomi", "Redmi Note 11",  "spes",           "community", ["redmi-note-11"]),
    EosDevice("Xiaomi", "Redmi Note 12",  "tapas",          "community", ["redmi-note-12"]),

    # ---- Motorola ----
    EosDevice("Motorola", "Edge 20",       "berlna",  "community", ["edge-20"]),
    EosDevice("Motorola", "Edge 30 Fusion","tundra",  "community", ["edge-30"]),
    EosDevice("Motorola", "Edge 30 Ultra", "eqs",     "community", ["edge-30-ultra"]),
    EosDevice("Motorola", "Edge 30 Neo",   "miami",   "community", ["edge-30-neo"]),
    EosDevice("Motorola", "Edge 40 Pro",   "rtwo",    "community", ["edge-40"]),
]

# ---------------------------------------------------------------------------
# Database Functions
# ---------------------------------------------------------------------------

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS device_variants (
            brand TEXT,
            model TEXT,
            codename TEXT,
            status TEXT,
            android_versions TEXT,
            zustand TEXT,
            price TEXT,
            url TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (brand, model, zustand)
        )
    """)
    conn.commit()
    conn.close()

def load_previous_state() -> Dict[tuple, Dict[str, str]]:
    """Loads the previous state as {(brand, model): {zustand: price}}"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT brand, model, zustand, price FROM device_variants")
    rows = cursor.fetchall()
    conn.close()
    
    state = defaultdict(dict)
    for brand, model, zustand, price in rows:
        state[(brand, model)][zustand] = price
    return dict(state)

def save_to_db(results: list[MatchResult]):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for r in results:
        # Delete old variants for this specific model to cleanly handle disappeared ones
        cursor.execute("DELETE FROM device_variants WHERE brand=? AND model=?", (r.brand, r.eos_device.model))
        for v in r.variants:
            url = f"https://www.buyzoxs.de/kaufen/{r.slug}.html"
            cursor.execute("""
                INSERT INTO device_variants 
                (brand, model, codename, status, android_versions, zustand, price, url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (r.brand, r.eos_device.model, r.eos_device.codename, r.eos_device.status, 
                  r.eos_device.android_versions, v.zustand, v.price, url))
    conn.commit()
    conn.close()

# ---------------------------------------------------------------------------
# Step 1 – Fetch buyzoxs.de device list from sitemap
# ---------------------------------------------------------------------------

def fetch_sitemap_urls(url: str) -> list[str]:
    resp = scraper.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    
    ns_uri = "http://www.sitemaps.org/schemas/sitemap/0.9"
    
    if root.tag == f"{{{ns_uri}}}sitemapindex":
        urls = []
        for loc_el in root.iter(f"{{{ns_uri}}}loc"):
            child_url = loc_el.text
            if child_url:
                try:
                    urls.extend(fetch_sitemap_urls(child_url.strip()))
                except Exception as e:
                    print(f"\n   Warning: Failed to fetch child sitemap {child_url}: {e}")
        return urls
    else:
        return [loc_el.text.strip() for loc_el in root.iter(f"{{{ns_uri}}}loc") if loc_el.text]

def slug_to_display_name(slug: str) -> str:
    return slug.replace("-", " ").title()

def fetch_buyzoxs_devices() -> list[tuple[str, str]]:
    print("[*] Fetching buyzoxs.de sitemap...", end=" ", flush=True)
    try:
        urls = fetch_sitemap_urls(SITEMAP_URL)
        print("done.")
    except Exception as e:
        print(f"failed ({type(e).__name__}). Falling back to known /e/OS devices list.")
        return []

    NON_PHONE_TERMS = ("watch", "tab-s", "galaxy-tab", "buds", "gear", "pixel-tablet")

    devices: list[tuple[str, str]] = []
    for loc in urls:
        if "/kaufen/" not in loc:
            continue
        slug = loc.split("/kaufen/")[-1].replace(".html", "").strip("/")
        if any(t in slug for t in NON_PHONE_TERMS):
            continue
        if len(slug) < 5:
            continue
        display = slug_to_display_name(slug)
        devices.append((slug, display))

    print(f"   Found {len(devices)} device pages in sitemap.")
    return devices

# ---------------------------------------------------------------------------
# Step 2 – Match a buyzoxs slug against /e/OS devices
# ---------------------------------------------------------------------------

_SLUG_INDEX: dict[str, EosDevice] = {}

def _build_index() -> None:
    for dev in EOS_DEVICES:
        for kw in dev.keywords:
            _SLUG_INDEX[kw] = dev

_build_index()

_SORTED_KEYWORDS: list[tuple[str, EosDevice]] = sorted(
    ((kw, dev) for dev in EOS_DEVICES for kw in dev.keywords),
    key=lambda x: len(x[0]),
    reverse=True,
)

def _extract_asin(slug: str) -> Optional[str]:
    m = re.search(r"_([A-Z0-9]{10})$", slug)
    return m.group(1) if m else None

def match_eos_device(slug: str) -> Optional[EosDevice]:
    slug_lower = slug.lower()
    if slug_lower in _SLUG_INDEX:
        return _SLUG_INDEX[slug_lower]

    if "/" in slug_lower:
        filename = slug_lower.rsplit("/", 1)[-1]
        for kw, dev in _SORTED_KEYWORDS:
            if filename.startswith(kw) and (
                len(filename) == len(kw) or filename[len(kw)] in ("-", "_")
            ):
                return dev
    return None

# ---------------------------------------------------------------------------
# Step 3 – Run the full cross-reference
# ---------------------------------------------------------------------------

def search_buyzoxs_for_device(dev: EosDevice, threshold: int = 80) -> Optional[MatchResult]:
    query = f"{dev.brand} {dev.model}"
    api_headers = {**HEADERS, "Content-Type": "application/json", "Accept": "application/json", "Referer": "https://www.buyzoxs.de/"}
    _DISCRIMINATORS = frozenset({"tab", "tablet", "lite", "pro", "mini", "ultra", "plus", "fe", "max", "neo", "fusion", "wifi"})

    try:
        resp = scraper.post(
            f"https://www.buyzoxs.de/sys_filter.php?q={requests.utils.quote(query)}",
            headers=api_headers, json={}, timeout=REQUEST_TIMEOUT,
        )
        if resp.status_code != 200: return None
        products = resp.json().get("products", [])
        if not products: return None

        target = query.lower()
        best_product = max(products, key=lambda p: fuzz.token_set_ratio(p.get("title", "").lower(), target))
        best_score = fuzz.token_set_ratio(best_product.get("title", "").lower(), target)
        
        if best_score < threshold: return None

        query_words = set(re.findall(r'\w+', target))
        result_words = set(re.findall(r'\w+', best_product.get("title", "").lower()))
        if (result_words - query_words) & _DISCRIMINATORS: return None

        link = best_product.get("link", "")
        slug = link.replace("https://www.buyzoxs.de/kaufen/", "").replace(".html", "")
        return MatchResult(slug=slug, display_name=best_product.get("title", dev.model), eos_device=dev, brand=dev.brand)
    except Exception:
        return None

def run_crawler(threshold: int = 80) -> list[MatchResult]:
    buyzoxs_devices = fetch_buyzoxs_devices()
    results: list[MatchResult] = []

    if not buyzoxs_devices:
        print("[*] Sitemap unavailable. Using known /e/OS device slugs to fetch prices...")
        for dev in EOS_DEVICES:
            slug = dev.keywords[0] if dev.keywords else dev.model.lower().replace(" ", "-")
            display = f"{dev.brand} {dev.model}"
            results.append(MatchResult(slug=slug, display_name=display, eos_device=dev, brand=dev.brand))
    else:
        print(f"[*] Matching {len(buyzoxs_devices)} pages against {len(EOS_DEVICES)} /e/OS devices...")
        for slug, display in buyzoxs_devices:
            eos = match_eos_device(slug)
            if eos:
                results.append(MatchResult(slug=slug, display_name=display, eos_device=eos, brand=eos.brand))

    by_key: dict[tuple[str, str], MatchResult] = {}
    by_key_score: dict[tuple[str, str], int] = defaultdict(int)

    for r in results:
        key = (r.brand, r.eos_device.model)
        score = fuzz.token_set_ratio(r.display_name.lower(), r.eos_device.search_text())
        if score >= threshold and score > by_key_score[key]:
            by_key_score[key] = score
            by_key[key] = r

    matched = set((r.brand, r.eos_device.model) for r in by_key.values())
    unmatched = [dev for dev in EOS_DEVICES if (dev.brand, dev.model) not in matched]
    
    if unmatched and buyzoxs_devices:
        print(f"[*] Searching buyzoxs.de for {len(unmatched)} device(s) not in sitemap...")
        for dev in unmatched:
            r = search_buyzoxs_for_device(dev, threshold=threshold)
            if r:
                print(f"   Found: {dev.model} -> {r.slug}")
                by_key[(dev.brand, dev.model)] = r
            time.sleep(0.3)

    return list(by_key.values())

STATUS_ICON = {"official": "[official]", "community": "[community]", "test": "[test]"}

def print_report(results: list[MatchResult]) -> None:
    by_brand: dict[str, list[MatchResult]] = defaultdict(list)
    for r in results: by_brand[r.brand].append(r)

    total = sum(len(v) for v in by_brand.values())
    print("\n" + "=" * 60)
    print(f"  buyzoxs.de x /e/OS Compatibility Report")
    print(f"  {total} compatible device model(s) found")
    print("=" * 60)

    for brand in sorted(by_brand.keys()):
        entries = sorted(by_brand[brand], key=lambda r: r.eos_device.model)
        print(f"\n  {brand} ({len(entries)} model(s))")
        for r in entries:
            icon = STATUS_ICON.get(r.eos_device.status, "[?]")
            if r.variants:
                best_v = r.variants[0]
                extra_count = len(r.variants) - 1
                extra_text = f" (+{extra_count} more)" if extra_count > 0 else ""
                print(f"     {icon:<12} {r.eos_device.model:<30} [{r.eos_device.codename}] -> {best_v.zustand} @ {best_v.price}{extra_text}")
            else:
                print(f"     {icon:<12} {r.eos_device.model:<30} [{r.eos_device.codename}] -> No stock/price data")
    print("=" * 60)

# ---------------------------------------------------------------------------
# /e/OS version fetcher
# ---------------------------------------------------------------------------

EOS_DOC_BASE = "https://doc.e.foundation/devices"
_version_cache: dict[str, str] = {}

def fetch_eos_version(codename: str) -> str:
    if codename in _version_cache: return _version_cache[codename]
    url = f"{EOS_DOC_BASE}/{codename}"
    try:
        resp = scraper.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200: return ""
        soup = BeautifulSoup(resp.text, "html.parser")
        for dt in soup.find_all("dt"):
            if "build versions" in dt.get_text(strip=True).lower():
                dd = dt.find_next_sibling("dd")
                if dd:
                    text = dd.get_text(separator=", ", strip=True)
                    _version_cache[codename] = text
                    return text
    except Exception: pass
    return ""

def enrich_with_versions(results: list[MatchResult], delay: float = 0.4) -> None:
    seen_codenames: set[str] = set()
    total = len({r.eos_device.codename for r in results})
    done = 0
    for r in results:
        codename = r.eos_device.codename
        if codename in seen_codenames: continue
        seen_codenames.add(codename)
        done += 1
        print(f"   [{done}/{total}] Fetching /e/OS version for {r.eos_device.model} ({codename})...", end=" ", flush=True)
        version = fetch_eos_version(codename)
        r.eos_device.android_versions = version
        print(version or "(not found)")
        time.sleep(delay)

# ---------------------------------------------------------------------------
# buyzoxs.de price & condition fetcher
# ---------------------------------------------------------------------------

EXCLUDED_CONDITIONS = {"Fair", "Chance", "Steel", "Stealth"}
_CONDITION_RANK: dict[str, int] = {
    "Neu": 1, "Wie Neu": 2, "Sehr Gut": 3, "Gut": 4, "OK": 5, "Akzeptabel": 5,
    "Fair": 10, "Chance": 11, "Steel": 12, "Stealth": 13,
}

def fetch_category_id(slug: str) -> Optional[str]:
    url = f"https://www.buyzoxs.de/kaufen/{slug}.html"
    try:
        resp = scraper.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200: return None
        soup = BeautifulSoup(resp.text, "html.parser")
        div = soup.find("div", id="vue-filter")
        if div: return div.get("data-category-id")
    except Exception: pass
    return None

def fetch_article_by_asin(asin: str) -> list[dict]:
    api_headers = {**HEADERS, "Accept": "application/json", "Referer": "https://www.buyzoxs.de/"}
    url = f"https://www.buyzoxs.de/api/article/{asin}"
    try:
        resp = scraper.get(url, headers=api_headers, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200: return []
        data = resp.json()
        skus = data.get("result", {}).get("skus", [])
        if not skus: return []
        variants = [{"variant_name": s.get("zustand_text", "").title() or str(s.get("zustand", "")),
                     "es_price": int(float(s.get("preis", 0) or 0) * 100),
                     "quantity": int(float(s.get("anz", 0) or 0)),
                     "lastInStock": s.get("lastInStock", False)} for s in skus]
        return [{"title": data.get("result", {}).get("article", {}).get("title", ""), "variants": variants}]
    except Exception: return []

def fetch_product_data(category_id: str) -> list[dict]:
    api_headers = {**HEADERS, "Content-Type": "application/json", "Accept": "application/json", "Referer": "https://www.buyzoxs.de/"}
    url = f"https://www.buyzoxs.de/sys_filter.php?page=0&category_id={category_id}"
    try:
        resp = scraper.post(url, headers=api_headers, json={}, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200: return []
        products = resp.json().get("products", [])
        for p in products:
            for v in p.get("variants", []):
                price = v.get("es_price", 0)
                try:
                    price_val = float(price)
                    if isinstance(price, float) or (isinstance(price, str) and '.' in str(price)): 
                        v["es_price"] = int(price_val * 100)
                    else: 
                        v["es_price"] = int(price_val)
                except Exception: 
                    v["es_price"] = 0
        return products
    except Exception: return []

def parse_price_to_float(price_str: str) -> float:
    try:
        return float(price_str.replace(" EUR", "").replace(",", "."))
    except ValueError:
        return 0.0

def enrich_with_prices_and_conditions(results: list[MatchResult], previous_state: Dict[tuple, Dict[str, str]], delay: float = 0.5) -> list[MatchResult]:
    total = len(results)
    kept: list[MatchResult] = []

    for idx, r in enumerate(results, 1):
        print(f"   [{idx}/{total}] {r.eos_device.model} ({r.slug})...", end=" ", flush=True)
        
        asin = _extract_asin(r.slug)
        if asin: 
            products = fetch_article_by_asin(asin)
        else:
            cat_id = fetch_category_id(r.slug)
            if not cat_id:
                print("(category ID not found)")
                r.variants = [Variant(zustand="Unknown", price="See website")]
                kept.append(r)
                time.sleep(delay)
                continue
            products = fetch_product_data(cat_id)
            
        if not products:
            print("(no product data)")
            r.variants = [Variant(zustand="Unknown", price="See website")]
            kept.append(r)
            time.sleep(delay)
            continue

        all_variants: list[dict] = []
        for product in products:
            for v in product.get("variants", []):
                if v.get("quantity", 0) > 0 or v.get("lastInStock", False):
                    all_variants.append(v)

        if not all_variants:
            print("(no variants in stock)")
            r.variants = [Variant(zustand="Unknown", price="See website")]
            kept.append(r)
            time.sleep(delay)
            continue

        acceptable = [v for v in all_variants if v.get("variant_name", "") not in EXCLUDED_CONDITIONS]
        if not acceptable:
            names = {v.get('variant_name', '?') for v in all_variants}
            print(f"(only {names} – excluded)")
            time.sleep(delay)
            continue

        # Sort acceptable variants by condition rank (best first), then by price (lowest first)
        acceptable.sort(key=lambda v: (_CONDITION_RANK.get(v.get("variant_name", ""), 6), v.get("es_price", 999999)))
        
        # FIXED: Deduplicate variants by keeping ONLY the best (lowest) price for each condition.
        # This guarantees exactly one row per condition per device, satisfying the DB UNIQUE constraint.
        seen_zustand = set()
        unique_variants = []
        for v in acceptable:
            zustand = v.get("variant_name", "Unknown")
            if zustand not in seen_zustand:
                seen_zustand.add(zustand)
                price_eur = v.get("es_price", 0) / 100.0
                price_str = f"{price_eur:.2f}".replace(".", ",") + " EUR"
                unique_variants.append(Variant(zustand=zustand, price=price_str))

        r.variants = unique_variants
        
        # --- CHANGE DETECTION & REPORTING ---
        key = (r.brand, r.eos_device.model)
        old_variants = previous_state.get(key, {})
        
        changes = []
        if not old_variants:
            changes.append("🆕 NEW DEVICE")
        else:
            for v in r.variants:
                if v.zustand not in old_variants:
                    changes.append(f"➕ NEW: {v.zustand} @ {v.price}")
                else:
                    old_price = old_variants[v.zustand]
                    if old_price != v.price:
                        old_val = parse_price_to_float(old_price)
                        new_val = parse_price_to_float(v.price)
                        if new_val < old_val and old_val > 0:
                            changes.append(f"📉 PRICE DROP: {v.zustand} {old_price} -> {v.price}")
                        elif new_val > old_val:
                            changes.append(f"📈 PRICE INCREASE: {v.zustand} {old_price} -> {v.price}")
                        else:
                            changes.append(f"🔄 PRICE CHANGED: {v.zustand} {old_price} -> {v.price}")
            
            for old_zustand, old_price in old_variants.items():
                if old_zustand not in [v.zustand for v in r.variants]:
                    changes.append(f"❌ DISAPPEARED: {old_zustand} (was {old_price})")
        
        # Print changes
        if changes:
            print()
            for change in changes:
                print(f"      {change}")
        else:
            best_v = r.variants[0]
            print(f"{best_v.zustand} @ {best_v.price} ({len(r.variants)} options, no changes)")
            
        kept.append(r)
        time.sleep(delay)

    return kept

# ---------------------------------------------------------------------------
# ODS Export
# ---------------------------------------------------------------------------

def save_ods(results: list[MatchResult], filename: str = "eos_results.ods") -> None:
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.style import Style, TextProperties, TableColumnProperties, TableCellProperties
    from odf.table import Table, TableColumn, TableRow, TableCell, TableHeaderRows, DatabaseRange, DatabaseRanges
    from odf.text import P
    from odf import text as odftext

    doc = OpenDocumentSpreadsheet()

    def _make_style(name: str, bold: bool = False, bg: str = "", wrap: bool = False) -> Style:
        style = Style(name=name, family="table-cell")
        tp_attrs = {}
        if bold: tp_attrs["fontweight"] = "bold"
        if tp_attrs: style.addElement(TextProperties(**tp_attrs))
        tcp_attrs = {}
        if bg: tcp_attrs["backgroundcolor"] = bg
        if wrap: tcp_attrs["wrapoption"] = "wrap"
        if tcp_attrs: style.addElement(TableCellProperties(**tcp_attrs))
        doc.automaticstyles.addElement(style)
        return style

    header_style = _make_style("HeaderCell", bold=True, bg="#1c4587")
    url_style    = _make_style("UrlCell", wrap=True)
    normal_style = _make_style("NormalCell")
    alt_style    = _make_style("AltCell", bg="#e8f0fe")

    header_text_style = Style(name="HeaderText", family="text")
    header_text_style.addElement(TextProperties(color="#ffffff", fontweight="bold"))
    doc.automaticstyles.addElement(header_text_style)

    # 8 columns: Brand, Device, Codename, /e/OS Android Version, Build Type, Zustand, Price (EUR), buyzoxs.de URL
    col_widths = ["3cm", "6cm", "4cm", "5cm", "3cm", "4cm", "4cm", "10cm"]
    col_style_names = []
    for i, w in enumerate(col_widths):
        cs = Style(name=f"Col{i}", family="table-column")
        cs.addElement(TableColumnProperties(columnwidth=w))
        doc.automaticstyles.addElement(cs)
        col_style_names.append(f"Col{i}")

    table = Table(name="eos-buyzoxs")
    for i, cs_name in enumerate(col_style_names): 
        table.addElement(TableColumn(stylename=cs_name))

    headers = ["Brand", "Device", "Codename", "/e/OS Android Version", "Build Type", "Zustand", "Price (EUR)", "buyzoxs.de URL"]
    header_row = TableRow()
    for h in headers:
        cell = TableCell(stylename=header_style, valuetype="string")
        p = P()
        span = odftext.Span(stylename=header_text_style)
        span.addText(h)
        p.addElement(span)
        cell.addElement(p)
        header_row.addElement(cell)

    header_rows_block = TableHeaderRows()
    header_rows_block.addElement(header_row)
    table.addElement(header_rows_block)

    sorted_results = sorted(results, key=lambda r: (r.brand, r.eos_device.model))
    total_rows_count = 1 # Start with header
    
    for r in sorted_results:
        url = f"https://www.buyzoxs.de/kaufen/{r.slug}.html"
        variants_to_export = r.variants if r.variants else [Variant(zustand="Unknown", price="See website")]
        
        for v in variants_to_export:
            row_style = alt_style if total_rows_count % 2 == 0 else normal_style
            
            row_data = [
                r.brand, 
                r.eos_device.model, 
                r.eos_device.codename, 
                r.eos_device.android_versions or "See doc.e.foundation", 
                r.eos_device.status, 
                v.zustand, 
                v.price, 
                url
            ]

            data_row = TableRow()
            for col_idx, value in enumerate(row_data):
                cell_style = url_style if col_idx == 7 else row_style
                
                # Price is index 6
                if col_idx == 6 and value not in ("See website", ""):
                    try:
                        float_val = float(value.replace(" EUR", "").replace(",", "."))
                        cell = TableCell(stylename=cell_style, valuetype="float", value=str(float_val))
                        cell.addElement(P(text=f"{float_val:.2f}"))
                    except ValueError:
                        cell = TableCell(stylename=cell_style, valuetype="string")
                        cell.addElement(P(text=value))
                else:
                    cell = TableCell(stylename=cell_style, valuetype="string")
                    cell.addElement(P(text=value))
                data_row.addElement(cell)
            table.addElement(data_row)
            total_rows_count += 1

    doc.spreadsheet.addElement(table)

    col_letter = chr(ord("A") + len(headers) - 1) # 'H'
    db_ranges = DatabaseRanges()
    db_range = DatabaseRange(name="__AutoFilter__", targetrangeaddress=f"eos-buyzoxs.A1:{col_letter}{total_rows_count}", displayfilterbuttons="true")
    db_ranges.addElement(db_range)
    doc.spreadsheet.addElement(db_ranges)

    doc.save(filename)
    print(f"\n  Spreadsheet saved to {filename}  ({total_rows_count - 1} data rows)")

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="BuyZOXS x /e/OS Compatibility Crawler")
    parser.add_argument("--min-score", type=int, default=80, help="Minimum fuzzy-match score")
    parser.add_argument("--json", action="store_true", help="Also save results to eos_results.json")
    parser.add_argument("--ods", action="store_true", help="Also create eos_results.ods spreadsheet")
    args = parser.parse_args()

    # Initialize database and load previous state
    init_db()
    previous_state = load_previous_state()

    results = run_crawler(threshold=args.min_score)
    print_report(results)

    if args.ods or args.json:
        print("\n[*] Fetching /e/OS Android versions from doc.e.foundation...")
        enrich_with_versions(results)
        print("\n[*] Fetching prices and conditions from buyzoxs.de...")
        results = enrich_with_prices_and_conditions(results, previous_state)
        print(f"\n  {len(results)} device(s) remain after condition filtering.")
        
        # Save the new state to the database
        print("\n[*] Saving updated state to SQLite database...")
        save_to_db(results)
        print("  Database updated successfully.")

    if args.json:
        output = [
            {
                "buyzoxs_slug": r.slug,
                "buyzoxs_url": f"https://www.buyzoxs.de/kaufen/{r.slug}.html",
                "brand": r.brand,
                "eos_model": r.eos_device.model,
                "eos_codename": r.eos_device.codename,
                "eos_status": r.eos_device.status,
                "eos_android_versions": r.eos_device.android_versions,
                "variants": [
                    {"zustand": v.zustand, "price": v.price}
                    for v in (r.variants if r.variants else [Variant(zustand="Unknown", price="See website")])
                ]
            }
            for r in results
        ]
        with open("eos_results.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\n  Results saved to eos_results.json")

    if args.ods:
        save_ods(results, "eos_results.ods")

if __name__ == "__main__":
    main()