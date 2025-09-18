
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
    file_path = r"C:\Learning\Sample.pdf"
    '''assert os.path.exists(file_path), f"Test file not found: {file_path}"
    with open(file_path, "rb") as f:
     data = f.read()
    print(data[:200])'''
    
    with open(file_path, "rb") as f:
        response = client.post(
            "/analyze",
            files={"file": (file_path, f, "application/pdf")}
        )

    assert response.status_code == 200


test_analyze_documents_with_real_pdf()
