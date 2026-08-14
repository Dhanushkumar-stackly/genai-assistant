from __future__ import annotations

from typing import Any

from app.embeddings import EmbeddingModel


class SemanticSearcher:

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_model: EmbeddingModel,
    ) -> None:

        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def search(
        self,
        query: str,
        top_k: int = 3,
        metadata_filter: dict[str, Any] | None = None,
        min_score: float | None = None,
    ) -> list[dict[str, Any]]:

        # -----------------------------------------------
        # Validate query
        # -----------------------------------------------

        if not query.strip():

            raise ValueError(
                "Search query cannot be empty."
            )

        # -----------------------------------------------
        # Query → embedding
        # -----------------------------------------------

        query_embedding = self.embedding_model.encode(
            [query],
            batch_size=1,
        )[0]

        # -----------------------------------------------
        # ChromaDB search
        # -----------------------------------------------

        raw_results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        # -----------------------------------------------
        # Extract ChromaDB results
        # -----------------------------------------------

        ids = raw_results.get(
            "ids",
            [[]]
        )[0]

        documents = raw_results.get(
            "documents",
            [[]]
        )[0]

        metadatas = raw_results.get(
            "metadatas",
            [[]]
        )[0]

        distances = raw_results.get(
            "distances",
            [[]]
        )[0]

        results = []

        # -----------------------------------------------
        # Convert results
        # -----------------------------------------------

        for index, chunk_id in enumerate(ids):

            metadata = {}

            if index < len(metadatas):

                metadata = (
                    metadatas[index]
                    or {}
                )

            distance = 0.0

            if index < len(distances):

                distance = distances[index]

            # Cosine distance:
            # 0 = most similar
            #
            # Convert to similarity score.
            score = 1.0 - distance

            text = ""

            if index < len(documents):

                text = documents[index]

            # -------------------------------------------
            # Metadata filter
            # -------------------------------------------

            if metadata_filter:

                if not self._matches_filter(
                    metadata,
                    metadata_filter,
                ):

                    continue

            # -------------------------------------------
            # Minimum score
            # -------------------------------------------

            if min_score is not None:

                if score < min_score:

                    continue

            # -------------------------------------------
            # Result object
            # -------------------------------------------

            result = {

                "chunk_id":
                    chunk_id,

                "text":
                    text,

                "score":
                    score,

                "distance":
                    distance,

                **metadata,
            }

            results.append(result)

        return results[:top_k]

    @staticmethod
    def _matches_filter(
        metadata: dict[str, Any],
        metadata_filter: dict[str, Any],
    ) -> bool:

        for key, expected_value in (
            metadata_filter.items()
        ):

            if metadata.get(key) != expected_value:

                return False

        return True