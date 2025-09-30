# src/core/memory_manager.py

import json
import os
from src.core.context_tracker import ContextTracker


class MemoryManager:
    def __init__(self, save_dir: str = "memory"):
        """
        Handles saving and loading of agent context to JSON files.
        :param save_dir: Directory to store memory files.
        """
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def save_context(self, context: ContextTracker, session_id: str = "latest") -> None:
        """
        Save the current context to a JSON file.
        :param context: ContextTracker object containing context data.
        :param session_id: Identifier for the session file.
        """
        path = os.path.join(self.save_dir, f"{session_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(context.get_context(), f, indent=2)
        print(f"💾 Context saved to {path}")

    def load_context(self, session_id: str = "latest") -> ContextTracker:
        """
        Load context from a JSON file into a ContextTracker.
        :param session_id: Identifier for the session file.
        :return: ContextTracker object with loaded context.
        """
        path = os.path.join(self.save_dir, f"{session_id}.json")
        context = ContextTracker()

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                context.load_context(data)
            print(f"📂 Context loaded from {path}")
        else:
            print(f"⚠️ No context found at {path}, returning empty tracker.")

        return context


