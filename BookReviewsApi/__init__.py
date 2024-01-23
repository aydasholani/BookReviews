import os
from flask import Flask, jsonify, request
from . import db_conn

# Create flask app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.json.sort_keys = False
    configure_app(app, test_config)
    register_blueprints(app)
    db_conn.init_app(app)

    @app.route("/", methods=["GET"])
    def index():
        ROOT_URL = request.url_root
        endpoints = {
            "GET/books": f"{ROOT_URL}books",
            "GET/books/top": f"{ROOT_URL}books/top",
            "GET/reviews": f"{ROOT_URL}reviews",
        }
        return jsonify(endpoints)

    app.add_url_rule("/", endpoint="index")

    return app

# Flask app configuration
def configure_app(app, test_config):
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'database.sqlite')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        app.config.from_pyfile(
            "config.py", silent=True
        )  # Silent=True står för att den inte gör någon felhantering om filen inte finns
    else:
        app.config.update(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


# Registrerar alla routes(Blueprints)
def register_blueprints(app):
    from . import books, reviews, author

    app.register_blueprint(books.bp, url_prefix="/books")
    app.register_blueprint(reviews.bp, url_prefix="/reviews")
    app.register_blueprint(author.bp, url_prefix="/author")
