from database.db import get_db_connection
from services.vector_service import add_chunks_to_index


def load_chunks_into_vector_db():

    conn = get_db_connection()

    rows = conn.execute(
        """
        SELECT c.chunk_text, d.classification, d.domain 
        FROM document_chunks c
        JOIN documents d ON c.document_id = d.id
        """
    ).fetchall()

    conn.close()

    chunks_data = [
        {
            "text": row["chunk_text"],
            "classification": row["classification"],
            "domain": row["domain"]
        }
        for row in rows
    ]

    if chunks_data:
        add_chunks_to_index(chunks_data)