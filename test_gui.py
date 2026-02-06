#!/usr/bin/env python3
"""
Test script for Arabic Morphological Engine GUI

This script tests all GUI components to ensure they work correctly.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported."""
    print("\n" + "="*60)
    print("Testing Imports...")
    print("="*60)
    
    errors = []
    
    # Test PyQt6
    try:
        from PyQt6.QtWidgets import QApplication
        print("✅ PyQt6.QtWidgets imported successfully")
    except ImportError as e:
        errors.append(f"PyQt6.QtWidgets: {e}")
        print(f"❌ PyQt6.QtWidgets import failed: {e}")
    
    # Test core modules
    core_modules = [
        ('arabic_types', 'RootCategory'),
        ('arabic_utils', 'ArabicUtils'),
        ('avl_tree', 'AVLTree'),
        ('hash_table', 'HashTable'),
        ('morphology', 'MorphologicalEngine'),
        ('pattern_manager', 'PatternManager'),
        ('root_classifier', 'RootClassifier'),
    ]
    
    for module_name, class_name in core_modules:
        try:
            module = __import__(module_name)
            getattr(module, class_name)
            print(f"✅ {module_name}.{class_name} imported successfully")
        except ImportError as e:
            errors.append(f"{module_name}: {e}")
            print(f"❌ {module_name} import failed: {e}")
        except AttributeError as e:
            errors.append(f"{module_name}.{class_name}: {e}")
            print(f"❌ {module_name}.{class_name} not found: {e}")
    
    # Test GUI modules
    gui_modules = [
        ('gui.main_window', 'MainWindow'),
        ('gui.dialogs', 'LoadDataDialog'),
        ('gui.widgets', 'DashboardWidget'),
    ]
    
    for module_name, class_name in gui_modules:
        try:
            parts = module_name.split('.')
            module = __import__(module_name, fromlist=[parts[-1]])
            getattr(module, class_name)
            print(f"✅ {module_name}.{class_name} imported successfully")
        except ImportError as e:
            errors.append(f"{module_name}: {e}")
            print(f"❌ {module_name} import failed: {e}")
        except AttributeError as e:
            errors.append(f"{module_name}.{class_name}: {e}")
            print(f"❌ {module_name}.{class_name} not found: {e}")
    
    if errors:
        print("\n❌ Import test FAILED")
        print("\nErrors found:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("\n✅ All imports successful!")
        return True

def test_engine_creation():
    """Test if MorphologicalEngine can be created."""
    print("\n" + "="*60)
    print("Testing Engine Creation...")
    print("="*60)
    
    try:
        from morphology import MorphologicalEngine
        
        engine = MorphologicalEngine()
        print("✅ MorphologicalEngine created successfully")
        
        # Check components
        assert hasattr(engine, 'roots_tree'), "Missing roots_tree"
        print("✅ AVL Tree component present")
        
        assert hasattr(engine, 'patterns_table'), "Missing patterns_table"
        print("✅ Hash Table component present")
        
        assert hasattr(engine, 'pattern_manager'), "Missing pattern_manager"
        print("✅ Pattern Manager component present")
        
        return True
    except Exception as e:
        print(f"❌ Engine creation failed: {e}")
        return False

def test_gui_creation():
    """Test if GUI can be created."""
    print("\n" + "="*60)
    print("Testing GUI Creation...")
    print("="*60)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from morphology import MorphologicalEngine
        from gui.main_window import MainWindow
        
        # Create application
        app = QApplication(sys.argv)
        print("✅ QApplication created")
        
        # Create engine
        engine = MorphologicalEngine()
        print("✅ MorphologicalEngine created")
        
        # Create main window
        window = MainWindow(engine)
        print("✅ MainWindow created")
        
        # Check window properties
        assert window.windowTitle() == "🌙 Arabic Morphological Engine"
        print("✅ Window title correct")
        
        # Check tabs
        assert window.tabs.count() == 6, f"Expected 6 tabs, got {window.tabs.count()}"
        print("✅ All 6 tabs present")
        
        # Don't show window or run event loop in test
        return True
        
    except Exception as e:
        print(f"❌ GUI creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_core_functionality():
    """Test core engine functionality."""
    print("\n" + "="*60)
    print("Testing Core Functionality...")
    print("="*60)
    
    try:
        from morphology import MorphologicalEngine
        from arabic_utils import ArabicUtils
        from root_classifier import RootClassifier
        
        engine = MorphologicalEngine()
        
        # Test root validation
        assert ArabicUtils.is_valid_root("كتب"), "Root validation failed"
        print("✅ Root validation works")
        
        # Test root insertion
        engine.roots_tree.insert("كتب")
        assert engine.roots_tree.search("كتب") is not None, "Root not found after insertion"
        print("✅ AVL tree insertion/search works")
        
        # Test root classification
        analysis = RootClassifier.classify("كتب")
        assert analysis.category is not None, "Root classification failed"
        print(f"✅ Root classification works: {analysis.category.value}")
        
        # Test pattern loading
        test_pattern = {
            "template": "1ا2و3",
            "description": "Test pattern",
            "example": "كاتب"
        }
        engine.patterns_table.insert("فاعل", test_pattern)
        assert "فاعل" in engine.patterns_table, "Pattern not found"
        print("✅ Hash table insertion/search works")
        
        # Test word generation
        result = engine.generate_word("كتب", "فاعل")
        assert result is not None, "Word generation failed"
        assert result['generated_word'], "No word generated"
        print(f"✅ Word generation works: {result['generated_word']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_files():
    """Test if data files exist and are valid."""
    print("\n" + "="*60)
    print("Testing Data Files...")
    print("="*60)
    
    try:
        import json
        
        # Find data directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(script_dir), 'data')
        
        # Check roots.txt
        roots_path = os.path.join(data_dir, 'roots.txt')
        if os.path.exists(roots_path):
            with open(roots_path, 'r', encoding='utf-8') as f:
                roots = [line.strip() for line in f if line.strip()]
            print(f"✅ roots.txt found ({len(roots)} roots)")
        else:
            print(f"⚠️  roots.txt not found at {roots_path}")
        
        # Check patterns.json
        patterns_path = os.path.join(data_dir, 'patterns.json')
        if os.path.exists(patterns_path):
            with open(patterns_path, 'r', encoding='utf-8') as f:
                patterns = json.load(f)
            print(f"✅ patterns.json found ({len(patterns)} patterns)")
        else:
            print(f"⚠️  patterns.json not found at {patterns_path}")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Data files check failed: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "🌙"*30)
    print("  Arabic Morphological Engine - GUI Test Suite")
    print("🌙"*30)
    
    tests = [
        ("Imports", test_imports),
        ("Engine Creation", test_engine_creation),
        ("GUI Creation", test_gui_creation),
        ("Core Functionality", test_core_functionality),
        ("Data Files", test_data_files),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} test crashed: {e}")
            import traceback
            traceback.print_exc()
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The GUI is ready to use.")
        print("\nTo start the GUI, run:")
        print("  cd src")
        print("  python gui_main.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())