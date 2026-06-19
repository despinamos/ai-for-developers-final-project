"""
Document Service

Provides:
  - validate_file(filename) → raises exception if file has a invalid extension
  - read_file(file: UploadFile) → returns text for file if file is valid
  - chunk_text(text, chunk_size, overlap) → returns chunks created from text
  - process_uploaded_file(file: UploadFile) → returns dictionary with file information
"""


from fastapi import UploadFile, HTTPException

class DocumentService:
    ALLOWED_EXTENSIONS = [".txt", ".md", ".py"]

    @staticmethod
    def validate_file(filename: str) -> None:
        """Validates acceptable file extensions."""
        if not any(filename.endswith(ext) for ext in DocumentService.ALLOWED_EXTENSIONS):
            raise HTTPException(
                status_code=400,
                detail="Only .txt, .md, and .py files are supported."
            )

    @staticmethod
    async def read_file(file: UploadFile) -> str:
        """Reads uploaded file after it is validated."""
        DocumentService.validate_file(file.filename)

        content = await file.read()

        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="File could not be decoded as UTF-8 text."
            )

        return text

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 1000,
        overlap: int = 150
    ) -> list[str]:
        """Chunks text."""
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += chunk_size - overlap

        return chunks

    @staticmethod
    async def process_uploaded_file(file: UploadFile) -> dict:
        """Includes the entire process for uploaded files, as it calls read_file and chunk_text."""
        text = await DocumentService.read_file(file)
        chunks = DocumentService.chunk_text(text)

        return {
            "filename": file.filename,
            "text": text,
            "chunks": chunks,
            "chunk_count": len(chunks),
            "preview": text[:500]
        }