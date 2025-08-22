# tests/test_post_book.py
import pytest
from api_client.books_api import BooksAPI
from config import config
from datetime import datetime, timezone
from http import HTTPStatus
from tests.utils.book_helpers import assert_book_data_matches
import uuid

books_api = BooksAPI()


def test_post_books_status_code_200(valid_book_payload):
    #Verify happy path returns 200 OK
    response = books_api.create_book(valid_book_payload)
    book_created = response.json()
    book_id = book_created["id"]
    assert response.status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK} but got {response.status_code}"
    
def test_post_books_content_type_json(valid_book_payload):
    # Verify header Content-Type is equals to Content-Type from config file
    response = books_api.create_book(valid_book_payload)
    assert response.headers["Content-Type"].startswith(config.HEADERS["Content-Type"].split("/")[0])

def test_post_books_returns_created_book_data(valid_book_payload):
    #Verify expected data 
    response = books_api.create_book(valid_book_payload)
    data = response.json()
    assert "id" in data
    assert_book_data_matches(valid_book_payload, data)

#  NEGATIVE TESTS 

def test_post_books_invalid_payload_returns_error(invalid_book_payload):
    #Verify that an invalid payload returns error code (400).
    response = books_api.create_book(invalid_book_payload)
    assert response.status_code == 400 
    data = response.json()
    assert "errors" in data 
    
def test_post_books_invalid_header_returns_error(invalid_book_payload):
    #Verify that an invalid content-type returns error code (415).
    headers = {"Content-Type": "1111"}
    response = books_api.create_book(invalid_book_payload, headers=headers)
    assert response.status_code == 415
    data = response.json()
    assert data.get("title") == "Unsupported Media Type"
        
@pytest.mark.skip(reason="It is skipped because this API doesnt requiere token yet")  
def test_post_books_without_token_should_fail(valid_book_payload):
    headers = {"Authorization": ""}  # No Authorization
    response = books_api.create_book(valid_book_payload, headers=headers)  
    assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
        f"Expected 401 or 403 but got {response.status_code}. Body: {response.text}"
    )
    data = response.json()
    assert "errors" in data 
