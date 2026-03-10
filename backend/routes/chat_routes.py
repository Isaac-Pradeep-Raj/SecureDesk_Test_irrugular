from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.vector_service import search_chunks
from services.escalation_service import build_escalation_response

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/ask", methods=["POST"])
@jwt_required()
def ask():

    data = request.json
    query = data.get("query")
    department = data.get("department")

    # Retrieve relevant document chunks
    results = search_chunks(query)

    if not results:
        return jsonify({
            "answer": "No relevant information found in the knowledge base.",
            "classification": "PUBLIC",
            "escalation": None
        })

    # Use the single most relevant chunk safely handling unicode
    context = results[0]
    
    # Try encoding/decoding to ascii to drop problematic chars for json
    context = context.encode('ascii', 'ignore').decode('ascii')

    # Temporary classification logic
    # (Later we will fetch classification from DB)
    classification = "INTERNAL"

    answer = None
    escalation = None

    if classification in ["PUBLIC", "INTERNAL"]:

        answer = context

    elif classification == "RESTRICTED":

        answer = (
            context +
            "\n\nNote: Full information requires department approval."
        )

        escalation = build_escalation_response(
            department,
            classification
        )

    elif classification == "CONFIDENTIAL":

        answer = None

        escalation = build_escalation_response(
            department,
            classification
        )

    return jsonify({
        "answer": answer,
        "classification": classification,
        "escalation": escalation
    })