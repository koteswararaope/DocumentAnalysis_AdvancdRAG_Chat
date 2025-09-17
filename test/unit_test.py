
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

def test_analysis():
      # Prepare a fake PDF file content
    file_path = r"data\document_analysis\NIPS-2017-attention-is-all-you-need-Paper.pdf"
    
    with open(file_path, "rb") as file:
        files = {
            "file": ("NIPS-2017-attention-is-all-you-need-Paper.pdf", file, "application/pdf"),
        }
        
        response = client.post("/analyze", files=files)
        assert response.status_code == 200

    json_response = response.json()
    assert json_response["filename"] == "NIPS-2017-attention-is-all-you-need-Paper.pdf"


'''def test_analysis11():
      # Prepare a fake PDF file content
    file_path = r"data\document_analysis\NIPS-2017-attention-is-all-you-need-Paper.pdf"
    reader = PdfReader(file_path)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"'''

