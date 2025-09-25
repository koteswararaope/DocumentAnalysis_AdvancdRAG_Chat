
import pytest
from fastapi.testclient import TestClient
from api.main import app   # or your FastAPI entrypoint
import io, os
from pathlib import Path
import logging
from deepeval.metrics import BaseMetric,SummarizationMetric
from deepeval.scorer import scorer
from deepeval.test_case import LLMTestCase
from langchain.document_loaders import PyPDFLoader

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
    monkeypatch.setenv("GROQ_API_KEY", "")
    monkeypatch.setenv("GOOGLE_API_KEY", "")
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
        logging.info("summary of docuemnt", response.text)
        
        
#use open AI key to run this test
'''def test_performance(monkeypatch):
    file_path = Path(__file__).parent / "Sample.pdf"
    referencetext= "attention all you  neeed"
    
    assert file_path.exists(), f"Test file not found: {file_path}"
    
    # Load PDF text
    loader = PyPDFLoader(str(file_path))
    docs = loader.load()
    document_text = " ".join([d.page_content for d in docs])
    with open(file_path, "rb") as f:
        response = client.post(
            "/analyze",
            files={"file": ("Sample.pdf", f, "application/pdf")}
        )
        assert response.status_code == 200
        logging.info("summary of docuemnt", response.text)
    
    test_case =LLMTestCase(input=document_text,actual_output=response.text,expected_output=referencetext)
    summarization_metric = SummarizationMetric()
    score = summarization_metric.measure(test_case)
    print("Summarization Score:", score)'''
    


