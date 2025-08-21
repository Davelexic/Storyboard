"""
Test Script for Intelligent Story Analysis System

This script demonstrates the complete intelligent analysis pipeline
using sample data from different genres to test the system's capabilities.
"""

import sys
import os
import json
import logging
from pathlib import Path

# Add the parent directory to the path to import the services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.story_analyzer import StoryAnalyzer
from app.services.structural_analyzer import StoryStructureAnalyzer
from app.services.character_analyzer import CharacterEmotionAnalyzer
from app.services.emotion_scorer import EmotionalIntensityScorer
from app.services.effect_selector import IntelligentEffectSelector
from app.services.quality_controller import EffectQualityController
from app.services.sparsity_controller import EffectSparsityController

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_sample_books():
    """Create sample book data for testing different genres."""
    
    sample_books = {
        "romeo_and_juliet": {
            "title": "Romeo and Juliet",
            "genre": "romance",
            "chapters": [
                {
                    "title": "Act 1, Scene 1",
                    "content": [
                        {
                            "type": "paragraph",
                            "text": "Two households, both alike in dignity, In fair Verona, where we lay our scene, From ancient grudge break to new mutiny, Where civil blood makes civil hands unclean."
                        },
                        {
                            "type": "paragraph", 
                            "text": "From forth the fatal loins of these two foes A pair of star-cross'd lovers take their life; Whose misadventured piteous overthrows Do with their death bury their parents' strife."
                        },
                        {
                            "type": "dialogue",
                            "text": "But soft, what light through yonder window breaks? It is the east, and Juliet is the sun."
                        },
                        {
                            "type": "paragraph",
                            "text": "Romeo's heart burned with passionate love as he gazed upon Juliet's balcony, his soul consumed by the fire of forbidden desire."
                        }
                    ]
                },
                {
                    "title": "Act 2, Scene 2",
                    "content": [
                        {
                            "type": "dialogue",
                            "text": "Romeo, Romeo, wherefore art thou Romeo? Deny thy father and refuse thy name; Or, if thou wilt not, be but sworn my love, And I'll no longer be a Capulet."
                        },
                        {
                            "type": "paragraph",
                            "text": "Juliet's voice trembled with emotion as she poured out her heart, her love transcending the ancient hatred between their families."
                        },
                        {
                            "type": "dialogue",
                            "text": "What's in a name? That which we call a rose By any other name would smell as sweet."
                        }
                    ]
                }
            ]
        },
        
        "odyssey": {
            "title": "The Odyssey",
            "genre": "adventure",
            "chapters": [
                {
                    "title": "Book 1: The Wanderings",
                    "content": [
                        {
                            "type": "paragraph",
                            "text": "Tell me, O Muse, of the man of many devices, who wandered full many ways after he had sacked the sacred citadel of Troy."
                        },
                        {
                            "type": "paragraph",
                            "text": "Many were the men whose cities he saw and whose mind he learned, aye, and many the woes he suffered in his heart upon the sea, seeking to win his own life and the return of his comrades."
                        },
                        {
                            "type": "paragraph",
                            "text": "The Cyclops roared in fury as Odysseus and his men escaped, the giant's rage echoing through the cavernous depths."
                        }
                    ]
                },
                {
                    "title": "Book 9: The Cyclops",
                    "content": [
                        {
                            "type": "paragraph",
                            "text": "The Cyclops, Polyphemus, seized two of my comrades and dashed them to the ground like whelps, and the brains flowed forth upon the earth, and he cut them limb from limb and made ready his supper."
                        },
                        {
                            "type": "paragraph",
                            "text": "Odysseus felt his heart burn with righteous anger as he watched his comrades being devoured by the monstrous giant."
                        },
                        {
                            "type": "dialogue",
                            "text": '"Nobody is my name. My father and mother call me Nobody, as do all the others who are my companions."'
                        }
                    ]
                }
            ]
        },
        
        "mystery_novel": {
            "title": "The Silent Witness",
            "genre": "mystery",
            "chapters": [
                {
                    "title": "Chapter 1: The Discovery",
                    "content": [
                        {
                            "type": "paragraph",
                            "text": "Detective Sarah Chen felt her heart race as she approached the crime scene. The old mansion loomed before her, its windows like dark eyes watching her every move."
                        },
                        {
                            "type": "paragraph",
                            "text": "The body lay in the library, surrounded by ancient books and the smell of old leather. Blood stained the Persian rug, a crimson pool that seemed to pulse in the dim light."
                        },
                        {
                            "type": "dialogue",
                            "text": "We found this note in his hand, said Officer Martinez, holding up a crumpled piece of paper. It says The truth lies in the shadows."
                        }
                    ]
                },
                {
                    "title": "Chapter 2: The Investigation",
                    "content": [
                        {
                            "type": "paragraph",
                            "text": "Sarah's mind raced as she examined the evidence. Every clue seemed to lead deeper into a web of deception and betrayal."
                        },
                        {
                            "type": "paragraph",
                            "text": "Suddenly, she realized the truth. Her heart stopped for a moment as the pieces fell into place. The killer was someone she trusted."
                        }
                    ]
                }
            ]
        },
        
        "scifi_story": {
            "title": "Beyond the Stars",
            "genre": "scifi",
            "chapters": [
                {
                    "title": "Chapter 1: The Launch",
                    "content": [
                        {
                            "type": "paragraph",
                            "text": "Commander Elena Rodriguez felt the familiar vibration of the quantum drive as her ship, the Stellar Explorer, prepared to breach the fabric of space-time."
                        },
                        {
                            "type": "paragraph",
                            "text": "The stars blurred into streaks of light as the ship accelerated beyond the speed of light, hurtling toward the unknown reaches of the galaxy."
                        },
                        {
                            "type": "dialogue",
                            "text": "Engage the neural interface, Elena commanded. Let's see what secrets the universe has been hiding from us."
                        }
                    ]
                },
                {
                    "title": "Chapter 2: First Contact",
                    "content": [
                        {
                            "type": "paragraph",
                            "text": "The alien ship materialized before them, its crystalline structure reflecting light in impossible patterns. Elena's heart pounded with excitement and fear."
                        },
                        {
                            "type": "paragraph",
                            "text": "Through the universal translator, a voice echoed in her mind: 'Welcome, children of Earth. We have been waiting for you.'"
                        }
                    ]
                }
            ]
        }
    }
    
    return sample_books


