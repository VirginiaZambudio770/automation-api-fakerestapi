import pytest
from api_client.books_api import BooksAPI
from config import config
from datetime import datetime, timezone
from http import HTTPStatus
from tests.utils.book_helpers import assert_book_data_matches

books_api = BooksAPI()


def test_put_book_happy_path(created_book, valid_book_payload):
    #Verify happy path returns 200 OK
    book_id = created_book["id"]
    response = books_api.update_book(book_id, valid_book_payload)  
    assert response.status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK} but got {response.status_code}"
    
def test_put_books_content_type_json(created_book, valid_book_payload):
    # Verify header Content-Type is equals to Content-Type from config file
    book_id = created_book["id"]
    response = books_api.update_book(book_id, valid_book_payload) 
    assert response.headers["Content-Type"].startswith(config.HEADERS["Content-Type"].split("/")[0])
    
def test_put_books_returns_created_book_data(created_book, valid_book_payload): 
    #Verify expected data 
    book_id = created_book["id"]
    response = books_api.update_book(book_id, valid_book_payload)    
    data = response.json()
    assert data["id"] == book_id
    assert_book_data_matches(valid_book_payload, data)


#  NEGATIVE TESTS 

def test_put_book_invalid_payload(created_book, invalid_book_payload):
    #Verify that an invalid payload returns error code (400).
    book_id = created_book["id"]
    response = books_api.update_book(book_id, invalid_book_payload)
    assert response.status_code == 400
    data = response.json()
    assert "errors" in data

def test_put_book_invalid_header(created_book, invalid_book_payload):
    #Verify that an invalid content-type returns error code (415).
    book_id = created_book["id"]
    headers = {"Content-Type": "1111"}
    response = books_api.update_book(book_id, invalid_book_payload, headers=headers)
    assert response.status_code == 415
    data = response.json()
    assert data.get("title") == "Unsupported Media Type"

@pytest.mark.skip(reason="It is skipped because this API doesnt requiere token yet")  
def test_put_book_without_token(created_book, valid_book_payload):
    book_id = created_book["id"]
    headers = {"Authorization": ""} # No Authorization
    response = books_api.update_book(book_id, valid_book_payload, headers=headers)
    assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
    data = response.json()
    assert "errors" in data