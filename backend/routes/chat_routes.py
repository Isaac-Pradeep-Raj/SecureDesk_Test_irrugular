from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.escalation_service import build_escalation_response

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/ask", methods=["POST"])
@jwt_required()
def ask():

    data = request.json
    query = data.get("query")
    department = data.get("department")

    # MOCK classification (later comes from documents)
    classification = "RESTRICTED"  # demo

    answer = None
    escalation = None

    if classification in ["PUBLIC", "INTERNAL"]:
        answer = f"Answer related to '{query}'."

    elif classification == "RESTRICTED":
        answer = (
            "Partial information available. "
            "Full details require department approval."
        )
        escalation = build_escalation_response(
            department, classification
        )

    elif classification == "CONFIDENTIAL":
        escalation = build_escalation_response(
            department, classification
        )

    return jsonify({
        "answer": answer,
        "classification": classification,
        "escalation": escalation
    })