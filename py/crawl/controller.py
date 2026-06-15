import time
from collections import defaultdict
from typing import List, Dict, Tuple, Optional

from models import EOS_DEVICES, EosDevice, MatchResult, Variant, EXCLUDED_CONDITIONS, _CONDITION_RANK
import scraper

# ---------------------------------------------------------------------------
# Matching Logic
# ---------------------------------------------------------------------------

_SLUG_INDEX: Dict[str, EosDevice] = {}
_SORTED_KEYWORDS: List[Tuple[str, EosDevice]] = []

def _init_matching_engine():
    global _SLUG_INDEX, _SORTED_KEYWORDS
    for dev in EOS_DEVICES:
        for kw in dev.keywords:
            _SLUG_INDEX[kw] = dev
    _SORTED_KEYWORDS = sorted(((kw, dev) for dev in EOS_DEVICES for kw in dev.keywords), key=lambda x: len(x[0]), reverse=True)

_init_matching_engine()

def _extract_asin(slug: str) -> Optional[str]:
    import re
    m = re.search(r"_([A-Z0-9]{10})$", slug)
    return m.group(1) if m else None

def match_eos_device(slug: str) -> Optional[EosDevice]:
    slug_lower = slug.lower()
    if slug_lower in _SLUG_INDEX:
        return _SLUG_INDEX[slug_lower]
    if "/" in slug_lower:
        filename = slug_lower.rsplit("/", 1)[-1]
        for kw, dev in _SORTED_KEYWORDS:
            if filename.startswith(kw) and (len(filename) == len(kw) or filename[len(kw)] in ("-", "_")):
                return dev
    return None

def run_crawler(threshold: int = 80) -> List[MatchResult]:
    buyzoxs_devices = scraper.fetch_buyzoxs_devices()
    results: List[MatchResult] = []

    if not buyzoxs_devices:
        print("[*] Sitemap unavailable. Using known /e/OS device slugs to fetch prices...")
        for dev in EOS_DEVICES:
            slug = dev.keywords[0] if dev.keywords else dev.model.lower().replace(" ", "-")
            results.append(MatchResult(slug=slug, display_name=f"{dev.brand} {dev.model}", eos_device=dev, brand=dev.brand))
    else:
        print(f"[*] Matching {len(buyzoxs_devices)} pages against {len(EOS_DEVICES)} /e/OS devices...")
        from thefuzz import fuzz
        for slug, display in buyzoxs_devices:
            eos = match_eos_device(slug)
            if eos:
                results.append(MatchResult(slug=slug, display_name=display, eos_device=eos, brand=eos.brand))

    by_key: Dict[Tuple[str, str], MatchResult] = {}
    by_key_score: Dict[Tuple[str, str], int] = defaultdict(int)

    from thefuzz import fuzz
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
            r = scraper.search_buyzoxs_for_device(dev, threshold=threshold)
            if r:
                print(f"   Found: {dev.model} -> {r.slug}")
                by_key[(dev.brand, dev.model)] = r
            time.sleep(0.3)

    return list(by_key.values())

def enrich_with_versions(results: List[MatchResult], delay: float = 0.4) -> None:
    cache = {}
    seen = set()
    total = len({r.eos_device.codename for r in results})
    done = 0
    for r in results:
        if r.eos_device.codename in seen: continue
        seen.add(r.eos_device.codename)
        done += 1
        print(f"   [{done}/{total}] Fetching /e/OS version for {r.eos_device.model} ({r.eos_device.codename})...", end=" ", flush=True)
        version = scraper.fetch_eos_version(r.eos_device.codename, cache)
        r.eos_device.android_versions = version
        print(version or "(not found)")
        time.sleep(delay)

def parse_price_to_float(price_str: str) -> float:
    try:
        return float(price_str.replace(" EUR", "").replace(",", "."))
    except ValueError:
        return 0.0

def enrich_with_prices_and_conditions(results: List[MatchResult], previous_state: Dict[Tuple[str, str], Dict[str, str]], delay: float = 0.5) -> Tuple[List[MatchResult], List[str]]:
    changes_log = []
    kept = []

    for idx, r in enumerate(results, 1):
        print(f"   [{idx}/{len(results)}] {r.eos_device.model} ({r.slug})...", end=" ", flush=True)
        
        asin = _extract_asin(r.slug)
        if asin:
            products = scraper.fetch_article_by_asin(asin)
        else:
            cat_id = scraper.fetch_category_id(r.slug)
            if not cat_id:
                print("(category ID not found)")
                r.variants = [Variant(zustand="Unknown", price="See website")]
                kept.append(r)
                time.sleep(delay)
                continue
            products = scraper.fetch_product_data(cat_id)
            
        if not products:
            print("(no product data)")
            r.variants = [Variant(zustand="Unknown", price="See website")]
            kept.append(r)
            time.sleep(delay)
            continue

        all_variants = [v for product in products for v in product.get("variants", []) if v.get("quantity", 0) > 0 or v.get("lastInStock", False)]
        if not all_variants:
            print("(no variants in stock)")
            r.variants = [Variant(zustand="Unknown", price="See website")]
            kept.append(r)
            time.sleep(delay)
            continue

        acceptable = [v for v in all_variants if v.get("variant_name", "") not in EXCLUDED_CONDITIONS]
        if not acceptable:
            print(f"(only { {v.get('variant_name', '?') for v in all_variants} } – excluded)")
            time.sleep(delay)
            continue

        acceptable.sort(key=lambda v: (_CONDITION_RANK.get(v.get("variant_name", ""), 6), v.get("es_price", 999999)))
        
        # Deduplicate: keep ONLY the best (lowest) price for each condition
        seen_zustand = set()
        unique_variants = []
        for v in acceptable:
            zustand = v.get("variant_name", "Unknown")
            if zustand not in seen_zustand:
                seen_zustand.add(zustand)
                price_str = f"{v.get('es_price', 0) / 100.0:.2f}".replace(".", ",") + " EUR"
                unique_variants.append(Variant(zustand=zustand, price=price_str))

        r.variants = unique_variants
        
        # Change Detection
        key = (r.brand, r.eos_device.model)
        old_variants = previous_state.get(key, {})
        device_changes = []
        
        if not old_variants:
            device_changes.append(f"🆕 NEW DEVICE: {r.eos_device.model}")
        else:
            for v in r.variants:
                if v.zustand not in old_variants:
                    device_changes.append(f"➕ NEW: {v.zustand} @ {v.price}")
                else:
                    old_price = old_variants[v.zustand]
                    if old_price != v.price:
                        old_val, new_val = parse_price_to_float(old_price), parse_price_to_float(v.price)
                        if new_val < old_val and old_val > 0:
                            device_changes.append(f"📉 PRICE DROP: {v.zustand} {old_price} -> {v.price}")
                        elif new_val > old_val:
                            device_changes.append(f"📈 PRICE INCREASE: {v.zustand} {old_price} -> {v.price}")
            
            for old_zustand, old_price in old_variants.items():
                if old_zustand not in [v.zustand for v in r.variants]:
                    device_changes.append(f"❌ DISAPPEARED: {old_zustand} (was {old_price})")
        
        if device_changes:
            changes_log.extend([f"  {r.eos_device.model}: {c}" for c in device_changes])
            print()
            for c in device_changes:
                print(f"      {c}")
        else:
            print(f"{r.variants[0].zustand} @ {r.variants[0].price} ({len(r.variants)} options, no changes)")
            
        kept.append(r)
        time.sleep(delay)

    return kept, changes_log