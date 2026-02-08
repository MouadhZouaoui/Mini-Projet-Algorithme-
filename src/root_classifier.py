"""
Arabic Triliteral Root Classifier

Classifies Arabic roots into morphological categories:
1. الصحيح (Sound)
2. المعتل (Weak)
3. المهموز (Hamzated)
4. المضعف (Doubled)

Author: [Your Name]
Date: [Today's Date]
"""

from enum import Enum
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

from arabic_utils import ArabicUtils
from arabic_types import RootCategory, RootAnalysis, SoundSubtype, WeakSubtype
class RootClassifier:
    """Classifies Arabic triliteral roots into morphological categories."""
    
    # Weak letters (و ي ا)
    WEAK_LETTERS = {'و', 'ي', 'ا', 'ى'}
    
    # Hamza letters and their forms
    HAMZA_LETTERS = {'ء', 'أ', 'إ', 'آ', 'ؤ', 'ئ'}
    
    # All possible hamza forms for matching
    HAMZA_VARIANTS = {
        'ء': ['ء'],
        'أ': ['أ', 'أ'],
        'إ': ['إ', 'إ'],
        'آ': ['آ'],
        'ؤ': ['ؤ'],
        'ئ': ['ئ']
    }
    
    @staticmethod
    def classify(root: str) -> RootAnalysis:
        """
        Classify an Arabic triliteral root.
        Now handles roots with shadda.
        
        Args:
            root (str): Arabic root (3 letters, may include shadda)
            
        Returns:
            RootAnalysis: Complete analysis of the root
        """
        # First, expand shadda to get the actual letters
        normalized_root = ArabicUtils.normalize_arabic(root, aggressive=False, expand_shadda=True)
        
        if len(normalized_root) != 3:
            return RootAnalysis(
                root=root,
                category=RootCategory.UNKNOWN,
                subtype=None,
                weak_positions=[],
                hamza_positions=[],
                is_doubled=False,
                description=f"Invalid root length after normalization: {len(normalized_root)}"
            )
        
        
        # Check for doubled letters (second and third same)
        # Use the expanded root for this check
        is_doubled = (normalized_root[1] == normalized_root[2] and 
                     normalized_root[1] not in RootClassifier.WEAK_LETTERS)
        
        # Rest of the classification logic remains the same
        # but use the normalized (shadda-expanded) version
        hamza_positions = RootClassifier._find_hamza_positions(normalized_root)
        weak_positions = RootClassifier._find_weak_positions(normalized_root)
        
        # Determine category
        category, subtype, description = RootClassifier._determine_category(
            normalized_root, hamza_positions, weak_positions, is_doubled
        )
        
        # Update description to mention shadda if present
        if 'ّ' in root:
            description += " (contains shadda)"
        
        return RootAnalysis(
                root=normalized_root,
                category=category,
                subtype=subtype,
                weak_positions=weak_positions,
                hamza_positions=hamza_positions,
                is_doubled=is_doubled,
                description=description
        )
            
    
    @staticmethod
    def _normalize_for_analysis(root: str) -> str:
        """Normalize root for analysis."""
        # Replace hamza variants with standard hamza for consistent analysis
        hamza_map = {
            'أ': 'ء', 'إ': 'ء', 'آ': 'ء',
            'ؤ': 'ء', 'ئ': 'ء'
        }
        
        normalized = root
        for variant, standard in hamza_map.items():
            normalized = normalized.replace(variant, standard)
        
        return normalized
    
    @staticmethod
    def _find_hamza_positions(root: str) -> List[int]:
        """Find positions of hamza in root."""
        positions = []
        for i, char in enumerate(root):
            if char in RootClassifier.HAMZA_LETTERS:
                positions.append(i)
        return positions
    
    @staticmethod
    def _find_weak_positions(root: str) -> List[int]:
        """Find positions of weak letters in root."""
        positions = []
        for i, char in enumerate(root):
            if char in RootClassifier.WEAK_LETTERS:
                positions.append(i)
        return positions
    
    @staticmethod
    def _determine_category(root: str, hamza_positions: List[int], 
                           weak_positions: List[int], is_doubled: bool) -> Tuple[RootCategory, Optional[str], str]:
        """Determine the morphological category of the root."""
        
        # Handle hamzated roots (مهموز)
        if hamza_positions:
            if len(hamza_positions) == 1:
                hamza_position = hamza_positions[0]
                if hamza_position == 0:
                    subtype = "مهموز الفاء"
                    desc = "همزة في الحرف الأول"
                elif hamza_position == 1:
                    subtype = "مهموز العين"
                    desc = "همزة في الحرف الثاني"
                else:  # hamza_position == 2
                    subtype = "مهموز اللام"
                    desc = "همزة في الحرف الثالث"
                
                return RootCategory.HAMZATED, subtype, desc
            
            else:
                return RootCategory.HAMZATED, "مهموز متعدد", "أكثر من همزة في الجذر"
        
        # Handle doubled roots (مضعف)
        if is_doubled:
            return RootCategory.DOUBLED, "مضعف", "الحرفان الثاني والثالث متطابقان"
        
        # Handle weak roots (معتل)
        if weak_positions:
            weak_count = len(weak_positions)
            
            if weak_count == 1:
                pos = weak_positions[0]
                if pos == 0:
                    subtype = WeakSubtype.FIRST_RADICAL_WEAK.value
                    desc = "حرف علة في الموقع الأول (مثال)"
                elif pos == 1:
                    subtype = WeakSubtype.SECOND_RADICAL_WEAK.value
                    desc = "حرف علة في الموقع الثاني (أجوف)"
                else:  # pos == 2
                    subtype = WeakSubtype.THIRD_RADICAL_WEAK.value
                    desc = "حرف علة في الموقع الثالث (ناقص)"
            
            elif weak_count == 2:
                # Check which type of double weak
                if weak_positions == [0, 2]:
                    subtype = WeakSubtype.DOUBLE_WEAK_SEPARATED.value
                    desc = "لفيف مفروق: حرف علة في الأول والثالث"
                elif weak_positions == [1, 2]:
                    subtype = WeakSubtype.DOUBLE_WEAK_JOINED.value
                    desc = "لفيف مقرون: حرف علة في الثاني والثالث"
                else:
                    subtype = "لفيف آخر"
                    desc = "نوع آخر من اللفيف"
            else:
                subtype = "معتل كامل"
                desc = "جميع الأحرف حروف علة"
            
            return RootCategory.WEAK, subtype, desc
        
        # If no special characteristics, it's sound perfect
        return RootCategory.SOUND, SoundSubtype.SOUND_PERFECT.value, "صحيح سالم: لا حروف علة ولا همزة ولا إعلال"
    
    @staticmethod
    def get_examples() -> Dict[str, List[str]]:
        """Get example roots for each category."""
        return {
            "صحيح سالم": ["كتب", "جلس", "درس", "فهم", "سمع"],
            "مهموز الفاء": ["أكل", "أخذ", "أمر"],
            "مهموز العين": ["سأل", "رأى", "بئس"],
            "مهموز اللام": ["قرأ", "بدأ", "ملأ"],
            "مثال": ["وعد", "يسر", "وجد", "وضع"],
            "أجوف": ["قال", "باع", "خاف", "نام"],
            "ناقص": ["دعا", "رمى", "سعى", "غزا"],
            "لفيف مفروق": ["وفى", "وقى", "وحي"],
            "لفيف مقرون": ["طوى", "حيى", "سوى"],
            "مضعف": ["مدّ", "شدّ", "فرّ", "حبّ"]
        }
    
    @staticmethod
    def get_pattern_adjustments(root_type: str) -> Dict[str, str]:
        """
        Get pattern adjustments for specific root types.
        
        Args:
            root_type (str): The root subtype
            
        Returns:
            Dict: Pattern adjustments
        """
        adjustments = {
            "أجوف": {
                # For hollow roots, the middle weak letter often changes
                "فاعل": "1اء3",  # قال -> قائل (و -> ء)
                "مفعول": "م1و2و3",  # قال -> مقول (ألف becomes واو in some forms)
                "يفعل": "ي1و2و3",  # قال -> يقول
            },
            "ناقص": {
                # For defective roots, final weak letter changes
                "فاعل": "1ا2ي",  # رمى -> رامي
                "مفعول": "م1و2ى",  # رمى -> مرمى
            },
        }
        
        return adjustments.get(root_type, {})
    
    @staticmethod
    def analyze_all_roots(roots: List[str]) -> Dict[str, List[RootAnalysis]]:
        """
        Analyze multiple roots and group by category.
        
        Args:
            roots (List[str]): List of Arabic roots
            
        Returns:
            Dict: Roots grouped by category
        """
        categorized = {
            "صحيح سالم": [],
            "مهموز": [],
            "مثال": [],
            "أجوف": [],
            "ناقص": [],
            "لفيف": [],
            "مضعف": [],
            "آخر": []
        }
        
        for root in roots:
            analysis = RootClassifier.classify(root)
            
            if analysis.category == RootCategory.SOUND:
                categorized["صحيح سالم"].append(analysis)
            elif analysis.category == RootCategory.HAMZATED:
                categorized["مهموز"].append(analysis)
            elif analysis.category == RootCategory.WEAK:
                if "مثال" in analysis.subtype:
                    categorized["مثال"].append(analysis)
                elif "أجوف" in analysis.subtype:
                    categorized["أجوف"].append(analysis)
                elif "ناقص" in analysis.subtype:
                    categorized["ناقص"].append(analysis)
                elif "لفيف" in analysis.subtype:
                    categorized["لفيف"].append(analysis)
            elif analysis.category == RootCategory.DOUBLED:
                categorized["مضعف"].append(analysis)
            else:
                categorized["آخر"].append(analysis)
        
        return categorized

    @staticmethod
    def generate_with_root_type(root: str, pattern_template: str, pattern_name: str = "") -> str:
        """
        Generate word with root type consideration.
        
        Args:
            root (str): Arabic root
            pattern_template (str): Pattern template
            pattern_name (str): Pattern name for specific rules
            
        Returns:
            str: Generated word
        """

        normalized_root = ArabicUtils.normalize_arabic(root, aggressive=False, expand_shadda=True)
        # Classify the root
        analysis = RootClassifier.classify(normalized_root)
                
        # Generate basic word
        basic_word = ArabicUtils.apply_pattern(normalized_root, pattern_template)
        
        # Apply specific transformations based on root type and pattern
        transformed_word = RootClassifier._transform_by_root_type(
            basic_word, normalized_root, pattern_template, pattern_name, analysis
        )
        
        return transformed_word
    
    @staticmethod
    def _transform_by_root_type(word: str, root: str, pattern: str, 
                               pattern_name: str, analysis) -> str:
        """
        Apply specific transformations based on root type.
        
        Args:
            word (str): Basic generated word
            root (str): Arabic root
            pattern (str): Pattern template
            pattern_name (str): Pattern name
            analysis: RootAnalysis object
            
        Returns:
            str: Transformed word
        """
        # Default transformation
        result = word
        
        # Get root type for easier checking
        root_type = analysis.subtype or ""
        category = analysis.category
        
        # Handle specific cases
        if "أجوف" in root_type:  # Hollow roots
            result = RootClassifier._handle_hollow_root(word, root, pattern, pattern_name)
        
        elif "ناقص" in root_type:  # Defective roots
            result = RootClassifier._handle_defective_root(word, root, pattern, pattern_name)
        
        elif "مثال" in root_type:  # First radical weak
            result = RootClassifier._handle_first_weak_root(word, root, pattern, pattern_name)
        
        elif category == RootCategory.HAMZATED:  # Hamzated roots
            result = RootClassifier._handle_hamzated_root(word, root, pattern, pattern_name)
        
        elif category == RootCategory.DOUBLED:  # Doubled roots
            result = RootClassifier._handle_doubled_root(word, root, pattern, pattern_name)
        
        return result
    
    @staticmethod
    def _handle_hollow_root(word: str, root: str, pattern: str, pattern_name: str) -> str:
        """Handle hollow roots (second radical weak)."""
        # Default: return as is
        result = word
        
        # Specific pattern adjustments
        pattern_adjustments = {
            "فاعل": lambda w, r: r[0] + 'ائ' + r[2],  # قال -> قائل
            "يفعل": lambda w, r: 'ي' + r[0] + 'و' + r[2],  # قال -> يقول
            "مفعول": lambda r: 'م' + r[0] + 'و' + r[2]
            }
        
        if pattern_name in pattern_adjustments:
            result = pattern_adjustments[pattern_name](word, root)
        
        return result
    
    @staticmethod
    def _handle_defective_root(word: str, root: str, pattern: str, pattern_name: str) -> str:
        """Handle defective roots (third radical weak)."""
        result = word
        
        # Expand shadda to get actual letters
        expanded_root = ArabicUtils.expand_shadda(root)
        
        # Helper function for مفعول pattern
        def mafool_defective(w, r):
            """Generate مفعول for defective root."""
            third_radical = r[2]
            
            # Determine ending based on original weak letter
            if third_radical in ['و', 'ا']:
                ending = 'و'  # دعا -> مدعو
            elif third_radical in ['ي', 'ى']:
                ending = 'ى'  # رمى -> مرمى
            else:
                ending = 'و'  # Default
            
            return 'م' + r[0] + r[1] + ending
        
        pattern_adjustments = {
            "فاعل": lambda w, r: r[0] + 'ا' + r[1] + 'ي',  # رمى -> رامي
            "مفعول": mafool_defective,  # دعا -> مدعو, رمى -> مرمى
            "يفعل": lambda w, r: 'ي' + r[0] + r[1] + 'ي',  # رمى -> يرمي
        }
        
        if pattern_name in pattern_adjustments:
            result = pattern_adjustments[pattern_name](word, expanded_root)
        
        return result
    
    @staticmethod
    def _handle_first_weak_root(word: str, root: str, pattern: str, pattern_name: str) -> str:
        """Handle roots with weak first radical."""
        result = word
        # وعد -> عاهد in some forms, but this is complex
        return result
    
    @staticmethod
    def _handle_doubled_root(word: str, root: str, pattern: str, pattern_name: str) -> str:
        """Handle doubled roots (second and third same)."""
        result = word
                
        if pattern_name == "فاعل":
            # مدّ -> ماد (don't double in فاعل pattern)
            result = root[0] + 'ا' + root[1]
        
        return result
    
    @staticmethod
    def _handle_hamzated_root(word: str, root: str, pattern: str, pattern_name: str) -> str:
        """Handle hamzated roots with proper hamza seats."""
        result = word
                
        # For فاعل pattern with hamza in third position
        if pattern_name == "فاعل":
            if root[2] in ['ء', 'أ', 'إ', 'آ', 'ؤ', 'ئ']:
                # قرأ -> قارئ (hamza on ya seat after long alif)
                result = root[0] + 'ا' + root[1] + 'ئ'
            elif root[0] in ['ء', 'أ', 'إ', 'آ', 'ؤ', 'ئ']:
            # First radical is hamza: أكل -> آكل
                result = 'آ' + root[1] + root[2]
        
        # For مفعول pattern - keep as is (already works)
        
        return result