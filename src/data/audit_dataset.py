"""Audit the three MultiNLI CSV files supplied for WEX 428."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "pairID",
    "premise",
    "hypothesis",
    "genre",
    "label",
}
VALID_LABELS = {0, 1, 2}
LABEL_MAPPING = {
    0: "entailment",
    1: "neutral",
    2: "contradiction",
}


def audit_csv(path: Path, chunk_size: int = 50_000) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    header = pd.read_csv(path, nrows=0)
    missing_columns = REQUIRED_COLUMNS.difference(header.columns)
    if missing_columns:
        raise ValueError(
            f"{path.name} is missing required columns: {sorted(missing_columns)}"
        )

    row_count = 0
    label_counts: Counter[int] = Counter()
    genre_counts: Counter[str] = Counter()
    missing_counts: Counter[str] = Counter()
    seen_hashes: set[int] = set()
    duplicate_count = 0
    premise_lengths: list[int] = []
    hypothesis_lengths: list[int] = []

    usecols = ["pairID", "premise", "hypothesis", "genre", "label"]
    for chunk in pd.read_csv(path, usecols=usecols, chunksize=chunk_size):
        row_count += len(chunk)

        label_counts.update(chunk["label"].value_counts(dropna=False).to_dict())
        genre_counts.update(chunk["genre"].value_counts(dropna=False).to_dict())

        for column in usecols:
            missing_counts[column] += int(chunk[column].isna().sum())

        non_null_premises = chunk["premise"].dropna().astype(str)
        non_null_hypotheses = chunk["hypothesis"].dropna().astype(str)
        premise_lengths.extend(non_null_premises.str.split().str.len().tolist())
        hypothesis_lengths.extend(non_null_hypotheses.str.split().str.len().tolist())

        valid_for_hash = chunk.dropna(subset=["premise", "hypothesis", "label"])
        hashes = pd.util.hash_pandas_object(
            valid_for_hash[["premise", "hypothesis", "label"]],
            index=False,
        ).astype("uint64")

        for value in hashes.tolist():
            numeric_hash = int(value)
            if numeric_hash in seen_hashes:
                duplicate_count += 1
            else:
                seen_hashes.add(numeric_hash)

    actual_labels = {int(x) for x in label_counts if not pd.isna(x)}
    invalid_labels = sorted(actual_labels.difference(VALID_LABELS))

    def length_summary(values: list[int]) -> dict[str, float | int]:
        if not values:
            return {"mean": 0.0, "p95": 0.0, "max": 0}
        return {
            "mean": round(float(np.mean(values)), 4),
            "p95": round(float(np.percentile(values, 95)), 4),
            "max": int(np.max(values)),
        }

    return {
        "file": str(path),
        "rows": row_count,
        "label_counts": {
            str(int(key)): int(value)
            for key, value in sorted(label_counts.items())
            if not pd.isna(key)
        },
        "genre_counts": {
            str(key): int(value)
            for key, value in sorted(genre_counts.items())
        },
        "missing": {
            key: int(value)
            for key, value in sorted(missing_counts.items())
        },
        "invalid_labels": invalid_labels,
        "exact_triplet_duplicates": duplicate_count,
        "premise_words": length_summary(premise_lengths),
        "hypothesis_words": length_summary(hypothesis_lengths),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/raw"),
        help="Directory containing the three MultiNLI CSV files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/data_audit.json"),
        help="Output JSON report path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    filenames = {
        "train": "multinli_train.csv",
        "validation_matched": "multinli_validation_matched.csv",
        "validation_mismatched": "multinli_validation_mismatched.csv",
    }

    report = {
        "label_mapping": {
            str(key): value for key, value in LABEL_MAPPING.items()
        },
        "datasets": {
            split: audit_csv(args.data_dir / filename)
            for split, filename in filenames.items()
        },
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Audit completed: {args.output}")


if __name__ == "__main__":
    main()
