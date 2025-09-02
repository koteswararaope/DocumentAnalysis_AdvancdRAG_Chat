import os
import json
import uuid
import hashlib
import shutil
from pathlib import Path
from utils.model_loader import Modelloader
from logger.custom_struct_logger import CustomStructLogger
from exception.custom_exception import DocumentPortalException

from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader


class FaissManager:
    def __init__(self):
        pass
    def _exists(self):
        pass
    @staticmethod
    def _fingerprint(self):
        pass
    def _save_meta(self):
        pass
    def add_documents(self):
        pass
    def load_or_create(self):
        pass

class Dochandler:
    def __init__(self):
        pass
    def save_pdf(self):
        pass
    def read_pdf(self):
        pass

class DocumentComprator:
    def __init__(self):
        pass
        
    def save_uploaded_files(self):
        pass
    def read_pdf(self):
        pass
    def combined_docs(self):
        pass
    def clean_old_session(self):
        pass

class ChatIngestor:
    def __init__(self):
        pass
    def _resolve_dir(self):
        pass
    def _split(self):
        pass
    def build_retriver(self):
        pass