"""Launch the PlantForge AI server from the ai-server directory."""
import os

from dotenv import load_dotenv

from app.main import create_app

load_dotenv()

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_ENV", "development") == "development"
    print(f"PlantForge AI Server running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
