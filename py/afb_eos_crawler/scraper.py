import re
import time
from typing import Optional, List, Dict, Tuple
from urllib.parse import urlparse
import requests
import cloudscraper
from bs4 import BeautifulSoup
from models import HEADERS, REQUEST_TIMEOUT, EOS_DEVICES, EosDevice

scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False},
    delay=1
)

price_regex = re.compile(r'(\d{1,3}(?:\.\d{3})*(?:,\d{2}|,-)\s*€?)')

def _normalize_price(price_str: str) -> float:
    try:
        price_str = price_str.replace('€', '').replace(' ', '').strip()
        if price_str.endswith(',-'):
            price_str = price_str.replace(',-', '.00')
        return float(price_str.replace(".", "").replace(",", "."))
    except ValueError:
        return 0.0

def get_all_matching_products() -> Dict[str, Tuple[EosDevice, str]]:
    matched_products = {}
    all_slugs = set()
    
    print("   Scanning category pages for matching products...")
    
    for page in range(1, 6):
        url = f"https://www.afbshop.de/gebrauchte-tablets/?p={page}" if page > 1 else "https://www.afbshop.de/gebrauchte-tablets/"
        try:
            resp = scraper.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            if resp.status_code != 200:
                break
        except Exception:
            break
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        found_on_page = 0
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue
                
            if href.startswith('/'):
                full_href = f"https://www.afbshop.de{href}"
            elif href.startswith('http'):
                full_href = href
            else:
                continue
                
            if 'afbshop.de' not in full_href:
                continue
                
            parsed = urlparse(full_href)
            path_parts = parsed.path.strip('/').split('/')
            
            if len(path_parts) >= 2:
                base_slug = path_parts[0]
                
                if base_slug == 'gebrauchte-tablets' or 'p=' in base_slug:
                    continue
                    
                all_slugs.add(base_slug)
                
                if base_slug in matched_products:
                    continue
                    
                for device in EOS_DEVICES:
                    for kw in device.keywords:
                        kw_slug = kw.lower().replace(" ", "-").replace(".", "")
                        if kw_slug in base_slug:
                            matched_products[base_slug] = (device, full_href)
                            found_on_page += 1
                            break
                            
        print(f"      Page {page}: Found {found_on_page} new matching products.")
            
    # TARGETED DEBUG: Print ONLY slugs that look like tablets we care about
    target_keywords = ['samsung', 'galaxy', 'tab', 'pixel', 'volla', 'teracube', 'xiaomi', 'fairphone']
    relevant_slugs = [s for s in all_slugs if any(kw in s.lower() for kw in target_keywords)]
    
    print(f"\n   [DEBUG] Found {len(relevant_slugs)} potentially relevant tablet slugs:")
    for slug in sorted(relevant_slugs):
        # Check if it matched
        is_matched = slug in matched_products
        status = "✅ MATCHED" if is_matched else "❌ MISSED"
        print(f"      {status}: {slug}")
    print()
            
    return matched_products

def scrape_product_page(product_url: str) -> List[dict]:
    variants = []
    try:
        resp = scraper.get(product_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            return []
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        text = soup.get_text(" ", strip=True)
        
        conditions = ["Neuware", "OVP geöffnet", "Wie neu", "Sehr gut", "Gut", "Fair", "Akzeptabel"]
        
        for cond in conditions:
            start = 0
            while True:
                cond_idx = text.find(cond, start)
                if cond_idx == -1:
                    break
                
                # Strict forward matching (120 chars)
                search_window = text[cond_idx : cond_idx + 120]
                price_match = price_regex.search(search_window)
                
                if price_match:
                    price_str = price_match.group(1)
                    if not any(v['condition'] == cond for v in variants):
                        variants.append({
                            "condition": cond,
                            "price": price_str
                        })
                    break 
                
                start = cond_idx + len(cond)
                    
    except Exception as e:
        print(f"\n   [DEBUG] Error scraping {product_url}: {e}")
        
    return variants

def fetch_eos_version(codename: str, cache: dict) -> str:
    if codename in cache: return cache[codename]
    try:
        resp = scraper.get(f"https://doc.e.foundation/devices/{codename}", headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
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