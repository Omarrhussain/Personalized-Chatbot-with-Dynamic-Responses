import re
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class ContentGuard:
    def __init__(self):
        # Extremely basic regex for emails or phone numbers to prevent PII leakage
        self.pii_patterns = [
            re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"), # Emails
            re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b") # Phones
        ]

    def sanitize(self, content: str) -> Tuple[bool, str]:
        """
        Sanitizes retrieved content.
        Returns (is_clean, sanitized_content).
        """
        is_clean = True
        sanitized_content = content
        
        for pattern in self.pii_patterns:
            if pattern.search(sanitized_content):
                is_clean = False
                sanitized_content = pattern.sub("[REDACTED PII]", sanitized_content)
                logger.warning("PII detected and redacted from context.")
                
        return is_clean, sanitized_content
