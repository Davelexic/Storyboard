import pytest

from backend.app.services.utils import contains_dialogue
from backend.app.services.structural_analyzer import StoryStructureAnalyzer
from backend.app.services.emotion_scorer import EmotionalIntensityScorer


def test_contains_dialogue_detects_double_quotes():
    assert contains_dialogue('He said, "Hello."')


def test_contains_dialogue_detects_single_quotes():
    assert contains_dialogue("He said, 'Hello.'")


def test_contains_dialogue_false_when_no_quotes():
    assert not contains_dialogue('No dialogue here')


def test_structural_analyzer_dialogue_density_with_both_quote_styles():
    analyzer = StoryStructureAnalyzer()
    content = [
        {'text': 'He said, "Hello."'},
        {"text": "She replied, 'Hi.'"},
        {'text': 'No dialogue.'},
    ]
    assert analyzer._calculate_dialogue_density(content) == pytest.approx(2 / 3)


def test_emotion_scorer_detects_dialogue_with_quote_styles():
    scorer = EmotionalIntensityScorer()
    assert scorer._analyze_dialogue_emotion('He shouted, "I am angry!"') > 0.0
    assert scorer._analyze_dialogue_emotion("She whispered, 'I am sad.'") > 0.0
    assert scorer._analyze_dialogue_emotion('No dialogue here.') == 0.1

