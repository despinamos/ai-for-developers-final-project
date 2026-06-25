"""
RAG Service

Provides:
  - index_uploaded_file(file: UploadFile, user_id) → indexes user uploaded file into chunks
  - answer_question(question, document_id, user_id, top_k) → answer question with simple response
  - answer_question_stream(question, document_id, user_id, top_k) → answer question with streaming response
"""

from fastapi import UploadFile

from app.services.document_service import DocumentService
from app.services.vector_store_service import VectorStoreService
from app.llm_client import LLMClient


class RAGService:

    @staticmethod
    async def index_uploaded_file(file: UploadFile, user_id: int | None = None) -> dict:
        """Indexes user uploaded file into chunks."""
        document = await DocumentService.process_uploaded_file(file)

        result = VectorStoreService.add_chunks(
            chunks=document["chunks"],
            filename=document["filename"],
            user_id=user_id
        )

        return {
            "document_id": result["document_id"],
            "filename": document["filename"],
            "chunk_count": document["chunk_count"],
            "chunks_stored": result["chunks_stored"],
            "preview": document["preview"]
        }

    @staticmethod
    def answer_question(
        question: str,
        document_id: str,
        user_id: int | None = None,
        top_k: int = 4
    ) -> dict:
        """Answer user question using information based on chunks retrieved from the user uploaded/selected file."""
        chunks = VectorStoreService.search(
            query=question,
            document_id=document_id,
            top_k=top_k,
            user_id=user_id
        )

        if not chunks:
            return {
                "answer": "I could not find any relevant uploaded context.",
                "sources": []
            }

        context = "\n\n---\n\n".join(chunks)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful RAG assistant for code and documents. "
                    "Answer only using the provided context. "
                    "If the answer is not in the context, say so clearly."
                )
            },
            {
                "role": "user",
                "content": f"""
                Context:
                {context}

                Question:
                {question}

                Answer clearly and concisely.
                """
            }
        ]

        answer = LLMClient.chat(messages)

        return {
            "answer": answer,
            "sources": chunks
        }
    
    @staticmethod
    def answer_question_stream(
        question: str,
        document_id: str,
        user_id: int,
        top_k: int = 4
    ):
        """Answer user question using information based on chunks retrieved from the user uploaded/selected file.
        Offers response in streams."""
        chunks = VectorStoreService.search(
            query=question,
            document_id=document_id,
            top_k=top_k,
            user_id=user_id
        )

        if not chunks:
            yield "I could not find any relevant uploaded context."
            return

        context = "\n\n---\n\n".join(chunks)

        messages = [
            {
                "role": "system",
                "content": (
                    """
                    You are a helpful RAG assistant.
                    Answer only using the provided context.
                    If the answer is not in the context, say so clearly."""
                )
            },
            {
                "role": "user",
                "content": f"""
    Context:
    {context}

    Question:
    {question}

    Answer clearly and concisely.
    """
            }
        ]

        for chunk in LLMClient.stream_chat(messages):
            yield chunk

        yield "\n\n---\n\n## Retrieved Sources\n" 
        
        for index, source in enumerate(chunks, start=1):
            yield f"\n### Source {index}\n```text\n{source[:1000]}\n```\n"