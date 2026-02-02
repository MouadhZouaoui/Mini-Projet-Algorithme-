"""
Test file for Morphological Engine.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from morphology import MorphologicalEngine

def test_word_generation():
    """Test word generation from root and pattern."""
    print("🚀 Testing Word Generation...")


    
    engine = MorphologicalEngine()

    engine.load_roots(["كتب"])

    
    # Load sample patterns
    sample_patterns = {
        "فاعل": {
            "template": "1ا23",
            "description": "Active participle",
            "example": "كتب -> كاتب"
        },
        "مفعول": {
"template": "م12و3",
            "description": "Passive participle",
            "example": "كتب -> مكتوب"
        }
    }
    
    engine.load_patterns(sample_patterns)
    
    # Test generation
    result = engine.generate_word("كتب", "فاعل")


    
    assert result is not None
    assert result['generated_word'] == "كاتب"
    assert result['is_valid'] == True
    
    print(f"✅ Generated: {result['root']} + {result['pattern']} = {result['generated_word']}")
    
    # Test another
    result = engine.generate_word("كتب", "مفعول")
    assert result['generated_word'] == "مكتوب"
    
    print("✅ test_word_generation passed")

def test_validation():
    """Test word validation."""
    print("\n🔍 Testing Word Validation...")
    
    engine = MorphologicalEngine()
    
    # Load sample data
    engine.load_roots(["كتب", "قرأ", "درس"])
    
    sample_patterns = {
        "فاعل": {"template": "1ا23"},
        "مفعول": {"template": "م12و3"}
    }
    engine.load_patterns(sample_patterns)
    
    # Test validation with specific root
    validation = engine.validate_word("كاتب", "كتب")
    assert validation['is_valid'] == True
    assert validation['pattern'] == "فاعل"
    
    print(f"✅ Validation: 'كاتب' belongs to root 'كتب' with pattern '{validation['pattern']}'")
    
    # Test invalid case
    validation = engine.validate_word("كتاب", "قرأ")
    assert validation['is_valid'] == False
    
    print("✅ test_validation passed")

def test_generate_all():
    """Test generating all words for a root."""
    print("\n🎭 Testing Generate All Patterns...")
    
    engine = MorphologicalEngine()
    
    # Load multiple patterns
    sample_patterns = {
        "فاعل": {"template": "1ا23"},
        "مفعول": {"template": "م12و3"},
        "افعل": {"template": "ا123"}
    }
    engine.load_patterns(sample_patterns)
    
    # Generate all words for root
    results = engine.generate_all_for_root("كتب")
    
    assert len(results) == 3
    
    generated_words = [r['generated_word'] for r in results]
    print(f"✅ Generated {len(results)} words for root 'كتب': {generated_words}")
    
    # Display results
    print("\n" + engine.display_generation_results(results))
    
    print("✅ test_generate_all passed")

def test_statistics():
    """Test engine statistics."""
    print("\n📊 Testing Engine Statistics...")
    
    engine = MorphologicalEngine()
    
    # Load data
    engine.load_roots(["كتب", "قرأ", "درس", "عمل", "فهم"])
    
    sample_patterns = {
        "فاعل": {"template": "1ا2و3"},
        "مفعول": {"template": "م12و3"},
        "افعل": {"template": "ا123"}
    }
    engine.load_patterns(sample_patterns)
    
    # Generate some words
    engine.generate_all_for_root("كتب")
    engine.generate_all_for_root("قرأ")
    
    # Get statistics
    stats = engine.get_engine_statistics()
    
    assert stats['roots_count'] == 5
    assert stats['patterns_count'] == 3
    assert stats['generated_words_count'] == 6  # 3 patterns × 2 roots
    
    print("📈 Engine Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("✅ test_statistics passed")

def test_arabic_utils_integration():
    """Test integration with Arabic utilities."""
    print("\n🔤 Testing Arabic Utilities Integration...")
    
    from arabic_utils import ArabicUtils
    
    # Test normalization
    text = "كِتَابٌ"
    normalized = ArabicUtils.normalize_arabic(text)
    assert normalized == "كتاب"
    
    # Test root validation
    assert ArabicUtils.is_valid_root("كتب") == True
    assert ArabicUtils.is_valid_root("abc") == False
    assert ArabicUtils.is_valid_root("كت") == False  # Only 2 letters
    
    # Test pattern application
    generated = ArabicUtils.apply_pattern("كتب", "1ا23")
    print(f"[DEBUG] Generated: '{generated}' (expected: 'كاتب')")  # ← Add this line

    assert generated == "كاتب"
    
    print("✅ Arabic utilities working correctly")
    print("✅ test_arabic_utils_integration passed")

if __name__ == "__main__":
    print("🧪 Running Morphological Engine Tests...")
    print("=" * 60)
    
    test_arabic_utils_integration()
    print()
    
    test_word_generation()
    print()
    
    test_validation()
    print()
    
    test_generate_all()
    print()
    
    test_statistics()
    print()
    
    print("=" * 60)
    print("🎉 All morphological engine tests passed!")
    print("\n✅ Ready to build the complete CLI application!")