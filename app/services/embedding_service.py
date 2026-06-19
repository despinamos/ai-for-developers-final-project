"""
Embedding Service - Creates an embedder through OpenAIEmbeddings

Provides:
  - embed_text(text) → Converts a text string into embedding vector.
  - embed_textx(text: list) → Converts multiple text chunks into embedding vectors.
"""

from langchain_openai import OpenAIEmbeddings

EMBED_MODEL = "text-embedding-3-small"

class EmbeddingService:
    _embedder = OpenAIEmbeddings(model=EMBED_MODEL)

    @staticmethod
    def embed_text(text: str) -> list[float]:
        """
        Converts one text string into one embedding vector.
        """
        return EmbeddingService._embedder.embed_query(text)
    
    @staticmethod
    def embed_texts(texts: list[str]) -> list[list[float]]:
        """
        Converts multiple text chunks into embedding vectors.
        """
        return EmbeddingService._embedder.embed_documents(texts)