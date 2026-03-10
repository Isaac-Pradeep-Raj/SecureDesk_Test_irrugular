from app import create_app
from database.db import get_db_connection
from services.document_processor import process_document
from werkzeug.utils import secure_filename
import os

app = create_app()

with app.app_context():
    conn = get_db_connection()
    docs = conn.execute("SELECT id, filename FROM documents WHERE chunks = 0").fetchall()
    
    for doc in docs:
        doc_id = doc['id']
        original_name = doc['filename']
        secured_name = secure_filename(original_name)
        
        print(f"Processing doc {doc_id}: {original_name} -> {secured_name}")
        
        # update the db first so process_document gets the secured name
        cursor = conn.cursor()
        cursor.execute("UPDATE documents SET filename = ? WHERE id = ?", (secured_name, doc_id))
        conn.commit()
        
        process_document(doc_id, secured_name)

    conn.close()
    print("Done processing previous documents.")
