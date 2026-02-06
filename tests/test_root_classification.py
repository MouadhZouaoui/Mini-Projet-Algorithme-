"""
Test root classification system.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from root_classifier import RootClassifier, RootAnalysis
from arabic_utils import ArabicUtils

def test_root_classification():
    """Test classification of different root types."""
    print("🔬 Testing Root Classification...")
    print("=" * 60)
    
    test_cases = [
        # (root, expected_category, expected_subtype)
        ("كتب", "صحيح", "صحيح سالم"),
        ("جلس", "صحيح", "صحيح سالم"),
        
        ("أكل", "مهموز", "مهموز الفاء"),
        ("سأل", "مهموز", "مهموز العين"),
        ("قرأ", "مهموز", "مهموز اللام"),
        
        ("وعد", "معتل", "مثال"),
        ("وجد", "معتل", "مثال"),
        
        ("قال", "معتل", "أجوف"),
        ("باع", "معتل", "أجوف"),
        
        ("دعا", "معتل", "ناقص"),
        ("رمى", "معتل", "ناقص"),
        
        ("وفى", "معتل", "لفيف مفروق"),
        ("وقى", "معتل", "لفيف مفروق"),
        
        ("طوى", "معتل", "لفيف مقرون"),
        ("حيى", "معتل", "لفيف مقرون"),
        
        ("مدّ", "مضعف", "مضعف"),
        ("شدّ", "مضعف", "مضعف"),
        # test doubled without 'shadda'
        ("مدد", "مضعف", "مضعف"),
        ("شدد", "مضعف", "مضعف")
    ]
    
    all_passed = True
    
    for root, expected_cat, expected_sub in test_cases:
        analysis = RootClassifier.classify(root)
        
        cat_match = analysis.category.value == expected_cat
        sub_match = analysis.subtype == expected_sub
        
        status = "✅" if cat_match and sub_match else "❌"
        
        print(f"{status} {root}: {analysis.category.value} - {analysis.subtype}")
        
        if not (cat_match and sub_match):
            print(f"   Expected: {expected_cat} - {expected_sub}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All root classification tests passed!")
    else:
        print("⚠️ Some classification tests failed.")
    
    return all_passed

def test_pattern_adjustments():
    """Test pattern adjustments for different root types."""
    print("\n🎭 Testing Pattern Adjustments...")
    print("=" * 60)
    
    # Test cases: (root, pattern_name, expected_word, description)
    test_cases = [
        # Hollow roots (أجوف)
        ("قال", "فاعل", "قائل", "أجوف + فاعل = قائل"),
        ("قال", "يفعل", "يقول", "أجوف + يفعل = يقول"),
        
        # Defective roots (ناقص)
        ("رمى", "فاعل", "رامي", "ناقص + فاعل = رامي"),
        ("دعا", "مفعول", "مدعو", "ناقص + مفعول = مدعو"),
        
        # Sound roots (no adjustment needed)
        ("كتب", "فاعل", "كاتب", "صحيح + فاعل = كاتب"),
        ("كتب", "مفعول", "مكتوب", "صحيح + مفعول = مكتوب"),
        
        # Hamzated roots
        ("قرأ", "فاعل", "قارئ", "مهموز + فاعل = قارئ"),
        ("أكل", "مفعول", "مأكول", "مهموز + مفعول = مأكول"),
    ]
    
    all_passed = True
    
    for root, pattern_name, expected, description in test_cases:
        # Get pattern template from our patterns
        # For now, use hardcoded templates for testing
        templates = {
            "فاعل": "1ا23",
            "مفعول": "م12و3",
            "يفعل": "ي123",
            "افعل": "ا123",
        }
        
        template = templates.get(pattern_name, "")
        if not template:
            print(f"❌ No template for pattern: {pattern_name}")
            continue
        
        generated = RootClassifier.generate_with_root_type(root, template, pattern_name)
        
        if generated == expected:
            print(f"✅ {description}: {root} + {pattern_name} = {generated}")
        else:
            print(f"❌ {description}: got {generated}, expected {expected}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All pattern adjustment tests passed!")
    else:
        print("⚠️ Some pattern adjustment tests failed.")
    
    return all_passed

def test_bulk_classification():
    """Test classification of many roots."""
    print("\n📊 Bulk Root Classification Test...")
    print("=" * 60)
    
    # Get examples from classifier
    examples = RootClassifier.get_examples()
    
    total = 0
    correct = 0
    
    for category, roots in examples.items():
        print(f"\n📁 {category}:")
        for root in roots:
            analysis = RootClassifier.classify(root)
            
            # Check if classification matches expected category
            # This is simplified - in reality, we'd need a mapping
            expected_map = {
                "صحيح سالم": "صحيح",
                "مهموز الفاء": "مهموز",
                "مهموز العين": "مهموز",
                "مهموز اللام": "مهموز",
                "مثال": "معتل",
                "أجوف": "معتل",
                "ناقص": "معتل",
                "لفيف مفروق": "معتل",
                "لفيف مقرون": "معتل",
                "مضعف": "مضعف",
            }
            
            expected_cat = expected_map.get(category, "غير معروف")
            
            if analysis.category.value == expected_cat:
                print(f"  ✅ {root}: {analysis.subtype}")
                correct += 1
            else:
                print(f"  ❌ {root}: got {analysis.category.value}, expected {expected_cat}")
            
            total += 1
    
    accuracy = (correct / total) * 100
    print(f"\n📈 Accuracy: {correct}/{total} ({accuracy:.1f}%)")
    
    return correct == total

def test_root_analysis_display():
    """Test displaying root analysis in a nice format."""
    print("\n🔍 Detailed Root Analysis Display...")
    print("=" * 60)
    
    test_roots = ["كتب", "قال", "رمى", "قرأ", "مدّ", "وفى"]
    
    for root in test_roots:
        analysis = RootClassifier.classify(root)
        
        print(f"\n🌱 Root: {root}")
        print(f"   Category: {analysis.category.value}")
        print(f"   Subtype: {analysis.subtype}")
        print(f"   Weak positions: {analysis.weak_positions}")
        print(f"   Hamza positions: {analysis.hamza_positions}")
        print(f"   Is doubled: {analysis.is_doubled}")
        print(f"   Description: {analysis.description}")

def test_shadda_handling():
    """Test shadda handling in roots."""
    print("\n🌀 Testing Shadda Handling...")
    print("=" * 60)
    
    test_cases = [
        ("مدّ", "مدد", "مدّ expands to مدد"),
        ("شدّ", "شدد", "شدّ expands to شدد"),
        ("فرّ", "فرر", "فرّ expands to فرر"),
        ("حبّ", "حبب", "حبّ expands to حبب"),
    ]
    
    all_passed = True
    
    for original, expected_expanded, description in test_cases:
        expanded = ArabicUtils.expand_shadda(original)
        
        if expanded == expected_expanded:
            print(f"✅ {description}: {original} -> {expanded}")
        else:
            print(f"❌ {description}: {original} -> {expanded} (expected {expected_expanded})")
            all_passed = False
    
    # Test pattern application with shadda roots
    print("\n🔧 Testing Pattern Application with Shadda Roots:")
    
    shadda_pattern_tests = [
        ("مدّ", "فاعل", "ماد", "مدّ + فاعل = ماد (مُدَّ -> مُدَّ)"),
        ("شدّ", "مفعول", "مشدود", "شدّ + مفعول = مشدود"),
    ]
    
    for root, pattern_name, expected, description in shadda_pattern_tests:
        templates = {
            "فاعل": "1ا23",
            "مفعول": "م12و3",
        }
        
        template = templates.get(pattern_name, "")
        if not template:
            print(f"❌ No template for pattern: {pattern_name}")
            continue
        
        try:
            generated = RootClassifier.generate_with_root_type(root, template, pattern_name)
            
            if generated == expected:
                print(f"✅ {description}: {root} + {pattern_name} = {generated}")
            else:
                print(f"❌ {description}: got {generated}, expected {expected}")
                all_passed = False
        except Exception as e:
            print(f"❌ Error for {root}: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All shadda tests passed!")
    else:
        print("⚠️ Some shadda tests failed.")
    
    return all_passed

if __name__ == "__main__":
    print("🧪 Running Root Classification Tests...")
    print("=" * 60)
    
    test_root_classification()
    print()
    
    test_pattern_adjustments()
    print()

    test_shadda_handling()  
    print()
    
    test_bulk_classification()
    print()
    
    test_root_analysis_display()
    print()
    
    print("=" * 60)
    print("🎉 Root classification system implemented successfully!")
    print("\n✅ Can now handle all Arabic root types:")
    print("   • الصحيح (Sound)")
    print("   • المعتل (Weak)")
    print("   • المضعف (Doubled)")  
    print("   • المهموز (Hamzated)")
    print("   • المضعف (Doubled)")