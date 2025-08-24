import pytest
from api_client.books_api import BooksAPI
from config import config
from http import HTTPStatus
import requests

from tests.utils.book_helpers import assert_book_data_matches

books_api = BooksAPI()

def test_get_books_status_code_200():
    """Verify happy path returns 200 OK """
    response = books_api.get_books()
    assert response.status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK} but got {response.status_code}"

def test_get_books_content_type():
    """ Verify header Content-Type is equals to Content-Type from config file """
    response = books_api.get_books()
    assert response.headers["Content-Type"].startswith(config.HEADERS["Content-Type"].split("/")[0])

def test_get_books_body_not_empty():
    """ Verify Books body is not empty """
    response = books_api.get_books()
    assert len(response.text) > 0
    
#@pytest.mark.xfail(reason="API does not persist data, so GET after POST will fail")
def test_post_and_get_book_persists_data(valid_book_payload):
    """ Verify the post persists data """
    response = books_api.create_book(valid_book_payload)
    assert response.status_code == HTTPStatus.OK, (
        f"Expected 200 OK but got {response.status_code}. Body: {response.text}"
    )
    book_created = response.json()
    book_id = book_created["id"]
    get_response = books_api.get_book_by_id(book_id)
    assert get_response.status_code == HTTPStatus.OK, (
        f"Expected 200 OK but got {get_response.status_code}. Body: {get_response.text}"
    )
    book_retrieved = get_response.json()
    assert_book_data_matches(valid_book_payload, book_retrieved)

#  NEGATIVE TESTS 

def test_get_books_wrong_endpoint():
    """ Verify wrong endpoint -with a typo - returns 404 Not Found """
    response = requests.get(f"{config.BASE_URL}/api/v1/Bookss") 
    assert response.status_code == HTTPStatus.NOT_FOUND, f"Expected {HTTPStatus.NOT_FOUND} but got {response.status_code}. Body: {response.text}"
    
@pytest.mark.xfail(reason="API doesn´t recognize invalid header") 
def test_get_books_bad_request_invalid_header():
    """Verify invalid Content-Type header returns 400 Bad Request"""
    headers = {"Content-Type": "invalid/type"}  # Unsupported header 
    response = requests.get(f"{config.BASE_URL}/api/v1/Books", headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        f"Expected {HTTPStatus.BAD_REQUEST} but got {response.status_code}. Body: {response.text}"
    )

@pytest.mark.xfail(reason="API doesn´t recognize an invalid param")  
def test_get_books_bad_request_invalid_query():
    """Verify invalid query parameter returns 400 Bad Request"""
    params = {"id": "abc"}  # <> number
    response = requests.get(f"{config.BASE_URL}/api/v1/Books", params=params)
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        f"Expected {HTTPStatus.BAD_REQUEST} but got {response.status_code}. Body: {response.text}"
    )
    
@pytest.mark.xfail(reason="API does not require authentication") 
def test_get_books_without_token_should_fail():
    """ Verify status code 401 or 403 without token """
    headers = {"Authorization": ""}  # No Authorization
    response = books_api.get_books()
    assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
        f"Expected 401 or 403 but got {response.status_code}. Body: {response.text}"
    )
    data = response.json()
    assert "error" in data 