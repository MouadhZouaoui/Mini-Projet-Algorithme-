"""
Hash Table implementation for Arabic morphological patterns.

Features:
- Separate chaining for collision resolution
- Dynamic resizing when load factor > 0.75
- Hash function optimized for Arabic strings
- Stores pattern templates and metadata

Author: [Your Name]
Date: [Today's Date]
"""

class HashEntry:
    """Entry in hash table storing a morphological pattern."""
    
    def __init__(self, key: str, value: dict):
        """
        Initialize a hash table entry.
        
        Args:
            key (str): Pattern name (e.g., "فاعل", "مفعول")
            value (dict): Pattern data including template, description, etc.
        """
        self.key = key
        self.value = value
        self.next = None  # For separate chaining


class HashTable:
    """Hash table for Arabic morphological patterns using separate chaining."""
    
    def __init__(self, initial_capacity: int = 50):
        """
        Initialize hash table with given initial capacity.
        
        Args:
            initial_capacity (int): Initial number of buckets (default 10)
        """
        self.capacity = initial_capacity
        self.size = 0  # Number of entries
        self.buckets = [None] * self.capacity
        self.load_factor_threshold = 0.75
    
    def hash_function(self, key: str) -> int:
        """
        Hash function for Arabic strings using polynomial rolling hash.
        
        Formula: hash = Σ (char_code * prime^i) mod capacity
        This provides good distribution for Arabic strings.
        
        Args:
            key (str): Arabic pattern name
            
        Returns:
            int: Hash index between 0 and capacity-1
        """
        prime = 31  # Common prime for polynomial hash
        hash_value = 0
        
        # Use Unicode code points for Arabic characters
        for i, char in enumerate(key):
            # Multiply character code by prime^i and accumulate
            hash_value = (hash_value * prime + ord(char)) % self.capacity
        
        return hash_value
    
    def insert(self, key: str, value: dict) -> None:
        """
        Insert or update a pattern in the hash table.
        
        Args:
            key (str): Pattern name
            value (dict): Pattern data
        """
        # Check if resizing is needed
        if self.size / self.capacity >= self.load_factor_threshold:
            self._resize()
        
        index = self.hash_function(key)
        entry = self.buckets[index]
        
        # If bucket is empty, create new entry
        if entry is None:
            self.buckets[index] = HashEntry(key, value)
            self.size += 1
            return
        
        # Traverse the chain
        prev = None
        while entry is not None:
            # If key exists, update value
            if entry.key == key:
                entry.value = value
                return
            prev = entry
            entry = entry.next
        
        # Key doesn't exist, add new entry at end of chain
        prev.next = HashEntry(key, value)
        self.size += 1
    
    def search(self, key: str) -> dict:
        """
        Search for a pattern by key.
        
        Args:
            key (str): Pattern name to search for
            
        Returns:
            dict: Pattern data if found, None otherwise
        """
        index = self.hash_function(key)
        entry = self.buckets[index]
        
        # Traverse the chain
        while entry is not None:
            if entry.key == key:
                return entry.value
            entry = entry.next
        
        return None
    
    def delete(self, key: str) -> bool:
        """
        Delete a pattern from the hash table.
        
        Args:
            key (str): Pattern name to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        index = self.hash_function(key)
        entry = self.buckets[index]
        prev = None
        
        while entry is not None:
            if entry.key == key:
                # Remove the entry
                if prev is None:
                    # Removing first entry in chain
                    self.buckets[index] = entry.next
                else:
                    prev.next = entry.next
                
                self.size -= 1
                return True
            
            prev = entry
            entry = entry.next
        
        return False
    
    def _resize(self) -> None:
        """Double the capacity and rehash all entries."""
        old_buckets = self.buckets
        old_capacity = self.capacity
        
        # Double the capacity
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        
        # Rehash all entries
        for i in range(old_capacity):
            entry = old_buckets[i]
            while entry is not None:
                self.insert(entry.key, entry.value)
                entry = entry.next
        
        print(f"🔄 Hash table resized to capacity {self.capacity}")
    
    def display_stats(self) -> dict:
        """
        Display statistics about the hash table.
        
        Returns:
            dict: Statistics including load factor, chain lengths, etc.
        """
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
            
            while entry is not None:
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
        """Get all patterns as a list of (key, value) pairs."""
        patterns = []
        
        for i in range(self.capacity):
            entry = self.buckets[i]
            while entry is not None:
                patterns.append((entry.key, entry.value))
                entry = entry.next
        
        return patterns
    
    def __len__(self) -> int:
        """Return number of entries in hash table."""
        return self.size
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists in hash table."""
        return self.search(key) is not None 

    # In hash_table.py, add to HashTable class:

    def add_pattern_with_validation(self, key: str, pattern_data: dict) -> tuple[bool, str]:
        """Add pattern with validation."""
        # Validate pattern data
        if 'template' not in pattern_data:
            return False, "Pattern must have 'template' field"
        
        template = pattern_data['template']
        if not self._validate_template(template):
            return False, f"Invalid template format: {template}"
        
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
        
        # Merge updates
        existing.update(updates)
        self.insert(key, existing)  # Re-insert to update
        return True, f"Pattern '{key}' updated successfully"

    def _validate_template(self, template: str) -> bool:
        """Validate pattern template syntax."""
        if not template:
            return False
        
        # Count root positions (1, 2, 3)
        root_positions = sum(1 for char in template if char in '123')
        return root_positions == 3  # Must have exactly 3 root positions

    def get_pattern_names(self) -> list[str]:
        """Get list of all pattern names."""
        return [key for key, _ in self.get_all_patterns()]