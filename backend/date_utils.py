from __future__ import annotations
from typing import Optional
import re
from datetime import datetime

from ja_timex import TimexParser

ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def normalize_due_date(due: Optional[str], *, base: Optional[datetime] = None) -> Optional[str]:
    if due is None:
        return None

    due = due.strip()
    if due == "":
        return None

    if ISO_DATE_RE.match(due):
        return due

    reference = base or datetime.now()
    parser = TimexParser(reference=reference)

    try:
        timexes = parser.parse(due)
    except Exception:
        timexes = []

    for timex in timexes:
        if timex.type == "DATE":
            dt = timex.to_datetime()
            if dt:
                return dt.date().isoformat()
        elif timex.type in ("DURATION", "TIME"):
            dt = timex.to_datetime()
            if dt:
                return dt.date().isoformat()

    return due
