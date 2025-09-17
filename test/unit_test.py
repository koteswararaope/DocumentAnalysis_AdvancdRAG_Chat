
import pytest
from fastapi.testclient import TestClient
from api.main import app   # or your FastAPI entrypoint
import io, os
from pathlib import Path
client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Document Portal" in response.text
from pypdf import PdfReader

def test_analyze_documents_with_real_pdf():
    # Path to the actual PDF file
    file_path = Path(__file__).parent / "data" / "document_analysis" / "sample.pdf"
    
    # Check if file exists
    assert file_path.is_file(), f"File not found: {file_path}"

    # Open the PDF in binary mode
    with open(file_path, "rb") as pdf_file:
        files = {
            "file": (file_path.name, pdf_file, "application/pdf"),
        }

        response = client.post("/analyze", files=files)

    # Assert success
    assert response.status_code == 200
    json_response = response.json()
    print(json_response)  # Inspect the returned analysis result
    




