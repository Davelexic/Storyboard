import pytest

from backend.app.services.story_analyzer import StoryAnalyzer


def test_effect_distribution_average_multiple_chapters():
    analyzer = StoryAnalyzer()
    effect_history = [
        {"chapter": 0, "position": 0, "effects": ["rain"]},
        {"chapter": 1, "position": 1, "effects": ["wind"]},
        {"chapter": 1, "position": 2, "effects": ["light"]},
    ]

    stats = analyzer._analyze_effect_distribution(effect_history)
    assert stats["distribution"] == {0: 1, 1: 2}
    assert stats["average_effects_per_chapter"] == pytest.approx(1.5)
