"""Services package for the Cinematic Reading Engine."""

from .story_analyzer import StoryAnalyzer
from .structural_analyzer import StoryStructureAnalyzer
from .character_analyzer import CharacterEmotionAnalyzer
from .emotion_scorer import EmotionalIntensityScorer
from .effect_selector import IntelligentEffectSelector
from .quality_controller import EffectQualityController
from .sparsity_controller import EffectSparsityController
from .theme_classifier import ThemeClassifier
from .parser import parse_epub
from .converter import generate_cinematic_markup

__all__ = [
    "StoryAnalyzer",
    "StoryStructureAnalyzer", 
    "CharacterEmotionAnalyzer",
    "EmotionalIntensityScorer",
    "IntelligentEffectSelector",
    "EffectQualityController",
    "EffectSparsityController",
    "ThemeClassifier",
    "parse_epub",
    "generate_cinematic_markup",
]
