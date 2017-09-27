from flask import Flask
from .config import Config


def create_app(config=Config):
    app = Flask(__name__)

    app.config.from_object(config)

    from .blueprints.views import blueprint as views
    app.register_blueprint(views)

    return app
