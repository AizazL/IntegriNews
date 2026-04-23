from app.services.classifier import build_analysis_summary, run_inference, score_to_signal


class FakeTokenizer:
    def texts_to_sequences(self, texts):
        assert texts == ["Headline\n\nBody copy"]
        return [[5, 4, 3]]


class FakeModel:
    def __init__(self):
        self.received = None

    def predict(self, padded, verbose=0):
        self.received = padded
        return [[0.73]]


def test_score_to_signal_maps_thresholds():
    assert score_to_signal(0.91) == ("High fake-risk signal", "Critical")
    assert score_to_signal(0.61) == ("Elevated fake-risk signal", "High")
    assert score_to_signal(0.49) == ("Mixed credibility signal", "Moderate")
    assert score_to_signal(0.24) == ("Leaning toward legitimate reporting", "Guarded")
    assert score_to_signal(0.08) == ("Strong legitimate-reporting signal", "Low")


def test_run_inference_uses_tokenizer_and_model():
    tokenizer = FakeTokenizer()
    model = FakeModel()

    probability = run_inference(tokenizer, model, "Headline\n\nBody copy", max_length=6)

    assert probability == 0.73
    assert model.received.tolist() == [[5, 4, 3, 0, 0, 0]]


def test_build_analysis_summary_includes_explanatory_metadata():
    summary = build_analysis_summary(
        "SHOCKING DEVELOPMENT",
        "This fabricated story uses dramatic language!!! and keeps the evidence very short.",
        0.88,
    )

    assert summary["label"] == "fake"
    assert summary["risk_band"] == "Critical"
    assert summary["confidence_percent"] == 88.0
    assert summary["input_stats"]["word_count"] > 0
    badge_ids = {badge["id"] for badge in summary["warning_badges"]}
    assert {"capitalization-spike", "punctuation-intensity", "sensational-language"}.issubset(badge_ids)
