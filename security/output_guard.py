import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class OutputGuard:
    def __init__(self):
        self.restricted_terms = ["password:", "api_key", "secret="]

    def check(self, generated_output: str) -> Tuple[bool, str]:
        """
        Validates generated output.
        Returns (is_safe, error_message).
        """
        output_lower = generated_output.lower()
        for term in self.restricted_terms:
            if term in output_lower:
                logger.warning("Output blocked due to restricted content.")
                return False, "Output violates safety policies. Restricted information blocked."
        return True, ""
