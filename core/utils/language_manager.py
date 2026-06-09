"""Language management for internationalization."""

import json
from pathlib import Path


class LanguageManager:
    _current_lang = "EN"
    _LANG_FILE = Path.home() / ".nanocoatbuilder_lang.json"
    
    @classmethod
    def init(cls):
        try:
            if cls._LANG_FILE.exists():
                with open(cls._LANG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cls._current_lang = data.get("language", "EN")
        except Exception:
            pass
    
    @classmethod
    def set_language(cls, lang: str):
        if lang in ("EN", "FR"):
            cls._current_lang = lang
            try:
                cls._LANG_FILE.parent.mkdir(parents=True, exist_ok=True)
                with open(cls._LANG_FILE, 'w', encoding='utf-8') as f:
                    json.dump({"language": lang}, f)
            except Exception:
                pass
    
    @classmethod
    def get_current_lang(cls) -> str:
        return cls._current_lang