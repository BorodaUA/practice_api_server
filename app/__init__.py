from flask import Flask, g

from flask_jwt_extended import JWTManager
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from app.config import configs
from auth.routers import auth_bp
from auth.utils.exceptions import AuthUserInvalidPasswordException, invalid_user_password_error_handler
from common.constants.api import ApiVersion
from db import create_db_engine, get_session
from students.routers import students_bp
from students.utils.exceptions import TeacherExistsError, teacher_exists_error_handler
from teachers.routers import teachers_bp
from teachers.utils.exceptions import StudentExistsError, student_exists_error_handler
from users.routers import users_bp
from users.utils.exceptions import UserNotFoundError, user_not_found_error_handler, user_validation_error_handler
from utils.exceptions import duplicate_error_handler
from utils.jwt import generic_token_verifier


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    # JWT initialization.
    jwt = JWTManager()
    jwt.init_app(app)
    jwt.token_verification_loader(generic_token_verifier)
    # Blueprints registering.
    blueprints_register(app=app)
    # Error handlers registering.
    error_handler_register(app=app)

    app.db_engine = create_db_engine(config=app.config, echo=app.config['SQLALCHEMY_ENGINE_ECHO'])

    @app.before_request
    def set_session() -> None:
        """Adding sqlalchemy session to the flask g object."""
        g.db_session = get_session(engine=app.db_engine)

    @app.teardown_appcontext
    def remove_session(exception=None) -> None:
        """Closing sqlalchemy session on the app teardown."""
        if g.db_session:
            g.db_session.remove()

    return app


def blueprints_register(app: Flask) -> Flask:
    """Registers blueprints in the flask app."""
    app.register_blueprint(users_bp, url_prefix=f'/api/v{ApiVersion.V1.value}/{users_bp.url_prefix}')
    app.register_blueprint(auth_bp, url_prefix=f'/api/v{ApiVersion.V1.value}/{auth_bp.url_prefix}')
    app.register_blueprint(teachers_bp, url_prefix=f'/api/v{ApiVersion.V1.value}/{teachers_bp.url_prefix}')
    app.register_blueprint(students_bp, url_prefix=f'/api/v{ApiVersion.V1.value}/{students_bp.url_prefix}')
    return app


def error_handler_register(app: Flask) -> Flask:
    """Registers error handlers in the flask app."""
    app.register_error_handler(ValidationError, user_validation_error_handler)
    app.register_error_handler(UserNotFoundError, user_not_found_error_handler)
    app.register_error_handler(IntegrityError, duplicate_error_handler)
    app.register_error_handler(AuthUserInvalidPasswordException, invalid_user_password_error_handler)
    app.register_error_handler(StudentExistsError, student_exists_error_handler)
    app.register_error_handler(TeacherExistsError, teacher_exists_error_handler)
    return app
