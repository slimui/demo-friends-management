from flask import Flask
from .config import Config


def create_app(config=Config):
    app = Flask(__name__)

    app.config.from_object(config)

    from .models import db
    db.init_app(app)

    from .blueprints.views import blueprint as views
    app.register_blueprint(views)

    # graphql endpoint
    from .graphql import schema
    from flask_graphql import GraphQLView
    graphql_view = GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    app.add_url_rule('/graphql', view_func=graphql_view)

    return app
