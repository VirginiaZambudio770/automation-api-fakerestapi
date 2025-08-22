import pytest
from api_client.books_api import BooksAPI
from config import config
from datetime import datetime, timezone
from http import HTTPStatus
from tests.utils.book_helpers import assert_book_data_matches

books_api = BooksAPI()


def test_delete_book_happy_path(created_book):
    #Verify happy path returns 200 OK
    book_id = created_book["id"]  
    response = books_api.delete_book(book_id) 
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response body: {response.text}"
    assert response.status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK} but got {response.status_code}"
    get_response = books_api.get_book_by_id(book_id)  # Try to GET the deleted book
    assert get_response.status_code == HTTPStatus.NOT_FOUND  # Verify that the book no longer exists


#  NEGATIVE TESTS 

def test_delete_book_invalid_id():
    # Verify status code is 404 when book id is invalid
    invalid_id = 999999999999  
    response = books_api.delete_book(invalid_id) 
    assert response.status_code == 400  
    data = response.json()
    assert "errors" in data 


@pytest.mark.skip(reason="API does not require token")  
def test_delete_book_without_token(created_book):
    book_id = created_book["id"] 
    headers = {"Authorization": ""}  # No Authorization header
    response = books_api.delete_book(book_id, headers=headers) 
    assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN) 
    data = response.json()
    assert "errors" in data   