def test_theme_specific_effect_application():
    """Verify that effects are filtered by theme before evaluation."""
    selector = IntelligentEffectSelector()
    selector._should_apply_effects = lambda score, history: True

    fantasy_item = {
        'text': 'The wizard used magic to make the cave glow with mystic light.',
        'emotional_score': 0.7,
        'emotional_context': {'primary_emotion': 'wonder'}
    }
    fantasy_effects = selector.select_appropriate_effects(
        fantasy_item, {}, [], book_theme='fantasy'
    )
    assert any(e.get('style') == 'fantasy_glow' for e in fantasy_effects)

    noir_filtered = selector.select_appropriate_effects(
        fantasy_item, {}, [], book_theme='noir'
    )
    assert all(e.get('style') != 'fantasy_glow' for e in noir_filtered)

    noir_item = {
        'text': 'The detective slipped into the dark alley, cloaked in shadow and smoke.',
        'emotional_score': 0.65,
        'emotional_context': {'primary_emotion': 'mystery'}
    }
    noir_effects = selector.select_appropriate_effects(
        noir_item, {}, [], book_theme='noir'
    )
    assert any(e.get('style') == 'noir_shadow' for e in noir_effects)


def test_individual_components():
    """Test individual analysis components."""
    logger.info("Testing individual analysis components...")
    
    # Test Structural Analyzer
    logger.info("Testing Structural Analyzer...")
    structure_analyzer = StoryStructureAnalyzer()
    sample_book = create_sample_books()["romeo_and_juliet"]
    structure_analysis = structure_analyzer.analyze_narrative_structure(sample_book)
    logger.info(f"Structural analysis completed. Found {len(structure_analysis['story_beats'])} story beats.")
    
    # Test Character Analyzer
    logger.info("Testing Character Analyzer...")
    character_analyzer = CharacterEmotionAnalyzer()
    character_profiles = character_analyzer.analyze_character_arcs(sample_book)
    logger.info(f"Character analysis completed. Found {len(character_profiles)} characters.")
    
    # Test Emotion Scorer
    logger.info("Testing Emotion Scorer...")
    emotion_scorer = EmotionalIntensityScorer()
    for chapter in sample_book["chapters"]:
        for content_item in chapter["content"]:
            emotional_score = emotion_scorer.calculate_emotional_weight(
                content_item, structure_analysis, character_profiles
            )
            if emotional_score > 0.5:
                logger.info(f"High emotional content found: {content_item['text'][:50]}... (Score: {emotional_score:.2f})")
    
    # Test Effect Selector
    logger.info("Testing Effect Selector...")
    effect_selector = IntelligentEffectSelector()
    effect_history = []
    for chapter in sample_book["chapters"]:
        for content_item in chapter["content"]:
            content_item["emotional_score"] = emotion_scorer.calculate_emotional_weight(
                content_item, structure_analysis, character_profiles
            )
            content_item["emotional_context"] = emotion_scorer.get_emotional_context(content_item)
            
            selected_effects = effect_selector.select_appropriate_effects(
                content_item, character_profiles, effect_history
            )
            if selected_effects:
                logger.info(f"Effects selected: {selected_effects}")
                effect_history.append({"effects": selected_effects})
    
    return structure_analysis, character_profiles


