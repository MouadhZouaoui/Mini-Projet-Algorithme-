"""
Test file for Hash Table implementation.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from hash_table import HashTable

def test_hash_function():
    """Test hash function with Arabic strings."""
    ht = HashTable(10)
    
    # Test that same string gives same hash
    key1 = "فاعل"
    key2 = "فاعل"
    assert ht.hash_function(key1) == ht.hash_function(key2)
    
    # Different strings should (usually) give different hashes
    key3 = "مفعول"
    # Note: Might collide, but that's OK
    print(f"✅ Hash of 'فاعل': {ht.hash_function(key1)}")
    print(f"✅ Hash of 'مفعول': {ht.hash_function(key3)}")

def test_insert_and_search():
    """Test basic insert and search operations."""
    ht = HashTable(10)
    
    # Create sample pattern data
    pattern1 = {
        "template": "1ا2و3",
        "description": "Active participle",
        "example": "كتب -> كاتب"
    }
    
    pattern2 = {
        "template": "م1و2و3",
        "description": "Passive participle",
        "example": "كتب -> مكتوب"
    }
    
    # Insert patterns
    ht.insert("فاعل", pattern1)
    ht.insert("مفعول", pattern2)
    
    # Test search
    result1 = ht.search("فاعل")
    assert result1 is not None
    assert result1["template"] == "1ا2و3"
    
    result2 = ht.search("مفعول")
    assert result2 is not None
    assert result2["template"] == "م1و2و3"
    
    # Test non-existent key
    assert ht.search("غيرموجود") is None
    
    print("✅ test_insert_and_search passed")

def test_update():
    """Test updating existing key."""
    ht = HashTable(10)
    
    pattern = {"template": "1ا2و3", "desc": "Old"}
    ht.insert("فاعل", pattern)
    
    # Update
    new_pattern = {"template": "1ا2و3", "desc": "New"}
    ht.insert("فاعل", new_pattern)
    
    result = ht.search("فاعل")
    assert result["desc"] == "New"
    print("✅ test_update passed")

def test_delete():
    """Test deleting entries."""
    ht = HashTable(10)
    
    pattern = {"template": "1ا2و3"}
    ht.insert("فاعل", pattern)
    
    # Should exist
    assert ht.search("فاعل") is not None
    
    # Delete
    assert ht.delete("فاعل") is True
    
    # Should not exist
    assert ht.search("فاعل") is None
    
    # Delete non-existent
    assert ht.delete("غيرموجود") is False
    
    print("✅ test_delete passed")

def test_resize():
    """Test automatic resizing."""
    ht = HashTable(5)  # Small capacity
    
    # Insert enough entries to trigger resize
    for i in range(10):
        ht.insert(f"pattern{i}", {"template": f"template{i}"})
    
    # Should have resized (capacity doubled to 10)
    stats = ht.display_stats()
    print(f"✅ Capacity after resize: {stats['capacity']}")
    print(f"✅ Load factor: {stats['load_factor']:.2f}")
    
    # All entries should still be accessible
    for i in range(10):
        assert ht.search(f"pattern{i}") is not None
    
    print("✅ test_resize passed")

def test_get_all_patterns():
    """Test retrieving all patterns."""
    ht = HashTable(10)
    
    patterns = {
        "فاعل": {"template": "1ا2و3"},
        "مفعول": {"template": "م1و2و3"},
        "افعل": {"template": "ا1و2و3"}
    }
    
    for key, value in patterns.items():
        ht.insert(key, value)
    
    all_patterns = ht.get_all_patterns()
    
    # Should have 3 patterns
    assert len(all_patterns) == 3
    
    # Convert to dict for easier checking
    retrieved = {key: value for key, value in all_patterns}
    
    for key in patterns:
        assert key in retrieved
        assert retrieved[key]["template"] == patterns[key]["template"]
    
    print("✅ Retrieved patterns:", [p[0] for p in all_patterns])
    print("✅ test_get_all_patterns passed")

def test_statistics():
    """Test hash table statistics."""
    ht = HashTable(10)
    
    # Insert some patterns
    arabic_patterns = ["فاعل", "مفعول", "افعل", "تفاعل", "استفعل"]
    
    for i, pattern_name in enumerate(arabic_patterns):
        ht.insert(pattern_name, {"id": i, "template": f"template{i}"})
    
    stats = ht.display_stats()
    
    print("\n📊 Hash Table Statistics:")
    print(f"  Capacity: {stats['capacity']}")
    print(f"  Size: {stats['size']}")
    print(f"  Load Factor: {stats['load_factor']:.2f}")
    print(f"  Buckets Used: {stats['buckets_used']}")
    print(f"  Max Chain Length: {stats['max_chain_length']}")
    print(f"  Avg Chain Length: {stats['avg_chain_length']:.2f}")
    
    assert stats['size'] == len(arabic_patterns)
    print("✅ test_statistics passed")

if __name__ == "__main__":
    print("🚀 Running Hash Table Tests...\n")
    
    test_hash_function()
    print()
    
    test_insert_and_search()
    print()
    
    test_update()
    print()
    
    test_delete()
    print()
    
    test_get_all_patterns()
    print()
    
    test_resize()
    print()
    
    test_statistics()
    print()
    
    print("🎉 All hash table tests passed!")
    