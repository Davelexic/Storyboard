"""
Effect Sparsity Controller

Enforces the "less is more" philosophy by ensuring effects are used sparingly
and meaningfully. Prevents overuse and maintains the "book is the star" principle.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class EffectSparsityController:
    """
    Controls the sparsity of effects to maintain reading immersion.
    
    Features:
    - Global effect density control
    - Chapter-level sparsity enforcement
    - Effect spacing and distribution
    - Overuse prevention algorithms
    """
    
    def __init__(self):
        """Initialize the sparsity controller."""
        self.sparsity_rules = {
            'global_effect_density': 0.02,  # 2% of content segments should have effects
            'chapter_effect_limit': 0.05,   # 5% of chapter content can have effects
            'minimum_effect_spacing': 8,    # Minimum segments between effects
            'maximum_consecutive_effects': 2,  # Max effects in consecutive segments
            'climax_effect_boost': 1.5,     # Allow more effects in climax chapters
            'exposition_effect_reduction': 0.5  # Reduce effects in exposition
        }
        
        self.chapter_type_multipliers = {
            'exposition': 0.3,
            'setup': 0.5,
            'rising_action': 0.8,
            'climax': 1.5,
            'resolution': 0.7
        }
    
    def enforce_sparsity_rules(self, enhanced_markup: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enforce sparsity rules on the enhanced markup.
        
        Args:
            enhanced_markup: The enhanced markup with effects
            
        Returns:
            Sparsity-controlled markup with reduced effects
        """
        try:
            logger.info("Starting sparsity control enforcement")
            
            # Calculate global effect targets
            total_content_segments = self._count_total_segments(enhanced_markup)
            target_effects = int(total_content_segments * self.sparsity_rules['global_effect_density'])
            
            # Apply sparsity control
            controlled_chapters = []
            total_effects_removed = 0
            
            for chapter in enhanced_markup.get('chapters', []):
                controlled_content, removed_count = self._apply_chapter_sparsity(chapter, target_effects)
                controlled_chapters.append(controlled_content)
                total_effects_removed += removed_count
            
            # Apply global spacing rules
            controlled_chapters = self._enforce_global_spacing(controlled_chapters)
            
            # Add sparsity metadata
            sparsity_metadata = {
                'total_effects_removed': total_effects_removed,
                'final_effect_density': self._calculate_final_density(controlled_chapters),
                'sparsity_rules_applied': list(self.sparsity_rules.keys()),
                'spacing_violations_fixed': self._count_spacing_violations(enhanced_markup, controlled_chapters)
            }
            
            controlled_markup = {
                **enhanced_markup,
                'chapters': controlled_chapters,
                'sparsity_metadata': sparsity_metadata
            }
            
            logger.info(f"Sparsity control completed. Removed {total_effects_removed} effects.")
            return controlled_markup
            
        except Exception as e:
            logger.error(f"Error in sparsity control: {str(e)}")
            return enhanced_markup
    
    def _count_total_segments(self, markup: Dict[str, Any]) -> int:
        """Count total content segments in the markup."""
        total = 0
        for chapter in markup.get('chapters', []):
            total += len(chapter.get('content', []))
        return total
    
    def _apply_chapter_sparsity(self, chapter: Dict[str, Any], global_target: int) -> tuple[List[Dict], int]:
        """Apply sparsity rules to a single chapter."""
        content = chapter.get('content', [])
        chapter_type = self._determine_chapter_type(chapter)
        
        # Calculate chapter-specific effect limit
        chapter_multiplier = self.chapter_type_multipliers.get(chapter_type, 1.0)
        chapter_limit = int(len(content) * self.sparsity_rules['chapter_effect_limit'] * chapter_multiplier)
        
        # Get content items with effects
        items_with_effects = []
        items_without_effects = []
        
        for item in content:
            if item.get('effects'):
                items_with_effects.append(item)
            else:
                items_without_effects.append(item)
        
        # If we're over the limit, remove some effects
        effects_removed = 0
        if len(items_with_effects) > chapter_limit:
            # Sort by emotional score and keep the best ones
            items_with_effects.sort(key=lambda x: x.get('emotional_score', 0.0), reverse=True)
            
            # Remove effects from excess items
            for item in items_with_effects[chapter_limit:]:
                effects_removed += len(item.get('effects', []))
                item['effects'] = []
                items_without_effects.append(item)
            
            # Keep only the best items with effects
            items_with_effects = items_with_effects[:chapter_limit]
        
        # Reconstruct chapter content
        controlled_content = items_with_effects + items_without_effects
        
        # Sort by original position to maintain order
        controlled_content.sort(key=lambda x: x.get('position', 0))
        
        return controlled_content, effects_removed
    
    def _determine_chapter_type(self, chapter: Dict[str, Any]) -> str:
        """Determine the type of chapter for sparsity control."""
        # Check if chapter has structural role information
        structural_role = chapter.get('structural_role')
        if structural_role:
            return structural_role
        
        # Fallback: analyze chapter content
        content = chapter.get('content', [])
        if not content:
            return 'exposition'
        
        # Simple analysis based on emotional intensity
        avg_emotional_score = sum(item.get('emotional_score', 0.0) for item in content) / len(content)
        
        if avg_emotional_score > 0.7:
            return 'climax'
        elif avg_emotional_score > 0.5:
            return 'rising_action'
        elif avg_emotional_score > 0.3:
            return 'setup'
        else:
            return 'exposition'
    
    def _enforce_global_spacing(self, chapters: List[List[Dict]]) -> List[List[Dict]]:
        """Enforce global spacing rules across all chapters."""
        all_content = []
        chapter_boundaries = []
        
        # Flatten all content and track chapter boundaries
        for chapter in chapters:
            chapter_boundaries.append(len(all_content))
            all_content.extend(chapter)
        
        # Apply spacing rules
        controlled_content = self._apply_spacing_rules(all_content)
        
        # Reconstruct chapters
        controlled_chapters = []
        for i, boundary in enumerate(chapter_boundaries):
            if i == len(chapter_boundaries) - 1:
                # Last chapter
                chapter_content = controlled_content[boundary:]
            else:
                # Regular chapter
                chapter_content = controlled_content[boundary:chapter_boundaries[i + 1]]
            
            controlled_chapters.append(chapter_content)
        
        return controlled_chapters
    
    def _apply_spacing_rules(self, content: List[Dict]) -> List[Dict]:
        """Apply spacing rules to content."""
        if not content:
            return content
        
        controlled_content = []
        last_effect_position = -self.sparsity_rules['minimum_effect_spacing']
        consecutive_effects = 0
        
        for i, item in enumerate(content):
            effects = item.get('effects', [])
            
            # Check spacing rule
            spacing_violation = (i - last_effect_position) < self.sparsity_rules['minimum_effect_spacing']
            
            # Check consecutive effects rule
            consecutive_violation = consecutive_effects >= self.sparsity_rules['maximum_consecutive_effects']
            
            # Remove effects if rules are violated
            if effects and (spacing_violation or consecutive_violation):
                item = {**item, 'effects': []}
                logger.debug(f"Removed effects from position {i} due to spacing/consecutive rules")
            
            # Update tracking variables
            if item.get('effects'):
                last_effect_position = i
                consecutive_effects += 1
            else:
                consecutive_effects = 0
            
            controlled_content.append(item)
        
        return controlled_content
    
    def _calculate_final_density(self, chapters: List[List[Dict]]) -> float:
        """Calculate the final effect density."""
        total_segments = 0
        segments_with_effects = 0
        
        for chapter in chapters:
            for item in chapter:
                total_segments += 1
                if item.get('effects'):
                    segments_with_effects += 1
        
        return segments_with_effects / total_segments if total_segments > 0 else 0.0
    
    def _count_spacing_violations(self, original_markup: Dict[str, Any], 
                                controlled_markup: List[List[Dict]]) -> int:
        """Count spacing violations that were fixed."""
        violations_fixed = 0
        
        # Count original violations
        original_violations = 0
        all_original_content = []
        for chapter in original_markup.get('chapters', []):
            all_original_content.extend(chapter.get('content', []))
        
        last_effect_position = -self.sparsity_rules['minimum_effect_spacing']
        for i, item in enumerate(all_original_content):
            if item.get('effects'):
                if (i - last_effect_position) < self.sparsity_rules['minimum_effect_spacing']:
                    original_violations += 1
                last_effect_position = i
        
        # Count final violations
        final_violations = 0
        all_final_content = []
        for chapter in controlled_markup:
            all_final_content.extend(chapter)
        
        last_effect_position = -self.sparsity_rules['minimum_effect_spacing']
        for i, item in enumerate(all_final_content):
            if item.get('effects'):
                if (i - last_effect_position) < self.sparsity_rules['minimum_effect_spacing']:
                    final_violations += 1
                last_effect_position = i
        
        violations_fixed = original_violations - final_violations
        return max(0, violations_fixed)
    
    def get_sparsity_metrics(self, markup: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive sparsity metrics."""
        total_segments = 0
        segments_with_effects = 0
        effect_distribution = {}
        chapter_densities = []
        
        for chapter in markup.get('chapters', []):
            chapter_segments = 0
            chapter_effects = 0
            
            for item in chapter.get('content', []):
                total_segments += 1
                chapter_segments += 1
                
                effects = item.get('effects', [])
                if effects:
                    segments_with_effects += 1
                    chapter_effects += 1
                    
                    # Count effect types
                    for effect in effects:
                        effect_type = effect.get('type', 'unknown')
                        effect_distribution[effect_type] = effect_distribution.get(effect_type, 0) + 1
            
            # Calculate chapter density
            if chapter_segments > 0:
                chapter_density = chapter_effects / chapter_segments
                chapter_densities.append(chapter_density)
        
        return {
            'total_segments': total_segments,
            'segments_with_effects': segments_with_effects,
            'global_effect_density': segments_with_effects / total_segments if total_segments > 0 else 0.0,
            'effect_distribution': effect_distribution,
            'chapter_density_average': sum(chapter_densities) / len(chapter_densities) if chapter_densities else 0.0,
            'chapter_density_variance': self._calculate_variance(chapter_densities),
            'sparsity_compliance': self._check_sparsity_compliance(markup)
        }
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values."""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        squared_diff_sum = sum((value - mean) ** 2 for value in values)
        return squared_diff_sum / (len(values) - 1)
    
    def _check_sparsity_compliance(self, markup: Dict[str, Any]) -> Dict[str, bool]:
        """Check if the markup complies with sparsity rules."""
        compliance = {}
        
        # Check global density
        total_segments = 0
        segments_with_effects = 0
        
        for chapter in markup.get('chapters', []):
            for item in chapter.get('content', []):
                total_segments += 1
                if item.get('effects'):
                    segments_with_effects += 1
        
        global_density = segments_with_effects / total_segments if total_segments > 0 else 0.0
        compliance['global_density_rule'] = global_density <= self.sparsity_rules['global_effect_density']
        
        # Check chapter limits
        chapter_violations = 0
        for chapter in markup.get('chapters', []):
            content = chapter.get('content', [])
            chapter_type = self._determine_chapter_type(chapter)
            chapter_multiplier = self.chapter_type_multipliers.get(chapter_type, 1.0)
            chapter_limit = int(len(content) * self.sparsity_rules['chapter_effect_limit'] * chapter_multiplier)
            
            chapter_effects = sum(1 for item in content if item.get('effects'))
            if chapter_effects > chapter_limit:
                chapter_violations += 1
        
        compliance['chapter_limit_rule'] = chapter_violations == 0
        
        # Check spacing rules
        spacing_violations = 0
        last_effect_position = -self.sparsity_rules['minimum_effect_spacing']
        
        for chapter in markup.get('chapters', []):
            for i, item in enumerate(chapter.get('content', [])):
                if item.get('effects'):
                    if (i - last_effect_position) < self.sparsity_rules['minimum_effect_spacing']:
                        spacing_violations += 1
                    last_effect_position = i
        
        compliance['spacing_rule'] = spacing_violations == 0
        
        return compliance
    
    def adjust_sparsity_rules(self, markup: Dict[str, Any], target_density: float) -> Dict[str, Any]:
        """Adjust sparsity rules to achieve a target effect density."""
        current_metrics = self.get_sparsity_metrics(markup)
        current_density = current_metrics['global_effect_density']
        
        if current_density > target_density:
            # Need to reduce effects
            reduction_factor = target_density / current_density
            self.sparsity_rules['global_effect_density'] *= reduction_factor
            self.sparsity_rules['chapter_effect_limit'] *= reduction_factor
        else:
            # Need to increase effects (but still maintain sparsity)
            increase_factor = min(1.5, target_density / current_density)
            self.sparsity_rules['global_effect_density'] *= increase_factor
            self.sparsity_rules['chapter_effect_limit'] *= increase_factor
        
        logger.info(f"Adjusted sparsity rules. Target density: {target_density:.3f}, "
                   f"Current density: {current_density:.3f}")
        
        return markup
