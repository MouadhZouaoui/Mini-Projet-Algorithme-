"""
Arabic text utilities for morphological processing.

Features:
- Arabic character normalization
- Root extraction and validation
- Pattern matching helpers
- Unicode utilities for Arabic script
"""

import re
from typing import Optional, List, Tuple

from arabic_types import RootCategory
class ArabicUtils:
    """Utilities for handling Arabic text in morphological processing."""
    
    # All Arabic letters 
    ARABIC_LETTERS = {
        # Base Arabic letters
        'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص',
        'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي',
        
        # Hamza and its forms
        'ء', 'آ', 'أ', 'إ', 'ئ', 'ؤ',
        
        # Other Arabic letters
        'ة', 'ى', 'ٱ', 'ە',
        
        # Persian/Arabic extensions
        'پ', 'چ', 'ژ', 'گ', 'ڤ',
    }

    NORMALIZATION_MAP = {
        'آ': 'ا',    # Maddah alef to alef
        'أ': 'ا',    # Alef with hamza above to alef
        'إ': 'ا',    # Alef with hamza below to alef
        'ٱ': 'ا',    # Alef wasla to alef
        'ى': 'ي',    # Alef maqsura to ya
        'ة': 'ه',    # Ta marbuta to ha
        'ؤ': 'و',    # Waw with hamza to waw
        'ئ': 'ي',    # Ya with hamza to ya
    }
    
    # Diacritics (tashkeel) to remove
    DIACRITICS = {
        '\u064B', '\u064C', '\u064D', '\u064E', '\u064F', '\u0650',
        '\u0651', '\u0652', '\u0653', '\u0654', '\u0655'
    }

    ## Handles Shadda roots
    @staticmethod
    def expand_shadda(text: str) -> str:
        """
        Expand shadda (ّ) by doubling the letter before it.
        
        Example: 
        - "مدّ" -> "مدد"
        - "شدّ" -> "شدد"
        
        Args:
            text (str): Arabic text with shadda
            
        Returns:
            str: Text with shadda expanded
        """
        if not text:
            return text
        
        result = []
        i = 0
        while i < len(text):
            # Check if current character is a letter that might have shadda
            if i + 1 < len(text) and text[i + 1] == '\u0651':  # Shadda
                # Double the letter and skip the shadda
                result.append(text[i])
                result.append(text[i])
                i += 2
            else:
                result.append(text[i])
                i += 1
        
        return ''.join(result)
    
    @staticmethod
    def normalize_arabic(text: str, aggressive: bool = False, expand_shadda: bool = True) -> str:
        """
        Normalize Arabic text with shadda expansion option.
        
        Args:
            text (str): Input Arabic text
            aggressive (bool): If True, normalize hamza and variations
            expand_shadda (bool): If True, expand shadda to double letters
            
        Returns:
            str: Normalized text
        """
        if not text:
            return ""
        
        # Expand shadda first if requested
        if expand_shadda:
            text = ArabicUtils.expand_shadda(text)
        
        # Remove diacritics (except shadda which we already handled)
        for diacritic in ArabicUtils.DIACRITICS:
            text = text.replace(diacritic, '')
        
        if aggressive:
            # Apply full normalization
            for variant, standard in ArabicUtils.NORMALIZATION_MAP.items():
                text = text.replace(variant, standard)
        else:
            # Preserve hamza for root letters
            for variant, standard in [('آ', 'ا'), ('إ', 'ا'), ('ٱ', 'ا'), ('ى', 'ي'), ('ة', 'ه')]:
                text = text.replace(variant, standard)
        
        # Remove non-Arabic characters
        text = re.sub(r'[^\u0600-\u06FF\s]', '', text)
        
        return text.strip()
    
    @staticmethod
    def is_valid_root(root: str) -> bool:
        """
        Check if a string is a valid Arabic triliteral root.
        Now handles shadda and Alif Maqsura.
        
        Args:
            root (str): String to check
            
        Returns:
            bool: True if valid 3-letter Arabic root
        """
        if not root:
            return False
        
        # First expand shadda
        expanded_root = ArabicUtils.expand_shadda(root)
        
        # Now check length - should be 3 letters after expanding shadda
        if len(expanded_root) != 3:
            return False
        
        # Check each character is an Arabic letter (ignoring diacritics)
        for char in expanded_root:
            if char not in ArabicUtils.ARABIC_LETTERS and not ArabicUtils.is_diacritic(char):
                return False
        
        return True
    
    @staticmethod
    def extract_possible_root(word: str, pattern_template: str) -> Optional[str]:
        """
        Attempt to extract root from word using pattern template.
        
        Args:
            word (str): Arabic word
            pattern_template (str): Pattern template (e.g., "1ا2و3")
            
        Returns:
            Optional[str]: Extracted root or None
        """
        if not word or not pattern_template:
            return None
        
        # Normalize both
        word = ArabicUtils.normalize_arabic(word)
        
        # Create root placeholder
        root_chars = ['', '', '']
        
        i, j = 0, 0
        while i < len(word) and j < len(pattern_template):
            if pattern_template[j] in '123':
                root_index = int(pattern_template[j]) - 1
                if root_index < 3:
                    # Take the Arabic character (may be 1 or more bytes in UTF-8, but in Python string it's fine)
                    if i < len(word):
                        root_chars[root_index] = word[i]
                        i += 1
                j += 1
            else:
                # Skip fixed pattern character if it matches word
                if i < len(word) and word[i] == pattern_template[j]:
                    i += 1
                j += 1
        
        # Check if we got all three root letters
        if all(root_chars) and len(''.join(root_chars)) == 3:
            return ''.join(root_chars)
        
        return None
    

    @staticmethod
    def apply_pattern(root: str, pattern_template: str) -> str:
        """
        Apply morphological pattern to root.
        
        Args:
            root (str): Arabic root (3 letters, may include shadda)
            pattern_template (str): Pattern template (e.g., "122ا3")
            
        Returns:
            str: Generated word
            
        Examples:
            >>> apply_pattern("كتب", "122ا3")
            'كتّاب'
            >>> apply_pattern("غفر", "122ا3")
            'غفّار'
            >>> apply_pattern("كتب", "1ا23")
            'كاتب'
        """
        # Expand shadda first (in case root contains shadda)
        expanded_root = ArabicUtils.expand_shadda(root)
        
        # Validate root length
        if len(expanded_root) != 3:
            raise ValueError(f"Root must be 3 letters after shadda expansion: {root}")
        
        result = []
        
        for char in pattern_template:
            if char.isdigit():
                # It's a root position indicator (1, 2, or 3)
                root_position = int(char)
                
                # Validate position
                if root_position < 1 or root_position > 3:
                    raise ValueError(f"Invalid root position '{char}' in template. Must be 1, 2, or 3.")
                
                # Get the corresponding letter from root (convert to 0-based index)
                root_idx = root_position - 1
                result.append(expanded_root[root_idx])
            else:
                # It's a fixed letter (ا, و, ي, م, etc.)
                result.append(char)
        
        return ''.join(result)



    # @staticmethod
    # def apply_pattern(root: str, pattern_template: str) -> str:
    #     """
    #     Apply morphological pattern to root.
    #     Now handles roots with shadda.
        
    #     Args:
    #         root (str): Arabic root (3 letters, may include shadda)
    #         pattern_template (str): Pattern template
            
    #     Returns:
    #         str: Generated word
    #     """
    #     # Expand shadda first
    #     expanded_root = ArabicUtils.expand_shadda(root)
        
    #     # Check if valid (after shadda expansion)
    #     if len(expanded_root) != 3:
    #         raise ValueError(f"Root must be 3 letters after shadda expansion: {root}")
        
    #     result = []
    #     i = 0  # Index in pattern template
    #     root_index = 0  # Index in expanded root
        
    #     while i < len(pattern_template):
    #         char = pattern_template[i]
            
    #         if char == '1':
    #             if root_index < len(expanded_root):
    #                 result.append(expanded_root[root_index])
    #                 root_index += 1
    #             i += 1
    #         elif char == '2':
    #             if root_index < len(expanded_root):
    #                 result.append(expanded_root[root_index])
    #                 root_index += 1
    #             i += 1
    #         elif char == '3':
    #             if root_index < len(expanded_root):
    #                 result.append(expanded_root[root_index])
    #                 root_index += 1
    #             i += 1
    #         else:
    #             # Check for multi-digit numbers (like 12, 23)
    #             if char.isdigit() and i + 1 < len(pattern_template) and pattern_template[i + 1].isdigit():
    #                 num_str = char
    #                 while i + 1 < len(pattern_template) and pattern_template[i + 1].isdigit():
    #                     num_str += pattern_template[i + 1]
    #                     i += 1
    #                 root_idx = int(num_str) - 1
    #                 if 0 <= root_idx < len(expanded_root):
    #                     result.append(expanded_root[root_idx])
    #                     root_index += 1
    #             elif char.isdigit():
    #                 root_idx = int(char) - 1
    #                 if 0 <= root_idx < len(expanded_root):
    #                     result.append(expanded_root[root_idx])
    #                     root_index += 1
    #             else:
    #                 result.append(char)
    #             i += 1
        
    #     return ''.join(result)
    

    @staticmethod
    def find_pattern_match(word: str, root: str, pattern_template: str) -> bool:
        """
        Check if word matches pattern for given root.
        
        Args:
            word (str): Arabic word to check
            root (str): Arabic root
            pattern_template (str): Pattern template
            
        Returns:
            bool: True if word matches pattern
        """
        try:
            # Generate word from root and pattern
            generated = ArabicUtils.apply_pattern(root, pattern_template)
            
            # Normalize both for comparison
            normalized_word = ArabicUtils.normalize_arabic(word, aggressive=False)
            normalized_generated = ArabicUtils.normalize_arabic(generated, aggressive=False)
            
            # First attempt: non-aggressive normalization
            if normalized_word == normalized_generated:
                return True
            
            # Second attempt: aggressive normalization
            aggressive_word = ArabicUtils.normalize_arabic(word, aggressive=True)
            aggressive_generated = ArabicUtils.normalize_arabic(generated, aggressive=True)
            
            if aggressive_word == aggressive_generated:
                return True
            
            # Third attempt: direct comparison (no normalization)
            if word == generated:
                return True
            
            return False
            
        except Exception as e:
            # If generation fails, it's not a match
            return False
    # @staticmethod
    # def find_pattern_match(word: str, root: str, pattern_template: str) -> bool:
    #     """
    #     Check if word matches pattern for given root.
    #     Uses less aggressive normalization for roots.
        
    #     Args:
    #         word (str): Arabic word to check
    #         root (str): Arabic root
    #         pattern_template (str): Pattern template
            
    #     Returns:
    #         bool: True if word matches pattern
    #     """
    #     # Generate word from root and pattern
    #     generated = ArabicUtils.apply_pattern(root, pattern_template)
        
    #     # Use less aggressive normalization for comparison
    #     # This preserves hamza in roots like "قرأ"
    #     normalized_word = ArabicUtils.normalize_arabic(word, aggressive=False)
    #     normalized_generated = ArabicUtils.normalize_arabic(generated, aggressive=False)
        
    #     # Also try with aggressive normalization for broader matching
    #     if normalized_word != normalized_generated:
    #         aggressive_word = ArabicUtils.normalize_arabic(word, aggressive=True)
    #         aggressive_generated = ArabicUtils.normalize_arabic(generated, aggressive=True)
    #         return aggressive_word == aggressive_generated
        
    #     return True
    
    @staticmethod
    def get_all_possible_roots(word: str) -> List[str]:
        """
        Generate all possible 3-letter roots from a word.
        This is a simplified approach - in reality, Arabic morphology is complex.
        
        Args:
            word (str): Arabic word
            
        Returns:
            List[str]: List of possible roots
        """
        word = ArabicUtils.normalize_arabic(word)
        possible_roots = []
        
        # Very simplified: take combinations of 3 letters from the word
        # This is for demonstration only
        if len(word) >= 3:
            # Take first, middle, last (common pattern)
            possible_roots.append(word[0] + word[len(word)//2] + word[-1])
            
            # Take first three
            possible_roots.append(word[:3])
            
            # Take last three
            possible_roots.append(word[-3:])
        
        # Remove duplicates and invalid roots
        valid_roots = []
        for root in set(possible_roots):
            if ArabicUtils.is_valid_root(root):
                valid_roots.append(root)
        
        return valid_roots
    
    @staticmethod
    def display_arabic_table(data: List[Tuple[str, str, str]]) -> str:
        """
        Format Arabic data in a readable table.
        
        Args:
            data: List of tuples (root, pattern, word)
            
        Returns:
            str: Formatted table string
        """
        if not data:
            return "No data to display"
        
        # Calculate column widths
        root_width = max(len(str(item[0])) for item in data) + 2
        pattern_width = max(len(str(item[1])) for item in data) + 2
        word_width = max(len(str(item[2])) for item in data) + 2
        
        # Create header
        table = "=" * (root_width + pattern_width + word_width + 8) + "\n"
        table += f"{'الجذر':<{root_width}} {'الوزن':<{pattern_width}} {'الكلمة':<{word_width}}\n"
        table += "=" * (root_width + pattern_width + word_width + 8) + "\n"
        
        # Add rows
        for root, pattern, word in data:
            table += f"{root:<{root_width}} {pattern:<{pattern_width}} {word:<{word_width}}\n"
        
        table += "=" * (root_width + pattern_width + word_width + 8)
        
        return table
    
    @staticmethod
    def preserve_hamza(text: str) -> str:
        """
        Preserve hamza in Arabic text.
        
        Args:
            text (str): Arabic text
            
        Returns:
            str: Text with preserved hamza
        """
        # This is a simplified approach - in reality, hamza rules are complex
        hamza_map = {
            'أ': 'أ',  # Alef with hamza above
            'إ': 'إ',  # Alef with hamza below
            'ؤ': 'ؤ',  # Waw with hamza
            'ئ': 'ئ',  # Ya with hamza
        }
        
        for plain, hamza in hamza_map.items():
            text = text.replace(plain, hamza)
        
        return text
    

    ########################THIS PART IS WHERE WE HANDLE WORD GENERATION WITH ROOT TYPE (  مشتد, مثال, أجوف, ناقص, لفيف .... )########################

    @staticmethod
    def apply_pattern_with_root_type(root: str, pattern_template: str, root_analysis) -> str:
        """
        Apply morphological pattern considering root type.
        
        Args:
            root (str): Arabic root
            pattern_template (str): Pattern template
            root_analysis: RootAnalysis object
            
        Returns:
            str: Generated word with root type adjustments
        """
        # For now, use basic application
        # We'll add special handling based on root type
        basic_result = ArabicUtils.apply_pattern(root, pattern_template)
        
        # Apply adjustments based on root type
        adjusted_result = ArabicUtils._adjust_for_root_type(
            basic_result, root, pattern_template, root_analysis
        )
        
        return adjusted_result
    
    @staticmethod
    def _adjust_for_root_type(word: str, root: str, pattern: str, analysis) -> str:
        """
        Adjust generated word based on root type.
        
        Args:
            word (str): Basic generated word
            root (str): Arabic root
            pattern (str): Pattern template
            analysis: RootAnalysis object
            
        Returns:
            str: Adjusted word
        """
        # Default: no adjustment
        adjusted = word
        
        # Handle hollow roots (أجوف)
        if "أجوف" in analysis.subtype:
            # Middle letter is weak (و/ي/ا)
            # In many patterns, it changes or disappears
            if pattern == "1ا23":  # فاعل pattern
                # Example: قال -> قائل (و becomes ء on ا)
                if root[1] in ['و', 'ي']:
                    # Replace middle with hamza on alif
                    adjusted = root[0] + 'ائ' + root[2]
            
            elif pattern == "123":  # فعل pattern (past tense)
                # Hollow root in past tense: و/ي becomes ا
                if root[1] in ['و', 'ي']:
                    adjusted = root[0] + 'ا' + root[2]
        
        # Handle defective roots (ناقص)
        elif "ناقص" in analysis.subtype:
            # Final letter is weak
            if pattern in ["1ا23", "12ا3"]:
                # Final weak letter often becomes ي
                if root[2] in ['و', 'ا', 'ى']:
                    adjusted = word[:-1] + 'ي'
        
        # Handle hamzated roots (مهموز)
        elif analysis.category == RootCategory.HAMZATED:
            # Preserve hamza properly
            adjusted = ArabicUtils.preserve_hamza(word)
        
        return adjusted
    
    @staticmethod
    def is_diacritic(char: str) -> bool:
        """Check if character is a diacritic."""
        return char in ArabicUtils.DIACRITICS or char == '\u0651'  # Include shadda