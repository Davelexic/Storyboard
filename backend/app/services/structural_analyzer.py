"""
Story Structure Analysis Service

Analyzes the narrative structure, pacing, and story beats of a book
to understand the overall flow and identify key moments for effects.
"""

from __future__ import annotations
from typing import Dict, List, Any, Optional
import re
import logging

logger = logging.getLogger(__name__)


class StoryStructureAnalyzer:
    """
    Analyzes the structural elements of a story including:
    - Narrative pacing and rhythm
    - Story beats and climax points
    - Chapter structure and flow
    - Tension curves and emotional arcs
    """
    
    def __init__(self):
        """Initialize the structural analyzer."""
        self.pacing_keywords = {
            'action': ['fight', 'battle', 'chase', 'run', 'attack', 'defend', 'escape'],
            'tension': ['suddenly', 'finally', 'at last', 'meanwhile', 'however', 'but'],
            'climax': ['climax', 'peak', 'moment', 'turning point', 'decision', 'choice'],
            'resolution': ['finally', 'at last', 'peace', 'calm', 'settled', 'resolved']
        }
        
        self.structure_patterns = {
            'dialogue_intensity': r'["""].*?["""]',  # Dialogue markers
            'action_sequences': r'\b(ran|jumped|fought|moved|walked|entered|left)\b',
            'emotional_markers': r'\b(felt|thought|realized|understood|knew|wished|hoped)\b',
            'scene_transitions': r'\b(Meanwhile|Later|Soon|After|Before|When|While)\b'
        }
    
    def analyze_narrative_structure(self, parsed_book: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the complete narrative structure of the book.
        
        Args:
            parsed_book: Parsed book data from EPUB parser
            
        Returns:
            Dictionary containing structural analysis data
        """
        try:
            logger.info("Starting narrative structure analysis")
            
            chapters = parsed_book.get('chapters', [])
            
            analysis = {
                'overall_structure': self._analyze_overall_structure(chapters),
                'chapter_analysis': self._analyze_chapters(chapters),
                'pacing_curve': self._calculate_pacing_curve(chapters),
                'story_beats': self._identify_story_beats(chapters),
                'tension_points': self._find_tension_points(chapters),
                'emotional_arcs': self._map_emotional_arcs(chapters),
                'narrative_rhythm': self._analyze_narrative_rhythm(chapters)
            }
            
            logger.info("Narrative structure analysis completed")
            return analysis
            
        except Exception as e:
            logger.error(f"Error in narrative structure analysis: {str(e)}")
            return self._create_fallback_structure_analysis()
    
    def _analyze_overall_structure(self, chapters: List[Dict]) -> Dict[str, Any]:
        """Analyze the overall structure and flow of the book."""
        total_chapters = len(chapters)
        total_content = sum(len(chapter.get('content', [])) for chapter in chapters)
        
        # Identify structural phases
        phases = self._identify_story_phases(chapters)
        
        return {
            'total_chapters': total_chapters,
            'total_content_segments': total_content,
            'average_chapter_length': total_content / total_chapters if total_chapters > 0 else 0,
            'story_phases': phases,
            'structural_balance': self._assess_structural_balance(chapters)
        }
    
    def _analyze_chapters(self, chapters: List[Dict]) -> List[Dict]:
        """Analyze each chapter individually."""
        chapter_analyses = []
        
        for i, chapter in enumerate(chapters):
            content = chapter.get('content', [])
            
            analysis = {
                'chapter_index': i,
                'chapter_title': chapter.get('title', f'Chapter {i+1}'),
                'content_length': len(content),
                'dialogue_density': self._calculate_dialogue_density(content),
                'action_density': self._calculate_action_density(content),
                'emotional_intensity': self._calculate_chapter_emotion(content),
                'pacing_score': self._calculate_chapter_pacing(content),
                'structural_role': self._determine_chapter_role(i, len(chapters), content)
            }
            
            chapter_analyses.append(analysis)
        
        return chapter_analyses
    
    def _calculate_pacing_curve(self, chapters: List[Dict]) -> List[float]:
        """Calculate the pacing curve across all chapters."""
        pacing_scores = []
        
        for chapter in chapters:
            content = chapter.get('content', [])
            pacing_score = self._calculate_chapter_pacing(content)
            pacing_scores.append(pacing_score)
        
        return pacing_scores
    
    def _identify_story_beats(self, chapters: List[Dict]) -> List[Dict]:
        """Identify key story beats and turning points."""
        story_beats = []
        
        for i, chapter in enumerate(chapters):
            content = chapter.get('content', [])
            
            # Look for story beat indicators
            beat_indicators = self._find_beat_indicators(content)
            
            for indicator in beat_indicators:
                story_beats.append({
                    'chapter': i,
                    'position': indicator['position'],
                    'beat_type': indicator['type'],
                    'intensity': indicator['intensity'],
                    'description': indicator['description']
                })
        
        return story_beats
    
    def _find_tension_points(self, chapters: List[Dict]) -> List[Dict]:
        """Find points of high tension or conflict."""
        tension_points = []
        
        for i, chapter in enumerate(chapters):
            content = chapter.get('content', [])
            
            for j, item in enumerate(content):
                text = item.get('text', '').lower()
                
                # Check for tension indicators
                tension_score = self._calculate_tension_score(text)
                
                if tension_score > 0.6:  # High tension threshold
                    tension_points.append({
                        'chapter': i,
                        'position': j,
                        'tension_score': tension_score,
                        'tension_type': self._classify_tension_type(text),
                        'context': text[:100] + '...' if len(text) > 100 else text
                    })
        
        return tension_points
    
    def _map_emotional_arcs(self, chapters: List[Dict]) -> Dict[str, List[float]]:
        """Map emotional arcs throughout the story."""
        emotional_arcs = {
            'overall_emotion': [],
            'character_emotion': {},
            'relationship_emotion': [],
            'conflict_emotion': []
        }
        
        for chapter in chapters:
            content = chapter.get('content', [])
            
            # Overall emotional arc
            chapter_emotion = self._calculate_chapter_emotion(content)
            emotional_arcs['overall_emotion'].append(chapter_emotion)
            
            # Character-specific emotions (simplified)
            character_emotions = self._extract_character_emotions(content)
            for character, emotion in character_emotions.items():
                if character not in emotional_arcs['character_emotion']:
                    emotional_arcs['character_emotion'][character] = []
                emotional_arcs['character_emotion'][character].append(emotion)
        
        return emotional_arcs
    
    def _analyze_narrative_rhythm(self, chapters: List[Dict]) -> Dict[str, Any]:
        """Analyze the rhythm and flow of the narrative."""
        rhythm_data = {
            'sentence_lengths': [],
            'paragraph_breaks': [],
            'scene_transitions': [],
            'pacing_variations': []
        }
        
        for chapter in chapters:
            content = chapter.get('content', [])
            
            for item in content:
                text = item.get('text', '')
                
                # Analyze sentence structure
                sentences = text.split('.')
                avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
                rhythm_data['sentence_lengths'].append(avg_sentence_length)
                
                # Look for scene transitions
                if self._is_scene_transition(text):
                    rhythm_data['scene_transitions'].append({
                        'text': text[:50] + '...' if len(text) > 50 else text,
                        'transition_type': self._classify_transition_type(text)
                    })
        
        return rhythm_data
    
    def _identify_story_phases(self, chapters: List[Dict]) -> Dict[str, List[int]]:
        """Identify different phases of the story (exposition, rising action, etc.)."""
        total_chapters = len(chapters)
        
        # Simple phase identification based on chapter position
        phases = {
            'exposition': list(range(0, max(1, total_chapters // 4))),
            'rising_action': list(range(max(1, total_chapters // 4), total_chapters // 2)),
            'climax': list(range(total_chapters // 2, 3 * total_chapters // 4)),
            'falling_action': list(range(3 * total_chapters // 4, total_chapters))
        }
        
        return phases
    
    def _assess_structural_balance(self, chapters: List[Dict]) -> Dict[str, float]:
        """Assess the structural balance of the story."""
        if not chapters:
            return {'balance_score': 0.0, 'pacing_consistency': 0.0}
        
        chapter_lengths = [len(chapter.get('content', [])) for chapter in chapters]
        
        # Calculate balance metrics
        avg_length = sum(chapter_lengths) / len(chapter_lengths)
        length_variance = sum((length - avg_length) ** 2 for length in chapter_lengths) / len(chapter_lengths)
        
        # Balance score (lower variance = better balance)
        balance_score = max(0, 1 - (length_variance / (avg_length ** 2)))
        
        return {
            'balance_score': balance_score,
            'pacing_consistency': 1 - (length_variance / avg_length) if avg_length > 0 else 0,
            'length_variance': length_variance,
            'average_chapter_length': avg_length
        }
    
    def _calculate_dialogue_density(self, content: List[Dict]) -> float:
        """Calculate the density of dialogue in a chapter."""
        if not content:
            return 0.0
        
        dialogue_count = 0
        total_segments = len(content)
        
        for item in content:
            text = item.get('text', '')
            if self._contains_dialogue(text):
                dialogue_count += 1
        
        return dialogue_count / total_segments
    
    def _calculate_action_density(self, content: List[Dict]) -> float:
        """Calculate the density of action sequences in a chapter."""
        if not content:
            return 0.0
        
        action_count = 0
        total_words = 0
        
        for item in content:
            text = item.get('text', '')
            words = text.split()
            total_words += len(words)
            
            action_words = sum(1 for word in words if word.lower() in self.pacing_keywords['action'])
            action_count += action_words
        
        return action_count / total_words if total_words > 0 else 0.0
    
    def _calculate_chapter_emotion(self, content: List[Dict]) -> float:
        """Calculate the emotional intensity of a chapter."""
        if not content:
            return 0.0
        
        emotion_scores = []
        
        for item in content:
            text = item.get('text', '').lower()
            
            # Simple emotion scoring based on keywords
            emotion_keywords = ['love', 'hate', 'fear', 'joy', 'sadness', 'anger', 'surprise']
            emotion_count = sum(1 for keyword in emotion_keywords if keyword in text)
            
            # Normalize by text length
            word_count = len(text.split())
            emotion_score = emotion_count / word_count if word_count > 0 else 0
            emotion_scores.append(emotion_score)
        
        return sum(emotion_scores) / len(emotion_scores) if emotion_scores else 0.0
    
    def _calculate_chapter_pacing(self, content: List[Dict]) -> float:
        """Calculate the pacing score of a chapter."""
        if not content:
            return 0.0
        
        pacing_indicators = 0
        total_words = 0
        
        for item in content:
            text = item.get('text', '').lower()
            words = text.split()
            total_words += len(words)
            
            # Count pacing keywords
            for category, keywords in self.pacing_keywords.items():
                pacing_indicators += sum(1 for keyword in keywords if keyword in text)
        
        return pacing_indicators / total_words if total_words > 0 else 0.0
    
    def _determine_chapter_role(self, chapter_index: int, total_chapters: int, content: List[Dict]) -> str:
        """Determine the structural role of a chapter."""
        if chapter_index == 0:
            return 'exposition'
        elif chapter_index < total_chapters // 4:
            return 'setup'
        elif chapter_index < total_chapters // 2:
            return 'rising_action'
        elif chapter_index < 3 * total_chapters // 4:
            return 'climax'
        else:
            return 'resolution'
    
    def _find_beat_indicators(self, content: List[Dict]) -> List[Dict]:
        """Find story beat indicators in content."""
        beat_indicators = []
        
        for i, item in enumerate(content):
            text = item.get('text', '').lower()
            
            # Look for beat indicators
            if any(keyword in text for keyword in ['suddenly', 'finally', 'at last', 'turning point']):
                beat_indicators.append({
                    'position': i,
                    'type': 'turning_point',
                    'intensity': 0.8,
                    'description': 'Major turning point identified'
                })
            
            if any(keyword in text for keyword in ['decision', 'choice', 'realized', 'understood']):
                beat_indicators.append({
                    'position': i,
                    'type': 'character_development',
                    'intensity': 0.6,
                    'description': 'Character development moment'
                })
        
        return beat_indicators
    
    def _calculate_tension_score(self, text: str) -> float:
        """Calculate tension score for a text segment."""
        tension_keywords = ['fight', 'battle', 'conflict', 'danger', 'threat', 'attack', 'escape']
        tension_count = sum(1 for keyword in tension_keywords if keyword in text)
        
        # Normalize by text length
        word_count = len(text.split())
        return tension_count / word_count if word_count > 0 else 0.0
    
    def _classify_tension_type(self, text: str) -> str:
        """Classify the type of tension in the text."""
        if any(word in text for word in ['fight', 'battle', 'attack']):
            return 'physical_conflict'
        elif any(word in text for word in ['argument', 'dispute', 'disagreement']):
            return 'verbal_conflict'
        elif any(word in text for word in ['danger', 'threat', 'risk']):
            return 'environmental_tension'
        else:
            return 'emotional_tension'
    
    def _extract_character_emotions(self, content: List[Dict]) -> Dict[str, float]:
        """Extract character-specific emotions (simplified implementation)."""
        # This is a simplified version - would be enhanced with NLP
        character_emotions = {}
        
        for item in content:
            text = item.get('text', '')
            # Simple character detection (would be enhanced)
            if '"' in text:  # Dialogue
                emotion_score = self._calculate_dialogue_emotion(text)
                character_emotions['speaker'] = emotion_score
        
        return character_emotions
    
    def _calculate_dialogue_emotion(self, text: str) -> float:
        """Calculate emotion in dialogue."""
        emotion_keywords = ['love', 'hate', 'fear', 'joy', 'sadness', 'anger']
        emotion_count = sum(1 for keyword in emotion_keywords if keyword in text.lower())
        
        word_count = len(text.split())
        return emotion_count / word_count if word_count > 0 else 0.0
    
    def _contains_dialogue(self, text: str) -> bool:
        """Check if text contains dialogue."""
        return '"' in text or '"' in text or '"' in text
    
    def _is_scene_transition(self, text: str) -> bool:
        """Check if text represents a scene transition."""
        transition_markers = ['Meanwhile', 'Later', 'Soon', 'After', 'Before', 'When', 'While']
        return any(marker in text for marker in transition_markers)
    
    def _classify_transition_type(self, text: str) -> str:
        """Classify the type of scene transition."""
        if 'Meanwhile' in text:
            return 'parallel_action'
        elif 'Later' in text or 'Soon' in text:
            return 'time_advance'
        elif 'When' in text or 'While' in text:
            return 'simultaneous_action'
        else:
            return 'general_transition'
    
    def _create_fallback_structure_analysis(self) -> Dict[str, Any]:
        """Create fallback analysis when the main analysis fails."""
        logger.warning("Creating fallback structure analysis")
        
        return {
            'overall_structure': {
                'total_chapters': 0,
                'total_content_segments': 0,
                'average_chapter_length': 0,
                'story_phases': {},
                'structural_balance': {'balance_score': 0.0, 'pacing_consistency': 0.0}
            },
            'chapter_analysis': [],
            'pacing_curve': [],
            'story_beats': [],
            'tension_points': [],
            'emotional_arcs': {'overall_emotion': [], 'character_emotion': {}},
            'narrative_rhythm': {'sentence_lengths': [], 'scene_transitions': []}
        }
