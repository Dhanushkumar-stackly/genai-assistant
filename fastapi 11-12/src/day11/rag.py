class RAGService:
    """
    Application service responsible for communicating
    with the existing RAG pipeline.
    """

    def startup(self) -> None:
        """Initialize resources required by the RAG pipeline."""
        return None


rag_service = RAGService()