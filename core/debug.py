# core/debug.py
# DebugManager for DAZE: Centralized debug/logging system for components/pages/cards

from typing import List, Optional

class DebugManager:
    _instance = None

    def __init__(self):
        self.enabled = False
        self.logs: List[str] = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DebugManager()
        return cls._instance

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
        self.clear()

    def log(self, message: str):
        if self.enabled:
            self.logs.append(message)
            if len(self.logs) > 50:
                self.logs.pop(0)

    def get_logs(self) -> List[str]:
        return self.logs.copy() if self.enabled else []

    def clear(self):
        self.logs.clear()
