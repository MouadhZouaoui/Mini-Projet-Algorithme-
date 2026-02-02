"""
Test that derivatives are stored correctly in AVL nodes.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from morphology import MorphologicalEngine
from arabic_utils import ArabicUtils

def test_derivative_storage():
    """Test that generated words are stored in AVL nodes."""
    print("🧪 Testing Derivative Storage...")
    
    engine = MorphologicalEngine()
    
    # Load sample data
    engine.load_roots(["كتب", "درس"])
    
    sample_patterns = {
        "فاعل": {"template": "1ا23"},
        "مفعول": {"template": "م12و3"}
    }
    engine.load_patterns(sample_patterns)
    
    # Generate some words
    result1 = engine.generate_word("كتب", "فاعل")
    result2 = engine.generate_word("كتب", "مفعول")
    result3 = engine.generate_word("درس", "فاعل")
    
    # Get the root nodes
    كتب_node = engine.roots_tree.search("كتب")
    درس_node = engine.roots_tree.search("درس")
    
    # Check derivatives are stored in nodes
    assert كتب_node is not None
    assert درس_node is not None
    
    print(f"✅ Root 'كتب' has {كتب_node.get_derivative_count()} derivatives")
    print(f"✅ Root 'قرأ' has {درس_node.get_derivative_count()} derivatives")
    
    # Verify specific derivatives
    كتب_derivatives = كتب_node.get_derivatives()
    assert len(كتب_derivatives) == 2
    
    # Check the words are correct
    derived_words = [d['word'] for d in كتب_derivatives]
    assert "كاتب" in derived_words
    assert "مكتوب" in derived_words
    
    print(f"✅ Derivatives for 'كتب': {[d['word'] for d in كتب_derivatives]}")
    
    # Test validation also stores derivatives
    validation = engine.validate_word("دارس", "درس")
    درس_node = engine.roots_tree.search("درس")

    print(f"[DEBUG] درس derivatives: {[d['word'] for d in درس_node.get_derivatives()]}")
    print(f"[DEBUG] Validation result: {validation}")
    assert "دارس" in [d['word'] for d in درس_node.get_derivatives()]
    
    print("✅ test_derivative_storage passed")

def test_duplicate_derivatives():
    """Test that duplicate derivatives increase frequency."""
    print("\n🔄 Testing Duplicate Derivatives...")
    
    engine = MorphologicalEngine()
    engine.load_roots(["كتب"])
    engine.load_patterns({"فاعل": {"template": "1ا23"}})
    
    # Generate same word multiple times
    for _ in range(3):
        engine.generate_word("كتب", "فاعل")
    
    node = engine.roots_tree.search("كتب")
    derivatives = node.get_derivatives()

    print(f"[DEBUG] Derivatives: {derivatives}")  # ← Add debug

    
    # Should have only one derivative entry
    assert len(derivatives) == 1
    
    # Frequency should be 3
    assert derivatives[0]['frequency'] == 3
    
    print(f"✅ Derivative 'كاتب' has frequency {derivatives[0]['frequency']}")
    print("✅ test_duplicate_derivatives passed")

if __name__ == "__main__":
    print("🔍 Testing Storage Architecture...")
    print("=" * 50)
    
    test_derivative_storage()
    print()
    
    test_duplicate_derivatives()
    print()
    
    print("=" * 50)
    print("🎉 All storage tests passed!")
    print("\n✅ Derivatives are correctly stored in AVL nodes.")