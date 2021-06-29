from typing import Optional

from flask import Flask, Response, jsonify

from .api import api
from .exceptions import ValidationException
from .models import db


def create_app(config: Optional[dict] = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE="postgresql://user:pass@localhost:5432/nory",
    )
    if config:
        app.config.update(config)

    @app.errorhandler(ValidationException)
    def handle_validation_error(error: ValidationException) -> Response:
        """Transforms caught ValidationException into a Json response"""
        response = jsonify(errors=error.message, detail='Validation Error')
        response.status_code = error.status_code
        return response

    db.init_app(app)
    app.register_blueprint(api)

    return app
