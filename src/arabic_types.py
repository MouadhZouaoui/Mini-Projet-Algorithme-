"""
Arabic morphological types and data structures.
"""

### THIS FILE WAS CREATED TO AVOID CIRCULAR LOOP ( IMPORT INSIDE AN IMPORT) SO I MIGRATED THE TYPES HERE IN A SOLE FILE

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class RootCategory(Enum):
    """Main categories of Arabic roots."""
    SOUND = "صحيح"
    WEAK = "معتل"
    HAMZATED = "مهموز"
    DOUBLED = "مضعف"
    UNKNOWN = "غير معروف"

class SoundSubtype(Enum):
    """Subtypes of sound roots."""
    SOUND_PERFECT = "صحيح سالم"
    HAMZATED = "مهموز"
    DOUBLED = "مضعف"

class WeakSubtype(Enum):
    """Subtypes of weak roots."""
    FIRST_RADICAL_WEAK = "مثال"
    SECOND_RADICAL_WEAK = "أجوف"
    THIRD_RADICAL_WEAK = "ناقص"
    DOUBLE_WEAK_SEPARATED = "لفيف مفروق"
    DOUBLE_WEAK_JOINED = "لفيف مقرون"

@dataclass
class RootAnalysis:
    """Complete analysis of an Arabic root."""
    root: str
    category: RootCategory
    subtype: Optional[str]
    weak_positions: List[int]  # Positions of weak letters (0,1,2)
    hamza_positions: List[int]  # Positions of hamza
    is_doubled: bool
    description: str
    
    def __str__(self) -> str:
        return f"{self.root}: {self.category.value} ({self.subtype})"