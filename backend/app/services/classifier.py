import sys
import types
import pickle
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np

from ..config import get_settings
from .heuristics import build_warning_badges, compute_input_stats


def prepare_article_input(title: str, article_text: str) -> str:
    return "\n\n".join(part.strip() for part in (title, article_text) if part and part.strip())


def run_inference(tokenizer, model, combined_text: str, max_length: int = 1000) -> float:
    sequence = tokenizer.texts_to_sequences([combined_text])
    padded = []
    for row in sequence:
        trimmed = list(row[:max_length])
        padded.append(trimmed + [0] * max(0, max_length - len(trimmed)))
    prediction = model.predict(np.array(padded, dtype="int32"), verbose=0)
    return float(prediction[0][0])


def install_legacy_keras_compat() -> type:
    import keras
    import keras.src.legacy.preprocessing.sequence as legacy_sequence
    import keras.src.legacy.preprocessing.text as legacy_text

    preprocessing_module = types.ModuleType("keras.src.preprocessing")
    preprocessing_module.sequence = legacy_sequence
    preprocessing_module.text = legacy_text

    sys.modules["keras.src.preprocessing"] = preprocessing_module
    sys.modules["keras.src.preprocessing.sequence"] = legacy_sequence
    sys.modules["keras.src.preprocessing.text"] = legacy_text

    class CompatLSTM(keras.layers.LSTM):
        def __init__(self, *args, time_major=None, **kwargs):
            super().__init__(*args, **kwargs)

    return CompatLSTM


def score_to_signal(fake_probability: float) -> tuple[str, str]:
    if fake_probability >= 0.8:
        return "High fake-risk signal", "Critical"
    if fake_probability >= 0.6:
        return "Elevated fake-risk signal", "High"
    if fake_probability >= 0.4:
        return "Mixed credibility signal", "Moderate"
    if fake_probability >= 0.2:
        return "Leaning toward legitimate reporting", "Guarded"
    return "Strong legitimate-reporting signal", "Low"


def merge_article_sources(body: str | None, uploaded_text: str | None) -> str:
    chunks = [chunk.strip() for chunk in (body or "", uploaded_text or "") if chunk and chunk.strip()]
    return "\n\n".join(chunks)


def build_analysis_summary(title: str, article_text: str, fake_probability: float) -> dict[str, object]:
    label = "fake" if fake_probability >= 0.5 else "real"
    verdict, risk_band = score_to_signal(fake_probability)
    confidence_percent = round(max(fake_probability, 1 - fake_probability) * 100, 1)
    input_stats = compute_input_stats(article_text)
    warning_badges = build_warning_badges(title, article_text)

    return {
        "label": label,
        "verdict": verdict,
        "risk_band": risk_band,
        "fake_probability": round(fake_probability, 4),
        "confidence_percent": confidence_percent,
        "input_stats": input_stats,
        "warning_badges": warning_badges,
        "advisory_note": "This result is advisory and should be combined with source verification and editorial judgment.",
    }


@dataclass
class LoadedArtifacts:
    tokenizer: object
    model: object


class NewsClassifier:
    def __init__(self, model_path: Path, tokenizer_path: Path):
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self._artifacts: LoadedArtifacts | None = None

    def _load(self) -> LoadedArtifacts:
        if self._artifacts is None:
            from tensorflow.keras.models import load_model

            compat_lstm = install_legacy_keras_compat()
            with self.tokenizer_path.open("rb") as handle:
                tokenizer = pickle.load(handle)

            model = load_model(self.model_path, compile=False, custom_objects={"LSTM": compat_lstm})
            self._artifacts = LoadedArtifacts(tokenizer=tokenizer, model=model)

        return self._artifacts

    def predict_fake_probability(self, title: str, article_text: str) -> float:
        combined_text = prepare_article_input(title, article_text)
        artifacts = self._load()
        return run_inference(artifacts.tokenizer, artifacts.model, combined_text)


@lru_cache
def get_classifier() -> NewsClassifier:
    settings = get_settings()
    return NewsClassifier(settings.model_path, settings.tokenizer_path)
