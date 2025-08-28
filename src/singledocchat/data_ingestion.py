import os
import sys
from pathlib import Path
from langchain.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.output_parsers import StructuredOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.model_loader import Modelloader
from logger.custom_struct_logger import CustomStructLogger
from  exception.custom_exception import DocumentPortalException

class Singledocingestor:
    def __init__(self):
        try:
            self.logger = CustomStructLogger().get_logger(__name__)
        except Exception as e:
            self.logger("Singledocingestor Intialization has Failed", error =str(e))
            raise DocumentPortalException("Singledocingestor Intialization has Failed",sys)
           
    def add_docs(self, file):
        try:
            pass
        except Exception as e:
            self.logger("Exception occured in add_docs ", error =str(e))
            raise DocumentPortalException("Exception occured in add_docs",sys)
        
    def _get_retriver(self):
        try:
            pass
        except Exception as e:
            self.logger("exception in _get_retriver", error=str(e))
            raise DocumentPortalException("exception in _get_retriver",sys)