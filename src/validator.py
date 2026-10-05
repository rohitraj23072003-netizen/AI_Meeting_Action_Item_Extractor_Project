import re
from typing import List, Dict, Tuple

def validate_actions(actions: List[Dict]) -> Tuple[List[Dict], List[str]]:
    issues = []
    seen = set()
    cleaned = []

    for i, item in enumerate(actions, start=1):
        task = str(item.get("task") or "").strip()
        person = item.get("person")
        date = item.get("date")
        status = str(item.get("status") or "unknown").strip().lower()
        confidence = item.get("confidence")

        if not task:
            issues.append(f"Item {i}: missing task.")
            continue

        if not person:
            issues.append(f"Item {i}: missing owner/person.")

        if date and not isinstance(date, str):
            issues.append(f"Item {i}: invalid date format.")

        normalized = re.sub(r"\W+", " ", task.lower()).strip()
        if normalized in seen:
            issues.append(f"Item {i}: duplicate task detected.")
            continue
        seen.add(normalized)

        try:
            confidence = float(confidence)
        except (TypeError, ValueError):
            confidence = 0.0

        confidence = max(0.0, min(1.0, confidence))
        cleaned.append({
            "task": task,
            "person": person,
            "date": date,
            "status": status,
            "confidence": confidence
        })

    return cleaned, issues
