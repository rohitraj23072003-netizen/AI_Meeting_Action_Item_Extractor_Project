import json
import os
import re
from typing import List, Dict
import requests

SYSTEM_PROMPT = """You extract meeting action items.
Return ONLY a JSON array. Each item must contain:
task, person, date, status, confidence.
Use null when a value is missing. Confidence must be between 0 and 1.
Do not invent facts. Prefer explicit assignments and deadlines."""

def _ollama_extract(transcript: str) -> List[Dict]:
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    model = os.getenv("OLLAMA_MODEL", "llama3.2")
    prompt = f"""{SYSTEM_PROMPT}

Meeting transcript:
{transcript}
"""
    response = requests.post(
        url,
        json={"model": model, "prompt": prompt, "stream": False, "format": "json"},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    raw = payload.get("response", "[]")
    data = json.loads(raw)
    if isinstance(data, dict) and "items" in data:
        data = data["items"]
    if not isinstance(data, list):
        raise ValueError("LLM did not return a JSON array")
    return data

def _fallback_extract(transcript: str) -> List[Dict]:
    # Demo-safe fallback when a local LLM is not running.
    actions = []
    patterns = [
        (r"(?P<person>[A-Z][a-z]+).*?(?:will|can|should)\s+(?P<task>[^.]+?)(?:\s+by\s+(?P<date>[^.]+))?\.", "assigned"),
        (r"(?P<person>[A-Z][a-z]+),\s+can you\s+(?P<task>[^?]+)\?", "assigned"),
    ]
    for line in transcript.splitlines():
        for pattern, status in patterns:
            m = re.search(pattern, line)
            if m:
                task = re.sub(r"\s+", " ", m.group("task")).strip()
                date = (m.groupdict().get("date") or "").strip() or None
                actions.append({
                    "task": task[0].upper() + task[1:],
                    "person": m.group("person"),
                    "date": date,
                    "status": status,
                    "confidence": 0.82
                })
                break
    return actions

def extract_actions(transcript: str) -> List[Dict]:
    try:
        return _ollama_extract(transcript)
    except Exception:
        return _fallback_extract(transcript)
