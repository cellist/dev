from dataclasses import dataclass, field
from typing import List

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SITEMAP_URL = "https://www.buyzoxs.de/sitemap.xml"
DB_PATH = "eos_buyzoxs.db"
REQUEST_TIMEOUT = 15

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
}

EXCLUDED_CONDITIONS = {"Fair", "Chance", "Steel", "Stealth"}
_CONDITION_RANK = {
    "Neu": 1, "Wie Neu": 2, "Sehr Gut": 3, "Gut": 4, "OK": 5, "Akzeptabel": 5,
    "Fair": 10, "Chance": 11, "Steel": 12, "Stealth": 13,
}
STATUS_ICON = {"official": "[official]", "community": "[community]", "test": "[test]"}

# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# Master Data
# ---------------------------------------------------------------------------

EOS_DEVICES: List[EosDevice] = [
    EosDevice("BQ", "Aquaris X", "bardock", "community", ["bq-aquaris-x"]),
    EosDevice("BQ", "Aquaris X Pro", "bardockpro", "community", ["bq-aquaris-x-pro"]),
    EosDevice("Fairphone", "Fairphone 3", "FP3", "official", ["fairphone/fairphone-3"]),
    EosDevice("Fairphone", "Fairphone 4", "FP4", "official", ["fairphone/fairphone-4"]),
    EosDevice("Fairphone", "Fairphone 5", "FP5", "official", ["fairphone/fairphone-5"]),
    EosDevice("Gigaset", "GS290", "GS290", "official", ["gigaset/gigaset-gs290"]),
    EosDevice("Gigaset", "GS6 / GS6 PRO", "GS6_Venus", "official", ["gigaset/gigaset-gs6"]),
    EosDevice("Google", "Pixel 4a 5G", "bramble", "community", ["google-pixel-4a-5g"]),
    EosDevice("Google", "Pixel 6a", "bluejay", "community", ["google-pixel-6a"]),
    EosDevice("Google", "Pixel 7a", "lynx", "community", ["google-pixel-7a"]),
    EosDevice("Google", "Pixel 6", "oriole", "official", ["google/pixel-6"]),
    EosDevice("Google", "Pixel 6 Pro", "raven", "official", ["google/pixel-6-pro"]),
    EosDevice("Google", "Pixel 7", "panther", "official", ["google/pixel-7"]),
    EosDevice("Google", "Pixel 7 Pro", "cheetah", "official", ["google/pixel-7-pro"]),
    EosDevice("Google", "Pixel 8", "shiba", "official", ["google/pixel-8"]),
    EosDevice("Google", "Pixel 8 Pro", "husky", "official", ["google/pixel-8-pro"]),
    EosDevice("Google", "Pixel 9", "tokay", "official", ["google/pixel-9"]),
    EosDevice("Google", "Pixel 9 Pro", "caiman", "official", ["google/pixel-9-pro"]),
    EosDevice("Google", "Pixel 9 Pro XL", "komodo", "official", ["google/pixel-9-pro-xl"]),
    EosDevice("Google", "Pixel 9 Pro Fold", "comet", "official", ["google/pixel-9-pro-fold"]),
    EosDevice("Samsung", "Galaxy S7", "herolte", "community", ["samsung-galaxy-s7"]),
    EosDevice("Samsung", "Galaxy S7 Edge", "hero2lte", "community", ["samsung-galaxy-s7-edge"]),
    EosDevice("Samsung", "Galaxy S8", "dreamlte", "community", ["samsung-galaxy-s8"]),
    EosDevice("Samsung", "Galaxy S8+", "dream2lte", "community", ["samsung-galaxy-s8-plus"]),
    EosDevice("Samsung", "Galaxy S9", "starlte", "official", ["samsung-galaxy-s9"]),
    EosDevice("Samsung", "Galaxy S9+", "star2lte", "official", ["samsung-galaxy-s9-plus"]),
    EosDevice("Samsung", "Galaxy S10e", "beyond0lte", "community", ["samsung-galaxy-s10e"]),
    EosDevice("Samsung", "Galaxy S10", "beyond1lte", "community", ["samsung-galaxy-s10"]),
    EosDevice("Samsung", "Galaxy S10+", "beyond2lte", "community", ["samsung-galaxy-s10-plus"]),
    EosDevice("Samsung", "Galaxy S10 Lite", "beyondxq", "community", ["samsung-galaxy-s10-lite"]),
    EosDevice("Samsung", "Galaxy S20 FE", "r8q", "community", ["samsung-galaxy-s20-fe"]),
    EosDevice("Samsung", "Galaxy S20+", "y2s", "community", ["samsung-galaxy-s20-plus"]),
    EosDevice("Samsung", "Galaxy S20 Ultra", "z3q", "community", ["samsung-galaxy-s20-ultra"]),
    EosDevice("Samsung", "Galaxy A21s", "a21s", "community", ["samsung-galaxy-a21"]),
    EosDevice("Samsung", "Galaxy A52s 5G", "a52sxq", "community", ["samsung-galaxy-a52"]),
    EosDevice("Samsung", "Galaxy A53 5G", "a53x", "community", ["samsung-galaxy-a53"]),
    EosDevice("Samsung", "Galaxy Note 9", "crownlte", "community", ["samsung-galaxy-note-9"]),
    EosDevice("Samsung", "Galaxy Note 10", "d1", "community", ["samsung-galaxy-note-10"]),
    EosDevice("Samsung", "Galaxy Note 20", "c1s", "community", ["samsung-galaxy-note-20"]),
    EosDevice("OnePlus", "OnePlus Nord", "avicii", "official", ["oneplus-nord"]),
    EosDevice("OnePlus", "OnePlus 3", "oneplus3", "community", ["oneplus-3"]),
    EosDevice("OnePlus", "OnePlus 5", "cheeseburger", "community", ["oneplus-5"]),
    EosDevice("OnePlus", "OnePlus 6", "enchilada", "community", ["oneplus-6"]),
    EosDevice("OnePlus", "OnePlus 7", "guacamoleb", "community", ["oneplus-7"]),
    EosDevice("OnePlus", "OnePlus 8", "instantnoodle", "official", ["oneplus-8"]),
    EosDevice("OnePlus", "OnePlus 9", "lemonade", "official", ["oneplus-9"]),
    EosDevice("Sony", "Xperia 1 III / IV", "pdx215", "community", ["sony-xperia-1"]),
    EosDevice("Sony", "Xperia 5 III / V", "pdx214", "community", ["sony-xperia-5"]),
    EosDevice("Sony", "Xperia 10 IV / V", "pdx225", "official", ["sony-xperia-10"]),
    EosDevice("Xiaomi", "Mi A1", "tissot", "official", ["mi-a1"]),
    EosDevice("Xiaomi", "Mi A2", "jasmine_sprout", "official", ["mi-a2"]),
    EosDevice("Xiaomi", "Mi A3", "laurel_sprout", "official", ["mi-a3"]),
    EosDevice("Xiaomi", "Mi 8", "dipper", "community", ["mi-8"]),
    EosDevice("Xiaomi", "Mi 9", "cepheus", "community", ["mi-9"]),
    EosDevice("Xiaomi", "Mi 10", "umi", "community", ["mi-10"]),
    EosDevice("Xiaomi", "Mi 11", "venus", "community", ["mi-11", "xiaomi-11"]),
    EosDevice("Xiaomi", "Xiaomi 12", "cupid", "community", ["xiaomi-12"]),
    EosDevice("Xiaomi", "POCO F5", "marble", "community", ["xiaomi-poco-f5", "poco-f5"]),
    EosDevice("Xiaomi", "POCO X3 Pro", "vayu", "community", ["xiaomi-poco-x3-pro"]),
    EosDevice("Xiaomi", "Redmi Note 9S", "miatoll", "community", ["redmi-note-9"]),
    EosDevice("Xiaomi", "Redmi Note 10 Pro", "sweet", "community", ["redmi-note-10"]),
    EosDevice("Xiaomi", "Redmi Note 11", "spes", "community", ["redmi-note-11"]),
    EosDevice("Xiaomi", "Redmi Note 12", "tapas", "community", ["redmi-note-12"]),
    EosDevice("Motorola", "Edge 20", "berlna", "community", ["edge-20"]),
    EosDevice("Motorola", "Edge 30 Fusion", "tundra", "community", ["edge-30"]),
    EosDevice("Motorola", "Edge 30 Ultra", "eqs", "community", ["edge-30-ultra"]),
    EosDevice("Motorola", "Edge 30 Neo", "miami", "community", ["edge-30-neo"]),
    EosDevice("Motorola", "Edge 40 Pro", "rtwo", "community", ["edge-40"]),
]