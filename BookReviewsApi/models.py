from functools import wraps
from flask import jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


# Scehmas för Book och Review
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text)
    genre = db.Column(db.String(100), nullable=False)
    reviews = db.relationship(
        "Review",
        backref="book",
        lazy=True,
    )

    # Denna function returnerar boken som en dict tillsammans med avg_rating och länk till författaren
    def as_dict(self):
        avg_rating = self.calculate_avg_rating()

        base_dict = {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

        base_dict["avg_rating"] = avg_rating

        return base_dict

    # Function för att uppdatera information om boken
    def update(self, data):
        self.title = data.get("title", self.title)
        self.author = data.get("author", self.author)
        self.summary = data.get("summary", self.summary)
        self.genre = data.get("genre", self.genre)
        db.session.commit()

    # Function för att radera boken
    def delete_book(self):
        Review.query.filter_by(book_id=self.id).delete()
        db.session.delete(self)
        db.session.commit()
        return True

    # Function som räknar ut genomsnittliga betyget för boken
    def calculate_avg_rating(self):
        avg_rating = (
            db.session.query(func.avg(Review.rating))
            .filter(Review.book_id == self.id)
            .scalar()
        )
        avg_rating = round(avg_rating, 2) if avg_rating else 0
        return avg_rating

    # Classmethod för att filtrera och hämta alla böcker
    @classmethod
    def filter_books(cls, title=None, author=None, genre=None):
        filters = {
            key: value
            for key, value in {
                "title": title,
                "author": author,
                "genre": genre,
            }.items()
            if value
        }

        try:
            books_query = cls.query.filter(
                *(
                    getattr(cls, key).ilike(f"%{value}%")
                    for key, value in filters.items()
                )
            )
            books = books_query.all()

            return [book.as_dict() for book in books] if books else False
        except Exception as e:
            print(f"An error occurred in filter_books: {e}")
            db.session.rollback()

    # En classmethod för att lägga till böcker
    @classmethod
    def add_books(cls, book_data_list):
        try:
            new_books = [cls(**book_data) for book_data in book_data_list]
            db.session.add_all(new_books)
            db.session.commit()

            return new_books
        except Exception as e:
            db.session.rollback()
            return (
                jsonify({"message": "Failed to add books.", "error": str(e)}),
                500,
            )


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)

    def as_dict(self):
        review_dict = {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

        # Inkluderar en länk till boken
        if hasattr(self, "book") and self.book:
            review_dict["book_link"] = url_for(
                "books.handle_single_book",
                book_id=self.book.id,
                _external=True,
            )

        return review_dict


# Wrapper för att printa ut POST requests
def print_post_requests(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == "POST" or request.method == "PUT":
            print(f"POST request received. Data: {request.get_json()}")
        return func(*args, **kwargs)

    return wrapper
