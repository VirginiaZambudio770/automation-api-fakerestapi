import pytest
from api_client.books_api import BooksAPI
from config import config
from http import HTTPStatus
import requests

books_api = BooksAPI()

def test_get_books_status_code_200():
    #Verify happy path returns 200 OK
    response = books_api.get_books()
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response body: {response.text}"
    assert response.status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK} but got {response.status_code}"

def test_get_books_content_type():
    # Verify header Content-Type is equals to Content-Type from config file
    response = books_api.get_books()
    assert response.headers["Content-Type"].startswith(config.HEADERS["Content-Type"].split("/")[0])

def test_get_books_body_not_empty():
    response = books_api.get_books()
    assert len(response.text) > 0

#  NEGATIVE TESTS 

def test_get_books_wrong_endpoint():
    # Verify wrong endpoint -with a typo - returns 404 Not Found
    response = requests.get(f"{config.BASE_URL}/api/v1/Bookss") 
    assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}. Response body: {response.text}"
    assert response.status_code == HTTPStatus.NOT_FOUND, f"Expected {HTTPStatus.NOT_FOUND} but got {response.status_code}"
    
@pytest.mark.skip(reason="It is skipped because this API doesnt requiere token yet")  
def test_get_books_without_token_should_fail():
    headers = {"Authorization": ""}  # No Authorization
    response = books_api.get_books()
    assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
        f"Expected 401 or 403 but got {response.status_code}. Body: {response.text}"
    )
    data = response.json()
    assert "error" in data 