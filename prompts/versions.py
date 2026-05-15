from prompts.types import PromptTemplate, PromptVariable

PROMPT_VERSIONS = {
    "rag_base": {
        "v1.0": PromptTemplate(
            name="rag_base",
            version="v1.0",
            template="Context: {context}\nQuestion: {question}\nAnswer:",
            variables=[PromptVariable("context", "Retrieved documents"), PromptVariable("question", "User query")]
        ),
        "v1.1": PromptTemplate(
            name="rag_base",
            version="v1.1",
            template=(
                "You are a helpful, knowledgeable AI assistant.\n\n"
                "You may be given some retrieved context below. "
                "If the context is relevant to the user's question, use it to enrich your answer. "
                "If the context is NOT relevant or is empty, answer the question using your own knowledge. "
                "Never say 'there is no information' — always provide a helpful response.\n\n"
                "--- Retrieved Context ---\n{context}\n--- End Context ---\n\n"
                "{history}"
                "User: {question}\n\n"
                "Assistant:"
            ),
            variables=[
                PromptVariable("context", "Retrieved documents"),
                PromptVariable("history", "Conversation history", required=False),
                PromptVariable("question", "User query")
            ]
        )
    }
}
