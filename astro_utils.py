"""
astro_utils.py — shared astronomy helpers built on pyephem.

Provides: observer factory, time utilities, moon phase logic.
All times fed to ephem are UTC. Display formatting is done in local time.
"""

import ephem
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from config import LATITUDE, LONGITUDE, ELEVATION, TIMEZONE, UTC_OFFSET, PHASES_DIR

_tz = ZoneInfo(TIMEZONE)


# ── Time helpers ─────────────────────────────────────────────────────────────

def utc_now() -> datetime:
    """Current time as a naive UTC datetime (what ephem expects)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def local_now() -> datetime:
    """Current time as a timezone-aware datetime (for display)."""
    return datetime.now(_tz)


def ephem_to_local(ephem_date: ephem.Date) -> datetime:
    """Convert an ephem UTC date to a local naive datetime."""
    return ephem_date.datetime() + timedelta(hours=UTC_OFFSET)


# ── Observer ─────────────────────────────────────────────────────────────────

def make_observer(date: datetime | None = None) -> ephem.Observer:
    """
    Return a configured ephem Observer for Singapore.
    Always pass UTC — ephem requires it.
    """
    obs           = ephem.Observer()
    obs.lat       = LATITUDE
    obs.lon       = LONGITUDE
    obs.elevation = ELEVATION
    obs.date      = date or utc_now()
    return obs


# ── Moon phase ───────────────────────────────────────────────────────────────

def moon_phase_name(observer: ephem.Observer) -> str:
    """
    Return the current moon phase as a human-readable string.
    Uses illumination percentage and elongation direction (waxing/waning).
    """
    moon        = ephem.Moon(observer)
    illumination = moon.phase
    waxing      = 0 < float(moon.elong) < ephem.pi

    if illumination < 1:
        return "New Moon"
    if illumination < 45:
        return "Waxing Crescent" if waxing else "Waning Crescent"
    if illumination < 55:
        return "First Quarter"   if waxing else "Last Quarter"
    if illumination < 99:
        return "Waxing Gibbous"  if waxing else "Waning Gibbous"
    return "Full Moon"


_PHASE_IMAGES = {
    "new moon":        "new_moon.png",
    "waxing crescent": "waxing_crescent.png",
    "first quarter":   "first_quarter.png",
    "waxing gibbous":  "waxing_gibbous.png",
    "full moon":       "full_moon.png",
    "waning gibbous":  "waning_gibbous.png",
    "last quarter":    "last_quarter.png",
    "waning crescent": "waning_crescent.png",
}

def phase_image_path(phase: str):
    """Return the Path to the moon phase image, or None if unknown."""
    filename = _PHASE_IMAGES.get(phase.lower())
    return (PHASES_DIR / filename) if filename else None


# ── Rise / set helpers ───────────────────────────────────────────────────────

def rise_set_times(observer: ephem.Observer, body: ephem.Body) -> tuple[str, str]:
    """
    Return (rise_time, set_time) as formatted local-time strings.
    Falls back to 'Not visible' if the body never rises/sets today.
    """
    fmt = "%H:%M %a"
    try:
        rise = ephem_to_local(observer.next_rising(body)).strftime(fmt)
    except (ephem.AlwaysUpError, ephem.NeverUpError):
        rise = "Not visible"
    try:
        sset = ephem_to_local(observer.next_setting(body)).strftime(fmt)
    except (ephem.AlwaysUpError, ephem.NeverUpError):
        sset = "Not visible"
    return rise, sset


# ── Text wrapping ─────────────────────────────────────────────────────────────

def wrap_text(text: str, font, draw, max_width: int, max_lines: int) -> list[str]:
    """
    Word-wrap text to fit within max_width pixels using the given font.
    Truncates cleanly at a sentence boundary and appends '...' if needed.
    """
    import re

    words = text.split()
    lines: list[str] = []
    line  = ""

    for word in words:
        candidate = line + word + " "
        if draw.textlength(candidate, font=font) <= max_width:
            line = candidate
        else:
            lines.append(line.rstrip())
            line = word + " "
        if len(lines) >= max_lines:
            break

    if line and len(lines) < max_lines:
        lines.append(line.rstrip())
    elif len(lines) == max_lines:
        # Try to cut at the last sentence boundary
        full = " ".join(lines) + " " + line
        matches = list(re.finditer(r"[.!?]\s+", full))
        clean   = full[: matches[-1].end()].strip() if matches else full.strip()

        lines, line = [], ""
        for word in clean.split():
            candidate = line + word + " "
            if draw.textlength(candidate, font=font) <= max_width:
                line = candidate
            else:
                lines.append(line.rstrip())
                line = word + " "
                if len(lines) >= max_lines - 1:
                    break
        if line:
            lines.append(line.rstrip())

        if not full.strip().endswith(clean.strip()):
            lines[-1] = lines[-1].rstrip(".!? ") + "..."

    return lines
