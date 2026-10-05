import re
from typing import List, Dict

def clean_transcript(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()

def segment_transcript(text: str) -> List[Dict[str, str]]:
    text = clean_transcript(text)
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        match = re.match(r"^(?:\[(?P<time>[^\]]+)\]\s*)?(?P<speaker>[^:]+):\s*(?P<sentence>.+)$", line)
        if match:
            rows.append({
                "time": match.group("time") or "",
                "speaker": match.group("speaker").strip(),
                "sentence": match.group("sentence").strip(),
            })
        else:
            # Sentence-level fallback for lines without speaker labels.
            for sentence in re.split(r"(?<=[.!?])\s+", line):
                if sentence.strip():
                    rows.append({"time": "", "speaker": "Unknown", "sentence": sentence.strip()})
    return rows
