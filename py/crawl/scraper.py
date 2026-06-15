import re
import xml.etree.ElementTree as ET
from typing import Optional, List, Dict

import requests
import cloudscraper
from bs4 import BeautifulSoup
from thefuzz import fuzz

from models import HEADERS, REQUEST_TIMEOUT, SITEMAP_URL, EosDevice, MatchResult

scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})

# ---------------------------------------------------------------------------
# Helper: Safe Price Normalization
# ---------------------------------------------------------------------------

def _normalize_price_to_cents(price_val) -> int:
    """
    Safely converts a price to cents (int).
    The buyzoxs.de APIs are inconsistent: sometimes they return prices in Euros 
    (e.g., 362) and sometimes in cents (e.g., 36200).
    
    We use a heuristic threshold:
    - If the raw value is > 5000, it's almost certainly in cents.
    - If the raw value is <= 5000, it's almost certainly in Euros.
    (Smartphones typically cost between 100€ and 2000€. 5000 cents is 50€, which is 
    too cheap for a phone, and 5000€ is too expensive. So the threshold is safe.)
    """
    try:
        if isinstance(price_val, str):
            # Handle potential German formatting like "1.234,56" or "362,00"
            price_val = price_val.replace(".", "").replace(",", ".")
        
        val = float(price_val)
        
        if val > 5000:
            # Assume it's already in cents
            return int(val)
        else:
            # Assume it's in Euros, convert to cents
            return int(val * 100)
    except (ValueError, TypeError):
        return 0

# ---------------------------------------------------------------------------
# Scraping Functions
# ---------------------------------------------------------------------------

def fetch_sitemap_urls(url: str) -> List[str]:
    resp = scraper.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns_uri = "http://www.sitemaps.org/schemas/sitemap/0.9"
    
    if root.tag == f"{{{ns_uri}}}sitemapindex":
        urls = []
        for loc_el in root.iter(f"{{{ns_uri}}}loc"):
            if loc_el.text:
                try:
                    urls.extend(fetch_sitemap_urls(loc_el.text.strip()))
                except Exception as e:
                    print(f"\n   Warning: Failed to fetch child sitemap {loc_el.text}: {e}")
        return urls
    return [loc_el.text.strip() for loc_el in root.iter(f"{{{ns_uri}}}loc") if loc_el.text]

def fetch_buyzoxs_devices() -> List[tuple[str, str]]:
    try:
        urls = fetch_sitemap_urls(SITEMAP_URL)
    except Exception as e:
        print(f"failed ({type(e).__name__}). Falling back to known /e/OS devices list.")
        return []

    NON_PHONE_TERMS = ("watch", "tab-s", "galaxy-tab", "buds", "gear", "pixel-tablet")
    devices = []
    for loc in urls:
        if "/kaufen/" not in loc:
            continue
        slug = loc.split("/kaufen/")[-1].replace(".html", "").strip("/")
        if any(t in slug for t in NON_PHONE_TERMS) or len(slug) < 5:
            continue
        display = slug.replace("-", " ").title()
        devices.append((slug, display))
    return devices

def search_buyzoxs_for_device(dev: EosDevice, threshold: int = 80) -> Optional[MatchResult]:
    query = f"{dev.brand} {dev.model}"
    api_headers = {**HEADERS, "Content-Type": "application/json", "Accept": "application/json", "Referer": "https://www.buyzoxs.de/"}
    _DISCRIMINATORS = frozenset({"tab", "tablet", "lite", "pro", "mini", "ultra", "plus", "fe", "max", "neo", "fusion", "wifi"})

    try:
        resp = scraper.post(f"https://www.buyzoxs.de/sys_filter.php?q={requests.utils.quote(query)}", headers=api_headers, json={}, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200: return None
        products = resp.json().get("products", [])
        if not products: return None

        target = query.lower()
        best_product = max(products, key=lambda p: fuzz.token_set_ratio(p.get("title", "").lower(), target))
        if fuzz.token_set_ratio(best_product.get("title", "").lower(), target) < threshold:
            return None

        query_words = set(re.findall(r'\w+', target))
        result_words = set(re.findall(r'\w+', best_product.get("title", "").lower()))
        if (result_words - query_words) & _DISCRIMINATORS:
            return None

        link = best_product.get("link", "")
        slug = link.replace("https://www.buyzoxs.de/kaufen/", "").replace(".html", "")
        return MatchResult(slug=slug, display_name=best_product.get("title", dev.model), eos_device=dev, brand=dev.brand)
    except Exception:
        return None

def fetch_category_id(slug: str) -> Optional[str]:
    try:
        resp = scraper.get(f"https://www.buyzoxs.de/kaufen/{slug}.html", headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200: return None
        soup = BeautifulSoup(resp.text, "html.parser")
        div = soup.find("div", id="vue-filter")
        return div.get("data-category-id") if div else None
    except Exception:
        return None

def fetch_article_by_asin(asin: str) -> List[dict]:
    try:
        resp = scraper.get(f"https://www.buyzoxs.de/api/article/{asin}", headers={**HEADERS, "Accept": "application/json"}, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200: return []
        data = resp.json()
        skus = data.get("result", {}).get("skus", [])
        
        variants = []
        for s in skus:
            variants.append({
                "variant_name": s.get("zustand_text", "").title() or str(s.get("zustand", "")),
                "es_price": _normalize_price_to_cents(s.get("preis", 0)),
                "quantity": int(float(s.get("anz", 0) or 0)),
                "lastInStock": s.get("lastInStock", False)
            })
        return [{"title": data.get("result", {}).get("article", {}).get("title", ""), "variants": variants}]
    except Exception:
        return []

def fetch_product_data(category_id: str) -> List[dict]:
    try:
        resp = scraper.post(f"https://www.buyzoxs.de/sys_filter.php?page=0&category_id={category_id}", 
                            headers={**HEADERS, "Content-Type": "application/json", "Accept": "application/json"}, json={}, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200: return []
        products = resp.json().get("products", [])
        
        for p in products:
            for v in p.get("variants", []):
                # FIXED: Uses the smart heuristic to handle both Euros and Cents
                v["es_price"] = _normalize_price_to_cents(v.get("es_price", 0))
                
        return products
    except Exception:
        return []

def fetch_eos_version(codename: str, cache: dict) -> str:
    if codename in cache: return cache[codename]
    try:
        resp = scraper.get(f"https://doc.e.foundation/devices/{codename}", headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            for dt in soup.find_all("dt"):
                if "build versions" in dt.get_text(strip=True).lower():
                    dd = dt.find_next_sibling("dd")
                    if dd:
                        cache[codename] = dd.get_text(separator=", ", strip=True)
                        return cache[codename]
    except Exception:
        pass
    cache[codename] = ""
    return ""