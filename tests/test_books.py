import pytest

   
# Testar hämtning av böcker med filtrering av genre=fiction.
# Testar om alla keys existerar
# Testar första element i listan
def test_get_books(client):
    response = client.get("/books?genre=fiction", follow_redirects=True)
    expected_keys = ["id", "title", "author", "summary", "genre", "avg_rating"]
    
    for book in response.json:
        for key in expected_keys:
            assert key in book
        
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert response.json[0] == {
            "id": 1,
            "author": "Harper Lee",
            "title": "To Kill a Mockingbird",
            "summary": "A classic novel that explores racial injustice and moral growth in the American South.",
            "genre": "Fiction",
            "avg_rating": 4.0,
        }    

# Testar hämtning av top 5 böcker
def test_get_top_books(client):
    response = client.get("/books/top", follow_redirects=True )
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 5
    assert response.json[0] ==   {
        "id": 11,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "summary": "A fantasy novel that follows the adventures of Bilbo Baggins as he helps a group of dwarves reclaim their homeland.",
        "genre": "Fantasy",
        "avg_rating": 4.75,
    }

# Testar att lägga till bok/böcker     
def test_add_books(client):
    data = [
        {
        "title": "Test Title 1",
        "author": "Test Author name 1",
        "summary": "Lorem ipsum 1",
        "genre": "Lorem ipsum 1",
        },
        {
        "title": "Test Title 2",
        "author": "Test Author name 2",
        "summary": "Lorem ipsum 2",
        "genre": "Lorem ipsum 2",
        }
    ]
    response = client.post("/books", json=data, follow_redirects=True)
    assert response.status_code == 201
    

# Testar hämta en bok
@pytest.mark.parametrize("book_id", [1])
def test_get_book(client, book_id):
    response = client.get(f'/books/{book_id}', follow_redirects=True)
    
    assert response.status_code == 200
    expected_data = {
        "id": 1,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "summary": "A classic novel that explores racial injustice and moral growth in the American South.",
        "genre": "Fiction",
        "avg_rating": 4.0,
    }
    assert response.json == expected_data

# Testar updatera en bok 
@pytest.mark.parametrize("book_id", [1])
def test_update_book(client, book_id):
    data = {
        "title": "Test Changed Title",
        "author": "Test Changed Author Name",
        "summary": "Changed Lorem Ipsum",
        "genre": "Changed Lorem Ipsum",
    }
    response = client.put(f'/books/{book_id}', json=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.json == {"message": "Book updated successfully!"}
    
# Testar radera en bok
@pytest.mark.parametrize("book_id", [1])
def test_delete_book(client, book_id):
    response = client.delete(f'/books/{book_id}', follow_redirects=True)
    assert response.status_code == 200
    assert response.json == {"message": "Book deleted successfully!"}

