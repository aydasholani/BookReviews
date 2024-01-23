
from flask import current_app, g, logging
import click
import json
from .models import db, Book, Review

# Databas connection
def get_db():
    if not hasattr(g, "db"):
        g.db = db.engine.connect()
    return g.db

# Stänger databasconnection efter varje request
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

# Initierar databasen 
@click.command("init-db")
def init_db():
    db.drop_all()
    db.create_all()
    with current_app.open_resource("data.json") as f:
        data = json.load(f)
        for book_data in data.get("books", []):
            book = Book(**book_data)
            db.session.add(book)

        for review_data in data.get("reviews", []):
            review = Review(**review_data)
            db.session.add(review)

    db.session.commit()
    print("Database initialization successful.")

# Initierar appen, appkontext och lägger till init-db commando
def init_app(app):
    db.init_app(app)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)
