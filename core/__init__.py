"""Core business logic module for NanoCoatBuilder."""

from core.database.ingredient_db import IngredientDB
from core.database.history_manager import HistoryManager, FormulationRecord
from core.analysis.coating_analyzer import CoatingAnalyzer, AnalysisResult, PerformancePrediction
from core.analysis.validator import FormulationValidator
from core.analysis.protocol_generator import ProtocolGenerator, SynthesisProtocol
from core.utils.language_manager import LanguageManager
from core.utils.constants import APPLICATION_TYPES, TRANSLATIONS
from core.utils.rag_agent import RAGAgent
from core.models import ValidationRule, FormulationItem
from core.models.ingredient import CoatingType, Ingredient

__all__ = [
    'IngredientDB',
    'HistoryManager',
    'FormulationRecord',
    'CoatingAnalyzer',
    'AnalysisResult',
    'PerformancePrediction',
    'FormulationValidator',
    'ProtocolGenerator',
    'SynthesisProtocol',
    'LanguageManager',
    'APPLICATION_TYPES',
    'TRANSLATIONS',
    'RAGAgent',
    'ValidationRule',
    'FormulationItem',
    'CoatingType',
    'Ingredient'
]