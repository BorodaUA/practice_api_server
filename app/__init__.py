from flask import Flask

from app.config import configs
from hello_world import hello_world_bp


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    app.register_blueprint(hello_world_bp)
    return app
