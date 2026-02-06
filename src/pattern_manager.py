"""
Pattern Manager for Arabic morphological patterns.
Handles CRUD operations and validation for patterns.
"""

import json
from typing import Dict, List, Optional, Tuple
from hash_table import HashTable
from arabic_utils import ArabicUtils

class PatternManager:
    """Manages Arabic morphological patterns with validation."""
    
    def __init__(self, hash_table: HashTable):
        self.patterns_table = hash_table
        
    def add_pattern(self, name: str, template: str, 
                    description: str = "", example: str = "",
                    rule: str = "") -> Tuple[bool, str]:
        """
        Add a new morphological pattern.
        
        Args:
            name (str): Arabic pattern name (e.g., "فاعل")
            template (str): Pattern template (e.g., "1ا2و3")
            description (str): Pattern description
            example (str): Example usage
            rule (str): Transformation rule
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        # Validate name
        if not name or not name.strip():
            return False, "Pattern name cannot be empty"
        
        # Validate template
        if not self._validate_template_syntax(template):
            return False, f"Invalid template syntax: {template}"
        
        # Create pattern data
        pattern_data = {
            'template': template,
            'description': description,
            'example': example,
            'rule': rule,
            'created_at': 'now'  # You can use datetime.now().isoformat()
        }
        
        # Add to hash table
        return self.patterns_table.add_pattern_with_validation(name, pattern_data)
    
    def edit_pattern(self, name: str, **kwargs) -> Tuple[bool, str]:
        """
        Edit existing pattern.
        
        Args:
            name (str): Pattern name to edit
            **kwargs: Fields to update (template, description, example, rule)
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        # Validate that pattern exists
        if not self.patterns_table.search(name):
            return False, f"Pattern '{name}' not found"
        
        # Validate template if provided
        if 'template' in kwargs:
            if not self._validate_template_syntax(kwargs['template']):
                return False, f"Invalid template syntax: {kwargs['template']}"
        
        return self.patterns_table.update_pattern(name, kwargs)
    
    def delete_pattern(self, name: str) -> Tuple[bool, str]:
        """
        Delete a pattern.
        
        Args:
            name (str): Pattern name to delete
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if self.patterns_table.delete(name):
            return True, f"Pattern '{name}' deleted successfully"
        return False, f"Pattern '{name}' not found"
    
    def list_patterns(self, detailed: bool = False) -> Dict:
        """
        List all patterns.
        
        Args:
            detailed (bool): If True, return full pattern data
            
        Returns:
            Dict: Pattern information
        """
        all_patterns = self.patterns_table.get_all_patterns()
        
        if detailed:
            return {name: data for name, data in all_patterns}
        else:
            # Just names and templates
            return {
                name: {
                    'template': data.get('template', ''),
                    'description': data.get('description', '')[:50]
                }
                for name, data in all_patterns
            }
    
    def validate_template_syntax(self, template: str) -> Tuple[bool, str]:
        """
        Validate pattern template syntax.
        
        Args:
            template (str): Pattern template
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not template:
            return False, "Template cannot be empty"
        
        # Count root positions
        root_positions = []
        for char in template:
            if char in '123':
                root_positions.append(int(char))
        
        # Must have exactly 3 root positions
        if len(root_positions) != 3:
            return False, f"Template must have exactly 3 root positions, found {len(root_positions)}"
        
        # Must have 1, 2, 3 in order (not necessarily consecutive)
        if sorted(root_positions) != [1, 2, 3]:
            return False, "Template must use root positions 1, 2, and 3"
        
        # Check for duplicate root positions
        if len(set(root_positions)) != 3:
            return False, "Duplicate root positions found"
        
        # Check for invalid characters (only Arabic letters and root positions allowed)
        for char in template:
            if char not in '123' and char not in ArabicUtils.ARABIC_LETTERS:
                return False, f"Invalid character in template: '{char}'"
        
        return True, "Template syntax is valid"
    
    def _validate_template_syntax(self, template: str) -> bool:
        """Internal validation method."""
        is_valid, _ = self.validate_template_syntax(template)
        return is_valid
    
    def export_patterns(self, filepath: str) -> bool:
        """
        Export all patterns to JSON file.
        
        Args:
            filepath (str): Path to export file
            
        Returns:
            bool: True if successful
        """
        try:
            patterns_dict = {
                name: data 
                for name, data in self.patterns_table.get_all_patterns()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(patterns_dict, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting patterns: {e}")
            return False
    
    def import_patterns(self, filepath: str) -> Tuple[bool, str]:
        """
        Import patterns from JSON file.
        
        Args:
            filepath (str): Path to import file
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                patterns = json.load(f)
            
            count = 0
            errors = []
            
            for name, data in patterns.items():
                success, message = self.add_pattern(
                    name, 
                    data.get('template', ''),
                    data.get('description', ''),
                    data.get('example', ''),
                    data.get('rule', '')
                )
                
                if success:
                    count += 1
                else:
                    errors.append(f"{name}: {message}")
            
            message = f"Imported {count} patterns"
            if errors:
                message += f". Errors: {', '.join(errors[:3])}"
                if len(errors) > 3:
                    message += f" and {len(errors) - 3} more"
            
            return True, message
            
        except FileNotFoundError:
            return False, f"File not found: {filepath}"
        except json.JSONDecodeError:
            return False, "Invalid JSON file"
        except Exception as e:
            return False, f"Error importing patterns: {e}"