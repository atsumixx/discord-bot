import json
import os
import re
import uuid

EARNINGS_FILE = "earnings.json"

# ----------------- COMMISSION SPLIT -----------------
# 20% total is deducted off the top. Of that 20%, you (Atsumi) keep 15
# percentage points and Xylo gets 5 percentage points. The pilot keeps
# the remaining 80%.
PILOT_SHARE = 0.80
ATSUMI_SHARE = 0.15
XYLO_SHARE = 0.05


def _load():
    if not os.path.exists(EARNINGS_FILE):
        return []
    try:
        with open(EARNINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _save(records):
    with open(EARNINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def extract_total_from_summary(summary_text: str) -> float:
    """Pulls the dollar amount out of a line like '💰 **Estimated Total:** `$42.50`'"""
    match = re.search(r"Estimated Total:\*?\*?\s*`?\$([\d.]+)", summary_text)
    return float(match.group(1)) if match else 0.0


def extract_pilot_from_job_message(job_message) -> str:
    """Pulls the pilot mention/name out of a line like '✈️ **Pilot:** <@123>'"""
    if not job_message:
        return "Unassigned"
    match = re.search(r"Pilot:\*\*\s*(.+)", job_message.content)
    if match:
        pilot_str = match.group(1).strip()
        return pilot_str if pilot_str and pilot_str != "Unassigned" else "Unassigned"
    return "Unassigned"


def record_commission(client_name: str, pilot_name: str, total_price: float):
    records = _load()
    entry = {
        "id": uuid.uuid4().hex[:8],
        "client": client_name,
        "pilot": pilot_name,
        "total": round(total_price, 2),
        "pilot_cut": round(total_price * PILOT_SHARE, 2),
        "atsumi_cut": round(total_price * ATSUMI_SHARE, 2),
        "xylo_cut": round(total_price * XYLO_SHARE, 2),
    }
    records.append(entry)
    _save(records)
    return entry


def add_manual_entry(client_name: str, pilot_name: str, total_price: float):
    return record_commission(client_name, pilot_name, total_price)


def get_all():
    return _load()


def get_summary():
    records = _load()
    pilot_totals = {}
    for r in records:
        pilot_totals[r["pilot"]] = pilot_totals.get(r["pilot"], 0.0) + r["pilot_cut"]
    return {
        "count": len(records),
        "total_revenue": round(sum(r["total"] for r in records), 2),
        "atsumi_total": round(sum(r["atsumi_cut"] for r in records), 2),
        "xylo_total": round(sum(r["xylo_cut"] for r in records), 2),
        "pilot_totals": {k: round(v, 2) for k, v in pilot_totals.items()},
    }


def edit_entry(entry_id: str, total=None, pilot=None, client=None):
    records = _load()
    for r in records:
        if r["id"] == entry_id:
            if total is not None:
                r["total"] = round(total, 2)
                r["pilot_cut"] = round(total * PILOT_SHARE, 2)
                r["atsumi_cut"] = round(total * ATSUMI_SHARE, 2)
                r["xylo_cut"] = round(total * XYLO_SHARE, 2)
            if pilot:
                r["pilot"] = pilot
            if client:
                r["client"] = client
            _save(records)
            return r
    return None


def delete_entry(entry_id: str) -> bool:
    records = _load()
    new_records = [r for r in records if r["id"] != entry_id]
    if len(new_records) == len(records):
        return False
    _save(new_records)
    return True
