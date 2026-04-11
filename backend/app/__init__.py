"""
Finvee Backend - Flask Application Factory
"""

import os
import warnings

warnings.filterwarnings("ignore", message=".*resource_tracker.*")

from flask import Flask, request
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logger, get_logger


def create_app(config_class=Config):
    """Flask application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    if hasattr(app, "json") and hasattr(app.json, "ensure_ascii"):
        app.json.ensure_ascii = False

    logger = setup_logger("finvee")

    is_reloader_process = os.environ.get("WERKZEUG_RUN_MAIN") == "true"
    debug_mode = app.config.get("DEBUG", False)
    should_log_startup = not debug_mode or is_reloader_process

    if should_log_startup:
        logger.info("=" * 50)
        logger.info("Finvee Backend Starting...")
        logger.info("=" * 50)

    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-User-ID", "Accept-Language"],
    )

    @app.before_request
    def log_request():
        logger = get_logger("finvee.request")
        logger.debug(f"Request: {request.method} {request.path}")
        if request.content_type and "json" in request.content_type:
            logger.debug(f"Request Body: {request.get_json(silent=True)}")

    @app.after_request
    def log_response(response):
        logger = get_logger("finvee.request")
        logger.debug(f"Response: {response.status_code}")
        return response

    # Import blueprints directly to avoid circular import issues
    from .api.auth import auth_bp
    from .api.financial import financial_bp
    from .api.learning import learning_bp
    from .api.simulation import simulation_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(financial_bp, url_prefix="/api/financial")
    app.register_blueprint(learning_bp, url_prefix="/api/learning")
    app.register_blueprint(simulation_bp, url_prefix="/api/simulation")

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "Finvee Backend"}

    if should_log_startup:
        logger.info("Finvee Backend Started")

    return app
