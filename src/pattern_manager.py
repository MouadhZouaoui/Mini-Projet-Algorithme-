"""
Pattern Manager for Arabic morphological patterns.
DEBUG VERSION with console output.
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
        """
        print(f"🔍 DEBUG: add_pattern called with template='{template}'")
        if not name or not name.strip():
            return False, "Pattern name cannot be empty"

        is_valid, msg = self.validate_template_syntax(template)
        print(f"🔍 DEBUG: validate_template_syntax returned ({is_valid}, '{msg}')")
        if not is_valid:
            return False, msg

        pattern_data = {
            'template': template,
            'description': description,
            'example': example,
            'rule': rule,
            'created_at': 'now'
        }
        return self.patterns_table.add_pattern_with_validation(name, pattern_data)

    def edit_pattern(self, name: str, **kwargs) -> Tuple[bool, str]:
        if not self.patterns_table.search(name):
            return False, f"Pattern '{name}' not found"
        if 'template' in kwargs:
            is_valid, msg = self.validate_template_syntax(kwargs['template'])
            if not is_valid:
                return False, msg
        return self.patterns_table.update_pattern(name, kwargs)

    def delete_pattern(self, name: str) -> Tuple[bool, str]:
        if self.patterns_table.delete(name):
            return True, f"Pattern '{name}' deleted successfully"
        return False, f"Pattern '{name}' not found"

    def list_patterns(self, detailed: bool = False) -> Dict:
        all_patterns = self.patterns_table.get_all_patterns()
        if detailed:
            return {name: data for name, data in all_patterns}
        else:
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
        Allows repeated digits as long as 1,2,3 all appear at least once.
        """
        print(f"🔍 DEBUG: validate_template_syntax called with '{template}'")
        if not template:
            return False, "Template cannot be empty"

        template = template.strip()
        root_positions = []
        for char in template:
            if char.isdigit():
                if char not in '123':
                    return False, f"Invalid root position '{char}'. Only digits 1,2,3 are allowed."
                root_positions.append(int(char))

        present = set(root_positions)
        if present != {1, 2, 3}:
            missing = {1, 2, 3} - present
            if missing:
                msg = f"Missing root positions: {', '.join(str(i) for i in missing)}"
                print(f"🔍 DEBUG: validation failed: {msg}")
                return False, msg

        for char in template:
            if char.isdigit():
                continue
            if char not in ArabicUtils.ARABIC_LETTERS:
                msg = f"Invalid character in template: '{char}'"
                print(f"🔍 DEBUG: validation failed: {msg}")
                return False, msg

        print("🔍 DEBUG: validation passed")
        return True, "Template syntax is valid"

    def export_patterns(self, filepath: str) -> bool:
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