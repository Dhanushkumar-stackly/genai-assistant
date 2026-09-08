from uuid import uuid4


class RAGService:
    """
    Service boundary for the existing RAG pipeline.
    """

    def __init__(self) -> None:
        self.documents: dict[str, dict] = {}

    def startup(self) -> None:
        return None

    def ingest_document(self, title: str, content: str) -> dict:
        document_id = str(uuid4())

        chunks = [
            chunk.strip()
            for chunk in content.split("\n\n")
            if chunk.strip()
        ]

        if not chunks:
            chunks = [content.strip()]

        self.documents[document_id] = {
            "document_id": document_id,
            "title": title,
            "content": content,
            "chunks": chunks,
            "status": "processed",
        }

        return {
            "document_id": document_id,
            "chunk_count": len(chunks),
            "status": "processed",
        }

    def get_document(self, document_id: str) -> dict | None:
        return self.documents.get(document_id)

    def ask(
        self,
        question: str,
        filters: dict | None = None,
    ) -> dict:
        if not self.documents:
            return {
                "answer": "No documents are available.",
                "sources": [],
            }

        document = next(iter(self.documents.values()))

        return {
            "answer": f"Answer based on document: {document['title']}",
            "sources": [
                {
                    "document_id": document["document_id"],
                    "title": document["title"],
                }
            ],
        }


rag_service = RAGService()


def get_rag_service() -> RAGService:
    return rag_service