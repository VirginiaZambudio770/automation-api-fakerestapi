#global fixtures

import pytest
from api_client.books_api import BooksAPI
from datetime import datetime, timezone
import uuid

books_api = BooksAPI()

@pytest.fixture
def valid_book_payload():
    #Valid Payload
    return {
        "id": 0,
        "title": f"Test Book {uuid.uuid4()}",  # Unique title
        "description": "This is a test book description",
        "pageCount": 123,
        "excerpt": "This is an excerpt",
        "publishDate": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }

@pytest.fixture
def invalid_book_payload():
    #Invalid Payload -invalid publishDate
    return {
        "id": 0,
        "title":"This is a title",
        "description": "This is the description",
        "pageCount": 1, 
        "excerpt": "This is an excerpt",
        "publishDate": "invalid"
    }
    
@pytest.fixture() #It is created by test file (scope="module")
def created_book(valid_book_payload):
    response = books_api.create_book(valid_book_payload)
    book = response.json()
    yield book
