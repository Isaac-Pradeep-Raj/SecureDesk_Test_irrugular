from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from services.vector_service import search_chunks
from services.escalation_service import build_escalation_response
from database.db import get_db_connection
from datetime import datetime

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/ask", methods=["POST"])
@jwt_required()
def ask():

    data = request.json
    query = data.get("query")
    department = data.get("department")
    
    claims = get_jwt()
    user_role = claims.get("role")

    # Retrieve relevant document chunks
    results = search_chunks(query)

    if not results:
        return jsonify({
            "answer": "No relevant information found in the knowledge base.",
            "classification": "PUBLIC",
            "escalation": None
        })

    # Use the single most relevant chunk safely handling unicode
    context_obj = results[0]
    
    # Try encoding/decoding to ascii to drop problematic chars for json
    context_text = context_obj["text"].encode('ascii', 'ignore').decode('ascii')
    classification = context_obj["classification"]
    doc_domain = context_obj["domain"]

    answer = None
    escalation = None

    if classification in ["PUBLIC", "INTERNAL"]:
        answer = context_text

    elif classification == "RESTRICTED":
        if user_role == doc_domain or user_role == "SuperAdmin":
            answer = context_text
        else:
            # Check for approved access
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            req = cursor.execute("""
                SELECT * FROM access_requests
                WHERE requester_role=? AND target_domain=? AND classification='RESTRICTED'
                AND status='APPROVED' AND expires_at > ?
            """, (user_role, doc_domain, now)).fetchone()
            conn.close()

            if req:
                answer = context_text
            else:
                answer = (
                    context_text[:150] +
                    "...\n\n[NOTICE] Full information requires department approval."
                )

                escalation = build_escalation_response(
                    doc_domain,
                    classification
                )

    elif classification == "CONFIDENTIAL":
        if user_role == doc_domain or user_role == "SuperAdmin":
            answer = context_text
        else:
            # Check for approved access
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            req = cursor.execute("""
                SELECT * FROM access_requests
                WHERE requester_role=? AND target_domain=? AND classification='CONFIDENTIAL'
                AND status='APPROVED' AND expires_at > ?
            """, (user_role, doc_domain, now)).fetchone()
            conn.close()

            if req:
                answer = context_text
            else:
                answer = None
                escalation = build_escalation_response(
                    doc_domain,
                    classification
                )

    return jsonify({
        "answer": answer,
        "classification": classification,
        "escalation": escalation,
        "domain": doc_domain
    })