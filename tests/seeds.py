from flask import current_app, json
import asyncio

# Denna funktion tar samma data som finns i databasen i modulen BookReviewsApi
# och skapar tables med values för test-databasen
def seed_test_data(db, Book, Review):
    with current_app.open_resource("data.json") as f:
        data = json.load(f)

    for book_data in data.get("books", []):
        book = Book(**book_data)
        db.session.add(book)

    for review_data in data.get("reviews", []):
        review = Review(**review_data)
        db.session.add(review)
    db.session.commit()