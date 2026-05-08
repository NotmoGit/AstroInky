"""
config.py — single source of truth for all project settings.
Change your location, timezone, font size, or paths here and
it takes effect everywhere automatically.
"""

from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
FONTS_DIR  = BASE_DIR / "fonts"
ICONS_DIR  = BASE_DIR / "icons"
PHASES_DIR = BASE_DIR / "phases"
PICS_DIR   = BASE_DIR / "pics"

FONT_FILE  = FONTS_DIR / "Merriweather-VariableFont_opsz,wdth,wght.ttf"
FACE_IMAGE = BASE_DIR / "face.jpg"
MOONS_JSON = BASE_DIR / "moons.json"
APOD_CACHE = BASE_DIR / "apod_picture.jpg"
CREDS_FILE = BASE_DIR / "creds.txt"

# ── Location ─────────────────────────────────────────────────────────────────
LATITUDE   = "YOUR LAT"
LONGITUDE  = "YOUR LONG"
ELEVATION  = 15          # metres
TIMEZONE   = "Europe/London"
UTC_OFFSET = 0           # hours ahead of UTC

# ── Display ──────────────────────────────────────────────────────────────────
FONT_SIZE       = 18
FONT_SIZE_LARGE = 24

# ── API Keys ─────────────────────────────────────────────────────────────────
def _load_nasa_key() -> str:
    """Read NASA API key from creds.txt so it's never in source code."""
    try:
        return CREDS_FILE.read_text().strip()
    except FileNotFoundError:
        raise RuntimeError(
            f"NASA API key not found. Create {CREDS_FILE} containing just the key."
        )

NASA_API_KEY = _load_nasa_key()
