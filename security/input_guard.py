import re
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class InputGuard:
    def __init__(self):
        self.blocked_keywords = ["ignore previous instructions", "system prompt", "hack"]

    def check(self, user_input: str) -> Tuple[bool, str]:
        """
        Validates user input.
        Returns (is_safe, error_message).
        """
        input_lower = user_input.lower()
        for word in self.blocked_keywords:
            if word in input_lower:
                logger.warning(f"Blocked input detected: matched keyword '{word}'")
                return False, "Input violates safety policies."
        return True, ""
