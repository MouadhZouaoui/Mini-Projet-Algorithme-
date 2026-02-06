# src/gui_main.py
"""
Arabic Morphological Engine - GUI Version
PyQt6 GUI entry point.
"""

import sys
import os

# For absolute imports within the package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from PyQt6.QtWidgets import QApplication
    from gui.main_window import MainWindow
    from morphology import MorphologicalEngine
    import json
except ImportError as e:
    print(f"Error: {e}")
    print("Please install PyQt6: pip install PyQt6")
    sys.exit(1)

def main():
    """Main entry point for GUI application."""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Arabic Morphological Engine")
    app.setApplicationDisplayName("Arabic Morphology")
    
    # Create engine instance
    engine = MorphologicalEngine()
    
    # Create and show main window
    window = MainWindow(engine)
    window.show()
    
    # Run application
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())