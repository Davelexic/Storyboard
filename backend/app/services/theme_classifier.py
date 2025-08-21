from __future__ import annotations
from typing import Dict, Tuple
import re
import math
from collections import Counter

class ThemeClassifier:
    """Lightweight theme classifier using simple embeddings.

    This stub classifier mimics a fine-tuned transformer by producing
    token-frequency embeddings and applying learned weights to predict a
    theme label. It is intentionally simple to keep the example
    self-contained without external ML dependencies.
    """

    def __init__(self) -> None:
        # Pre-computed weights for themes; in a real system these would be
        # learned parameters from a training process.
        self.label_word_weights: Dict[str, Dict[str, float]] = {
            'historical': {
                'king': 1.5,
                'queen': 1.2,
                'castle': 1.0,
                'sword': 1.0,
                'battle': 1.0,
                'ancient': 1.0,
            },
            'romance': {
                'love': 1.5,
                'heart': 1.2,
                'kiss': 1.0,
                'romance': 1.0,
                'passion': 1.0,
            },
            'adventure': {
                'journey': 1.2,
                'quest': 1.2,
                'adventure': 1.0,
                'explore': 1.0,
                'discover': 1.0,
            },
            'mystery': {
                'secret': 1.2,
                'mystery': 1.0,
                'clue': 1.2,
                'investigate': 1.0,
                'solve': 1.0,
            },
            'scifi': {
                'space': 1.2,
                'future': 1.0,
                'robot': 1.0,
                'technology': 1.0,
                'planet': 1.0,
            },
        }

    def encode(self, text: str) -> Dict[str, float]:
        """Create a token frequency embedding from text."""
        tokens = re.findall(r"\w+", text.lower())
        return Counter(tokens)

    def predict(self, embedding: Dict[str, float]) -> Tuple[str, float]:
        """Predict a theme label and probability from an embedding."""
        scores: Dict[str, float] = {}
        for label, weights in self.label_word_weights.items():
            score = sum(embedding.get(tok, 0.0) * weight for tok, weight in weights.items())
            scores[label] = score
        if not scores:
            return "general", 0.0

        max_score = max(scores.values())
        exp_scores = {label: math.exp(score - max_score) for label, score in scores.items()}
        total = sum(exp_scores.values())
        probabilities = {label: val / total for label, val in exp_scores.items()}
        best_label = max(probabilities, key=probabilities.get)
        return best_label, probabilities[best_label]
