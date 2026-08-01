"""Evaluate the improved NLI model on both official validation datasets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import torch
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)


MODEL_DIRECTORY = Path(
    "models/improved_test/final_model"
)

MATCHED_FILE = Path(
    "data/raw/multinli_validation_matched.csv"
)

MISMATCHED_FILE = Path(
    "data/raw/multinli_validation_mismatched.csv"
)

JSON_REPORT_FILE = Path(
    "reports/full_evaluation_results.json"
)

TEXT_REPORT_FILE = Path(
    "reports/full_evaluation_summary.txt"
)

BATCH_SIZE = 32
MAX_LENGTH = 128

LABEL_IDS = [0, 1, 2]

LABEL_NAMES = [
    "ENTAILMENT",
    "NEUTRAL",
    "CONTRADICTION",
]


def make_json_safe(value: Any) -> Any:
    """Convert values into JSON-compatible Python types."""

    if isinstance(value, dict):
        return {
            str(key): make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            make_json_safe(item)
            for item in value
        ]

    if hasattr(value, "item"):
        return value.item()

    return value


def load_model():
    """Load the improved tokenizer and classification model."""

    if not MODEL_DIRECTORY.exists():
        raise FileNotFoundError(
            f"Model directory was not found: "
            f"{MODEL_DIRECTORY}"
        )

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    tokenizer = AutoTokenizer.from_pretrained(
        str(MODEL_DIRECTORY)
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        str(MODEL_DIRECTORY)
    )

    model.to(device)
    model.eval()

    return tokenizer, model, device


def read_validation_file(file_path: Path) -> pd.DataFrame:
    """Read and validate an official validation CSV file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Validation file was not found: {file_path}"
        )

    required_columns = [
        "premise",
        "hypothesis",
        "genre",
        "label",
    ]

    dataframe = pd.read_csv(
        file_path,
        usecols=required_columns,
    )

    missing_rows = dataframe[
        ["premise", "hypothesis", "label"]
    ].isna().any(axis=1)

    if missing_rows.any():
        raise ValueError(
            f"{file_path.name} contains missing required values."
        )

    invalid_labels = ~dataframe["label"].isin(LABEL_IDS)

    if invalid_labels.any():
        raise ValueError(
            f"{file_path.name} contains invalid labels."
        )

    return dataframe


def predict_dataframe(
    dataframe: pd.DataFrame,
    tokenizer,
    model,
    device,
) -> list[int]:
    """Generate predictions for all rows in a dataframe."""

    predictions: list[int] = []

    total_rows = len(dataframe)

    total_batches = (
        total_rows + BATCH_SIZE - 1
    ) // BATCH_SIZE

    for batch_number, start_index in enumerate(
        range(0, total_rows, BATCH_SIZE),
        start=1,
    ):
        end_index = min(
            start_index + BATCH_SIZE,
            total_rows,
        )

        batch = dataframe.iloc[
            start_index:end_index
        ]

        inputs = tokenizer(
            batch["premise"].astype(str).tolist(),
            batch["hypothesis"].astype(str).tolist(),
            padding=True,
            truncation=True,
            max_length=MAX_LENGTH,
            return_tensors="pt",
        )

        inputs = {
            name: tensor.to(device)
            for name, tensor in inputs.items()
        }

        with torch.inference_mode():
            if device.type == "cuda":
                with torch.autocast(
                    device_type="cuda",
                    dtype=torch.float16,
                ):
                    logits = model(**inputs).logits
            else:
                logits = model(**inputs).logits

        batch_predictions = (
            torch.argmax(logits, dim=-1)
            .cpu()
            .tolist()
        )

        predictions.extend(batch_predictions)

        if (
            batch_number % 25 == 0
            or batch_number == total_batches
        ):
            print(
                f"Processed batch "
                f"{batch_number}/{total_batches}"
            )

    return predictions


def calculate_basic_metrics(
    correct_labels: list[int],
    predicted_labels: list[int],
) -> dict[str, Any]:
    """Calculate accuracy, macro metrics and confusion matrix."""

    precision, recall, f1_score, _ = (
        precision_recall_fscore_support(
            correct_labels,
            predicted_labels,
            labels=LABEL_IDS,
            average="macro",
            zero_division=0,
        )
    )

    class_report = classification_report(
        correct_labels,
        predicted_labels,
        labels=LABEL_IDS,
        target_names=LABEL_NAMES,
        output_dict=True,
        zero_division=0,
    )

    matrix = confusion_matrix(
        correct_labels,
        predicted_labels,
        labels=LABEL_IDS,
    )

    return {
        "accuracy": float(
            accuracy_score(
                correct_labels,
                predicted_labels,
            )
        ),
        "precision_macro": float(precision),
        "recall_macro": float(recall),
        "f1_macro": float(f1_score),
        "classification_report": class_report,
        "confusion_matrix": matrix.tolist(),
    }


def calculate_genre_metrics(
    dataframe: pd.DataFrame,
    predicted_labels: list[int],
) -> dict[str, Any]:
    """Calculate accuracy and macro F1 for each genre."""

    dataframe = dataframe.copy()

    dataframe["prediction"] = predicted_labels

    genre_results: dict[str, Any] = {}

    for genre in sorted(
        dataframe["genre"].astype(str).unique()
    ):
        genre_rows = dataframe[
            dataframe["genre"].astype(str) == genre
        ]

        correct_labels = (
            genre_rows["label"]
            .astype(int)
            .tolist()
        )

        genre_predictions = (
            genre_rows["prediction"]
            .astype(int)
            .tolist()
        )

        _, _, f1_score, _ = (
            precision_recall_fscore_support(
                correct_labels,
                genre_predictions,
                labels=LABEL_IDS,
                average="macro",
                zero_division=0,
            )
        )

        genre_results[genre] = {
            "rows": int(len(genre_rows)),
            "accuracy": float(
                accuracy_score(
                    correct_labels,
                    genre_predictions,
                )
            ),
            "f1_macro": float(f1_score),
        }

    return genre_results


