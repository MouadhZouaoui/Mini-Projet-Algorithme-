# Copilot Instructions for Arabic Morphology Engine

## Project Overview
This is an **Arabic morphological analysis and word generation system** with dual interfaces (CLI and PyQt6 GUI). It uses specialized data structures (AVL Tree, Hash Table) to analyze Arabic roots, apply morphological patterns, and generate/validate derived words.

## Architecture Overview

### Core Components
- **Morphological Engine** (`morphology.py`): Central orchestrator connecting all subsystems
  - Manages AVL Tree of roots and Hash Table of patterns
  - Generates words from root + pattern combinations
  - Validates generated words against roots

- **Data Structures** (`avl_tree.py`, `hash_table.py`):
  - **AVLTree**: Self-balancing BST storing 3-letter Arabic roots with O(log n) operations
  - **HashTable**: Separate chaining hash table for morphological patterns with dynamic resizing (threshold 0.75)
  - Both store derivatives and metadata for linguistic analysis

- **Arabic Text Processing** (`arabic_utils.py`):
  - Root extraction and validation (3-letter constraints)
  - Character normalization (hamza variants, ta marbuta → ha, etc.)
  - Pattern application (placeholder-based: "1ا23" = 1st letter + alef + 2nd + 3rd)
  - Diacritic (tashkeel) removal

- **Root Classification** (`root_classifier.py`):
  - Categorizes roots by linguistic type (Sound/Weak/Hamzated/Doubled)
  - Identifies weak letter positions and hamza patterns
  - Returns `RootAnalysis` objects with detailed linguistic metadata

## Data Flow & Integration Points

**Startup (CLI - main.py → Morphological Engine)**
1. Load `data/roots.txt` (newline-separated 3-letter roots)
2. Load `data/patterns.json` (template-based morphological patterns)
3. User inputs: root + pattern → `generate_word()` → validated word or error

**Word Generation Logic**
- Root validation via `ArabicUtils.is_valid_root()` (3 letters, all Arabic)
- Template retrieval from HashTable
- Pattern application: `ArabicUtils.apply_pattern(root, template)` replaces "1", "2", "3" with root letters
- Optional validation checks if generated word exists as a stored root

**GUI Mode (gui_main.py → MainWindow)**
- PyQt6 interface with tabs for different operations
- Each tab connects to engine methods through dialog/widget layer
- Data loading, pattern management, word generation all routed through engine

## Key Conventions & Patterns

### Arabic Morphology Specifics
- **Roots**: Always 3 letters (triliteral focus)
- **Pattern Templates**: Use placeholders (1,2,3) for root letters; Arabic letters/diacritics for affixes
  - Example: "1ا23" (active participle) + كتب = كاتب
  - Example: "م12و3" (passive participle) + كتب = مكتوب
- **Normalization**: Shadda expansion, vowel reduction, alef unification (آ/أ/إ → ا)

### Error Handling
- Silently skip invalid roots during loading (`is_valid_root()` check)
- Return `None` or empty results for invalid operations
- CLI uses rich formatting for visual feedback (✅ success, ❌ errors)

### Testing Pattern
Tests use minimal hardcoded data:
```python
sample_patterns = {
    "فاعل": {"template": "1ا23", "description": "Active participle"},
    "مفعول": {"template": "م12و3", "description": "Passive participle"}
}
engine.load_patterns(sample_patterns)
```
Run tests via pytest framework; test files in `tests/` directory.

## Critical Developer Workflows

### Running the Application
```bash
# CLI mode
python src/main.py

# GUI mode (requires PyQt6)
python src/gui_main.py

# Tests
pytest tests/
```

### Adding New Features
1. **New morphological pattern**: Add to `data/patterns.json` with template structure
2. **New root classification rule**: Extend `root_classifier.py` RootCategory/WeakSubtype enums and logic
3. **New data structure method**: Maintain O(log n) for AVL, O(1) avg for HashTable operations
4. **New GUI component**: Create widget in `src/gui/widgets.py`, add tab in `MainWindow`

### File Organization
- **src/**: Core engine, data structures, utilities
- **src/gui/**: PyQt6 interface (main_window.py, widgets.py, dialogs.py)
- **data/**: JSON patterns and text roots (loaded at runtime)
- **tests/**: Pytest-compatible test suite
- **root_classifier.py**: Linguistically separated classification logic

## Dependencies & External Integration
- **rich**: CLI formatting (Tables, Panels, Progress bars)
- **colorama**: Cross-platform colored terminal output
- **PyQt6**: GUI (conditional import; CLI works without it)
- **Standard library**: `json`, `os`, `sys`, `typing`, `enum`, `dataclasses`

## Import Architecture
- Avoid circular imports via dedicated `arabic_types.py` for enums/dataclasses
- CLI imports from src via path manipulation or sys.path adjustments
- GUI imports conditionally check for PyQt6 availability

## Performance Considerations
- AVL Tree: O(log n) search/insert, automatic balancing
- Hash Table: O(1) avg search, resizes when load factor > 0.75
- Pattern matching: O(n) where n = root length (always 3)
- Large root sets: Tree handles sorted traversal efficiently

---

**Last Updated**: February 2026 | For questions about architecture, refer to class docstrings and method signatures in each module.
