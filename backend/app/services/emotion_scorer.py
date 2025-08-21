"""
Emotional Intensity Scoring Service

Calculates emotional intensity and context for text segments to determine
when and how effects should be applied while maintaining the "book is the star" philosophy.
"""

from __future__ import annotations
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class EmotionalIntensityScorer:
    """
    Scores emotional intensity and context for text segments.
    
    Features:
    - Multi-factor emotional analysis
    - Context-aware scoring
    - Character-specific emotional weighting
    - Narrative importance assessment
    """
    
    def __init__(self):
        """Initialize the emotion scorer."""
        self.emotion_weights = {
            'dialogue_intensity': 0.3,
            'action_urgency': 0.25,
            'sensory_richness': 0.2,
            'conflict_level': 0.15,
            'character_vulnerability': 0.1
        }
        
        self.emotion_keywords = {
            'high_intensity': [
                'rage', 'fury', 'terror', 'ecstasy', 'despair', 'passion', 'hatred',
                'love', 'joy', 'grief', 'panic', 'wonder', 'shock', 'amazement'
            ],
            'medium_intensity': [
                'angry', 'sad', 'happy', 'afraid', 'excited', 'worried', 'surprised',
                'confused', 'annoyed', 'pleased', 'disappointed', 'relieved'
            ],
            'low_intensity': [
                'slightly', 'somewhat', 'a bit', 'kind of', 'sort of', 'maybe',
                'perhaps', 'possibly', 'gently', 'softly', 'quietly'
            ]
        }
        
        self.context_indicators = {
            'climactic': ['suddenly', 'finally', 'at last', 'moment', 'turning point'],
            'reflective': ['thought', 'realized', 'understood', 'remembered', 'considered'],
            'action': ['ran', 'jumped', 'fought', 'moved', 'entered', 'left', 'grabbed'],
            'dialogue': ['said', 'asked', 'replied', 'whispered', 'shouted', 'muttered'],
            'sensory': ['saw', 'heard', 'felt', 'smelled', 'tasted', 'touched']
        }
    
    def calculate_emotional_weight(self, content_item: Dict[str, Any], 
                                 structure_data: Dict[str, Any], 
                                 character_profiles: Dict[str, Dict]) -> float:
        """
        Calculate the emotional weight of a content segment.
        
        Args:
            content_item: The content segment to analyze
            structure_data: Structural analysis data
            character_profiles: Character analysis data
            
        Returns:
            Emotional weight score between 0.0 and 1.0
        """
        try:
            text = content_item.get('text', '')
            if not text.strip():
                return 0.0
            
            # Calculate individual factors
            factors = {
                'dialogue_intensity': self._analyze_dialogue_emotion(text),
                'action_urgency': self._measure_action_pacing(text),
                'sensory_richness': self._assess_sensory_language(text),
                'conflict_level': self._evaluate_conflict_intensity(text),
                'character_vulnerability': self._assess_character_openness(text, character_profiles)
            }
            
            # Apply narrative context weighting
            context_weight = self._calculate_narrative_context_weight(content_item, structure_data)
            
            # Calculate weighted emotional score
            emotional_score = sum([
                factors[factor] * self.emotion_weights[factor] * context_weight
                for factor in factors
            ])
            
            # Normalize to 0.0-1.0 range
            return min(1.0, max(0.0, emotional_score))
            
        except Exception as e:
            logger.error(f"Error calculating emotional weight: {str(e)}")
            return 0.0
    
    def get_emotional_context(self, content_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get detailed emotional context for a content segment.
        
        Args:
            content_item: The content segment to analyze
            
        Returns:
            Dictionary containing emotional context information
        """
        try:
            text = content_item.get('text', '')
            
            context = {
                'primary_emotion': self._identify_primary_emotion(text),
                'emotional_complexity': self._calculate_emotional_complexity(text),
                'intensity_level': self._classify_intensity_level(text),
                'context_type': self._classify_context_type(text),
                'emotional_keywords': self._extract_emotional_keywords(text),
                'narrative_function': self._determine_narrative_function(text)
            }
            
            return context
            
        except Exception as e:
            logger.error(f"Error getting emotional context: {str(e)}")
            return {
                'primary_emotion': 'neutral',
                'emotional_complexity': 0.0,
                'intensity_level': 'low',
                'context_type': 'narrative',
                'emotional_keywords': [],
                'narrative_function': 'description'
            }
    
    def _analyze_dialogue_emotion(self, text: str) -> float:
        """Analyze emotional intensity in dialogue."""
        if not text:
            return 0.0
        
        text_lower = text.lower()
        
        # Check for dialogue markers
        has_dialogue = '"' in text or '"' in text or '"' in text
        
        if not has_dialogue:
            return 0.1  # Low emotion for non-dialogue
        
        # Analyze dialogue emotion
        emotion_score = 0.0
        
        # High intensity emotions in dialogue
        high_emotion_count = sum(1 for word in self.emotion_keywords['high_intensity'] 
                               if word in text_lower)
        emotion_score += high_emotion_count * 0.3
        
        # Medium intensity emotions
        medium_emotion_count = sum(1 for word in self.emotion_keywords['medium_intensity'] 
                                 if word in text_lower)
        emotion_score += medium_emotion_count * 0.2
        
        # Dialogue intensity indicators
        intensity_indicators = ['shouted', 'whispered', 'cried', 'laughed', 'screamed', 'muttered']
        intensity_count = sum(1 for indicator in intensity_indicators if indicator in text_lower)
        emotion_score += intensity_count * 0.15
        
        # Normalize by text length
        word_count = len(text.split())
        return emotion_score / word_count if word_count > 0 else 0.0
    
    def _measure_action_pacing(self, text: str) -> float:
        """Measure the urgency and pacing of action sequences."""
        if not text:
            return 0.0
        
        text_lower = text.lower()
        
        # Action verbs
        action_verbs = [
            'ran', 'jumped', 'fought', 'moved', 'entered', 'left', 'grabbed', 'pushed',
            'pulled', 'threw', 'caught', 'escaped', 'chased', 'attacked', 'defended'
        ]
        
        action_count = sum(1 for verb in action_verbs if verb in text_lower)
        
        # Urgency indicators
        urgency_words = ['suddenly', 'quickly', 'rapidly', 'immediately', 'instantly', 'urgently']
        urgency_count = sum(1 for word in urgency_words if word in text_lower)
        
        # Pacing indicators
        pacing_words = ['finally', 'at last', 'moment', 'turning point', 'climax']
        pacing_count = sum(1 for word in pacing_words if word in text_lower)
        
        # Calculate action urgency score
        total_indicators = action_count + urgency_count + pacing_count
        word_count = len(text.split())
        
        return total_indicators / word_count if word_count > 0 else 0.0
    
    def _assess_sensory_language(self, text: str) -> float:
        """Assess the richness of sensory language."""
        if not text:
            return 0.0
        
        text_lower = text.lower()
        
        # Sensory words
        sensory_words = {
            'visual': ['saw', 'looked', 'watched', 'observed', 'noticed', 'appeared', 'seemed'],
            'auditory': ['heard', 'listened', 'sounded', 'echoed', 'whispered', 'shouted'],
            'tactile': ['felt', 'touched', 'grasped', 'held', 'pressed', 'squeezed'],
            'olfactory': ['smelled', 'scented', 'aroma', 'fragrance', 'odor', 'stench'],
            'gustatory': ['tasted', 'flavor', 'sweet', 'bitter', 'sour', 'spicy']
        }
        
        sensory_count = 0
        for sense, words in sensory_words.items():
            sensory_count += sum(1 for word in words if word in text_lower)
        
        # Sensory richness indicators
        richness_words = ['vivid', 'bright', 'loud', 'soft', 'sharp', 'smooth', 'rough']
        richness_count = sum(1 for word in richness_words if word in text_lower)
        
        total_sensory = sensory_count + richness_count
        word_count = len(text.split())
        
        return total_sensory / word_count if word_count > 0 else 0.0
    
    def _evaluate_conflict_intensity(self, text: str) -> float:
        """Evaluate the intensity of conflict in the text."""
        if not text:
            return 0.0
        
        text_lower = text.lower()
        
        # Conflict indicators
        conflict_words = [
            'fight', 'battle', 'conflict', 'argument', 'dispute', 'disagreement',
            'struggle', 'war', 'attack', 'defend', 'resist', 'oppose', 'challenge'
        ]
        
        conflict_count = sum(1 for word in conflict_words if word in text_lower)
        
        # Emotional conflict indicators
        emotional_conflict = [
            'hate', 'anger', 'rage', 'fury', 'resentment', 'jealousy', 'envy',
            'betrayal', 'deception', 'lies', 'secrets', 'mistrust'
        ]
        
        emotional_conflict_count = sum(1 for word in emotional_conflict if word in text_lower)
        
        # Physical conflict indicators
        physical_conflict = [
            'punch', 'kick', 'hit', 'strike', 'wound', 'injury', 'blood', 'pain'
        ]
        
        physical_conflict_count = sum(1 for word in physical_conflict if word in text_lower)
        
        # Weight different types of conflict
        total_conflict = (conflict_count * 0.4 + 
                         emotional_conflict_count * 0.4 + 
                         physical_conflict_count * 0.2)
        
        word_count = len(text.split())
        return total_conflict / word_count if word_count > 0 else 0.0
    
    def _assess_character_openness(self, text: str, character_profiles: Dict[str, Dict]) -> float:
        """Assess character vulnerability and openness in the text."""
        if not text or not character_profiles:
            return 0.0
        
        text_lower = text.lower()
        
        # Vulnerability indicators
        vulnerability_words = [
            'confessed', 'admitted', 'revealed', 'told', 'shared', 'opened up',
            'trusted', 'believed', 'hoped', 'feared', 'worried', 'doubted'
        ]
        
        vulnerability_count = sum(1 for word in vulnerability_words if word in text_lower)
        
        # Character-specific vulnerability
        character_vulnerability = 0.0
        for character, profile in character_profiles.items():
            if character.lower() in text_lower:
                # Check character's emotional state
                emotional_signature = profile.get('emotional_signature', {})
                primary_emotion = emotional_signature.get('primary_emotion', 'neutral')
                
                # Vulnerable emotions
                vulnerable_emotions = ['fear', 'sadness', 'love', 'trust']
                if primary_emotion in vulnerable_emotions:
                    character_vulnerability += 0.3
        
        # Normalize by text length
        word_count = len(text.split())
        base_vulnerability = vulnerability_count / word_count if word_count > 0 else 0.0
        
        return min(1.0, base_vulnerability + character_vulnerability)
    
    def _calculate_narrative_context_weight(self, content_item: Dict[str, Any], 
                                          structure_data: Dict[str, Any]) -> float:
        """Calculate narrative context weight for the content segment."""
        # Default weight
        context_weight = 1.0
        
        # Check if this is a climactic moment
        story_beats = structure_data.get('story_beats', [])
        tension_points = structure_data.get('tension_points', [])
        
        # Increase weight for important story moments
        for beat in story_beats:
            if (beat.get('chapter') == content_item.get('chapter', -1) and
                beat.get('position') == content_item.get('position', -1)):
                context_weight *= 1.5
                break
        
        # Increase weight for tension points
        for tension in tension_points:
            if (tension.get('chapter') == content_item.get('chapter', -1) and
                tension.get('position') == content_item.get('position', -1)):
                context_weight *= 1.3
                break
        
        return context_weight
    
    def _identify_primary_emotion(self, text: str) -> str:
        """Identify the primary emotion in the text."""
        if not text:
            return 'neutral'
        
        text_lower = text.lower()
        
        # Emotion categories
        emotions = {
            'joy': ['happy', 'joy', 'delighted', 'excited', 'cheerful', 'laugh', 'smile'],
            'sadness': ['sad', 'depressed', 'melancholy', 'grief', 'sorrow', 'tears'],
            'anger': ['angry', 'furious', 'rage', 'hate', 'hostile', 'aggressive'],
            'fear': ['afraid', 'fear', 'terrified', 'scared', 'anxious', 'worried'],
            'love': ['love', 'adore', 'passion', 'affection', 'tender', 'romantic'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned'],
            'disgust': ['disgusted', 'revolted', 'sickened', 'repulsed'],
            'trust': ['trust', 'faith', 'confidence', 'belief', 'reliable']
        }
        
        emotion_scores = {}
        for emotion, keywords in emotions.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score
        
        if emotion_scores:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            return primary_emotion if emotion_scores[primary_emotion] > 0 else 'neutral'
        
        return 'neutral'
    
    def _calculate_emotional_complexity(self, text: str) -> float:
        """Calculate the complexity of emotions in the text."""
        if not text:
            return 0.0
        
        text_lower = text.lower()
        
        # Count different emotions present
        emotion_categories = 0
        for emotion, keywords in self.emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                emotion_categories += 1
        
        # Normalize by number of possible emotion categories
        max_categories = len(self.emotion_keywords)
        return emotion_categories / max_categories if max_categories > 0 else 0.0
    
    def _classify_intensity_level(self, text: str) -> str:
        """Classify the intensity level of emotions in the text."""
        if not text:
            return 'low'
        
        text_lower = text.lower()
        
        # Count high intensity words
        high_intensity_count = sum(1 for word in self.emotion_keywords['high_intensity'] 
                                 if word in text_lower)
        
        # Count medium intensity words
        medium_intensity_count = sum(1 for word in self.emotion_keywords['medium_intensity'] 
                                   if word in text_lower)
        
        # Count low intensity words
        low_intensity_count = sum(1 for word in self.emotion_keywords['low_intensity'] 
                                if word in text_lower)
        
        # Classify based on counts
        if high_intensity_count > 0:
            return 'high'
        elif medium_intensity_count > 0:
            return 'medium'
        elif low_intensity_count > 0:
            return 'low'
        else:
            return 'neutral'
    
    def _classify_context_type(self, text: str) -> str:
        """Classify the context type of the text."""
        if not text:
            return 'narrative'
        
        text_lower = text.lower()
        
        # Check for different context types
        for context_type, indicators in self.context_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                return context_type
        
        return 'narrative'
    
    def _extract_emotional_keywords(self, text: str) -> List[str]:
        """Extract emotional keywords from the text."""
        if not text:
            return []
        
        text_lower = text.lower()
        found_keywords = []
        
        # Extract keywords from all emotion categories
        for category, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_keywords.append(keyword)
        
        return found_keywords
    
    def _determine_narrative_function(self, text: str) -> str:
        """Determine the narrative function of the text segment."""
        if not text:
            return 'description'
        
        text_lower = text.lower()
        
        # Check for different narrative functions
        if any(indicator in text_lower for indicator in self.context_indicators['dialogue']):
            return 'dialogue'
        elif any(indicator in text_lower for indicator in self.context_indicators['action']):
            return 'action'
        elif any(indicator in text_lower for indicator in self.context_indicators['reflective']):
            return 'reflection'
        elif any(indicator in text_lower for indicator in self.context_indicators['sensory']):
            return 'sensory'
        else:
            return 'description'
