"""
Intelligent Story Analysis Service

This service orchestrates the complete analysis pipeline for converting
raw book content into enhanced cinematic markup with intelligent effects.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any
import logging

from .structural_analyzer import StoryStructureAnalyzer
from .character_analyzer import CharacterEmotionAnalyzer
from .emotion_scorer import EmotionalIntensityScorer
from .effect_selector import IntelligentEffectSelector
from .quality_controller import EffectQualityController
from .sparsity_controller import EffectSparsityController

logger = logging.getLogger(__name__)


class StoryAnalyzer:
    """
    Main orchestrator for intelligent story analysis and effect application.
    
    This class coordinates all analysis components to create enhanced
    cinematic markup while maintaining the core philosophy: "The book is the star."
    """
    
    def __init__(self):
        """Initialize all analysis components."""
        self.structure_analyzer = StoryStructureAnalyzer()
        self.character_analyzer = CharacterEmotionAnalyzer()
        self.emotion_scorer = EmotionalIntensityScorer()
        self.effect_selector = IntelligentEffectSelector()
        self.quality_controller = EffectQualityController()
        self.sparsity_controller = EffectSparsityController()
        
        logger.info("StoryAnalyzer initialized with all components")
    
    def analyze_and_enhance(self, parsed_book: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete analysis and enhancement pipeline.
        
        Args:
            parsed_book: Raw parsed book data from EPUB parser
            
        Returns:
            Enhanced cinematic markup with intelligent effects
        """
        try:
            logger.info(f"Starting analysis for book: {parsed_book.get('title', 'Unknown')}")
            
            # Step 1: Structural Analysis
            structure_data = self.structure_analyzer.analyze_narrative_structure(parsed_book)
            logger.debug("Structural analysis completed")
            
            # Step 2: Character Analysis
            character_profiles = self.character_analyzer.analyze_character_arcs(parsed_book)
            logger.debug(f"Character analysis completed for {len(character_profiles)} characters")
            
            # Step 3: Emotional Scoring
            enhanced_chapters = self._apply_emotional_scoring(parsed_book, structure_data, character_profiles)
            logger.debug("Emotional scoring completed")
            
            # Step 4: Effect Selection and Application
            final_markup = self._apply_intelligent_effects(enhanced_chapters, character_profiles)
            logger.debug("Effect application completed")
            
            # Step 5: Quality Control
            validated_markup = self.quality_controller.validate_all_effects(final_markup)
            logger.debug("Quality control completed")
            
            # Step 6: Sparsity Control
            final_result = self.sparsity_controller.enforce_sparsity_rules(validated_markup)
            logger.info("Analysis and enhancement pipeline completed successfully")
            
            return final_result
            
        except Exception as e:
            logger.error(f"Error in analysis pipeline: {str(e)}")
            # Fallback to basic markup without effects
            return self._create_fallback_markup(parsed_book)
    
    def _apply_emotional_scoring(self, parsed_book: Dict, structure_data: Dict, character_profiles: Dict) -> List[Dict]:
        """Apply emotional scoring to all content segments."""
        enhanced_chapters = []
        
        for chapter in parsed_book.get('chapters', []):
            enhanced_content = []
            
            for content_item in chapter.get('content', []):
                # Calculate emotional intensity
                emotional_score = self.emotion_scorer.calculate_emotional_weight(
                    content_item, structure_data, character_profiles
                )
                
                # Add emotional metadata
                enhanced_item = {
                    **content_item,
                    'emotional_score': emotional_score,
                    'emotional_context': self.emotion_scorer.get_emotional_context(content_item),
                    'character_relevance': self._get_character_relevance(content_item, character_profiles)
                }
                
                enhanced_content.append(enhanced_item)
            
            enhanced_chapters.append({
                **chapter,
                'content': enhanced_content,
                'chapter_emotional_profile': self._analyze_chapter_emotion(enhanced_content)
            })
        
        return enhanced_chapters
    
    def _apply_intelligent_effects(self, enhanced_chapters: List[Dict], character_profiles: Dict) -> Dict[str, Any]:
        """Apply intelligent effects based on analysis."""
        final_chapters = []
        effect_history = []
        
        for chapter in enhanced_chapters:
            enhanced_content = []
            
            for content_item in chapter['content']:
                # Select appropriate effects
                selected_effects = self.effect_selector.select_appropriate_effects(
                    content_item, character_profiles, effect_history
                )
                
                # Apply effects if any selected
                if selected_effects:
                    enhanced_item = {
                        **content_item,
                        'effects': selected_effects
                    }
                    effect_history.append({
                        'chapter': len(final_chapters),
                        'position': len(enhanced_content),
                        'effects': selected_effects
                    })
                else:
                    enhanced_item = {
                        **content_item,
                        'effects': []
                    }
                
                enhanced_content.append(enhanced_item)
            
            final_chapters.append({
                **chapter,
                'content': enhanced_content
            })
        
        return {
            'bookTitle': enhanced_chapters[0].get('bookTitle', 'Unknown'),
            'theme': self._determine_book_theme(enhanced_chapters),
            'chapters': final_chapters,
            'analysis_metadata': {
                'total_effects_applied': len(effect_history),
                'effect_distribution': self._analyze_effect_distribution(effect_history),
                'character_effect_usage': self._analyze_character_effect_usage(effect_history, character_profiles)
            }
        }
    
    def _get_character_relevance(self, content_item: Dict, character_profiles: Dict) -> Dict[str, float]:
        """Calculate relevance scores for each character in the content."""
        relevance_scores = {}
        
        for character, profile in character_profiles.items():
            # Simple relevance calculation - can be enhanced
            if character.lower() in content_item.get('text', '').lower():
                relevance_scores[character] = 0.8
            else:
                relevance_scores[character] = 0.1
        
        return relevance_scores
    
    def _analyze_chapter_emotion(self, content_items: List[Dict]) -> Dict[str, float]:
        """Analyze overall emotional profile of a chapter."""
        if not content_items:
            return {'average_intensity': 0.0, 'emotional_range': 0.0}
        
        scores = [item.get('emotional_score', 0.0) for item in content_items]
        
        return {
            'average_intensity': sum(scores) / len(scores),
            'emotional_range': max(scores) - min(scores) if len(scores) > 1 else 0.0,
            'peak_emotion': max(scores),
            'emotional_variance': self._calculate_variance(scores)
        }
    
    def _determine_book_theme(self, chapters: List[Dict]) -> str:
        """Determine the overall theme of the book based on content analysis."""
        # Simple theme detection - can be enhanced with NLP
        all_text = ' '.join([
            item.get('text', '') 
            for chapter in chapters 
            for item in chapter.get('content', [])
        ]).lower()
        
        theme_keywords = {
            'historical': ['king', 'queen', 'castle', 'sword', 'battle', 'ancient'],
            'romance': ['love', 'heart', 'kiss', 'romance', 'passion'],
            'adventure': ['journey', 'quest', 'adventure', 'explore', 'discover'],
            'mystery': ['secret', 'mystery', 'clue', 'investigate', 'solve'],
            'scifi': ['space', 'future', 'robot', 'technology', 'planet']
        }
        
        theme_scores = {}
        for theme, keywords in theme_keywords.items():
            score = sum(1 for keyword in keywords if keyword in all_text)
            theme_scores[theme] = score
        
        if theme_scores:
            return max(theme_scores, key=theme_scores.get)
        
        return 'general'
    
    def _analyze_effect_distribution(self, effect_history: List[Dict]) -> Dict[str, Any]:
        """Analyze how effects are distributed throughout the book."""
        if not effect_history:
            return {'total_effects': 0, 'distribution': {}}
        
        chapter_distribution = {}
        for effect in effect_history:
            chapter = effect['chapter']
            chapter_distribution[chapter] = chapter_distribution.get(chapter, 0) + 1
        
        return {
            'total_effects': len(effect_history),
            'distribution': chapter_distribution,
            'average_effects_per_chapter': len(effect_history) / max(chapter_distribution.keys()) if chapter_distribution else 0
        }
    
    def _analyze_character_effect_usage(self, effect_history: List[Dict], character_profiles: Dict) -> Dict[str, int]:
        """Analyze which characters receive the most effects."""
        character_usage = {character: 0 for character in character_profiles.keys()}
        
        for effect in effect_history:
            for effect_detail in effect.get('effects', []):
                if 'character' in effect_detail:
                    character = effect_detail['character']
                    if character in character_usage:
                        character_usage[character] += 1
        
        return character_usage
    
    def _calculate_variance(self, scores: List[float]) -> float:
        """Calculate variance of emotional scores."""
        if len(scores) < 2:
            return 0.0
        
        mean = sum(scores) / len(scores)
        squared_diff_sum = sum((score - mean) ** 2 for score in scores)
        return squared_diff_sum / (len(scores) - 1)
    
    def _create_fallback_markup(self, parsed_book: Dict) -> Dict[str, Any]:
        """Create basic markup without effects when analysis fails."""
        logger.warning("Creating fallback markup due to analysis failure")
        
        return {
            'bookTitle': parsed_book.get('title', 'Unknown'),
            'theme': 'general',
            'chapters': [
                {
                    'chapterTitle': chapter.get('title', ''),
                    'content': [
                        {
                            'type': item.get('type', 'paragraph'),
                            'text': item.get('text', ''),
                            'effects': []
                        }
                        for item in chapter.get('content', [])
                    ]
                }
                for chapter in parsed_book.get('chapters', [])
            ],
            'analysis_metadata': {
                'status': 'fallback',
                'error': 'Analysis pipeline failed, using basic markup'
            }
        }
