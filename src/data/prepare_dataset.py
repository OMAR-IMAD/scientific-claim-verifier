"""Create a minimal cleaned training CSV while preserving validation files."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


KEEP_COLUMNS = ["pairID", "premise", "hypothesis", "genre", "label"]
VALID_LABELS = {0, 1, 2}


def clean_training_file(
    input_path: Path,
    output_path: Path,
    chunk_size: int = 50_000,
) -> dict[str, int]:
    if not input_path.exists():
        raise FileNotFoundError(f"Training file not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()

    seen_hashes: set[int] = set()
    input_rows = 0
    written_rows = 0
    removed_missing = 0
    removed_invalid_labels = 0
    removed_duplicates = 0
    first_write = True

    for chunk in pd.read_csv(
        input_path,
        usecols=KEEP_COLUMNS,
        chunksize=chunk_size,
    ):
        input_rows += len(chunk)

        missing_mask = chunk[["premise", "hypothesis"]].isna().any(axis=1)
        removed_missing += int(missing_mask.sum())
        chunk = chunk.loc[~missing_mask].copy()

        valid_label_mask = chunk["label"].isin(VALID_LABELS)
        removed_invalid_labels += int((~valid_label_mask).sum())
        chunk = chunk.loc[valid_label_mask].copy()

        hashes = pd.util.hash_pandas_object(
            chunk[["premise", "hypothesis", "label"]],
            index=False,
        ).astype("uint64")

        keep_mask: list[bool] = []
        for value in hashes.tolist():
            numeric_hash = int(value)
            if numeric_hash in seen_hashes:
                keep_mask.append(False)
                removed_duplicates += 1
            else:
                seen_hashes.add(numeric_hash)
                keep_mask.append(True)

        chunk = chunk.loc[keep_mask]
        written_rows += len(chunk)

        chunk.to_csv(
            output_path,
            mode="w" if first_write else "a",
            header=first_write,
            index=False,
            encoding="utf-8",
        )
        first_write = False

    return {
        "input_rows": input_rows,
        "written_rows": written_rows,
        "removed_missing": removed_missing,
        "removed_invalid_labels": removed_invalid_labels,
        "removed_duplicates": removed_duplicates,
    }


def validate_official_split(path: Path) -> dict[str, int]:
    if not path.exists():
        raise FileNotFoundError(f"Validation file not found: {path}")

    frame = pd.read_csv(path, usecols=KEEP_COLUMNS)
    missing_required = int(
        frame[["premise", "hypothesis", "label"]].isna().any(axis=1).sum()
    )
    invalid_labels = int((~frame["label"].isin(VALID_LABELS)).sum())

    if missing_required or invalid_labels:
        raise ValueError(
            f"{path.name} failed validation: "
            f"missing={missing_required}, invalid_labels={invalid_labels}"
        )

    return {
        "rows": len(frame),
        "missing_required": missing_required,
        "invalid_labels": invalid_labels,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/raw"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    train_summary = clean_training_file(
        args.data_dir / "multinli_train.csv",
        args.output_dir / "multinli_train_clean.csv",
    )
    matched_summary = validate_official_split(
        args.data_dir / "multinli_validation_matched.csv"
    )
    mismatched_summary = validate_official_split(
        args.data_dir / "multinli_validation_mismatched.csv"
    )

    print("Training cleaning:", train_summary)
    print("Matched validation:", matched_summary)
    print("Mismatched validation:", mismatched_summary)


if __name__ == "__main__":
    main()
