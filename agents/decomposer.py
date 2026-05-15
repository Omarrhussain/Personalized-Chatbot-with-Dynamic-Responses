class Decomposer:
    def decompose(self, query: str) -> list[str]:
        """
        Decomposes a complex query into simpler sub-queries.
        """
        if " and " in query.lower():
            return [q.strip() for q in query.lower().split(" and ")]
        return [query]
