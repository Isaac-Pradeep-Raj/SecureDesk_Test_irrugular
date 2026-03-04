import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.utils import secure_filename

from database.db import get_db_connection

doc_bp = Blueprint("documents", __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_DOMAINS = {"HR", "DEV", "IT", "Security"}
ALLOWED_CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "RESTRICTED", "CONFIDENTIAL"}


@doc_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_document():
    claims = get_jwt()
    role = claims.get("role")

    if role != "SuperAdmin":
        return jsonify({"msg": "Only admin can upload documents"}), 403

    if "file" not in request.files:
        return jsonify({"msg": "No file provided"}), 400

    file = request.files["file"]
    domain = request.form.get("domain")
    classification = request.form.get("classification")

    if file.filename == "":
        return jsonify({"msg": "Empty filename"}), 400

    if domain not in ALLOWED_DOMAINS:
        return jsonify({"msg": "Invalid domain"}), 400

    if classification not in ALLOWED_CLASSIFICATIONS:
        return jsonify({"msg": "Invalid classification"}), 400

    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({"msg": "Invalid filename"}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    user = get_jwt_identity()

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO documents (filename, domain, classification, uploaded_by) VALUES (?, ?, ?, ?)",
        (filename, domain, classification, user),
    )
    conn.commit()
    conn.close()

    return jsonify({"msg": "File uploaded successfully"})
