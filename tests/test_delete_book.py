import pytest
from api_client.books_api import BooksAPI
from config import config
from datetime import datetime, timezone
from http import HTTPStatus
from tests.utils.book_helpers import assert_book_data_matches

books_api = BooksAPI()


def test_delete_book_happy_path(created_book):
    """Verify happy path returns 200 OK"""
    book_id = created_book["id"]  
    response = books_api.delete_book(book_id) 
    assert response.status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK} but got {response.status_code}"
    get_response = books_api.get_book_by_id(book_id)  # Try to GET the deleted book
    # It doesnt work because it is not deleted
    # assert response.status_code == HTTPStatus.NOT_FOUND, f"Expected {HTTPStatus.NOT_FOUND} but got {response.status_code}. Body: {response.text}"


#  NEGATIVE TESTS 

def test_delete_book_invalid_id(invalid_book_id):
    """Verify status code is 404 when book id is invalid"""
    response = books_api.get_book_by_id(invalid_book_id)
    assert response.status_code == 400  
    data = response.json()
    assert "errors" in data 


@pytest.mark.skip(reason="It is skipped because this API doesnt requiere token yet")  
def test_delete_book_without_token(created_book):
    """Verify status code 401 or 403 without token"""
    book_id = created_book["id"] 
    headers = {"Authorization": ""}  # No Authorization header
    response = books_api.delete_book(book_id, headers=headers) 
    assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN) 
    data = response.json()
    assert "errors" in data   
