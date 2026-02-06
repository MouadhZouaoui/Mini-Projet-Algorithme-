"""
GUI package for Arabic Morphological Engine.
"""

from .main_window import MainWindow
from .dialogs import (
    LoadDataDialog, AddRootDialog, SearchRootDialog,
    GenerateWordDialog, ValidateWordDialog, AnalyzeRootDialog,
    PatternManagementDialog, StatisticsDialog, TreeVisualizationDialog
)
from .widgets import (
    DashboardWidget, RootsWidget, PatternsWidget,
    GenerationWidget, ValidationWidget, AnalysisWidget
)

__all__ = [
    'MainWindow',
    'LoadDataDialog', 'AddRootDialog', 'SearchRootDialog',
    'GenerateWordDialog', 'ValidateWordDialog', 'AnalyzeRootDialog',
    'PatternManagementDialog', 'StatisticsDialog', 'TreeVisualizationDialog',
    'DashboardWidget', 'RootsWidget', 'PatternsWidget',
    'GenerationWidget', 'ValidationWidget', 'AnalysisWidget'
]