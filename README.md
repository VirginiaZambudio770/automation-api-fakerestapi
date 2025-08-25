## Automation API Project

Automation of FakerestAPI APIs with Python:
This project implements automated tests for the Books API using Python, Pytest, and GitHub Actions for continuous integration.

## Description

The API allows managing books with CRUD operations.
Supported endpoints:

GET /api/v1/Books – Retrieve a list of all books.
GET /api/v1/Books/{id} – Retrieve details of a specific book by its ID.
POST /api/v1/Books – Add a new book.
PUT /api/v1/Books/{id} – Update an existing book by its ID.
DELETE /api/v1/Books/{id} – Delete a book by its ID.

## Project Structure

AUTOMATION-API-PYTHON/
├── .github/
├── .pytest_cache/
├── api_client/ # Likely contains API client classes or functions
├── assets/ # Report style file
├── config/ # Configuration files (URL, endpoint, header)
├── reports/ # Test reports (HTML, logs)
├── tests/
│ ├── **pycache**/ # Python cache files
│ ├── utils/ # Utility functions or helper methods
│ ├── conftest.py # Pytest configuration and fixtures
│ ├── test_delete_book.py # Tests for DELETE /Books/{id}
│ ├── test_get_books_by_id.py # Tests for GET /Books/{id}
│ ├── test_get_books.py # Tests for GET /Books
│ ├── test_post_book.py # Tests for POST /Books
│ └── test_put_book.py # Tests for PUT /Books/{id}
├── venv/ # Python virtual environment
│ ├── Include/
│ ├── Lib/
│ └── Scripts/
├── .gitignore
├── README.md
└── requirements.txt

## Requirements

Python 3.9+
pip
virtualenv (recommended)

Create and activate virtual environment:
python -m venv venv

# Windows

venv\Scripts\activate

# Mac/Linux

source venv/bin/activate

Install dependencies:
pytest
requests
pytest-html
python-dotenv
pip install -r requirements.txt

## Run Tests Locally

1. Clone the repository
   git clone https://github.com/VirginiaZambudio770/automation-api-fakerestapi.git
   cd automation-api-fakerestapi
2. Set up environment variables in config.py:
   BASE_URL = "https://fakerestapi.azurewebsites.net"
   BOOKS_ENDPOINT = "/api/v1/Books"
   HEADERS = {"Content-Type": "application/json"}
3. Run all tests:
   pytest -v --self-contained-html
4. Run specific tests (e.g., GET):
   pytest tests/test_get_books.py

## Continuous Integration with GitHub Actions

This project includes a workflow that:
Installs dependencies
Runs tests
Generates an HTML report in the reports folder

## Test Reports

Generates HTML reports with Pytest locally, as a history, in reports folder with detailed execution results and timestamp, using the following command:
$fecha = Get-Date -Format "yyyyMMdd_HHmmss"
pytest -v --html="reports/report_$fecha.html" --self-contained-html

## CI/CD with GitHub Actions

The workflow is defined in .github/workflows/ci.yml.
It runs automatically on:
Push to main or feature/_
Pull requests to main or feature/_
Manual trigger from the GitHub Actions tab (Run workflow button).

## Where to find results

After the job finishes, go to the Actions tab → select the workflow run → Artifacts section.
Download the test-report artifact to view the HTML test report. Open it with a browser.

## Notes

The provided FakeRestAPI has some known limitations that impact certain test cases:

Data is not persisted between requests:
Tests that verify persistence (e.g., POST followed by GET, DELETE followed by GET) will fail because the API does not store created or updated data.

Security features are not implemented:
The API does not require authentication, so tests expecting 401 Unauthorized or 403 Forbidden are marked as expected failures.

Not all HTTP status codes are correctly handled:
For example, when requesting a non-existent book, the API may return 200 OK instead of 404 Not Found.
Tests for these scenarios are still included for completeness but are marked as expected failures.

For these cases, Pytest flags (xfail) are used so that they appear as expected failures in the report, rather than incorrect implementations.
