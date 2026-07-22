"""Train a small NLI baseline model to test the complete training pipeline."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
)
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
    set_seed,
)


# ---------------------------------------------------------
# Project settings
# ---------------------------------------------------------

MODEL_NAME = "distilbert-base-uncased"

TRAIN_FILE = Path("data/processed/multinli_train_clean.csv")
VALIDATION_FILE = Path(
    "data/raw/multinli_validation_matched.csv"
)

RUN_DIRECTORY = Path("models/baseline_test")
FINAL_MODEL_DIRECTORY = RUN_DIRECTORY / "final_model"
CHECKPOINT_DIRECTORY = RUN_DIRECTORY / "checkpoints"
METRICS_FILE = Path("reports/baseline_test_metrics.json")

TRAIN_SAMPLE_SIZE = 3000
VALIDATION_SAMPLE_SIZE = 600
MAX_LENGTH = 128
SEED = 42

ID_TO_LABEL = {
    0: "ENTAILMENT",
    1: "NEUTRAL",
    2: "CONTRADICTION",
}

LABEL_TO_ID = {
    label_name: label_id
    for label_id, label_name in ID_TO_LABEL.items()
}


# ---------------------------------------------------------
# Data preparation
# ---------------------------------------------------------

def balanced_sample(
    dataframe: pd.DataFrame,
    total_size: int,
    seed: int,
) -> pd.DataFrame:
    """Select the same number of examples from each label."""

    labels = sorted(dataframe["label"].unique())
    samples_per_label = total_size // len(labels)
    sampled_parts = []

    for label in labels:
        label_rows = dataframe[dataframe["label"] == label]

        sample_size = min(samples_per_label, len(label_rows))

        sampled_part = label_rows.sample(
            n=sample_size,
            random_state=seed + int(label),
        )

        sampled_parts.append(sampled_part)

    sampled_data = pd.concat(
        sampled_parts,
        ignore_index=True,
    )

    return sampled_data.sample(
        frac=1,
        random_state=seed,
    ).reset_index(drop=True)


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read and sample the training and validation files."""

    if not TRAIN_FILE.exists():
        raise FileNotFoundError(
            f"Training file was not found: {TRAIN_FILE}"
        )

    if not VALIDATION_FILE.exists():
        raise FileNotFoundError(
            f"Validation file was not found: {VALIDATION_FILE}"
        )

    required_columns = [
        "premise",
        "hypothesis",
        "label",
    ]

    train_frame = pd.read_csv(
        TRAIN_FILE,
        usecols=required_columns,
    )

    validation_frame = pd.read_csv(
        VALIDATION_FILE,
        usecols=required_columns,
    )

    train_frame = balanced_sample(
        train_frame,
        TRAIN_SAMPLE_SIZE,
        SEED,
    )

    validation_frame = balanced_sample(
        validation_frame,
        VALIDATION_SAMPLE_SIZE,
        SEED,
    )

    return train_frame, validation_frame


# ---------------------------------------------------------
# Evaluation metrics
# ---------------------------------------------------------

def compute_metrics(evaluation_prediction) -> dict[str, float]:
    """Calculate model evaluation measurements."""

    logits, correct_labels = evaluation_prediction
    predicted_labels = np.argmax(logits, axis=-1)

    accuracy = accuracy_score(
        correct_labels,
        predicted_labels,
    )

    precision, recall, f1_score, _ = (
        precision_recall_fscore_support(
            correct_labels,
            predicted_labels,
            average="macro",
            zero_division=0,
        )
    )

    return {
        "accuracy": float(accuracy),
        "precision_macro": float(precision),
        "recall_macro": float(recall),
        "f1_macro": float(f1_score),
    }


# ---------------------------------------------------------
# Main training process
# ---------------------------------------------------------

def main() -> None:
    """Run the baseline training experiment."""

    set_seed(SEED)

    print("=" * 60)
    print("Scientific Claim Verifier - Baseline Training")
    print("=" * 60)

    device_name = (
        torch.cuda.get_device_name(0)
        if torch.cuda.is_available()
        else "CPU"
    )

    print(f"Training device: {device_name}")
    print(f"Model: {MODEL_NAME}")

    print("\nLoading CSV files...")

    train_frame, validation_frame = load_data()

    print(f"Training examples: {len(train_frame)}")
    print(f"Validation examples: {len(validation_frame)}")

    train_dataset = Dataset.from_pandas(
        train_frame,
        preserve_index=False,
    )

    validation_dataset = Dataset.from_pandas(
        validation_frame,
        preserve_index=False,
    )

    print("\nDownloading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
    )

    def tokenize_batch(batch):
        encoded_inputs = tokenizer(
            batch["premise"],
            batch["hypothesis"],
            truncation=True,
            max_length=MAX_LENGTH,
        )

        encoded_inputs["labels"] = batch["label"]

        return encoded_inputs

    print("Tokenizing training data...")

    tokenized_train = train_dataset.map(
        tokenize_batch,
        batched=True,
        remove_columns=train_dataset.column_names,
    )

    print("Tokenizing validation data...")

    tokenized_validation = validation_dataset.map(
        tokenize_batch,
        batched=True,
        remove_columns=validation_dataset.column_names,
    )

    print("\nDownloading pretrained model...")

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=3,
        id2label=ID_TO_LABEL,
        label2id=LABEL_TO_ID,
    )

    data_collator = DataCollatorWithPadding(
        tokenizer=tokenizer,
    )

    CHECKPOINT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    training_arguments = TrainingArguments(
        output_dir=str(CHECKPOINT_DIRECTORY),
        num_train_epochs=1,
        learning_rate=5e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        gradient_accumulation_steps=2,
        weight_decay=0.01,
        warmup_ratio=0.1,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=25,
        load_best_model_at_end=True,
        metric_for_best_model="eval_f1_macro",
        greater_is_better=True,
        save_total_limit=1,
        fp16=torch.cuda.is_available(),
        report_to="none",
        seed=SEED,
        data_seed=SEED,
    )

    trainer = Trainer(
        model=model,
        args=training_arguments,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_validation,
        processing_class=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    print("\nStarting baseline training...")

    trainer.train()

    print("\nEvaluating the trained model...")

    evaluation_results = trainer.evaluate()

    FINAL_MODEL_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    trainer.save_model(
        str(FINAL_MODEL_DIRECTORY)
    )

    tokenizer.save_pretrained(
        str(FINAL_MODEL_DIRECTORY)
    )

    METRICS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    serializable_results = {
        key: float(value)
        if isinstance(value, (np.floating, np.integer))
        else value
        for key, value in evaluation_results.items()
    }

    METRICS_FILE.write_text(
        json.dumps(
            serializable_results,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\nTraining completed successfully.")

    print(
        f"Final model saved in: "
        f"{FINAL_MODEL_DIRECTORY}"
    )

    print(
        f"Evaluation report saved in: "
        f"{METRICS_FILE}"
    )

    print("\nEvaluation results:")

    for metric_name, metric_value in serializable_results.items():
        print(f"{metric_name}: {metric_value}")


if __name__ == "__main__":
    main()