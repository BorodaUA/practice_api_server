from app import create_app
from app.config import DevelopmentConfig

app = create_app(config_name=DevelopmentConfig.CONFIG_NAME)

if __name__ == "__main__":
    app.run(host=app.config['APP_HOST'], port=app.config['APP_PORT'])
