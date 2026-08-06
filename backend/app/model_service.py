"""Load the trained NLI model and provide prediction services."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_DIRECTORY = (
    PROJECT_ROOT
    / "models"
    / "improved_test"
    / "final_model"
)

MAX_LENGTH = 128


class NLIModelService:
    """Manage the trained NLI model and its predictions."""

    def __init__(self) -> None:
        """Load the tokenizer and model into memory."""

        if not MODEL_DIRECTORY.exists():
            raise FileNotFoundError(
                f"Model directory was not found: "
                f"{MODEL_DIRECTORY}"
            )

        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            str(MODEL_DIRECTORY)
        )

        self.model = (
            AutoModelForSequenceClassification
            .from_pretrained(
                str(MODEL_DIRECTORY)
            )
        )

        self.model.to(self.device)
        self.model.eval()
    def is_ready(self) -> bool:
        """Return whether the tokenizer and model are ready."""

        return (
            hasattr(self, "tokenizer")
            and self.tokenizer is not None
            and hasattr(self, "model")
            and self.model is not None
        )

    def predict(
        self,
        premise: str,
        hypothesis: str,
    ) -> dict[str, Any]:
        """Predict the relationship between two sentences."""

        inputs = self.tokenizer(
            premise,
            hypothesis,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=MAX_LENGTH,
        )

        inputs = {
            name: tensor.to(self.device)
            for name, tensor in inputs.items()
        }

        with torch.inference_mode():
            logits = self.model(**inputs).logits

        probabilities = torch.softmax(
            logits,
            dim=-1,
        )[0]

        predicted_id = int(
            torch.argmax(probabilities).item()
        )

        predicted_label = (
            self.model.config.id2label[
                predicted_id
            ]
        )

        scores = {
            self.model.config.id2label[label_id]:
            round(
                float(
                    probabilities[label_id].item()
                ),
                6,
            )
            for label_id in range(
                len(probabilities)
            )
        }

        confidence = scores[predicted_label]

        return {
            "prediction": predicted_label,
            "confidence": confidence,
            "scores": scores,
            "device": str(self.device),
        }


_model_service: NLIModelService | None = None


def get_model_service() -> NLIModelService:
    """Return one shared model service instance."""

    global _model_service

    if _model_service is None:
        _model_service = NLIModelService()

    return _model_service