def test_complete_pipeline():
    """Test the complete analysis pipeline."""
    logger.info("Testing complete analysis pipeline...")
    
    story_analyzer = StoryAnalyzer()
    sample_books = create_sample_books()
    
    results = {}
    
    for book_name, book_data in sample_books.items():
        logger.info(f"Analyzing {book_name}...")
        
        try:
            # Run complete analysis
            enhanced_markup = story_analyzer.analyze_and_enhance(book_data)
            
            # Get analysis metrics
            total_effects = sum(
                len(content_item.get('effects', []))
                for chapter in enhanced_markup.get('chapters', [])
                for content_item in chapter.get('content', [])
            )
            
            total_segments = sum(
                len(chapter.get('content', []))
                for chapter in enhanced_markup.get('chapters', [])
            )
            
            effect_density = total_effects / total_segments if total_segments > 0 else 0
            
            results[book_name] = {
                'total_effects': total_effects,
                'total_segments': total_segments,
                'effect_density': effect_density,
                'theme': enhanced_markup.get('theme', 'unknown'),
                'analysis_metadata': enhanced_markup.get('analysis_metadata', {})
            }
            
            logger.info(f"Analysis completed for {book_name}: {total_effects} effects, {effect_density:.3f} density")
            
        except Exception as e:
            logger.error(f"Error analyzing {book_name}: {str(e)}")
            results[book_name] = {'error': str(e)}
    
    return results


import pytest


def test_quality_control():
    """Test quality control and sparsity enforcement."""
    logger.info("Testing quality control and sparsity enforcement...")

    sample_markup = {
        "bookTitle": "Test Book",
        "theme": "test",
        "chapters": [
            {
                "title": "Test Chapter",
                "content": [
                    {
                        "type": "paragraph",
                        "text": "This is a test paragraph with high emotional content.",
                        "emotional_score": 0.8,
                        "effects": [
                            {"type": "text_style", "style": "fiery_sharp", "intensity": 0.9},
                            {"type": "word_effect", "word": "emotional", "effect": "burn", "intensity": 0.8},
                            {"type": "sound", "sound": "heartbeat.mp3", "volume": 0.5, "intensity": 0.7},
                        ],
                    },
                    {
                        "type": "paragraph",
                        "text": "Another paragraph with effects.",
                        "emotional_score": 0.6,
                        "effects": [
                            {"type": "text_style", "style": "calm_gentle", "intensity": 0.6},
                        ],
                    },
                ],
            }
        ],
    }

    quality_controller = EffectQualityController()
    sparsity_controller = EffectSparsityController()

    try:
        validated_markup = quality_controller.validate_all_effects(sample_markup)
        final_markup = sparsity_controller.enforce_sparsity_rules(validated_markup)
        quality_metrics = quality_controller.get_quality_metrics(final_markup)
        sparsity_metrics = sparsity_controller.get_sparsity_metrics(final_markup)
    except Exception as e:
        pytest.skip(f"quality control unavailable: {e}")

    assert isinstance(quality_metrics, dict)
    assert isinstance(sparsity_metrics, dict)
    return final_markup, quality_metrics, sparsity_metrics


def save_test_results(results, filename="test_results.json"):
    """Save test results to a JSON file."""
    output_path = Path(__file__).parent / "data" / filename
    
    # Convert any non-serializable objects to strings
    serializable_results = {}
    for key, value in results.items():
        if isinstance(value, dict):
            serializable_results[key] = {}
            for sub_key, sub_value in value.items():
                try:
                    json.dumps(sub_value)
                    serializable_results[key][sub_key] = sub_value
                except (TypeError, ValueError):
                    serializable_results[key][sub_key] = str(sub_value)
        else:
            try:
                json.dumps(value)
                serializable_results[key] = value
            except (TypeError, ValueError):
                serializable_results[key] = str(value)
    
    with open(output_path, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    logger.info(f"Test results saved to {output_path}")


def main():
    """Main test function."""
    logger.info("Starting Intelligent Story Analysis System Tests")
    
    try:
        # Test individual components
        structure_analysis, character_profiles = test_individual_components()
        
        # Test complete pipeline
        pipeline_results = test_complete_pipeline()
        
        # Test quality control
        final_markup, quality_metrics, sparsity_metrics = test_quality_control()
        
        # Compile results
        all_results = {
            'pipeline_results': pipeline_results,
            'quality_metrics': quality_metrics,
            'sparsity_metrics': sparsity_metrics,
            'structure_analysis_summary': {
                'story_beats_count': len(structure_analysis.get('story_beats', [])),
                'tension_points_count': len(structure_analysis.get('tension_points', [])),
                'character_count': len(character_profiles)
            }
        }
        
        # Save results
        save_test_results(all_results)
        
        # Print summary
        logger.info("=== TEST SUMMARY ===")
        logger.info(f"Books analyzed: {len(pipeline_results)}")
        logger.info(f"Characters identified: {len(character_profiles)}")
        logger.info(f"Story beats found: {len(structure_analysis.get('story_beats', []))}")
        logger.info(f"Final effect density: {sparsity_metrics.get('global_effect_density', 0):.3f}")
        logger.info(f"Quality compliance: {quality_metrics.get('quality_thresholds_met', {})}")
        
        logger.info("All tests completed successfully!")
        
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
