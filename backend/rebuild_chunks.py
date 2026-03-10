from app import create_app
from database.db import get_db_connection
from services.document_processor import process_document

app = create_app()

with app.app_context():
    conn = get_db_connection()
    
    # clear all existing chunks from db
    conn.execute("DELETE FROM document_chunks")
    conn.execute("UPDATE documents SET chunks = 0, processed = 0")
    conn.commit()

    # Re-process all documents
    docs = conn.execute("SELECT id, filename FROM documents").fetchall()
    for doc in docs:
        print(f"Re-processing doc {doc['id']}: {doc['filename']}")
        process_document(doc['id'], doc['filename'])

    conn.close()
    print("Done re-processing all documents to new chunk sizes.")
