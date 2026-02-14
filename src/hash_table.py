"""
Hash Table implementation for Arabic morphological patterns.
Features:
- Separate chaining for collision resolution
- Dynamic resizing when load factor > 0.75
- Hash function optimized for Arabic strings
- Stores pattern templates and metadata
"""


class HashEntry:
    """Entry in hash table storing a morphological pattern."""

    def __init__(self, key: str, value: dict):
        self.key = key
        self.value = value
        self.next = None  # For separate chaining


class HashTable:
    """Hash table for Arabic morphological patterns using separate chaining."""

    def __init__(self, initial_capacity: int = 50):
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [None] * self.capacity
        self.load_factor_threshold = 0.75

    def hash_function(self, key: str) -> int:
        """Polynomial rolling hash for Arabic strings."""
        prime = 31
        hash_value = 0
        for char in key:
            hash_value = (hash_value * prime + ord(char)) % self.capacity
        return hash_value

    def insert(self, key: str, value: dict) -> None:
        """Insert or update a pattern."""
        if self.size / self.capacity >= self.load_factor_threshold:
            self._resize()

        index = self.hash_function(key)
        entry = self.buckets[index]

        if entry is None:
            self.buckets[index] = HashEntry(key, value)
            self.size += 1
            return

        prev = None
        while entry:
            if entry.key == key:
                entry.value = value  # update
                return
            prev = entry
            entry = entry.next

        prev.next = HashEntry(key, value)
        self.size += 1

    def search(self, key: str) -> dict:
        index = self.hash_function(key)
        entry = self.buckets[index]
        while entry:
            if entry.key == key:
                return entry.value
            entry = entry.next
        return None

    def delete(self, key: str) -> bool:
        index = self.hash_function(key)
        entry = self.buckets[index]
        prev = None
        while entry:
            if entry.key == key:
                if prev is None:
                    self.buckets[index] = entry.next
                else:
                    prev.next = entry.next
                self.size -= 1
                return True
            prev = entry
            entry = entry.next
        return False

    def _resize(self) -> None:
        old_buckets = self.buckets
        old_capacity = self.capacity
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        for i in range(old_capacity):
            entry = old_buckets[i]
            while entry:
                self.insert(entry.key, entry.value)
                entry = entry.next
        print(f"🔄 Hash table resized to capacity {self.capacity}")

    def display_stats(self) -> dict:
        stats = {
            'capacity': self.capacity,
            'size': self.size,
            'load_factor': self.size / self.capacity,
            'buckets_used': 0,
            'max_chain_length': 0,
            'avg_chain_length': 0
        }
        total_chain_length = 0
        for i in range(self.capacity):
            entry = self.buckets[i]
            chain_length = 0
            while entry:
                chain_length += 1
                entry = entry.next
            if chain_length > 0:
                stats['buckets_used'] += 1
                stats['max_chain_length'] = max(stats['max_chain_length'], chain_length)
                total_chain_length += chain_length
        if stats['buckets_used'] > 0:
            stats['avg_chain_length'] = total_chain_length / stats['buckets_used']
        return stats

    def get_all_patterns(self) -> list:
        patterns = []
        for i in range(self.capacity):
            entry = self.buckets[i]
            while entry:
                patterns.append((entry.key, entry.value))
                entry = entry.next
        return patterns

    def __len__(self) -> int:
        return self.size

    def __contains__(self, key: str) -> bool:
        return self.search(key) is not None

    # --- Methods used by PatternManager ---
    def add_pattern_with_validation(self, key: str, pattern_data: dict) -> tuple[bool, str]:
        """Add pattern with validation – used by PatternManager."""
        # Validate pattern data
        if 'template' not in pattern_data:
            return False, "Pattern must have 'template' field"

        template = pattern_data['template']
        is_valid, msg = self._validate_template(template)
        if not is_valid:
            return False, msg

        # Check if pattern already exists
        if self.search(key):
            return False, f"Pattern '{key}' already exists"

        self.insert(key, pattern_data)
        return True, f"Pattern '{key}' added successfully"

    def update_pattern(self, key: str, updates: dict) -> tuple[bool, str]:
        """Update existing pattern."""
        existing = self.search(key)
        if not existing:
            return False, f"Pattern '{key}' not found"

        # If template is being updated, validate it
        if 'template' in updates:
            is_valid, msg = self._validate_template(updates['template'])
            if not is_valid:
                return False, msg

        # Merge updates
        existing.update(updates)
        self.insert(key, existing)  # Re-insert to update
        return True, f"Pattern '{key}' updated successfully"

    def _validate_template(self, template: str) -> tuple[bool, str]:
        """
        Validate pattern template syntax.
        Allows repeated digits as long as 1,2,3 all appear at least once.
        """
        print(f"🔍 HASH DEBUG: _validate_template called with '{template}'")
        if not template:
            return False, "Template cannot be empty"

        template = template.strip()
        root_positions = []
        for char in template:
            if char.isdigit():
                if char not in '123':
                    return False, f"Invalid root position '{char}'. Only digits 1,2,3 are allowed."
                root_positions.append(int(char))

        # Must contain at least one of each 1,2,3
        present = set(root_positions)
        if present != {1, 2, 3}:
            missing = {1, 2, 3} - present
            if missing:
                msg = f"Missing root positions: {', '.join(str(i) for i in missing)}"
                return False, msg

        # Check for invalid characters (only Arabic letters and digits allowed)
        from arabic_utils import ArabicUtils
        for char in template:
            if char.isdigit():
                continue
            if char not in ArabicUtils.ARABIC_LETTERS:
                return False, f"Invalid character in template: '{char}'"

        return True, "Template syntax is valid"

    def get_pattern_names(self) -> list[str]:
        """Get list of all pattern names."""
        return [key for key, _ in self.get_all_patterns()]