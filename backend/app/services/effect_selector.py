"""
Intelligent Effect Selection Service

Selects appropriate effects based on emotional analysis, character profiles,
and narrative context while maintaining the "book is the star" philosophy.
"""

from __future__ import annotations
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class IntelligentEffectSelector:
    """
    Intelligently selects effects based on analysis results.
    
    Features:
    - Context-aware effect selection
    - Character-specific effect mapping
    - Emotional intensity-based effect scaling
    - Sparsity control and overuse prevention
    """
    
    def __init__(self):
        """Initialize the effect selector."""
        self.effect_library = {
            'text_style': {
                'fiery_sharp': {
                    'triggers': ['anger', 'rage', 'fury', 'aggressive'],
                    'intensity_threshold': 0.6,
                    'character_types': ['aggressive', 'hotheaded', 'warrior'],
                    'contexts': ['conflict', 'battle', 'confrontation']
                },
                'calm_gentle': {
                    'triggers': ['peace', 'calm', 'gentle', 'tender'],
                    'intensity_threshold': 0.4,
                    'character_types': ['wise', 'peaceful', 'healer'],
                    'contexts': ['reflection', 'healing', 'reconciliation']
                },
                'mysterious_shadow': {
                    'triggers': ['mystery', 'secret', 'hidden', 'unknown'],
                    'intensity_threshold': 0.5,
                    'character_types': ['mysterious', 'secretive', 'wizard'],
                    'contexts': ['revelation', 'discovery', 'magic']
                },
                'passionate_flame': {
                    'triggers': ['love', 'passion', 'desire', 'romance'],
                    'intensity_threshold': 0.7,
                    'character_types': ['romantic', 'passionate', 'lover'],
                    'contexts': ['romance', 'confession', 'intimate']
                },
                'fantasy_glow': {
                    'triggers': ['magic', 'enchanted', 'dragon', 'mystic'],
                    'intensity_threshold': 0.5,
                    'character_types': ['wizard', 'elf', 'hero'],
                    'contexts': ['magic', 'fantasy', 'enchanted'],
                    'themes': ['fantasy']
                },
                'noir_shadow': {
                    'triggers': ['shadow', 'smoke', 'dark', 'mystery'],
                    'intensity_threshold': 0.5,
                    'character_types': ['detective', 'antihero', 'criminal'],
                    'contexts': ['crime', 'investigation', 'night'],
                    'themes': ['noir']
                }
            },
            'word_effect': {
                'burn': {
                    'triggers': ['hate', 'rage', 'fire', 'burn'],
                    'intensity_threshold': 0.8,
                    'contexts': ['climax', 'conflict', 'transformation']
                },
                'glow': {
                    'triggers': ['light', 'hope', 'magic', 'divine'],
                    'intensity_threshold': 0.6,
                    'contexts': ['revelation', 'magic', 'divine']
                },
                'sparkle': {
                    'triggers': ['joy', 'wonder', 'magic', 'beautiful'],
                    'intensity_threshold': 0.5,
                    'contexts': ['joy', 'wonder', 'celebration']
                }
            },
            'sound': {
                'swords_clash': {
                    'triggers': ['fight', 'battle', 'sword', 'clash'],
                    'intensity_threshold': 0.8,
                    'contexts': ['battle', 'duel', 'conflict'],
                    'volume': 0.3
                },
                'gentle_wind': {
                    'triggers': ['wind', 'breeze', 'peace', 'calm'],
                    'intensity_threshold': 0.4,
                    'contexts': ['peace', 'nature', 'reflection'],
                    'volume': 0.2
                },
                'heartbeat': {
                    'triggers': ['heart', 'fear', 'tension', 'anticipation'],
                    'intensity_threshold': 0.6,
                    'contexts': ['tension', 'fear', 'anticipation'],
                    'volume': 0.25
                }
            }
        }
        
        self.effect_tiers = {
            'TIER_1_MICRO': {
                'usage_rate': 0.1,  # 0.1% of content
                'effects': ['calm_gentle', 'gentle_wind'],
                'intensity_range': (0.3, 0.5)
            },
            'TIER_2_MODERATE': {
                'usage_rate': 1.0,  # 1% of content
                'effects': ['fiery_sharp', 'mysterious_shadow', 'glow', 'sparkle', 'fantasy_glow', 'noir_shadow'],
                'intensity_range': (0.5, 0.7)
            },
            'TIER_3_DRAMATIC': {
                'usage_rate': 0.01,  # 0.01% of content (very rare)
                'effects': ['passionate_flame', 'burn', 'swords_clash', 'heartbeat'],
                'intensity_range': (0.7, 1.0)
            }
        }
    
    def select_appropriate_effects(self, content_item: Dict[str, Any],
                                 character_profiles: Dict[str, Dict],
                                 effect_history: List[Dict],
                                 book_theme: str = 'general') -> List[Dict[str, Any]]:
        """
        Select appropriate effects for a content segment.
        
        Args:
            content_item: The content segment with emotional analysis
            character_profiles: Character analysis data
            effect_history: History of previously applied effects
            
        Returns:
            List of selected effects (empty if no effects should be applied)
        """
        try:
            # Get emotional data
            emotional_score = content_item.get('emotional_score', 0.0)
            emotional_context = content_item.get('emotional_context', {})
            text = content_item.get('text', '')
            
            # Check if effects should be applied based on sparsity rules
            if not self._should_apply_effects(emotional_score, effect_history):
                return []
            
            # Determine effect tier based on emotional intensity
            effect_tier = self._determine_effect_tier(emotional_score)

            # Filter available effects by theme
            text_style_options = self._filter_effects_by_theme(
                self.effect_tiers[effect_tier]['effects'], 'text_style', book_theme
            )
            word_effect_options = self._filter_effects_by_theme(
                self.effect_tiers[effect_tier]['effects'], 'word_effect', book_theme
            )
            sound_effect_options = self._filter_effects_by_theme(
                self.effect_tiers[effect_tier]['effects'], 'sound', book_theme
            )

            # Select effects based on context and character profiles
            selected_effects = []

            # Text style effects
            text_style_effect = self._select_text_style_effect(
                emotional_context, character_profiles, text, text_style_options
            )
            if text_style_effect:
                selected_effects.append(text_style_effect)

            # Word effects
            word_effects = self._select_word_effects(
                emotional_context, text, word_effect_options
            )
            selected_effects.extend(word_effects)

            # Sound effects (only for very high intensity moments)
            if emotional_score > 0.8:
                sound_effect = self._select_sound_effect(
                    emotional_context, text, sound_effect_options
                )
                if sound_effect:
                    selected_effects.append(sound_effect)
            
            # Limit total effects per segment
            if len(selected_effects) > 3:
                selected_effects = selected_effects[:3]
            
            return selected_effects
            
        except Exception as e:
            logger.error(f"Error selecting effects: {str(e)}")
            return []
    
    def _should_apply_effects(self, emotional_score: float, effect_history: List[Dict]) -> bool:
        """Determine if effects should be applied based on sparsity rules."""
        # High emotional threshold
        if emotional_score < 0.5:
            return False
        
        # Check recent effect usage
        recent_effects = len([e for e in effect_history[-10:] if e])  # Last 10 segments
        if recent_effects > 2:  # Too many recent effects
            return False
        
        # Random sparsity control (additional layer)
        import random
        if random.random() > 0.3:  # 30% chance even if conditions are met
            return False
        
        return True
    
    def _determine_effect_tier(self, emotional_score: float) -> str:
        """Determine which effect tier to use based on emotional intensity."""
        if emotional_score > 0.8:
            return 'TIER_3_DRAMATIC'
        elif emotional_score > 0.6:
            return 'TIER_2_MODERATE'
        else:
            return 'TIER_1_MICRO'

    def _filter_effects_by_theme(self, effect_names: List[str], effect_type: str, book_theme: str) -> List[str]:
        """Filter effects based on the current book theme."""
        library = self.effect_library.get(effect_type, {})
        filtered = []
        for name in effect_names:
            config = library.get(name)
            if not config:
                continue
            themes = config.get('themes', ['general'])
            if book_theme in themes or 'general' in themes:
                filtered.append(name)
        return filtered

    def _select_text_style_effect(self, emotional_context: Dict[str, Any],
                                character_profiles: Dict[str, Dict],
                                text: str, available_effects: List[str]) -> Optional[Dict[str, Any]]:
        """Select appropriate text style effect."""
        primary_emotion = emotional_context.get('primary_emotion', 'neutral')
        context_type = emotional_context.get('context_type', 'narrative')

        # Filter effects that match the emotion and context
        matching_effects = []

        for effect_name in available_effects:
            if effect_name in self.effect_library['text_style']:
                effect_config = self.effect_library['text_style'][effect_name]

                # Check if effect matches current context
                if self._effect_matches_context(effect_config, primary_emotion, context_type, text):
                    matching_effects.append((effect_name, effect_config))
        
        # Select the best matching effect
        if matching_effects:
            # Sort by relevance score
            matching_effects.sort(key=lambda x: self._calculate_effect_relevance(x[1], text), reverse=True)
            selected_effect_name, selected_config = matching_effects[0]
            
            return {
                'type': 'text_style',
                'style': selected_effect_name,
                'intensity': self._calculate_effect_intensity(selected_config, text),
                'character': self._identify_character_for_effect(text, character_profiles)
            }
        
        return None
    
    def _select_word_effects(self, emotional_context: Dict[str, Any],
                           text: str, available_effects: List[str]) -> List[Dict[str, Any]]:
        """Select appropriate word effects."""
        word_effects = []
        primary_emotion = emotional_context.get('primary_emotion', 'neutral')

        for effect_name in available_effects:
            effect_config = self.effect_library['word_effect'][effect_name]

            # Check if effect matches current context
            if self._effect_matches_context(effect_config, primary_emotion, 'word', text):
                # Find matching words in text
                matching_words = self._find_matching_words(effect_config['triggers'], text)

                for word in matching_words:
                    word_effects.append({
                        'type': 'word_effect',
                        'word': word,
                        'effect': effect_name,
                        'intensity': self._calculate_effect_intensity(effect_config, text)
                    })
        
        # Limit word effects
        return word_effects[:2]  # Max 2 word effects per segment
    
    def _select_sound_effect(self, emotional_context: Dict[str, Any],
                           text: str, available_effects: List[str]) -> Optional[Dict[str, Any]]:
        """Select appropriate sound effect."""
        primary_emotion = emotional_context.get('primary_emotion', 'neutral')

        for effect_name in available_effects:
            effect_config = self.effect_library['sound'][effect_name]

            # Check if effect matches current context
            if self._effect_matches_context(effect_config, primary_emotion, 'sound', text):
                return {
                    'type': 'sound',
                    'sound': f"{effect_name}.mp3",
                    'volume': effect_config.get('volume', 0.3),
                    'intensity': self._calculate_effect_intensity(effect_config, text)
                }
        
        return None
    
    def _effect_matches_context(self, effect_config: Dict[str, Any],
                              primary_emotion: str, context_type: str, text: str) -> bool:
        """Check if an effect matches the current context."""
        text_lower = text.lower()
        
        # Check trigger words
        triggers = effect_config.get('triggers', [])
        trigger_matches = any(trigger in text_lower for trigger in triggers)
        
        # Check emotion match
        emotion_match = primary_emotion in triggers or primary_emotion == 'neutral'
        
        # Check context match
        contexts = effect_config.get('contexts', [])
        context_match = any(context in text_lower for context in contexts)
        
        # Effect matches if any condition is met
        return trigger_matches or emotion_match or context_match
    
    def _calculate_effect_relevance(self, effect_config: Dict[str, Any], text: str) -> float:
        """Calculate how relevant an effect is to the current text."""
        text_lower = text.lower()
        relevance_score = 0.0
        
        # Count trigger word matches
        triggers = effect_config.get('triggers', [])
        trigger_matches = sum(1 for trigger in triggers if trigger in text_lower)
        relevance_score += trigger_matches * 0.3
        
        # Count context matches
        contexts = effect_config.get('contexts', [])
        context_matches = sum(1 for context in contexts if context in text_lower)
        relevance_score += context_matches * 0.2
        
        return relevance_score
    
    def _calculate_effect_intensity(self, effect_config: Dict[str, Any], text: str) -> float:
        """Calculate the intensity of an effect based on context."""
        base_intensity = effect_config.get('intensity_threshold', 0.5)
        
        # Adjust based on text characteristics
        text_lower = text.lower()
        
        # Higher intensity for more trigger words
        triggers = effect_config.get('triggers', [])
        trigger_count = sum(1 for trigger in triggers if trigger in text_lower)
        intensity_boost = min(0.3, trigger_count * 0.1)
        
        return min(1.0, base_intensity + intensity_boost)
    
    def _identify_character_for_effect(self, text: str, character_profiles: Dict[str, Dict]) -> Optional[str]:
        """Identify which character the effect should be associated with."""
        for character, profile in character_profiles.items():
            if character.lower() in text.lower():
                return character
        
        return None
    
    def _find_matching_words(self, triggers: List[str], text: str) -> List[str]:
        """Find words in the text that match the effect triggers."""
        text_lower = text.lower()
        matching_words = []
        
        for trigger in triggers:
            if trigger in text_lower:
                # Find the actual word in the original text
                words = text.split()
                for word in words:
                    if trigger in word.lower():
                        matching_words.append(word)
                        break
        
        return matching_words[:3]  # Limit to 3 matching words
    
    def get_effect_statistics(self, effect_history: List[Dict]) -> Dict[str, Any]:
        """Get statistics about effect usage."""
        if not effect_history:
            return {'total_effects': 0, 'effect_distribution': {}}
        
        effect_counts = {}
        tier_counts = {'TIER_1_MICRO': 0, 'TIER_2_MODERATE': 0, 'TIER_3_DRAMATIC': 0}
        
        for effect_record in effect_history:
            effects = effect_record.get('effects', [])
            for effect in effects:
                effect_type = effect.get('type', 'unknown')
                effect_counts[effect_type] = effect_counts.get(effect_type, 0) + 1
                
                # Determine tier based on effect name
                effect_name = effect.get('style') or effect.get('effect') or effect.get('sound', '')
                for tier, tier_config in self.effect_tiers.items():
                    if effect_name in tier_config['effects']:
                        tier_counts[tier] += 1
                        break
        
        return {
            'total_effects': len(effect_history),
            'effect_distribution': effect_counts,
            'tier_distribution': tier_counts,
            'average_effects_per_segment': len(effect_history) / max(1, len(effect_history))
        }
