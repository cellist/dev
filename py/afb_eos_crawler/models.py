import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple

DB_PATH = "afb_eos.db"
REQUEST_TIMEOUT = 15

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
}

EXCLUDED_CONDITIONS = {"Fair", "Chance", "Steel", "Stealth"}
_CONDITION_RANK = {
    "Neuware": 1, "OVP geöffnet": 2, "Wie neu": 3, "Sehr gut": 4, "Gut": 5,
    "Fair": 10, "Chance": 11, "Steel": 12, "Stealth": 13,
}
STATUS_ICON = {"official": "[official]", "community": "[community]", "test": "[test]"}

@dataclass
class EosDevice:
    brand: str
    model: str
    codename: str
    status: str
    keywords: List[str] = field(default_factory=list)
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

# Expanded keywords to catch more URL variations
EOS_DEVICES: List[EosDevice] = [
    EosDevice("Samsung", "Galaxy Tab A 8.0", "gtowifi", "community", ["galaxy-tab-a-8", "tab-a-8"]),
    EosDevice("Samsung", "Galaxy Tab A7 10.4 2020", "gta4lwifi", "community", ["galaxy-tab-a7", "tab-a7-2020", "tab-a7"]),
    EosDevice("Samsung", "Galaxy Tab S5e", "gts4lvwifi", "community", ["galaxy-tab-s5e", "tab-s5e"]),
    EosDevice("Samsung", "Galaxy Tab S6 Lite", "gta4xlwifi", "community", ["galaxy-tab-s6-lite", "tab-s6-lite"]),
    EosDevice("Samsung", "Galaxy Tab S7", "gts7lwifi", "community", ["galaxy-tab-s7", "tab-s7"]),
    EosDevice("Google", "Pixel Tablet", "tangorpro", "official", ["pixel-tablet"]),
    EosDevice("Volla", "Volla Tablet", "mimir", "official", ["volla-tablet"]),
    EosDevice("Teracube", "Teracube 2e", "emerald", "official", ["teracube-2e"]),
    EosDevice("Teracube", "Teracube 2s", "sapphire", "official", ["teracube-2s"]),
]