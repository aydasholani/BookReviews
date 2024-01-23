# Testar resultatet av endpointen "/"
def test_index(client):
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert response.json == {
        "GET/books": "http://localhost/books",
        "GET/books/top": "http://localhost/books/top",
        "GET/reviews": "http://localhost/reviews",
    }