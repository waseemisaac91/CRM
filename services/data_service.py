"""
data_service.py — Data logic for all pages.
"""

from services.google_drive_service import (
    fetch_applications,
    fetch_mentor,
    fetch_interviews,
    fetch_vit1,
    fetch_vit2,
)

# --------------------------------------------------
# Error tracking
# --------------------------------------------------
_LAST_ERROR = None


def get_last_error():
    return _LAST_ERROR


def _set_error(msg):
    global _LAST_ERROR
    _LAST_ERROR = msg


def _clear_error():
    global _LAST_ERROR
    _LAST_ERROR = None


# --------------------------------------------------
# Name helpers
# --------------------------------------------------
def _normalise_name(value):
    if value is None:
        return ""
    return str(value).strip().lower()


def _find_name_column(record):
    if not record:
        return None
    keys_lower = {k.lower(): k for k in record.keys()}
    for candidate in ("full name", "candidate name", "name", "applicant"):
        if candidate in keys_lower:
            return keys_lower[candidate]
    if "first name" in keys_lower and "last name" in keys_lower:
        return ("__combined__",
                keys_lower["first name"],
                keys_lower["last name"])
    return None


def _get_name(record):
    col = _find_name_column(record)
    if col is None:
        return ""
    if isinstance(col, tuple):
        _, first_k, last_k = col
        first = str(record.get(first_k, "") or "").strip()
        last = str(record.get(last_k, "") or "").strip()
        return f"{first} {last}".strip()
    return str(record.get(col, "") or "").strip()


def name_matches(query, name):
    """True if any word in `name` starts with `query` (case-insensitive)."""
    if not query:
        return True
    if not name:
        return False
    q = query.strip().lower()
    for word in str(name).lower().split():
        if word.startswith(q):
            return True
    return False


def _header_and_rows(records):
    if not records:
        return [], []
    headers = list(records[0].keys())
    rows = [dict(r) for r in records]
    return headers, rows


# --------------------------------------------------
# De-duplication helper
# --------------------------------------------------
def _dedupe(rows, keys=("email", "full name")):
    """
    Remove duplicate rows by looking at the given column names
    (case-insensitive, in priority order). Keeps the first occurrence.

    If none of the requested columns exist, falls back to comparing
    the whole row as a tuple.

    NOTE: 'timestamp' is intentionally NOT part of the default key,
    so rows that differ only by timestamp are still considered duplicates.
    """
    if not rows:
        return []

    # Find the real column names present in the data
    lower_map = {k.lower(): k for k in rows[0].keys()}
    chosen = [lower_map[w] for w in keys if w in lower_map]

    seen = set()
    unique = []

    for r in rows:
        if chosen:
            key = tuple(
                str(r.get(col, "") or "").strip().lower()
                for col in chosen
            )
        else:
            key = tuple(
                str(v).strip().lower() for v in r.values()
            )

        if key in seen:
            continue
        seen.add(key)
        unique.append(r)

    return unique


# --------------------------------------------------
# Applications
# --------------------------------------------------
def get_applications():
    _clear_error()
    try:
        records = fetch_applications()
        headers, rows = _header_and_rows(records)
        rows = _dedupe(rows)
        return headers, rows
    except Exception as exc:
        _set_error(f"Could not read Applications: {exc}")
        return [], []


def search_applications(query):
    headers, rows = get_applications()
    if not query:
        return headers, rows
    filtered = [r for r in rows if name_matches(query, _get_name(r))]
    return headers, filtered


def get_mentor_defined():
    headers, rows = get_applications()
    filtered = []
    for r in rows:
        val = ""
        for k in r.keys():
            if "mentor" in k.lower() and "meeting" in k.lower():
                val = str(r[k] or "").strip()
                break
        if val and val.lower() not in ("no", "none", "false", "0"):
            filtered.append(r)
    return headers, _dedupe(filtered)


def get_mentor_not_defined():
    headers, rows = get_applications()
    filtered = []
    for r in rows:
        val = ""
        for k in r.keys():
            if "mentor" in k.lower() and "meeting" in k.lower():
                val = str(r[k] or "").strip()
                break
        if not val or val.lower() in ("no", "none", "false", "0"):
            filtered.append(r)
    return headers, _dedupe(filtered)


# --------------------------------------------------
# Duplicates / Unique
# --------------------------------------------------
def get_duplicate_applications():
    """
    Rows where (name + email) appear more than once.
    Intentionally NOT de-duplicated — duplicates are the point here.
    """
    headers, rows = get_applications()

    email_col = None
    if rows:
        for k in rows[0].keys():
            if "email" in k.lower() or "mail" in k.lower():
                email_col = k
                break

    if email_col is None:
        return headers, []

    from collections import Counter
    keys = [
        (_normalise_name(_get_name(r)), _normalise_name(r.get(email_col, "")))
        for r in rows
    ]
    counts = Counter(keys)
    filtered = [r for r, k in zip(rows, keys) if counts[k] > 1]
    return headers, filtered


def get_unique_applications():
    """Remove duplicates by name (first occurrence kept)."""
    headers, rows = get_applications()
    seen = set()
    filtered = []
    for r in rows:
        key = _normalise_name(_get_name(r))
        if key and key not in seen:
            seen.add(key)
            filtered.append(r)
    return headers, filtered


