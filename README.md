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
├── assets/ # Assets such as test data or images (if any)
├── config/ # Configuration files (URLs, environment, etc.)
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
   cd books-api-tests
2. Set up environment variables in config.py:
   BASE_URL = "https://fakerestapi.azurewebsites.net"
   BOOKS_ENDPOINT = "/api/v1/Books"
   HEADERS = {"Content-Type": "application/json"}
3. Run all tests:
   pytest -v --html=reports/report.html --self-contained-html
4. Run specific tests (e.g., GET):
   pytest tests/test_get_books.py

## Continuous Integration with GitHub Actions

This project includes a workflow that:
Installs dependencies
Runs tests
Generates an HTML report in the reports folder

## Test Reports

Pytest generates HTML reports in reports/ with detailed execution results and timestamp.
pytest -s --html=reports/report\_$(Get-Date -Format "yyyyMMdd_HHmmss").html

## CI/CD with GitHub Actions

The workflow is defined in .github/workflows/ci.yml.
It runs automatically on:
Push to main or feature/_
Pull requests to main or feature/_
Manual trigger from the GitHub Actions tab (Run workflow button).

## Where to find results

After the job finishes, go to the Actions tab → select the workflow run → Artifacts section.
Download the test-report artifact to view the HTML test report. Open it with a browser.
