class AdaptiveRouter:
    def route(self, query: str) -> str:
        """
        Routes the query to the best appropriate handler based on intent.
        Returns the name of the route.
        """
        lower_query = query.lower()
        if "hi" in lower_query or "hello" in lower_query:
            return "chitchat"
        elif "summarize" in lower_query:
            return "summarization"
        else:
            return "qa"
