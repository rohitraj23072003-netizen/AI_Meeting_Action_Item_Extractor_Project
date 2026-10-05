import json
from pathlib import Path
from typing import List, Dict

def load_annotations(path: str = "data/annotated_actions.jsonl") -> List[Dict]:
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def normalize(s):
    return " ".join(str(s or "").lower().split())

def evaluate(predicted: List[Dict], annotations: List[Dict]) -> Dict:
    gold = [x["action"] for x in annotations]
    matched = 0
    for g in gold:
        for p in predicted:
            if normalize(g["task"]) == normalize(p.get("task")) and normalize(g["person"]) == normalize(p.get("person")):
                matched += 1
                break
    precision = matched / max(len(predicted), 1)
    recall = matched / max(len(gold), 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-9)
    return {"matched": matched, "gold": len(gold), "predicted": len(predicted),
            "precision": precision, "recall": recall, "f1": f1}
