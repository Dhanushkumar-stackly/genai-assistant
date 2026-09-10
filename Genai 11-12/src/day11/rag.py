from uuid import uuid4


class NoEvidenceError(Exception):
    """Raised when the RAG pipeline has no usable evidence."""


class RAGService:
    """Service boundary for the existing RAG pipeline."""

    def __init__(self) -> None:
        self.documents: dict[str, dict] = {}
        self.ready = False

    def startup(self) -> None:
        self.ready = True

    def shutdown(self) -> None:
        self.ready = False

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

    def ask(self, question: str, filters: dict | None = None) -> dict:
        if not self.documents:
            raise NoEvidenceError("No evidence is available for this question")

        document = next(iter(self.documents.values()))
        return {
            "answer": f"Answer based on document: {document['title']}",
            "sources": [
                {
                    "document_id": document["document_id"],
                    "title": document["title"],
                    "score": 1.0,
                }
            ],
        }


rag_service = RAGService()


def get_rag_service() -> RAGService:
    return rag_service
