
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
    file_path = "data\document_analysis\NIPS-2017-attention-is-all-you-need-Paper.pdf"   # put a small test pdf in your repo

    with open(file_path, "rb") as f:
        response = client.post(
            "/analyze_documents", 
            files={"file": ("NIPS-2017-attention-is-all-you-need-Paper.pdf", f, "application/pdf")}
        )

    assert response.status_code == 200
    result = response.json()
    print(result)   # for debugging
    assert "some_expected_key" in result   # adjust based on your API response




