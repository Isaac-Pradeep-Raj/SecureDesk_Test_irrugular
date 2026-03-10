import fitz  # PyMuPDF
import os

from database.db import get_db_connection
from services.vector_service import add_chunks_to_index


UPLOAD_FOLDER = "uploads"


def extract_text_from_pdf(file_path):
    text = ""

    doc = fitz.open(file_path)

    for page in doc:
        text += page.get_text()

    doc.close()

    return text


def chunk_text(text, chunk_size=100):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def process_document(document_id, filename):

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return

    # Extract text
    text = extract_text_from_pdf(file_path)

    # Create chunks
    chunks = chunk_text(text)

    conn = get_db_connection()
    cursor = conn.cursor()

    for chunk in chunks:
        cursor.execute(
            """
            INSERT INTO document_chunks (document_id, chunk_text)
            VALUES (?, ?)
            """,
            (document_id, chunk),
        )

    # Update document metadata
    cursor.execute(
        """
        UPDATE documents
        SET processed = 1,
            chunks = ?
        WHERE id = ?
        """,
        (len(chunks), document_id),
    )

    conn.commit()
    conn.close()

    # Add to FAISS index
    if chunks:
        add_chunks_to_index(chunks)