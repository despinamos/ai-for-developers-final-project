import uuid
import chromadb

from app.services.embedding_service import EmbeddingService


class VectorStoreService:
    _client = chromadb.PersistentClient(path="chroma_db")
    _collection = _client.get_or_create_collection(name="documents")

    @staticmethod
    def add_chunks(
        chunks: list[str],
        filename: str,
        user_id: int | None = None
    ) -> dict:
        embeddings = EmbeddingService.embed_texts(chunks)

        ids = []
        metadatas = []

        for index, chunk in enumerate(chunks):
            ids.append(str(uuid.uuid4()))
            metadatas.append({
                "filename": filename,
                "chunk_index": index,
                "user_id": str(user_id) if user_id else "anonymous"
            })

        VectorStoreService._collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        return {
            "filename": filename,
            "chunks_stored": len(chunks)
        }

    @staticmethod
    def search(
        query: str,
        top_k: int = 4,
        user_id: int | None = None
    ) -> list[str]:
        query_embedding = EmbeddingService.embed_text(query)

        where_filter = None
        if user_id:
            where_filter = {"user_id": str(user_id)}

        results = VectorStoreService._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter
        )

        return results["documents"][0]