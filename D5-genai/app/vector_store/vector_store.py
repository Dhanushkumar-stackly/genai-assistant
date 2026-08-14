from pathlib import Path

import chromadb


class VectorStore:

    def __init__(
        self,
        persist_directory: str = "vector_db",
        collection_name: str = "d5_chunks",
    ):

        self.persist_directory = Path(
            persist_directory
        )

        self.collection_name = (
            collection_name
        )

        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.client = chromadb.PersistentClient(
            path=str(
                self.persist_directory
            )
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={
                    "hnsw:space": "cosine"
                }
            )
        )

    def add_documents(
        self,
        ids,
        documents,
        embeddings,
        metadatas,
    ):

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def count(self):

        return self.collection.count()

    def search(
        self,
        query_embedding,
        top_k: int = 5,
    ):

        return self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )