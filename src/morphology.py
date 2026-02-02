"""
Core morphological engine for Arabic word generation and validation.

This module connects:
- AVL Tree (for roots storage)
- Hash Table (for patterns storage)
- Arabic Utilities (for text processing)

Author: [Your Name]
Date: [Today's Date]
"""

from typing import Dict, List, Tuple, Optional, Any
from avl_tree import AVLTree, AVLNode
from hash_table import HashTable
from arabic_utils import ArabicUtils

class MorphologicalEngine:
    """Main engine for Arabic morphological operations."""
    
    def __init__(self):
        """Initialize the morphological engine with empty data structures."""
        self.roots_tree = AVLTree()
        self.patterns_table = HashTable()
        
    def load_roots(self, roots: List[str]) -> None:
        """
        Load Arabic roots into AVL tree.
        
        Args:
            roots (List[str]): List of Arabic roots (3 letters each)
        """
        print(f"📥 Loading {len(roots)} roots into AVL tree...")
        
        for root in roots:
            if ArabicUtils.is_valid_root(root):
                self.roots_tree.insert(root)
        
        print(f"✅ Loaded {self.roots_tree.count_nodes()} valid roots")
    
    def load_patterns(self, patterns: Dict[str, Dict]) -> None:
        """
        Load morphological patterns into hash table.
        
        Args:
            patterns (Dict[str, Dict]): Dictionary of pattern_name -> pattern_data
        """
        print(f"📥 Loading {len(patterns)} patterns into hash table...")
        
        for pattern_name, pattern_data in patterns.items():
            self.patterns_table.insert(pattern_name, pattern_data)
        
        print(f"✅ Loaded {len(self.patterns_table)} patterns")
    
    def generate_word(self, root: str, pattern_name: str) -> Optional[Dict[str, Any]]:
        """
        Generate a word from root and pattern.
        
        Args:
            root (str): Arabic root (3 letters)
            pattern_name (str): Name of morphological pattern
            
        Returns:
            Optional[Dict]: Dictionary with generation results or None if error
        """
        # Validate root
        if not ArabicUtils.is_valid_root(root):
            print(f"❌ Invalid root: {root}")
            return None
        
        # Get pattern from hash table
        pattern_data = self.patterns_table.search(pattern_name)
        if not pattern_data:
            print(f"❌ Pattern not found: {pattern_name}")
            return None
        
        # Get template from pattern data
        template = pattern_data.get('template')
        if not template:
            print(f"❌ No template found in pattern: {pattern_name}")
            return None
        
        try:
            # Generate the word
            generated_word = ArabicUtils.apply_pattern(root, template)
            
            # Validate the generated word (optional check)
            is_valid = self.validate_word(generated_word, root)['is_valid']
            
            if is_valid:
                root_node = self.roots_tree.search(root)
                if root_node:
                    root_node.add_derivative(generated_word, pattern_name)
            
            result = {
                'root': root,
                'pattern': pattern_name,
                'template': template,
                'generated_word': generated_word,
                'is_valid': is_valid,
                'description': pattern_data.get('description', ''),
                'example': pattern_data.get('example', '')
            }
            
            
            return result
            
        except Exception as e:
            print(f"❌ Error generating word: {e}")
            return None
    
    def generate_all_for_root(self, root: str) -> List[Dict[str, Any]]:
        """
        Generate words for a root using all available patterns.
        
        Args:
            root (str): Arabic root
            
        Returns:
            List[Dict]: List of generation results
        """
        if not ArabicUtils.is_valid_root(root):
            print(f"❌ Invalid root: {root}")
            return []
        
        results = []
        
        # Get all patterns
        all_patterns = self.patterns_table.get_all_patterns()
        
        print(f"🔮 Generating words for root '{root}' with {len(all_patterns)} patterns...")
        
        for pattern_name, pattern_data in all_patterns:
            result = self.generate_word(root, pattern_name)
            if result:
                results.append(result)
        
        return results
    
    def validate_word(self, word: str, root: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate if a word belongs to a root (or find possible roots).
        
        Args:
            word (str): Arabic word to validate
            root (Optional[str]): Specific root to check against (if None, try all)
            
        Returns:
            Dict: Validation results
        """
        # Normalize the word
        normalized_word = ArabicUtils.normalize_arabic(word)
        
        if root:
            # Check against specific root
            return self._validate_against_root(normalized_word, root)
        else:
            # Try to find matching root and pattern
            return self._find_matching_root_and_pattern(normalized_word)
    
    def _validate_against_root(self, word: str, root: str) -> Dict[str, Any]:
        """
        Validate word against a specific root.
        
        Args:
            word (str): Arabic word
            root (str): Arabic root
            
        Returns:
            Dict: Validation results
        """
        if not ArabicUtils.is_valid_root(root):
            return {
                'word': word,
                'root': root,
                'is_valid': False,
                'message': f"Invalid root: {root}"
            }
        
        # Check if root exists in tree
        root_node = self.roots_tree.search(root)
        if not root_node:
            return {
                'word': word,
                'root': root,
                'is_valid': False,
                'message': f"Root '{root}' not found in database"
            }
        
        # Try all patterns to see if any match
        all_patterns = self.patterns_table.get_all_patterns()
        
        for pattern_name, pattern_data in all_patterns:
            template = pattern_data.get('template', '')
            
            if ArabicUtils.find_pattern_match(word, root, template):
                return {
                    'word': word,
                    'root': root,
                    'is_valid': True,
                    'pattern': pattern_name,
                    'template': template,
                    'message': f"Word belongs to root '{root}' with pattern '{pattern_name}'"
                }
        
        return {
            'word': word,
            'root': root,
            'is_valid': False,
            'message': f"Word does not belong to root '{root}' with any known pattern"
        }
    
    def _find_matching_root_and_pattern(self, word: str) -> Dict[str, Any]:
        """
        Find which root and pattern produce this word.
        
        Args:
            word (str): Arabic word
            
        Returns:
            Dict: Matching results
        """
        # Get all patterns
        all_patterns = self.patterns_table.get_all_patterns()
        
        # Try all roots in the tree (this is computationally expensive)
        # For demonstration, we'll use a smarter approach
        all_roots = self.roots_tree.display_inorder()
        
        print(f"🔍 Searching for matches among {len(all_roots)} roots and {len(all_patterns)} patterns...")
        
        matches = []
        
        # Try common roots first (optional optimization)
        for root in all_roots:
            for pattern_name, pattern_data in all_patterns:
                template = pattern_data.get('template', '')
                
                if ArabicUtils.find_pattern_match(word, root, template):
                    matches.append({
                        'root': root,
                        'pattern': pattern_name,
                        'template': template,
                        'description': pattern_data.get('description', '')
                    })
        
        if matches:
            return {
                'word': word,
                'is_valid': True,
                'matches': matches,
                'message': f"Found {len(matches)} possible derivation(s)"
            }
        else:
            # Try to extract possible roots from the word itself
            possible_roots = ArabicUtils.get_all_possible_roots(word)
            
            return {
                'word': word,
                'is_valid': False,
                'possible_roots': possible_roots,
                'message': f"No derivation found. Possible roots: {possible_roots}"
            }
    
    def get_root_statistics(self, root: str) -> Dict[str, Any]:
        """
        Get statistics for a specific root.
        
        Args:
            root (str): Arabic root
            
        Returns:
            Dict: Statistics about the root
        """
        root_node = self.roots_tree.search(root)
        
        if not root_node:
            return {
                'root': root,
                'exists': False,
                'message': f"Root '{root}' not found"
            }
        # Get generated words for this root
        derivatives = root_node.get_derivatives()
        
        return {
            'root': root,
            'exists': True,
            'frequency': root_node.frequency,
            'derivative_count': len(derivatives),
            'derivatives': derivatives[:10]  # Limit to 10
        }
    
    def get_engine_statistics(self) -> Dict[str, Any]:
        """Get overall statistics."""
        total_roots = self.roots_tree.count_nodes()
        total_patterns = len(self.patterns_table)
    
    # Calculate derivatives across all nodes
        total_derivatives = 0
        roots_with_derivatives = 0
    
        all_nodes = self.roots_tree.get_all_nodes()
        for node in all_nodes:
            deriv_count = node.get_derivative_count()
            if deriv_count > 0:
                roots_with_derivatives += 1
                total_derivatives += deriv_count
    
        return {
            'roots_count': total_roots,
            'patterns_count': total_patterns,
            'generated_words_count': total_derivatives,  # ✅ Now calculated
            'unique_roots_with_generated': roots_with_derivatives,  # ✅ Now calculated
            'avl_tree_height': self.roots_tree.get_tree_height(),
            'hash_table_load_factor': self.patterns_table.display_stats().get('load_factor', 0)
        }
    
    def display_generation_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Format generation results as a readable string.
        
        Args:
            results (List[Dict]): List of generation results
            
        Returns:
            str: Formatted results
        """
        if not results:
            return "No results to display."
        
        # Prepare data for table display
        table_data = []
        for result in results:
            status = "✓" if result['is_valid'] else "✗"
            table_data.append((
                result['root'],
                result['pattern'],
                result['generated_word'],
                status
            ))
        
        # Simple text table
        output = "=" * 60 + "\n"
        output += f"{'Root':<10} {'Pattern':<15} {'Generated Word':<20} {'Valid'}\n"
        output += "=" * 60 + "\n"
        
        for root, pattern, word, valid in table_data:
            output += f"{root:<10} {pattern:<15} {word:<20} {valid}\n"
        
        output += "=" * 60
        
        return output
    
    def export_results(self, format: str = 'text') -> str:
        """
        Export all generated words in specified format.
        
        Args:
            format (str): Export format ('text', 'csv', 'json')
            
        Returns:
            str: Exported data
        """
        all_derivatives = []

        all_roots = self.roots_tree.display_inorder()

        for root in all_roots:
            node = self.roots_tree.search(root)
            if node:
                for derivative in node.get_derivatives():
                    all_derivatives.append({
                        'root': root,
                        'pattern': derivative['pattern'],
                        'word': derivative['word'],
                        'frequency': derivative['frequency']
                    })
        
        if format == 'json':
            import json
            return json.dumps(all_derivatives, ensure_ascii=False, indent=2)
        elif format == 'csv':
            csv_lines = ['Root,Pattern,Word,Frequency']
            for item in all_derivatives:
                csv_lines.append(
                    f"{item['root']},{item['pattern']},"
                    f"{item['word']},{item['frequency']}"
                )
            return '\n'.join(csv_lines)
        else:  # text
            return self._format_derivatives_text(all_derivatives)
        
    def _format_derivatives_text(self, derivatives: List[Dict]) -> str:
        """Format derivatives as readable text."""
        if not derivatives:
            return "No derivatives to display."
        
        # Prepare data for table display
        output = "=" * 70 + "\n"
        output += f"{'Root':<10} {'Pattern':<15} {'Word':<20} {'Frequency'}\n"
        output += "=" * 70 + "\n"
        
        for item in derivatives:
            output += f"{item['root']:<10} {item['pattern']:<15} {item['word']:<20} {item['frequency']}\n"
        
        output += "=" * 70
        
        return output
    

    def remove_derivative(self, root: str, word: str, pattern: str = None) -> bool:
        """
        Remove a derivative from engine.
        
        Args:
            root (str): Arabic root
            word (str): Derived word
            pattern (str, optional): Specific pattern to remove
        
        Returns:
            bool: True if removed, False if error
        """
        if not ArabicUtils.is_valid_root(root):
            print(f"❌ Invalid root: {root}")
            return False
        
        return self.roots_tree.remove_derivative(root, word, pattern)
    
    def clear_root_derivatives(self, root: str) -> bool:
        """
        Clear all derivatives for a root.
        
        Args:
            root (str): Arabic root
        
        Returns:
            bool: True if cleared, False if error
        """
        node = self.roots_tree.search(root)
        if node:
            node.clear_derivatives()
            return True
        return False