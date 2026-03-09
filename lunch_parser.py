"""
lunch_parser.py — Nutrislice school lunch menu fetcher.

Standalone module. No Alexa or AWS dependencies.
Requires only Python standard library.

Usage:
    from lunch_parser import LunchParser

    parser = LunchParser()
    entrees = parser.get_entrees("Los Cerros Middle")
    print(parser.format_menu(entrees))
"""

import json
import logging
import os
import socket
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

# ── Defaults (edit directly or override with env vars) ───────────────────────
DEFAULT_DISTRICT  = "srvusd"
DEFAULT_LOG_LEVEL = "INFO"   # DEBUG | INFO | WARNING | ERROR
# ─────────────────────────────────────────────────────────────────────────────

logger = logging.getLogger(__name__)
LOG_LEVEL = os.environ.get("LOG_LEVEL", DEFAULT_LOG_LEVEL).upper()
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))


class LunchParser:
    """
    Fetches and formats school lunch menus from the Nutrislice API.

    Supports case-insensitive school name lookup and returns entrees
    as a plain list of strings, leaving formatting up to the caller.

    Returns:
        get_entrees() → List[str]  — entrees for the day
                      → []         — day exists but has no menu
                      → None       — network / HTTP error

    Raises:
        ValueError from get_entrees() if the school name is not recognised.
    """

    API_TIMEOUT = 8  # seconds

    # Mapping: normalised name → (display name, Nutrislice API slug)
    SCHOOL_MAPPING: Dict[str, Tuple[str, str]] = {
        "los cerros middle":      ("Los Cerros Middle",      "los-cerros-middle"),
        "vista grande elementary": ("Vista Grande Elementary", "vista-grande-school"),
    }

    def __init__(self, district: str = None):
        """
        Args:
            district: Nutrislice district ID.
                      Falls back to NUTRISLICE_DISTRICT env var, then "srvusd".
        """
        self.district = (
            district
            or os.environ.get("NUTRISLICE_DISTRICT", DEFAULT_DISTRICT)
        )

    # ── Public API ────────────────────────────────────────────────────────────

    @property
    def schools(self) -> List[str]:
        """Display names of all supported schools."""
        return [display for display, _ in self.SCHOOL_MAPPING.values()]

    def get_entrees(
        self, school_name: str, date: datetime = None
    ) -> Optional[List[str]]:
        """
        Fetch entrees for a school on a given date.

        Args:
            school_name: Case-insensitive school name, e.g. "Los Cerros Middle".
            date:        Date to fetch (defaults to today).

        Returns:
            List of sanitised entree name strings — may be empty if no menu.
            None if the API call failed.

        Raises:
            ValueError: If school_name is not in SCHOOL_MAPPING.
        """
        if date is None:
            date = datetime.now()

        school_key = school_name.strip().lower()
        if school_key not in self.SCHOOL_MAPPING:
            raise ValueError(
                f"Unknown school: {school_name!r}. "
                f"Supported: {self.schools}"
            )

        display_name, school_slug = self.SCHOOL_MAPPING[school_key]
        logger.info(f"Fetching menu: {display_name} on {date.strftime('%Y-%m-%d')}")

        return self._fetch_entrees(school_slug, date)

    def format_menu(self, entrees: List[str]) -> str:
        """
        Format a list of entrees into a natural-language string.

        Examples:
            []                        → "no menu available"
            ["Pizza"]                 → "lunch is Pizza"
            ["Pizza", "Salad"]        → "lunch includes Pizza and Salad"
            ["Pizza", "Salad", "Fruit"] → "lunch includes Pizza, Salad, and Fruit"
        """
        if not entrees:
            return "no menu available"
        if len(entrees) == 1:
            return f"lunch is {entrees[0]}"
        if len(entrees) == 2:
            return f"lunch includes {entrees[0]} and {entrees[1]}"
        all_but_last = ", ".join(entrees[:-1])
        return f"lunch includes {all_but_last}, and {entrees[-1]}"

    # ── Private helpers ───────────────────────────────────────────────────────

    def _fetch_entrees(
        self, school_slug: str, date: datetime
    ) -> Optional[List[str]]:
        """Hit the Nutrislice API and return entrees for the given date."""
        date_str = date.strftime("%Y-%m-%d")
        url = (
            f"https://{self.district}.api.nutrislice.com/menu/api/weeks/"
            f"school/{school_slug}/menu-type/lunch/"
            f"{date.year}/{date.month:02d}/{date.day:02d}/"
        )
        logger.debug(f"GET {url}")

        try:
            with urlopen(url, timeout=self.API_TIMEOUT) as response:
                logger.debug(f"HTTP {response.getcode()}")
                data = json.loads(response.read().decode("utf-8"))
        except socket.timeout:
            logger.error(f"Request timed out: {url}")
            return None
        except HTTPError as e:
            logger.error(f"HTTP {e.code} from Nutrislice: {e.reason}")
            return None
        except URLError as e:
            logger.error(f"Network error: {e.reason}")
            return None

        return self._extract_entrees(data, date_str)

    def _extract_entrees(self, data: dict, date_str: str) -> List[str]:
        """Parse the Nutrislice JSON payload and return entrees for date_str."""
        for day in data.get("days", []):
            logger.debug(f"Checking day: {day.get('date')}")
            if day.get("date") != date_str:
                continue

            entrees = []
            for item in day.get("menu_items", []):
                food = item.get("food")
                if not food:
                    continue
                name     = food.get("name", "")
                category = food.get("food_category", "")
                logger.debug(f"  {category}: {name}")
                if category == "entree" and name:
                    entrees.append(self._sanitize(name))

            logger.info(f"Found {len(entrees)} entree(s) for {date_str}")
            return entrees

        logger.warning(f"Date {date_str} not found in API response")
        return []

    @staticmethod
    def _sanitize(text: str) -> str:
        """Strip characters that can break display or speech output."""
        return (
            text
            .replace("&", "and")
            .replace("<", "")
            .replace(">", "")
            .replace('"', "")
            .replace("'", "")
        )
