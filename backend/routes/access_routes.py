from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from database.db import get_db_connection
from datetime import datetime, timedelta

access_bp = Blueprint("access", __name__)

@access_bp.route("/request", methods=["POST"])
@jwt_required()
def request_access():
    data = request.json
    target_domain = data.get("domain")
    classification = data.get("classification")
    
    claims = get_jwt()
    requester_role = claims.get("role")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Determine who should approve this
    # For RESTRICTED -> The domain itself
    # For CONFIDENTIAL -> SuperAdmin
    if classification == "CONFIDENTIAL":
        approver = "SuperAdmin"
    else:
        approver = target_domain

    # Check if pending request already exists
    existing = cursor.execute("""
        SELECT id FROM access_requests 
        WHERE requester_role=? AND target_domain=? AND classification=? AND status='PENDING'
    """, (requester_role, target_domain, classification)).fetchone()

    if existing:
        conn.close()
        return jsonify({"msg": "Access request already pending"}), 400

    cursor.execute("""
        INSERT INTO access_requests (requester_role, target_domain, classification, status)
        VALUES (?, ?, ?, 'PENDING')
    """, (requester_role, target_domain, classification))
    
    conn.commit()
    conn.close()
    
    return jsonify({"msg": f"Access request sent to {approver}"}), 201

@access_bp.route("/requests", methods=["GET"])
@jwt_required()
def get_requests():
    claims = get_jwt()
    user_role = claims.get("role")

    conn = get_db_connection()
    cursor = conn.cursor()

    if user_role == "SuperAdmin":
        # SuperAdmin sees CONFIDENTIAL requests, and optionally any fallback.
        # But we'll specifically look for CONFIDENTIAL or requests targeted to SuperAdmin.
        # Actually any request for CONFIDENTIAL goes to SuperAdmin.
        reqs = cursor.execute("""
            SELECT id, requester_role, target_domain, classification, status, created_at, expires_at
            FROM access_requests
            WHERE status='PENDING' AND classification='CONFIDENTIAL'
        """).fetchall()
    else:
        # Department owners see RESTRICTED requests targeted to their domain
        reqs = cursor.execute("""
            SELECT id, requester_role, target_domain, classification, status, created_at, expires_at
            FROM access_requests
            WHERE status='PENDING' AND target_domain=? AND classification='RESTRICTED'
        """, (user_role,)).fetchall()

    conn.close()

    return jsonify([dict(r) for r in reqs]), 200

@access_bp.route("/approve", methods=["POST"])
@jwt_required()
def approve_request():
    data = request.json
    req_id = data.get("request_id")
    
    claims = get_jwt()
    user_role = claims.get("role")

    conn = get_db_connection()
    cursor = conn.cursor()

    req = cursor.execute("SELECT * FROM access_requests WHERE id=?", (req_id,)).fetchone()
    if not req:
        conn.close()
        return jsonify({"msg": "Request not found"}), 404
    
    # Verify auth
    if req["classification"] == "CONFIDENTIAL" and user_role != "SuperAdmin":
        conn.close()
        return jsonify({"msg": "Unauthorized"}), 403
    elif req["classification"] == "RESTRICTED" and req["target_domain"] != user_role:
        conn.close()
        return jsonify({"msg": "Unauthorized"}), 403

    # Approve and set expiration 1 minute from now
    expires_at = (datetime.utcnow() + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        UPDATE access_requests
        SET status='APPROVED', expires_at=?
        WHERE id=?
    """, (expires_at, req_id))

    conn.commit()
    conn.close()

    return jsonify({"msg": "Request approved for 1 minute."}), 200
