from functools import wraps
from flask import Blueprint, request, jsonify
from .models import Book, Review, print_post_requests, db

bp = Blueprint("reviews", __name__)

# Hämta alla reviews
@bp.route("/", methods=["GET"])
def get_reviews():
    try:
        reviews = Review.query.all()
        reviews_data = [review.as_dict() for review in reviews]
        return jsonify(reviews_data), 200
    except Exception as e:
        return (
            jsonify({"message": "Failed to get reviews.", "error": str(e)}),
            500,
        )


@bp.route("/<int:book_id>", methods=["GET", "POST"])
def handle_reviews(book_id):
    if request.method == "GET":
        return get_reviews_single_book(book_id)
    elif request.method == "POST":
        return create_review(book_id)


# Hämta alla review för en bok
def get_reviews_single_book(book_id):
    try:
        reviews = Review.query.filter_by(book_id=book_id).all()
        if not reviews:
            return jsonify({"message": "No reviews found for the book"}), 404
        reviews_data = [review.as_dict() for review in reviews]
        return jsonify(reviews_data), 200
    except Exception as e:
        return (
            jsonify({"message": "Failed to get reviews.", "error": str(e)}),
            500,
        )

# Skapa ny review för en bok
@print_post_requests
def create_review(book_id):
    data = request.get_json()
    book = Book.query.filter_by(id=book_id).first()

    if not book:
        return jsonify({"message": "Book not found"}), 404

    # Kollar om alla fält är ifyllda
    required_fields = {"username", "rating", "review_text"}
    if not required_fields.issubset(data):
        return jsonify({"message": "Missing required fields"}), 400

    try:
        new_review = Review(book_id=book_id, **data)
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review added successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return (
            jsonify({"message": f"Failed to add review. Reason: {str(e)}"}),
            500,
        )
