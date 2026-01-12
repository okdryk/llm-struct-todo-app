from __future__ import annotations
from typing import Optional
import re
from datetime import datetime

try:
    import dateparser
except Exception:
    dateparser = None

ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def normalize_due_date(due: Optional[str], *, base: Optional[datetime] = None) -> Optional[str]:
    """Normalize a user/LLM supplied due date.

    - If `due` is None or already an ISO date YYYY-MM-DD, return as-is.
    - Otherwise try to parse natural language (Japanese supported) using dateparser
      and return an ISO date string (YYYY-MM-DD) on success.
    - On failure, return the original value.
    """
    if due is None:
        return None

    due = due.strip()
    if due == "":
        return None

    if ISO_DATE_RE.match(due):
        return due

    if dateparser is None:
        # dateparser not available, return original
        return due

    settings = {
        "PREFER_DATES_FROM": "future",
        "RETURN_AS_TIMEZONE_AWARE": False,
    }
    if base is not None:
        settings["RELATIVE_BASE"] = base

    dt = dateparser.parse(due, settings=settings, languages=[
                          "ja"])  # type: ignore[arg-type]
    if dt is None:
        return due
    return dt.date().isoformat()
