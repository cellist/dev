import sqlite3
from typing import Dict, Tuple
from models import MatchResult, DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS device_variants (
            brand TEXT, model TEXT, codename TEXT, status TEXT,
            android_versions TEXT, zustand TEXT, price TEXT, url TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (brand, model, zustand)
        )
    """)
    conn.commit()
    conn.close()

def load_previous_state() -> Dict[Tuple[str, str], Dict[str, str]]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT brand, model, zustand, price FROM device_variants")
    rows = cursor.fetchall()
    conn.close()
    
    state = {}
    for brand, model, zustand, price in rows:
        key = (brand, model)
        if key not in state:
            state[key] = {}
        state[key][zustand] = price
    return state

def save_to_db(results: list[MatchResult]):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for r in results:
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