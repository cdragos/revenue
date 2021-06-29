from typing import Optional

from flask import Flask

from .models import db


def create_app(config: Optional[dict] = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE="postgresql://user:pass@localhost:5432/nory",
    )
    if config:
        app.config.update(config)

    db.init_app(app)

    return app
