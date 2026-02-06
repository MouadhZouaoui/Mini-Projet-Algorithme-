#!/usr/bin/env python3
"""
Test all 20 patterns with sample roots.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from morphology import MorphologicalEngine
import json

def test_all_patterns():
    """Test all patterns with sample roots."""
    engine = MorphologicalEngine()
    
    # Load the new patterns
    patterns_path = os.path.join(os.path.dirname(__file__), "data", "patterns.json")
    with open(patterns_path, 'r', encoding='utf-8') as f:
        patterns = json.load(f)
        engine.load_patterns(patterns)
    
    # Test roots
    test_roots = ["كتب", "فعل", "علم", "فتح", "غفر", "كرم", "شارك"]
    
    print("=" * 70)
    print("TESTING ALL 20 PATTERNS")
    print("=" * 70)
    
    results = []
    
    for root in test_roots:
        print(f"\n📌 Testing root: {root}")
        for pattern_name in patterns.keys():
            result = engine.generate_word(root, pattern_name)
            if result:
                results.append(result)
                status = "✓" if result['is_valid'] else "✗"
                print(f"  {status} {pattern_name}: {result['generated_word']}")
    
    print(f"\n📊 Total tests: {len(results)}")
    print(f"✅ Valid: {sum(1 for r in results if r['is_valid'])}")
    print(f"❌ Invalid: {sum(1 for r in results if not r['is_valid'])}")
    
    # Display by category
    categories = {}
    for result in results:
        if result.get('category'):
            cat = result['category']
            categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📈 By category:")
    for cat, count in categories.items():
        print(f"  {cat}: {count}")
    
    return results

if __name__ == "__main__":
    test_all_patterns()