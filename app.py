import json
from pathlib import Path
import pandas as pd
import streamlit as st

from src.transcript import clean_transcript, segment_transcript
from src.extractor import extract_actions
from src.validator import validate_actions
from src.evaluator import evaluate, load_annotations

st.set_page_config(page_title="AI Meeting Action-Item Extractor", layout="wide")
st.title("AI Meeting Action-Item Extractor")
st.caption("Convert meeting transcripts into structured action items containing the task, owner, deadline, and confidence.")

uploaded = st.file_uploader("Upload a meeting transcript", type=["txt"])
use_sample = st.checkbox("Use sample transcript", value=True)

if uploaded:
    transcript = uploaded.read().decode("utf-8", errors="ignore")
elif use_sample:
    transcript = Path("data/sample_transcripts.txt").read_text(encoding="utf-8")
else:
    transcript = ""

if transcript:
    st.subheader("Cleaned & segmented transcript")
    cleaned = clean_transcript(transcript)
    segments = segment_transcript(cleaned)
    st.dataframe(pd.DataFrame(segments), use_container_width=True, hide_index=True)

    if st.button("Extract action items", type="primary"):
        actions = extract_actions(cleaned)
        actions, issues = validate_actions(actions)

        st.subheader("Structured results")
        df = pd.DataFrame(actions, columns=["task", "person", "date", "status", "confidence"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        if issues:
            st.warning("\n".join(issues))
        else:
            st.success("Validation completed with no detected issues.")

        st.download_button(
            "Download results as JSON",
            data=json.dumps(actions, indent=2),
            file_name="action_items.json",
            mime="application/json",
        )

st.divider()
st.subheader("Evaluation")
if st.button("Evaluate against annotated examples"):
    try:
        annotations = load_annotations()
        predictions = extract_actions(Path("data/sample_transcripts.txt").read_text(encoding="utf-8"))
        predictions, _ = validate_actions(predictions)
        metrics = evaluate(predictions, annotations)
        st.json(metrics)
    except Exception as exc:
        st.error(f"Evaluation could not be completed: {exc}")
