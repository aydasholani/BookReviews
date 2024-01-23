import pytest
   
# Testar hämtning av alla reviews
# Testar om alla keys existerar
# Testar första element i listan
def test_get_reviews(client):
    response = client.get("/reviews", follow_redirects=True)
    expected_keys = ["id", "book_id", "username", "review_text", "rating", "book_link"]
    
    for review in response.json:
        for key in expected_keys:
            assert key in review
        
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert response.json[0] == {
        "id": 1,
        "username": "reader1",
        "rating": 5,
        "review_text": "A powerful and thought-provoking novel that beautifully addresses societal issues.",
        "book_id": 1,
        "book_link": "http://localhost/books/1"
    }
    
# Testar hämta reviews för en bok
# Testa första reviewn i listan
@pytest.mark.parametrize("book_id", [10])
def test_get_reviews_single_book(client, book_id):
    response = client.get(f'/reviews/{book_id}', follow_redirects=True)
    
    assert response.status_code == 200
    assert response.json[0] == {
            "id": 35,
            "username": "dystopian_aficionado",
            "rating": 4,
            "review_text": "A thought-provoking exploration of a controlled society and the consequences of technological advancement.",
            "book_id": 10,
            "book_link": "http://localhost/books/10"
        }
    

# Testar skapa en review för en specifik bok
@pytest.mark.parametrize("book_id", [45])
def test_post_review(client, book_id):
    data = {
        "username": "Test Username",
        "rating": 5,
        "review_text": "Lorem Ipsum",
    }
    response = client.post(f'/reviews/{book_id}', json=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.json == {"message": "Review added successfully"}
    