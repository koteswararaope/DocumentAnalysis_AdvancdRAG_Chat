
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

# Fixture to set and clean up environment variables
@pytest.fixture(autouse=True)
def set_and_cleanup_env(monkeypatch):
    # Setup: set env vars
    monkeypatch.setenv("GROQ_API_KEY", "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")
    monkeypatch.setenv("GOOGLE_API_KEY", "AIzaSyCXxhCtUOLdVsN-1uEvVulsSCNxGNEVkyw")

    # Yield control back to the test
    yield

    # Teardown: remove env vars
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    
def test_analyze_documents_with_real_pdf(monkeypatch):
    file_path = Path(__file__).parent / "Sample.pdf"
    
    assert file_path.exists(), f"Test file not found: {file_path}"
    
    with open(file_path, "rb") as f:
        response = client.post(
            "/analyze",
            files={"file": ("Sample.pdf", f, "application/pdf")}
        )
        assert response.status_code == 200
        assert "Document Portal" in response.text
    



