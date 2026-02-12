#!/usr/bin/env python3
"""
Launcher for Enhanced Arabic Morphological Engine GUI
Fixed and fully functional version.
"""

import sys
import os

# Add the parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point."""
    try:
        print("🌙 Starting Arabic Morphological Engine GUI...")
        print("📦 Initializing engine...")
        
        # Import the morphological engine
        from morphology import MorphologicalEngine
        
        # Create the engine
        engine = MorphologicalEngine()
        
        print("🎨 Launching GUI...")
        
        # Import the GUI
        from gui.enhanced_main_window import run_gui_app
        
        # Run the GUI
        run_gui_app(engine)
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n💡 Make sure PyQt6 is installed:")
        print("   pip install PyQt6")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()