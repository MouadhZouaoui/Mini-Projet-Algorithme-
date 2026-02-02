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

class ArabicUtils:
    """Utilities for handling Arabic text in morphological processing."""
    
    # Arabic letters (isolated forms for reference)
    ARABIC_LETTERS = {
        'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص',
        'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي',
        'ء', 'آ', 'أ', 'إ', 'ئ', 'ؤ', 'ة'
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
    
    @staticmethod
    def normalize_arabic(text: str, aggressive: bool = False) -> str:
        """
        Normalize Arabic text with configurable aggression level.
        
        Args:
            text (str): Input Arabic text
            aggressive (bool): If True, normalize hamza and variations.
                              If False, preserve root letters.
        
        Returns:
            str: Normalized text
        """
        if not text:
            return ""
        
        # Remove diacritics (always)
        for diacritic in ArabicUtils.DIACRITICS:
            text = text.replace(diacritic, '')
        
        if aggressive:
            # Apply full normalization (for word matching)
            for variant, standard in ArabicUtils.NORMALIZATION_MAP.items():
                text = text.replace(variant, standard)
        else:
            # Preserve hamza for root letters
            # Only normalize non-root variations
            for variant, standard in [('آ', 'ا'), ('إ', 'ا'), ('ٱ', 'ا'), ('ى', 'ي'), ('ة', 'ه')]:
                text = text.replace(variant, standard)
        
        # Remove non-Arabic characters
        text = re.sub(r'[^\u0600-\u06FF\s]', '', text)
        
        return text.strip()
    
    @staticmethod
    def is_valid_root(root: str) -> bool:
        """
        Check if a string is a valid Arabic triliteral root.
        
        Args:
            root (str): String to check
            
        Returns:
            bool: True if valid 3-letter Arabic root
        """
        if not root or len(root) != 3:
            return False
        
        # Check each character is an Arabic letter
        for char in root:
            if char not in ArabicUtils.ARABIC_LETTERS:
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
        Apply morphological pattern to root with better handling.
        
        Args:
            root (str): Arabic root (3 letters)
            pattern_template (str): Pattern template
        
        Returns:
            str: Generated word
        """
        if not ArabicUtils.is_valid_root(root):
            raise ValueError(f"Invalid root: {root}")
        
        result = []
        i = 0  # Index in pattern template
        j = 0  # Index in root
        
        while i < len(pattern_template):
            char = pattern_template[i]
            
            if char == '1':
                if j < len(root):
                    result.append(root[j])
                    j += 1
                i += 1
            elif char == '2':
                if j < len(root):
                    result.append(root[j])
                    j += 1
                i += 1
            elif char == '3':
                if j < len(root):
                    result.append(root[j])
                    j += 1
                i += 1
            else:
                # Check if next character is a number (for multi-digit patterns)
                if i + 1 < len(pattern_template) and pattern_template[i + 1].isdigit():
                    # Handle combined numbers (like 12, 23) - rare but possible
                    if char.isdigit():
                        num = char
                        while i + 1 < len(pattern_template) and pattern_template[i + 1].isdigit():
                            num += pattern_template[i + 1]
                            i += 1
                        root_index = int(num) - 1
                        if root_index < len(root):
                            result.append(root[root_index])
                            j += 1
                    else:
                        result.append(char)
                else:
                    result.append(char)
                i += 1
        
        return ''.join(result)
    
    @staticmethod
    def find_pattern_match(word: str, root: str, pattern_template: str) -> bool:
        """
        Check if word matches pattern for given root.
        Uses less aggressive normalization for roots.
        
        Args:
            word (str): Arabic word to check
            root (str): Arabic root
            pattern_template (str): Pattern template
            
        Returns:
            bool: True if word matches pattern
        """
        # Generate word from root and pattern
        generated = ArabicUtils.apply_pattern(root, pattern_template)
        
        # Use less aggressive normalization for comparison
        # This preserves hamza in roots like "قرأ"
        normalized_word = ArabicUtils.normalize_arabic(word, aggressive=False)
        normalized_generated = ArabicUtils.normalize_arabic(generated, aggressive=False)
        
        # Also try with aggressive normalization for broader matching
        if normalized_word != normalized_generated:
            aggressive_word = ArabicUtils.normalize_arabic(word, aggressive=True)
            aggressive_generated = ArabicUtils.normalize_arabic(generated, aggressive=True)
            return aggressive_word == aggressive_generated
        
        return True
    
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