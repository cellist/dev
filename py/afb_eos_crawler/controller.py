import time
from collections import defaultdict
from typing import List, Dict, Tuple
from models import EOS_DEVICES, EosDevice, MatchResult, Variant, EXCLUDED_CONDITIONS, _CONDITION_RANK
import scraper

def run_crawler() -> List[MatchResult]:
    print("[*] Fetching products from afbshop.de...")
    
    # Step 1: Find all matching products (returns base_slug -> (device, full_url))
    matched_products = scraper.get_all_matching_products()
    print(f"   Total matching products found: {len(matched_products)}")
    
    results: List[MatchResult] = []
    
    # Step 2: For each matched product, visit the FULL URL to get exact prices
    for base_slug, (device, product_url) in matched_products.items():
        print(f"   Scraping details for {device.model} ({base_slug})...", end=" ", flush=True)
        variants_data = scraper.scrape_product_page(product_url)
        
        device_variants = []
        seen_conditions = set()
        
        for v_data in variants_data:
            cond = v_data['condition']
            if cond in seen_conditions:
                continue
            seen_conditions.add(cond)
            
            price_eur = scraper._normalize_price(v_data['price'])
            price_str = f"{price_eur:.2f}".replace(".", ",") + " EUR"
            
            device_variants.append(Variant(zustand=cond, price=price_str))
            
        if device_variants:
            # Sort by condition rank (best first), then by price (lowest first)
            device_variants.sort(key=lambda v: (
                _CONDITION_RANK.get(v.zustand, 6),
                float(v.price.replace(" EUR", "").replace(",", "."))
            ))
            
            results.append(MatchResult(
                slug=product_url, # Use the full URL with the variant ID
                display_name=f"{device.brand} {device.model}",
                eos_device=device,
                brand=device.brand,
                variants=device_variants
            ))
            print(f"found {len(device_variants)} conditions.")
        else:
            print("no conditions found.")
            
    return results

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

def enrich_with_prices_and_conditions(results: List[MatchResult], previous_state: Dict[Tuple[str, str], Dict[str, str]]) -> Tuple[List[MatchResult], List[str]]:
    changes_log = []
    
    for r in results:
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
            print(f"\n  {r.eos_device.model}:")
            for c in device_changes:
                print(f"      {c}")
        else:
            print(f"  {r.eos_device.model}: No changes.")
            
    return results, changes_log