from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class Memory:
    def __init__(self, max_history: int = 5):
        self.max_history = max_history
        self.conversation_history: List[Tuple[str, str]] = []

    def get_history_text(self) -> str:
        if not self.conversation_history:
            return ""
        history_text = "\nPrevious conversation:\n"
        for q, a in self.conversation_history[-3:]:
            history_text += f"User: {q}\nAssistant: {a}\n"
        return history_text

    def add_exchange(self, question: str, answer: str):
        self.conversation_history.append((question, answer))
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)

    def clear(self):
        self.conversation_history.clear()
        logger.info("🗑️ Conversation history cleared")
    
    def get_raw_history(self) -> List[Tuple[str, str]]:
        return self.conversation_history
