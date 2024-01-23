from flask import Blueprint, current_app, jsonify, request
from .models import Book, print_post_requests, db

bp = Blueprint("books", __name__)


# Route '/books' för att hämta eller lägga till flera böcker
@bp.route("/", methods=["GET", "POST"])
def handle_books():
    if request.method == "POST":
        return add_books()
    else:
        return get_books()


# Hämtar böcker med möjlighet till filtrering
def get_books():
    title = request.args.get("title")
    author = request.args.get("author")
    genre = request.args.get("genre")

    books_data = Book.filter_books(title=title, author=author, genre=genre)
    if not books_data:
        return jsonify({"message": "No books found."}), 404
    return jsonify(books_data), 200


@print_post_requests
def add_books():
    try:
        data = request.get_json()
        new_books = Book.add_books(data)
        if not new_books:
            return jsonify({"message": "No books to add"}), 400
        return jsonify({"message": "Books added successfully!"}), 201
    except Exception as e:
        print(e)
        return (
            jsonify({"message": "Failed to add books.", "error": str(e)}),
            500,
        )


# Route '/books/<int:book_id>'för att hämta, updatera och radera en bok med book_id
@bp.route("/<int:book_id>", methods=["GET", "PUT", "DELETE"])
def handle_single_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if request.method == "GET":
        return get_book(book)
    elif request.method == "PUT":
        return update_book(book)
    elif request.method == "DELETE":
        return delete_book(book)


# Funktion för att hämta en specifik bok
def get_book(book):
    try:
        if not book:
            return jsonify({"message": "Book not found"}), 404
        return jsonify(book.as_dict()), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to get book."}), 500


# Uppdaterar en existerande bok
@print_post_requests
def update_book(book):
    if not book:
        return jsonify({"message": "Book not found"}), 404

    try:
        data = request.get_json()
        book.update(data)
        return jsonify({"message": "Book updated successfully!"}), 200
    except Exception as e:
        print(e)
        return (
            jsonify({"message": "Failed to update book.", "error": str(e)}),
            500,
        )


# Raderar en bok och tillhörande recensioner
def delete_book(book):
    if not book:
        return jsonify({"message": "Book not found"}), 404

    if not book.delete_book():
        return jsonify({"message": "Failed to delete book."}), 500

    return jsonify({"message": "Book deleted successfully!"}), 200


# Hämtar top 5 böcker med bäst betyg
@bp.route("/top", methods=["GET"])
def get_top_books():
    try:
        all_books = Book.query.all()
        if not all_books:
            return jsonify({"message": "Book not found"}), 404

        sorted_books = sorted(
            all_books,
            key=lambda book: book.calculate_avg_rating(),
            reverse=True,
        )

        top_books_data = sorted_books[:5]
        top_books = [book.as_dict() for book in top_books_data]
        return jsonify(top_books), 200

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
