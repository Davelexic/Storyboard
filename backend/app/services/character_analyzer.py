"""
Character Analysis Service

Analyzes characters, their dialogue patterns, emotional development,
and relationships to create character profiles for effect application.
"""

from __future__ import annotations
from typing import Dict, List, Any, Optional, Set
import re
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class CharacterEmotionAnalyzer:
    """
    Analyzes characters and their emotional development throughout the story.
    
    Features:
    - Character identification and extraction
    - Dialogue pattern analysis
    - Emotional state tracking
    - Character relationship mapping
    - Speech characteristic analysis
    """
    
    def __init__(self):
        """Initialize the character analyzer."""
        self.emotion_keywords = {
            'anger': ['angry', 'furious', 'rage', 'hate', 'hostile', 'aggressive', 'fierce'],
            'sadness': ['sad', 'depressed', 'melancholy', 'grief', 'sorrow', 'tears', 'wept'],
            'joy': ['happy', 'joy', 'delighted', 'excited', 'cheerful', 'laugh', 'smile'],
            'fear': ['afraid', 'fear', 'terrified', 'scared', 'anxious', 'worried', 'panic'],
            'love': ['love', 'adore', 'passion', 'affection', 'tender', 'romantic', 'heart'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned', 'wonder'],
            'disgust': ['disgusted', 'revolted', 'sickened', 'repulsed', 'nauseated'],
            'trust': ['trust', 'faith', 'confidence', 'belief', 'reliable', 'loyal']
        }
        
        self.speech_patterns = {
            'formal': ['indeed', 'therefore', 'thus', 'hence', 'moreover', 'furthermore'],
            'casual': ['yeah', 'okay', 'sure', 'whatever', 'gonna', 'wanna'],
            'aggressive': ['damn', 'hell', 'bastard', 'idiot', 'fool', 'coward'],
            'submissive': ['sorry', 'please', 'forgive', 'excuse', 'pardon', 'beg'],
            'confident': ['certainly', 'absolutely', 'definitely', 'obviously', 'clearly']
        }
        
        self.character_indicators = [
            r'["""]([^"""]*?)["""]',  # Quoted dialogue
            r'([A-Z][a-z]+)\s+said',  # "Name said" pattern
            r'([A-Z][a-z]+)\s+asked',  # "Name asked" pattern
            r'([A-Z][a-z]+)\s+replied',  # "Name replied" pattern
            r'([A-Z][a-z]+)\s+whispered',  # "Name whispered" pattern
            r'([A-Z][a-z]+)\s+shouted',  # "Name shouted" pattern
        ]
    
    def analyze_character_arcs(self, parsed_book: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Analyze character development and emotional arcs throughout the story.
        
        Args:
            parsed_book: Parsed book data from EPUB parser
            
        Returns:
            Dictionary of character profiles with emotional and speech analysis
        """
        try:
            logger.info("Starting character analysis")
            
            # Extract all text content
            all_content = self._extract_all_content(parsed_book)
            
            # Identify characters
            characters = self._identify_characters(all_content)
            logger.info(f"Identified {len(characters)} characters")
            
            # Analyze each character
            character_profiles = {}
            
            for character in characters:
                profile = self._analyze_character(character, parsed_book)
                character_profiles[character] = profile
            
            # Analyze character relationships
            relationship_map = self._analyze_character_relationships(character_profiles, parsed_book)
            
            # Add relationship data to profiles
            for character, profile in character_profiles.items():
                profile['relationships'] = relationship_map.get(character, {})
            
            logger.info("Character analysis completed successfully")
            return character_profiles
            
        except Exception as e:
            logger.error(f"Error in character analysis: {str(e)}")
            return self._create_fallback_character_profiles()
    
    def _extract_all_content(self, parsed_book: Dict[str, Any]) -> List[str]:
        """Extract all text content from the book."""
        all_content = []
        
        for chapter in parsed_book.get('chapters', []):
            for item in chapter.get('content', []):
                text = item.get('text', '')
                if text.strip():
                    all_content.append(text)
        
        return all_content
    
    def _identify_characters(self, content: List[str]) -> Set[str]:
        """Identify characters mentioned in the text."""
        characters = set()
        
        for text in content:
            # Look for character names in dialogue and narration
            found_characters = self._extract_character_names(text)
            characters.update(found_characters)
        
        # Filter out common words that might be mistaken for names
        filtered_characters = self._filter_character_names(characters)
        
        return filtered_characters
    
    def _extract_character_names(self, text: str) -> Set[str]:
        """Extract potential character names from text."""
        names = set()
        
        # Look for quoted dialogue with speaker attribution
        for pattern in self.character_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    # Handle groups in regex
                    for group in match:
                        if group and len(group) > 2:  # Minimum name length
                            names.add(group.strip())
                else:
                    if match and len(match) > 2:
                        names.add(match.strip())
        
        # Look for capitalized words that might be names
        words = text.split()
        for i, word in enumerate(words):
            # Check if word is capitalized and not at start of sentence
            if (word[0].isupper() and 
                len(word) > 2 and 
                i > 0 and 
                not words[i-1].endswith('.') and
                not words[i-1].endswith('!') and
                not words[i-1].endswith('?')):
                names.add(word.strip('.,!?;:'))
        
        return names
    
    def _filter_character_names(self, names: Set[str]) -> Set[str]:
        """Filter out common words that aren't character names."""
        common_words = {
            'the', 'and', 'but', 'for', 'with', 'from', 'this', 'that', 'they', 'them',
            'their', 'there', 'here', 'when', 'where', 'what', 'why', 'how', 'who',
            'which', 'each', 'every', 'some', 'any', 'all', 'none', 'both', 'either',
            'neither', 'first', 'last', 'next', 'previous', 'current', 'former', 'latter'
        }
        
        filtered = set()
        for name in names:
            # Remove common words and very short names
            if (name.lower() not in common_words and 
                len(name) > 2 and 
                not name.isdigit() and
                not all(c.isupper() for c in name)):  # Not all caps
                filtered.add(name)
        
        return filtered
    
    def _analyze_character(self, character: str, parsed_book: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a specific character's development and patterns."""
        character_data = {
            'name': character,
            'dialogue_segments': [],
            'emotional_timeline': [],
            'speech_characteristics': {},
            'emotional_signature': {},
            'development_arc': {},
            'key_moments': []
        }
        
        # Extract character-specific content
        character_content = self._extract_character_content(character, parsed_book)
        character_data['dialogue_segments'] = character_content
        
        # Analyze speech patterns
        character_data['speech_characteristics'] = self._analyze_speech_patterns(character_content)
        
        # Analyze emotional development
        character_data['emotional_signature'] = self._analyze_emotional_signature(character_content)
        
        # Create emotional timeline
        character_data['emotional_timeline'] = self._create_emotional_timeline(character, parsed_book)
        
        # Identify key character moments
        character_data['key_moments'] = self._identify_key_moments(character, parsed_book)
        
        # Analyze character development arc
        character_data['development_arc'] = self._analyze_development_arc(character_data)
        
        return character_data
    
    def _extract_character_content(self, character: str, parsed_book: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract all content related to a specific character."""
        character_content = []
        
        for chapter_idx, chapter in enumerate(parsed_book.get('chapters', [])):
            for content_idx, item in enumerate(chapter.get('content', [])):
                text = item.get('text', '')
                
                # Check if character is mentioned in this content
                if self._is_character_mentioned(character, text):
                    character_content.append({
                        'chapter': chapter_idx,
                        'position': content_idx,
                        'text': text,
                        'context': self._get_character_context(character, text)
                    })
        
        return character_content
    
    def _is_character_mentioned(self, character: str, text: str) -> bool:
        """Check if a character is mentioned in the text."""
        # Case-insensitive check
        return character.lower() in text.lower()
    
    def _get_character_context(self, character: str, text: str) -> str:
        """Get the context in which a character appears."""
        # Simple context extraction - can be enhanced
        if f'"{character}' in text or f'"{character}' in text:
            return 'dialogue'
        elif character in text:
            return 'narration'
        else:
            return 'mention'
    
    def _analyze_speech_patterns(self, character_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the speech patterns of a character."""
        if not character_content:
            return {}
        
        all_text = ' '.join([item['text'] for item in character_content])
        text_lower = all_text.lower()
        
        pattern_scores = {}
        
        # Analyze speech pattern categories
        for pattern_type, keywords in self.speech_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            pattern_scores[pattern_type] = score
        
        # Calculate vocabulary complexity
        words = all_text.split()
        unique_words = set(words)
        vocabulary_complexity = len(unique_words) / len(words) if words else 0
        
        # Analyze sentence structure
        sentences = all_text.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        return {
            'pattern_scores': pattern_scores,
            'vocabulary_complexity': vocabulary_complexity,
            'average_sentence_length': avg_sentence_length,
            'dominant_pattern': max(pattern_scores, key=pattern_scores.get) if pattern_scores else 'neutral'
        }
    
    def _analyze_emotional_signature(self, character_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the emotional signature of a character."""
        if not character_content:
            return {}
        
        all_text = ' '.join([item['text'] for item in character_content])
        text_lower = all_text.lower()
        
        emotion_scores = {}
        
        # Calculate emotion scores
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score
        
        # Find dominant emotions
        if emotion_scores:
            dominant_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
            primary_emotion = dominant_emotions[0][0] if dominant_emotions[0][1] > 0 else 'neutral'
            secondary_emotion = dominant_emotions[1][0] if len(dominant_emotions) > 1 and dominant_emotions[1][1] > 0 else None
        else:
            primary_emotion = 'neutral'
            secondary_emotion = None
        
        return {
            'emotion_scores': emotion_scores,
            'primary_emotion': primary_emotion,
            'secondary_emotion': secondary_emotion,
            'emotional_complexity': len([score for score in emotion_scores.values() if score > 0])
        }
    
    def _create_emotional_timeline(self, character: str, parsed_book: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create an emotional timeline for the character throughout the story."""
        timeline = []
        
        for chapter_idx, chapter in enumerate(parsed_book.get('chapters', [])):
            chapter_emotion = self._calculate_chapter_emotion_for_character(character, chapter)
            
            timeline.append({
                'chapter': chapter_idx,
                'emotional_state': chapter_emotion['state'],
                'emotional_intensity': chapter_emotion['intensity'],
                'emotional_keywords': chapter_emotion['keywords']
            })
        
        return timeline
    
    def _calculate_chapter_emotion_for_character(self, character: str, chapter: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate the emotional state of a character in a specific chapter."""
        character_text = ''
        
        for item in chapter.get('content', []):
            text = item.get('text', '')
            if self._is_character_mentioned(character, text):
                character_text += ' ' + text
        
        if not character_text:
            return {'state': 'neutral', 'intensity': 0.0, 'keywords': []}
        
        text_lower = character_text.lower()
        
        # Find emotions present in this chapter
        present_emotions = []
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    present_emotions.append(emotion)
                    break
        
        # Calculate emotional intensity
        emotion_count = sum(1 for emotion, keywords in self.emotion_keywords.items() 
                          for keyword in keywords if keyword in text_lower)
        word_count = len(character_text.split())
        intensity = emotion_count / word_count if word_count > 0 else 0.0
        
        # Determine dominant emotion
        if present_emotions:
            state = present_emotions[0]  # Most common emotion
        else:
            state = 'neutral'
        
        return {
            'state': state,
            'intensity': intensity,
            'keywords': present_emotions
        }
    
    def _identify_key_moments(self, character: str, parsed_book: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify key moments for a character in the story."""
        key_moments = []
        
        for chapter_idx, chapter in enumerate(parsed_book.get('chapters', [])):
            for content_idx, item in enumerate(chapter.get('content', [])):
                text = item.get('text', '')
                
                if self._is_character_mentioned(character, text):
                    # Check for key moment indicators
                    moment_type = self._classify_moment_type(text)
                    
                    if moment_type:
                        key_moments.append({
                            'chapter': chapter_idx,
                            'position': content_idx,
                            'type': moment_type,
                            'text': text[:100] + '...' if len(text) > 100 else text,
                            'significance': self._calculate_moment_significance(text)
                        })
        
        return key_moments
    
    def _classify_moment_type(self, text: str) -> Optional[str]:
        """Classify the type of moment in the text."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['realized', 'understood', 'knew', 'discovered']):
            return 'revelation'
        elif any(word in text_lower for word in ['decided', 'chose', 'determined', 'resolved']):
            return 'decision'
        elif any(word in text_lower for word in ['changed', 'transformed', 'became', 'turned']):
            return 'transformation'
        elif any(word in text_lower for word in ['confessed', 'admitted', 'revealed', 'told']):
            return 'confession'
        elif any(word in text_lower for word in ['died', 'killed', 'murdered', 'sacrificed']):
            return 'death'
        
        return None
    
    def _calculate_moment_significance(self, text: str) -> float:
        """Calculate the significance of a moment."""
        # Simple significance calculation based on emotional keywords
        emotion_count = sum(1 for emotion, keywords in self.emotion_keywords.items() 
                          for keyword in keywords if keyword in text.lower())
        
        word_count = len(text.split())
        return emotion_count / word_count if word_count > 0 else 0.0
    
    def _analyze_development_arc(self, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the character's development arc throughout the story."""
        timeline = character_data.get('emotional_timeline', [])
        
        if not timeline:
            return {'arc_type': 'static', 'development_score': 0.0}
        
        # Calculate emotional variance
        emotions = [entry['emotional_intensity'] for entry in timeline]
        emotional_variance = self._calculate_variance(emotions)
        
        # Determine arc type
        if emotional_variance > 0.1:
            arc_type = 'dynamic'
        elif emotional_variance > 0.05:
            arc_type = 'moderate'
        else:
            arc_type = 'static'
        
        # Calculate development score
        development_score = min(1.0, emotional_variance * 10)
        
        return {
            'arc_type': arc_type,
            'development_score': development_score,
            'emotional_variance': emotional_variance,
            'character_growth': len(character_data.get('key_moments', []))
        }
    
    def _analyze_character_relationships(self, character_profiles: Dict[str, Dict], parsed_book: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """Analyze relationships between characters."""
        relationships = defaultdict(lambda: defaultdict(float))
        
        characters = list(character_profiles.keys())
        
        # Analyze co-occurrence patterns
        for chapter in parsed_book.get('chapters', []):
            for item in chapter.get('content', []):
                text = item.get('text', '')
                
                # Find which characters appear together
                present_characters = [char for char in characters if self._is_character_mentioned(char, text)]
                
                # Update relationship scores
                for i, char1 in enumerate(present_characters):
                    for char2 in present_characters[i+1:]:
                        relationships[char1][char2] += 1
                        relationships[char2][char1] += 1
        
        # Normalize relationship scores
        for char1 in relationships:
            for char2 in relationships[char1]:
                relationships[char1][char2] = min(1.0, relationships[char1][char2] / 10)
        
        return dict(relationships)
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values."""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        squared_diff_sum = sum((value - mean) ** 2 for value in values)
        return squared_diff_sum / (len(values) - 1)
    
    def _create_fallback_character_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Create fallback character profiles when analysis fails."""
        logger.warning("Creating fallback character profiles")
        
        return {
            'narrator': {
                'name': 'narrator',
                'dialogue_segments': [],
                'emotional_timeline': [],
                'speech_characteristics': {},
                'emotional_signature': {'primary_emotion': 'neutral'},
                'development_arc': {'arc_type': 'static', 'development_score': 0.0},
                'key_moments': [],
                'relationships': {}
            }
        }
