"""Test the trained NLI model with a premise and hypothesis."""

from pathlib import Path

import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)


MODEL_DIRECTORY = Path(
    "models/improved_test/final_model"
)

MAX_LENGTH = 128


def load_model():
    """Load the saved tokenizer and trained model."""

    if not MODEL_DIRECTORY.exists():
        raise FileNotFoundError(
            f"Model directory was not found: {MODEL_DIRECTORY}"
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


def predict(
    premise: str,
    hypothesis: str,
    tokenizer,
    model,
    device,
):
    """Predict the NLI class and confidence scores."""

    inputs = tokenizer(
        premise,
        hypothesis,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH,
    )

    inputs = {
        name: tensor.to(device)
        for name, tensor in inputs.items()
    }

    with torch.inference_mode():
        logits = model(**inputs).logits

    probabilities = torch.softmax(
        logits,
        dim=-1,
    )[0]

    predicted_id = int(
        torch.argmax(probabilities).item()
    )

    predicted_label = model.config.id2label[
        predicted_id
    ]

    confidence_scores = {
        model.config.id2label[label_id]:
        float(probabilities[label_id].item())
        for label_id in range(len(probabilities))
    }

    return predicted_label, confidence_scores


def main() -> None:
    """Run an interactive prediction test."""

    print("=" * 60)
    print("Scientific Claim Verifier")
    print("=" * 60)

    tokenizer, model, device = load_model()

    print(f"Device: {device}")
    print("\nEnter the two English sentences.")

    premise = input("\nPremise: ").strip()

    if not premise:
        print("Premise cannot be empty.")
        return

    hypothesis = input("Hypothesis: ").strip()

    if not hypothesis:
        print("Hypothesis cannot be empty.")
        return

    predicted_label, scores = predict(
        premise,
        hypothesis,
        tokenizer,
        model,
        device,
    )

    print("\n" + "=" * 60)
    print("Prediction result")
    print("=" * 60)

    print(f"Predicted class: {predicted_label}")

    print("\nConfidence scores:")

    for label, score in scores.items():
        print(f"{label}: {score * 100:.2f}%")


if __name__ == "__main__":
    main()