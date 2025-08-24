#global fixtures

import pytest
from api_client.books_api import BooksAPI
from datetime import datetime, timezone
from http import HTTPStatus
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
    
@pytest.fixture() #It is created by test file if use(scope="module")
def created_book(valid_book_payload):
    # Create book with POST
    response = books_api.create_book(valid_book_payload)
    assert response.status_code == HTTPStatus.OK or response.status_code == HTTPStatus.CREATED, \
        f"Failed to create book. Status: {response.status_code}, Body: {response.text}"
    book_data = response.json()
    book_id = book_data.get("id")
    # Cleanup: delete the book after test
    yield book_data
    books_api.delete_book(book_id)
    
@pytest.fixture
def existing_book():
    return {
        "id": 1,
        "title": "Book 1",
        "description": "Lorem lorem lorem. Lorem lorem lorem. Lorem lorem lorem.\n",
        "pageCount": 100,
        "excerpt": "Lorem lorem lorem. Lorem lorem lorem. Lorem lorem lorem.\n"
    } 
    
@pytest.fixture
def invalid_book_id():
    return 9999999999

@pytest.fixture
def non_exist_book_id():
    return 555

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        rep.description = str(item.function.__doc__)
        rep.custom_message = getattr(item.function, "custom_message", "")

# Add docstrings to HTML report 
def pytest_html_results_table_row(report, cells):
    if hasattr(report, "description") and report.description:
        # Insert docstring before test column
        cells.insert(1, report.description)