# --------------------------------------------------
# VIT helpers
# --------------------------------------------------
def _names_set(records):
    """Set of normalised names from records."""
    return {_normalise_name(_get_name(r)) for r in records if _get_name(r)}


def _record_by_name(records):
    """Map normalised name → first record with that name."""
    result = {}
    for r in records:
        key = _normalise_name(_get_name(r))
        if key and key not in result:
            result[key] = r
    return result


# --------------------------------------------------
# Previous VIT Check
#   Rule: Applications ∩ (VIT1 ∪ VIT2)
# --------------------------------------------------
def get_previous_vit():
    _clear_error()

    headers, apps = get_applications()

    errors = []
    try:
        vit1 = fetch_vit1()
    except Exception as exc:
        vit1 = []
        errors.append(f"VIT1: {exc}")

    try:
        vit2 = fetch_vit2()
    except Exception as exc:
        vit2 = []
        errors.append(f"VIT2: {exc}")

    if errors:
        _set_error(" | ".join(errors))
        return [], []

    if not vit1 and not vit2:
        _set_error("VIT1 and VIT2 returned no rows.")
        return [], []

    vit1_names = _names_set(vit1)
    vit2_names = _names_set(vit2)

    filtered = []
    for r in apps:
        name = _normalise_name(_get_name(r))
        in_vit1 = name in vit1_names
        in_vit2 = name in vit2_names

        if in_vit1 or in_vit2:
            found_in = []
            if in_vit1:
                found_in.append("VIT1")
            if in_vit2:
                found_in.append("VIT2")
            r_copy = dict(r)
            r_copy["Found In"] = " + ".join(found_in)
            filtered.append(r_copy)

    new_headers = list(headers) + ["Found In"]
    return new_headers, _dedupe(filtered)


# --------------------------------------------------
# Different Record
#   Rule: (VIT1 \ VIT2) ∪ (VIT2 \ VIT1)
# --------------------------------------------------
def get_different_records():
    _clear_error()

    errors = []
    try:
        vit1 = fetch_vit1()
    except Exception as exc:
        errors.append(f"VIT1: {exc}")
        vit1 = []

    try:
        vit2 = fetch_vit2()
    except Exception as exc:
        errors.append(f"VIT2: {exc}")
        vit2 = []

    if errors:
        _set_error(" | ".join(errors))
        return [], []

    vit1_by_name = _record_by_name(vit1)
    vit2_by_name = _record_by_name(vit2)

    only_vit1 = set(vit1_by_name) - set(vit2_by_name)
    only_vit2 = set(vit2_by_name) - set(vit1_by_name)

    result = []
    used_headers = None

    for name in only_vit1:
        r = vit1_by_name[name]
        r_copy = dict(r)
        r_copy["VIT"] = "VIT1 only"
        if used_headers is None:
            used_headers = list(r.keys())
        result.append(r_copy)

    for name in only_vit2:
        r = vit2_by_name[name]
        r_copy = dict(r)
        r_copy["VIT"] = "VIT2 only"
        if used_headers is None:
            used_headers = list(r.keys())
        result.append(r_copy)

    if used_headers is None:
        return [], []
    return used_headers + ["VIT"], _dedupe(result)


# --------------------------------------------------
# Mentor
# --------------------------------------------------
def get_all_conversations(refresh=False):
    _clear_error()
    try:
        records = fetch_mentor()
        headers, rows = _header_and_rows(records)
        rows = _dedupe(rows)
        return headers, rows
    except Exception as exc:
        _set_error(f"Could not read Mentor: {exc}")
        return [], []


def search_conversations(query):
    headers, rows = get_all_conversations()
    if not query:
        return headers, rows
    return headers, [r for r in rows if name_matches(query, _get_name(r))]


def get_conversations_by_recommendation(value):
    headers, rows = get_all_conversations()
    if not value or value == "All Recommendations":
        return headers, rows
    filtered = []
    for r in rows:
        for k in r.keys():
            if "recommend" in k.lower():
                if value.lower() in str(r[k]).lower():
                    filtered.append(r)
                    break
    return headers, _dedupe(filtered)


# --------------------------------------------------
# Interviews
# --------------------------------------------------
def get_all_interviews(refresh=False):
    _clear_error()
    try:
        records = fetch_interviews()
        headers, rows = _header_and_rows(records)
        rows = _dedupe(rows)
        return headers, rows
    except Exception as exc:
        _set_error(f"Could not read Interviews: {exc}")
        return [], []


def search_interviews(query):
    headers, rows = get_all_interviews()
    if not query:
        return headers, rows
    return headers, [r for r in rows if name_matches(query, _get_name(r))]


def get_projects_sent():
    headers, rows = get_all_interviews()
    filtered = []
    for r in rows:
        for k in r.keys():
            if "sent" in k.lower() and str(r[k]).strip():
                filtered.append(r)
                break
    return headers, _dedupe(filtered)


def get_projects_received():
    headers, rows = get_all_interviews()
    filtered = []
    for r in rows:
        for k in r.keys():
            if "received" in k.lower() and str(r[k]).strip():
                filtered.append(r)
                break
    return headers, _dedupe(filtered)