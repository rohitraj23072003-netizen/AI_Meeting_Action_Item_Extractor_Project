# AI Meeting Action-Item Extractor

2. AI Meeting Action-Item Extractor

Short description: Create an AI assistant that converts meeting transcripts into structured action items containing the task, owner, deadline, and confidence.

## How to approach

1. Gather or generate meeting transcripts with annotated action items.
2. Clean and segment transcripts by speaker and sentence.
3. Use an LLM or transformer model for information extraction.
4. Design a structured output schema: task, person, date, and status.
5. Add validation rules for dates, missing owners, and duplicate tasks.
6. Evaluate extraction accuracy and build a simple upload-to-results interface.

## Project structure

- `app.py` — Streamlit upload-to-results interface.
- `src/transcript.py` — cleaning and speaker/sentence segmentation.
- `src/extractor.py` — LLM extraction using a local Ollama model, with a deterministic fallback for demo use.
- `src/validator.py` — validation for dates, missing owners, and duplicate tasks.
- `src/evaluator.py` — simple exact-match evaluation against annotated examples.
- `data/sample_transcripts.txt` — sample meeting transcript.
- `data/annotated_actions.jsonl` — annotated action-item examples.
- `requirements.txt` — Python dependencies.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

For LLM extraction, install and run Ollama separately and make a model available locally. The app reads:

```text
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3.2
```

If the local LLM is unavailable, the app uses the built-in fallback extractor so the complete upload-to-results workflow can still be demonstrated.
