from typing import List, Sequence

from sentence_transformers import SentenceTransformer

from retrieval.config import (
    EMBEDDING_MODEL_NAME,
    BATCH_SIZE,
)


class EmbeddingService:
    """
    Service responsible for generating text embeddings.
    """

    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL_NAME,
        batch_size: int = BATCH_SIZE,
    ):
        self.model_name = model_name
        self.batch_size = batch_size

        self.model = SentenceTransformer(self.model_name)

    def encode(
        self,
        texts: Sequence[str],
        batch_size: int | None = None,
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple text chunks.
        """

        if not texts:
            return []

        cleaned_texts = []

        for text in texts:
            if not isinstance(text, str):
                raise TypeError("Every text must be a string")

            if not text.strip():
                raise ValueError("Text cannot be empty")

            cleaned_texts.append(text)

        effective_batch_size = batch_size or self.batch_size

        embeddings = self.model.encode(
            cleaned_texts,
            batch_size=effective_batch_size,
            convert_to_numpy=True,
            show_progress_bar=True,
        )

        return embeddings.tolist()

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        """

        if not isinstance(text, str):
            raise TypeError("text must be a string")

        if not text.strip():
            raise ValueError("text cannot be empty")

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
        )

        return embedding.tolist()

    def embed_texts(
        self,
        texts: Sequence[str],
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        """

        return self.encode(texts)

    def dimension(self) -> int:
        """
        Return embedding vector dimension.
        """

        return self.model.get_sentence_embedding_dimension()

    def model_info(self) -> dict:
        """
        Return embedding model information.
        """

        return {
            "model_name": self.model_name,
            "dimension": self.dimension(),
            "batch_size": self.batch_size,
        }