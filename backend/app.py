from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from database.db import init_db
from security.jwt_handler import jwt
from routes.document_routes import doc_bp
from routes.auth_routes import auth_bp
from routes.chat_routes import chat_bp
from services.vector_loader import load_chunks_into_vector_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    jwt.init_app(app)
    init_db()
    load_chunks_into_vector_db()
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(doc_bp, url_prefix="/api/docs")

    @app.route("/")
    def home():
        return {"message": "SecureDesk Backend Running"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)