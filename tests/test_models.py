from BookReviewsApi.models import Book, Review

# Testar modellerna
def test_book_model():
    book = Book(title="Test Title", author="Test Author", genre="Test Genre", summary="Test Summary")
    assert book.title == "Test Title"
    assert book.author == "Test Author"
    assert book.genre == "Test Genre"
    assert book.summary == "Test Summary"
    print("Test Book Model Passed")
    
def test_review_model():
    review = Review(book_id=1, username="Test Username", rating=5, review_text="Test Review Text")
    assert review.book_id == 1
    assert review.username == "Test Username"
    assert review.rating == 5
    assert review.review_text == "Test Review Text"
    print("Test Review Model Passed")

