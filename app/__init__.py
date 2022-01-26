from flask import Flask, g

from marshmallow.exceptions import ValidationError

from app.config import configs
from common.constants.api import ApiVersion
from db import get_session
from users.routers import users_bp
from users.utils.exceptions import UserNotFoundError, user_not_found_error_handler, user_validation_error_handler


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    app.register_blueprint(users_bp, url_prefix=f'/api/v{ApiVersion.V1.value}/{users_bp.url_prefix}')
    app.register_error_handler(ValidationError, user_validation_error_handler)
    app.register_error_handler(UserNotFoundError, user_not_found_error_handler)

    @app.before_request
    def set_session() -> None:
        """Adding sqlalchemy session to the flask g object."""
        g.db_session = get_session()

    @app.teardown_appcontext
    def remove_session(exception=None) -> None:
        """Closing sqlalchemy session on the app teardown."""
        if g.db_session:
            g.db_session.remove()

    return app
