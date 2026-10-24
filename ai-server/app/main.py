"""PlantForge AI Server Main Entrypoint"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from .routes.identify import identify_bp
from .services.vision_service import provider_status

# 환경 변수 로드
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # 헬스체크 라우트
    @app.route("/", methods=["GET"])
    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "online",
            "service": "PlantForge AI Server",
            "version": "1.0.0",
            "provider": provider_status(),
        }), 200

    # 블루프린트 등록
    app.register_blueprint(identify_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_ENV", "development") == "development"
    print(f"🌿 PlantForge AI Server running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