def evaluate_split(
    split_name: str,
    file_path: Path,
    tokenizer,
    model,
    device,
) -> dict[str, Any]:
    """Evaluate one complete validation dataset."""

    print("\n" + "=" * 70)
    print(f"Evaluating: {split_name}")
    print("=" * 70)

    dataframe = read_validation_file(
        file_path
    )

    print(f"Rows: {len(dataframe)}")
    print(f"File: {file_path}")

    predicted_labels = predict_dataframe(
        dataframe,
        tokenizer,
        model,
        device,
    )

    correct_labels = (
        dataframe["label"]
        .astype(int)
        .tolist()
    )

    metrics = calculate_basic_metrics(
        correct_labels,
        predicted_labels,
    )

    metrics["rows"] = int(len(dataframe))

    metrics["genre_metrics"] = (
        calculate_genre_metrics(
            dataframe,
            predicted_labels,
        )
    )

    print(
        f"Accuracy: "
        f"{metrics['accuracy'] * 100:.2f}%"
    )

    print(
        f"Macro F1: "
        f"{metrics['f1_macro'] * 100:.2f}%"
    )

    evaluation_rows = dataframe.copy()
    evaluation_rows["prediction"] = predicted_labels
    evaluation_rows["label_name"] = [
        LABEL_NAMES[label]
        for label in correct_labels
    ]
    evaluation_rows["prediction_name"] = [
        LABEL_NAMES[label]
        for label in predicted_labels
    ]

    misclassified_rows = evaluation_rows[
        evaluation_rows["label"]
        != evaluation_rows["prediction"]
    ].copy()

    error_directory = Path("reports/error_analysis")
    error_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    safe_split_name = split_name.lower().replace(
        " ",
        "_",
    )

    error_file = (
        error_directory
        / f"{safe_split_name}_misclassified.csv"
    )

    error_columns = [
        "premise",
        "hypothesis",
        "genre",
        "label",
        "label_name",
        "prediction",
        "prediction_name",
    ]

    misclassified_rows[error_columns].to_csv(
        error_file,
        index=False,
        encoding="utf-8",
    )

    metrics["misclassified_rows"] = int(
        len(misclassified_rows)
    )
    metrics["error_file"] = str(error_file)

    print(
        "Misclassified rows: "
        f"{len(misclassified_rows)}"
    )
    print(f"Error file: {error_file}")

    return metrics

def create_text_summary(
    results: dict[str, Any],
) -> str:
    """Create a readable evaluation summary."""

    lines = [
        "Scientific Claim Verifier",
        "Full Official Validation Evaluation",
        "=" * 60,
        "",
    ]

    for split_name, metrics in results.items():
        lines.extend(
            [
                split_name,
                "-" * 60,
                f"Rows: {metrics['rows']}",
                (
                    "Accuracy: "
                    f"{metrics['accuracy'] * 100:.2f}%"
                ),
                (
                    "Macro Precision: "
                    f"{metrics['precision_macro'] * 100:.2f}%"
                ),
                (
                    "Macro Recall: "
                    f"{metrics['recall_macro'] * 100:.2f}%"
                ),
                (
                    "Macro F1: "
                    f"{metrics['f1_macro'] * 100:.2f}%"
                ),
                "",
                "Confusion Matrix:",
            ]
        )

        for row in metrics["confusion_matrix"]:
            lines.append(str(row))

        lines.append("")
        lines.append("Genre Results:")

        for genre, genre_metrics in (
            metrics["genre_metrics"].items()
        ):
            lines.append(
                f"- {genre}: "
                f"rows={genre_metrics['rows']}, "
                f"accuracy="
                f"{genre_metrics['accuracy'] * 100:.2f}%, "
                f"f1="
                f"{genre_metrics['f1_macro'] * 100:.2f}%"
            )

        lines.extend(["", "=" * 60, ""])

    return "\n".join(lines)


def main() -> None:
    """Run full evaluation on both official validation sets."""

    print("=" * 70)
    print("Scientific Claim Verifier")
    print("Full Validation Evaluation")
    print("=" * 70)

    tokenizer, model, device = load_model()

    print(f"Device: {device}")
    print(f"Model directory: {MODEL_DIRECTORY}")

    results = {
        "validation_matched": evaluate_split(
            "Validation Matched",
            MATCHED_FILE,
            tokenizer,
            model,
            device,
        ),
        "validation_mismatched": evaluate_split(
            "Validation Mismatched",
            MISMATCHED_FILE,
            tokenizer,
            model,
            device,
        ),
    }

    safe_results = make_json_safe(results)

    JSON_REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    JSON_REPORT_FILE.write_text(
        json.dumps(
            safe_results,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    text_summary = create_text_summary(
        safe_results
    )

    TEXT_REPORT_FILE.write_text(
        text_summary,
        encoding="utf-8",
    )

    print("\n" + "=" * 70)
    print("Full evaluation completed successfully.")
    print("=" * 70)

    print(
        f"JSON report saved in: "
        f"{JSON_REPORT_FILE}"
    )

    print(
        f"Text report saved in: "
        f"{TEXT_REPORT_FILE}"
    )


if __name__ == "__main__":
    main()