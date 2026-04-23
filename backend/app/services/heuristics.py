import re
from math import ceil


SENSATIONAL_PHRASES = {
    "shocking",
    "bombshell",
    "you won't believe",
    "unbelievable",
    "breaking",
    "exclusive",
    "exposed",
    "secret",
    "viral",
    "miracle",
}


def compute_input_stats(text: str) -> dict[str, int]:
    normalized = text.strip()
    words = [word for word in re.split(r"\s+", normalized) if word]
    word_count = len(words)
    character_count = len(normalized)
    reading_time_minutes = max(1, ceil(word_count / 220)) if word_count else 0
    return {
        "word_count": word_count,
        "character_count": character_count,
        "reading_time_minutes": reading_time_minutes,
    }


def build_warning_badges(title: str, text: str) -> list[dict[str, str]]:
    combined = f"{title} {text}".strip()
    if not combined:
        return []

    badges: list[dict[str, str]] = []
    uppercase_letters = sum(1 for char in combined if char.isupper())
    alpha_letters = sum(1 for char in combined if char.isalpha())
    uppercase_ratio = uppercase_letters / alpha_letters if alpha_letters else 0

    if uppercase_letters >= 12 and uppercase_ratio >= 0.18:
        badges.append(
            {
                "id": "capitalization-spike",
                "label": "Capitalization spike",
                "description": "Heavy capitalization can signal emotionally charged or manipulative framing.",
                "severity": "medium",
            }
        )

    punctuation_hits = len(re.findall(r"[!?]{2,}", combined))
    if punctuation_hits or combined.count("!") >= 4:
        badges.append(
            {
                "id": "punctuation-intensity",
                "label": "Punctuation intensity",
                "description": "Repeated punctuation often appears in sensationalized headlines and copy.",
                "severity": "low",
            }
        )

    lowered = combined.lower()
    triggered_terms = [term for term in SENSATIONAL_PHRASES if term in lowered]
    if triggered_terms:
        badges.append(
            {
                "id": "sensational-language",
                "label": "Sensational phrasing",
                "description": f"Detected high-arousal language such as {', '.join(sorted(triggered_terms)[:3])}.",
                "severity": "high",
            }
        )

    if len(text.split()) < 80:
        badges.append(
            {
                "id": "limited-context",
                "label": "Limited context",
                "description": "Short submissions provide less evidence for reliable classification.",
                "severity": "low",
            }
        )

    return badges
