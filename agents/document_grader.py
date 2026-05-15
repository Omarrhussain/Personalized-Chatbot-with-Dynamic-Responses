class DocumentGrader:
    def grade(self, document: str, query: str) -> bool:
        """
        Grades whether the document is relevant to the query.
        Returns True if relevant, False otherwise.
        """
        # Simplistic grade: Check if any keyword in the query appears in the document
        keywords = query.lower().split()
        doc_lower = document.lower()
        return any(keyword in doc_lower for keyword in keywords)
