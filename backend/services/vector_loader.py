from database.db import get_db_connection
from services.vector_service import add_chunks_to_index


def load_chunks_into_vector_db():

    conn = get_db_connection()

    rows = conn.execute(
        "SELECT chunk_text FROM document_chunks"
    ).fetchall()

    conn.close()

    chunks = [row["chunk_text"] for row in rows]

    if chunks:
        add_chunks_to_index(chunks)