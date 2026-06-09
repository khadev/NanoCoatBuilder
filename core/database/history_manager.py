"""History management for formulations."""

import json
from pathlib import Path
from typing import List
from pydantic import BaseModel
from datetime import datetime
import uuid


class FormulationRecord(BaseModel):
    unique_id: str = str(uuid.uuid4())
    name: str
    date: str = datetime.now().strftime("%Y-%m-%d")
    operator: str = ""
    coating_type: str = "Anti-corrosion"
    target_environment: str = "C5 (very high corrosivity)"
    items: List[dict] = []
    timestamp: float = datetime.now().timestamp()

    def total_weight(self) -> float:
        return sum(item.get('weight_grams', 0) for item in self.items)

    def get_display_name(self) -> str:
        dt = datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M")
        return f"{self.name} ({self.date}) - {self.operator} [{dt}]"


class HistoryManager:
    _HISTORY_FILE = Path.home() / ".nanocoatbuilder_history.json"
    
    @classmethod
    def save_history(cls, formulations: List[FormulationRecord]) -> None:
        data = [f.dict() for f in formulations]
        try:
            cls._HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(cls._HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    @classmethod
    def load_history(cls) -> List[FormulationRecord]:
        if not cls._HISTORY_FILE.exists():
            return []
        try:
            with open(cls._HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [FormulationRecord(**item) for item in data]
        except Exception as e:
            print(f"Error loading history: {e}")
            return []