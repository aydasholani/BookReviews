
import pytest
from BookReviewsApi import create_app
from BookReviewsApi.models import db, Book, Review
from tests.seeds import seed_test_data 

TEST_CONFIG = {
    'TESTING': True,
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.sqlite'
}
    
@pytest.fixture
def app():
    app = create_app(TEST_CONFIG)

    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_test_data(db, Book, Review)
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

