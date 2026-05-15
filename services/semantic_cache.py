import hashlib
import json
import logging

logger = logging.getLogger(__name__)

class SemanticCache:
    def __init__(self):
        self.cache = {}

    def _hash_query(self, query: str) -> str:
        return hashlib.md5(query.lower().strip().encode('utf-8')).hexdigest()

    def get(self, query: str):
        key = self._hash_query(query)
        if key in self.cache:
            logger.info("Cache hit for query.")
            return self.cache[key]
        return None

    def set(self, query: str, response: str):
        key = self._hash_query(query)
        self.cache[key] = response
        logger.info("Response cached.")
