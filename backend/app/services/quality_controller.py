"""
Effect Quality Controller

Validates effects and ensures they meet quality standards before being applied.
Maintains the "book is the star" philosophy by preventing overuse and inappropriate effects.
"""

from __future__ import annotations
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class EffectQualityController:
    """
    Controls the quality of effects to ensure they enhance rather than distract.
    
    Features:
    - Effect validation and filtering
    - Quality scoring and ranking
    - Inappropriate effect detection
    - Character consistency checking
    """
    
    def __init__(self):
        """Initialize the quality controller."""
        self.quality_thresholds = {
            'minimum_emotional_score': 0.5,
            'maximum_effects_per_segment': 3,
            'minimum_effect_spacing': 5,  # segments between effects
            'character_consistency_threshold': 0.7
        }
        
        self.inappropriate_combinations = [
            # Effects that shouldn't be used together
            ('fiery_sharp', 'calm_gentle'),
            ('swords_clash', 'gentle_wind'),
            ('burn', 'glow'),
            ('passionate_flame', 'mysterious_shadow')
        ]
        
        self.context_violations = {
            'romance': ['swords_clash', 'burn', 'fiery_sharp'],
            'peace': ['swords_clash', 'burn', 'heartbeat'],
            'reflection': ['swords_clash', 'burn', 'passionate_flame'],
            'dialogue': ['swords_clash']  # Sound effects in dialogue
        }
    
    def validate_all_effects(self, enhanced_markup: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate all effects in the enhanced markup.
        
        Args:
            enhanced_markup: The enhanced markup with effects
            
        Returns:
            Validated markup with quality-controlled effects
        """
        try:
            logger.info("Starting effect quality validation")
            
            validated_chapters = []
            total_effects_removed = 0
            
            for chapter in enhanced_markup.get('chapters', []):
                validated_content = []
                
                for content_item in chapter.get('content', []):
                    # Validate effects for this content item
                    validated_effects = self._validate_content_effects(content_item)
                    
                    # Count removed effects
                    original_effects = len(content_item.get('effects', []))
                    removed_effects = original_effects - len(validated_effects)
                    total_effects_removed += removed_effects
                    
                    # Create validated content item
                    validated_item = {
                        **content_item,
                        'effects': validated_effects,
                        'quality_score': self._calculate_quality_score(content_item, validated_effects)
                    }
                    
                    validated_content.append(validated_item)
                
                validated_chapters.append({
                    **chapter,
                    'content': validated_content
                })
            
            # Add quality metadata
            quality_metadata = {
                'total_effects_removed': total_effects_removed,
                'quality_improvements': self._generate_quality_report(enhanced_markup, validated_chapters),
                'validation_rules_applied': list(self.quality_thresholds.keys())
            }
            
            validated_markup = {
                **enhanced_markup,
                'chapters': validated_chapters,
                'quality_metadata': quality_metadata
            }
            
            logger.info(f"Quality validation completed. Removed {total_effects_removed} effects.")
            return validated_markup
            
        except Exception as e:
            logger.error(f"Error in quality validation: {str(e)}")
            return enhanced_markup
    
    def _validate_content_effects(self, content_item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Validate effects for a single content item."""
        effects = content_item.get('effects', [])
        if not effects:
            return []
        
        validated_effects = []
        
        for effect in effects:
            if self._is_effect_valid(effect, content_item):
                validated_effects.append(effect)
        
        # Apply additional quality filters
        validated_effects = self._apply_quality_filters(validated_effects, content_item)
        
        return validated_effects
    
    def _is_effect_valid(self, effect: Dict[str, Any], content_item: Dict[str, Any]) -> bool:
        """Check if an individual effect is valid."""
        # Check emotional score threshold
        emotional_score = content_item.get('emotional_score', 0.0)
        if emotional_score < self.quality_thresholds['minimum_emotional_score']:
            return False
        
        # Check effect type validity
        effect_type = effect.get('type')
        if not self._is_valid_effect_type(effect_type):
            return False
        
        # Check context appropriateness
        if not self._is_context_appropriate(effect, content_item):
            return False
        
        # Check character consistency
        if not self._is_character_consistent(effect, content_item):
            return False
        
        return True
    
    def _is_valid_effect_type(self, effect_type: str) -> bool:
        """Check if the effect type is valid."""
        valid_types = ['text_style', 'word_effect', 'sound']
        return effect_type in valid_types
    
    def _is_context_appropriate(self, effect: Dict[str, Any], content_item: Dict[str, Any]) -> bool:
        """Check if the effect is appropriate for the context."""
        text = content_item.get('text', '').lower()
        effect_name = effect.get('style') or effect.get('effect') or effect.get('sound', '')
        
        # Check for context violations
        for context, forbidden_effects in self.context_violations.items():
            if context in text and effect_name in forbidden_effects:
                return False
        
        # Check for inappropriate combinations with other effects
        other_effects = content_item.get('effects', [])
        for other_effect in other_effects:
            if other_effect == effect:
                continue
            
            other_name = other_effect.get('style') or other_effect.get('effect') or other_effect.get('sound', '')
            if (effect_name, other_name) in self.inappropriate_combinations:
                return False
        
        return True
    
    def _is_character_consistent(self, effect: Dict[str, Any], content_item: Dict[str, Any]) -> bool:
        """Check if the effect is consistent with character portrayal."""
        effect_character = effect.get('character')
        if not effect_character:
            return True  # No character specified, so no inconsistency
        
        # Get character relevance scores
        character_relevance = content_item.get('character_relevance', {})
        character_score = character_relevance.get(effect_character, 0.0)
        
        # Effect should only be applied if character is significantly relevant
        return character_score >= self.quality_thresholds['character_consistency_threshold']
    
    def _apply_quality_filters(self, effects: List[Dict[str, Any]], content_item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply additional quality filters to effects."""
        if not effects:
            return []
        
        # Limit number of effects per segment
        max_effects = self.quality_thresholds['maximum_effects_per_segment']
        if len(effects) > max_effects:
            # Sort by quality score and keep the best ones
            effects_with_scores = [(effect, self._calculate_effect_quality_score(effect, content_item)) 
                                 for effect in effects]
            effects_with_scores.sort(key=lambda x: x[1], reverse=True)
            effects = [effect for effect, score in effects_with_scores[:max_effects]]
        
        # Remove redundant effects
        effects = self._remove_redundant_effects(effects)
        
        return effects
    
    def _calculate_effect_quality_score(self, effect: Dict[str, Any], content_item: Dict[str, Any]) -> float:
        """Calculate a quality score for an individual effect."""
        score = 0.0
        
        # Base score from emotional intensity
        emotional_score = content_item.get('emotional_score', 0.0)
        score += emotional_score * 0.4
        
        # Effect intensity bonus
        effect_intensity = effect.get('intensity', 0.5)
        score += effect_intensity * 0.3
        
        # Character relevance bonus
        character = effect.get('character')
        if character:
            character_relevance = content_item.get('character_relevance', {})
            char_score = character_relevance.get(character, 0.0)
            score += char_score * 0.2
        
        # Context appropriateness bonus
        if self._is_context_appropriate(effect, content_item):
            score += 0.1
        
        return min(1.0, score)
    
    def _remove_redundant_effects(self, effects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove redundant or conflicting effects."""
        if len(effects) <= 1:
            return effects
        
        # Group effects by type
        effect_groups = {}
        for effect in effects:
            effect_type = effect.get('type')
            if effect_type not in effect_groups:
                effect_groups[effect_type] = []
            effect_groups[effect_type].append(effect)
        
        # Keep only the best effect of each type
        filtered_effects = []
        for effect_type, type_effects in effect_groups.items():
            if len(type_effects) > 1:
                # Keep the one with highest intensity
                best_effect = max(type_effects, key=lambda e: e.get('intensity', 0.0))
                filtered_effects.append(best_effect)
            else:
                filtered_effects.append(type_effects[0])
        
        return filtered_effects
    
    def _calculate_quality_score(self, content_item: Dict[str, Any], validated_effects: List[Dict[str, Any]]) -> float:
        """Calculate overall quality score for a content item."""
        if not validated_effects:
            return 0.0
        
        # Base quality from emotional score
        emotional_score = content_item.get('emotional_score', 0.0)
        quality_score = emotional_score * 0.5
        
        # Effect quality contribution
        effect_scores = [self._calculate_effect_quality_score(effect, content_item) 
                        for effect in validated_effects]
        avg_effect_score = sum(effect_scores) / len(effect_scores) if effect_scores else 0.0
        quality_score += avg_effect_score * 0.3
        
        # Context appropriateness bonus
        context_appropriate = all(self._is_context_appropriate(effect, content_item) 
                                for effect in validated_effects)
        if context_appropriate:
            quality_score += 0.2
        
        return min(1.0, quality_score)
    
    def _generate_quality_report(self, original_markup: Dict[str, Any], 
                               validated_markup: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a quality improvement report."""
        original_effects = 0
        validated_effects = 0
        
        # Count original effects
        for chapter in original_markup.get('chapters', []):
            for content_item in chapter.get('content', []):
                original_effects += len(content_item.get('effects', []))
        
        # Count validated effects
        for chapter in validated_markup.get('chapters', []):
            for content_item in chapter.get('content', []):
                validated_effects += len(content_item.get('effects', []))
        
        return {
            'original_effect_count': original_effects,
            'validated_effect_count': validated_effects,
            'effects_removed': original_effects - validated_effects,
            'quality_improvement_percentage': ((original_effects - validated_effects) / original_effects * 100) 
                                            if original_effects > 0 else 0,
            'average_quality_score': self._calculate_average_quality_score(validated_markup)
        }
    
    def _calculate_average_quality_score(self, validated_markup: Dict[str, Any]) -> float:
        """Calculate average quality score across all content."""
        quality_scores = []
        
        for chapter in validated_markup.get('chapters', []):
            for content_item in chapter.get('content', []):
                quality_score = content_item.get('quality_score', 0.0)
                quality_scores.append(quality_score)
        
        return sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
    
    def get_quality_metrics(self, markup: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive quality metrics for the markup."""
        total_content_items = 0
        items_with_effects = 0
        total_effects = 0
        effect_type_distribution = {}
        
        for chapter in markup.get('chapters', []):
            for content_item in chapter.get('content', []):
                total_content_items += 1
                effects = content_item.get('effects', [])
                
                if effects:
                    items_with_effects += 1
                    total_effects += len(effects)
                    
                    for effect in effects:
                        effect_type = effect.get('type', 'unknown')
                        effect_type_distribution[effect_type] = effect_type_distribution.get(effect_type, 0) + 1
        
        return {
            'total_content_items': total_content_items,
            'items_with_effects': items_with_effects,
            'effect_coverage_percentage': (items_with_effects / total_content_items * 100) 
                                        if total_content_items > 0 else 0,
            'total_effects': total_effects,
            'average_effects_per_item': total_effects / items_with_effects if items_with_effects > 0 else 0,
            'effect_type_distribution': effect_type_distribution,
            'quality_thresholds_met': self._check_threshold_compliance(markup)
        }
    
    def _check_threshold_compliance(self, markup: Dict[str, Any]) -> Dict[str, bool]:
        """Check if the markup complies with quality thresholds."""
        compliance = {}
        
        # Check emotional score threshold
        low_emotional_effects = 0
        total_effects = 0
        
        for chapter in markup.get('chapters', []):
            for content_item in chapter.get('content', []):
                effects = content_item.get('effects', [])
                emotional_score = content_item.get('emotional_score', 0.0)
                
                for effect in effects:
                    total_effects += 1
                    if emotional_score < self.quality_thresholds['minimum_emotional_score']:
                        low_emotional_effects += 1
        
        compliance['emotional_score_threshold'] = low_emotional_effects == 0
        
        # Check effect count threshold
        max_effects_violations = 0
        for chapter in markup.get('chapters', []):
            for content_item in chapter.get('content', []):
                effects = content_item.get('effects', [])
                if len(effects) > self.quality_thresholds['maximum_effects_per_segment']:
                    max_effects_violations += 1
        
        compliance['maximum_effects_threshold'] = max_effects_violations == 0
        
        return compliance
