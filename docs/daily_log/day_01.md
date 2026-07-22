# Day 01 — 22 July 2026

## Work completed
- Reviewed the university project guideline and extracted the mandatory requirements.
- Confirmed that the project is an NLI-based scientific claim verification platform.
- Inspected the three supplied MultiNLI CSV files.
- Defined the numeric label mapping:
  - 0: Entailment
  - 1: Neutral
  - 2: Contradiction
- Created the initial repository structure and reproducible data audit scripts.
- Defined a cleaning policy for the training data while preserving the official validation sets.

## Findings
- Training set: 392,702 rows.
- Matched validation set: 9,815 rows.
- Mismatched validation set: 9,832 rows.
- The training data contains 40 rows with a missing hypothesis.
- The training data contains 22 exact duplicate premise-hypothesis-label combinations.
- Labels in the training set are almost perfectly balanced.

## Decisions
- Use Python and transformer-based NLI fine-tuning.
- Use FastAPI for the backend, React for the frontend, and PostgreSQL for storage.
- Do not use GPT, Gemini, Claude, or another ready-made LLM API for the core classification task.
- Preserve validation files unchanged for comparable evaluation.

## Challenges
- The full dataset is large, so preprocessing must avoid unnecessary memory usage.
- The model and training strategy depend on the available GPU and RAM.

## Next step
- Run the environment checker on the development computer.
- Select the correct PyTorch installation and train a small baseline model.
