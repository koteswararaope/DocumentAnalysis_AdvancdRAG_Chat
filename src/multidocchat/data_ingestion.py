import os
import sys
from pathlib import Path
from langchain.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.output_parsers import StructuredOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, TextLoader
from utils.model_loader import Modelloader
from logger.custom_struct_logger import CustomStructLogger
from  exception.custom_exception import DocumentPortalException
import uuid
from datetime import datetime


class multidocIngestor:
    def __init__(self, data_dir:str="data\multidocument_chat", faiss_dir:str="faiss_index", session_id:str=None):
        try:
            self.logger = CustomStructLogger().get_logger(__name__)
            self.data_dir = Path(data_dir)
            self.data_dir.mkdir(parents=True,exist_ok=True)
            
            self.faiss_dir = Path(faiss_dir)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)
            
            self.session_id = f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.pdf"
            self.session_temp_dir = self.data_dir/self.session_id
            self.session_fiass_dir= self.faiss_dir/self.session_id
            self.session_temp_dir.mkdir(parents=True, exist_ok=True)
            self.session_fiass_dir.mkdir(parents=True,exist_ok=True)
            
            self.model_loader= Modelloader()
            self.Supported_extension= {'.pdf','.docx','.txt','.md'}
            self.logger.info("multidocIngestor is intialized", data_path=str(self.data_dir), faiss_path= str(self.faiss_dir) )
            
        except Exception as e:
            self.logger.error("Failed to Inaitalize the multidocIngestor", error=str(e))
            raise DocumentPortalException("Failed to Inaitalize the multidocIngestor", sys)
    def add_docs(self, files):
        try:
            documents=[]
            for file in files:
                ext = Path(file.name).suffix.lower()
                if ext not in self.Supported_extension:
                    self.logger.warning("Unsupported file skipped", file_name=file.name)
                    continue
                unique_filename= f"{uuid.uuid4().hex[:8]}{ext}"
                temp_path= self.session_temp_dir/unique_filename
                
                with open(temp_path,"rb") as f:
                    f.write(file.read())
                self.logger.info("file save ", file_name=file.name,saved_as=str(temp_path), session_id= self.session_id)
                
                if ext == ".pdf":
                    loader = PyPDFLoader(str(temp_path))
                elif ext ==".doc":
                    loader =Docx2txtLoader(str(temp_path))
                elif ext == ".txt":
                    loader= TextLoader(str(temp_path), encoding="utf-8")
                else:
                    self.logger.warning("Unsupported file encountered", file_name=file.name)
                    continue
                docs =loader.load()
                documents.extend(docs)
                
            if not documents:
                raise DocumentPortalException("no valid documnets to load", sys)
            self.logger.info("All documnets loaded sucessfully")
                
            return self._create_retriver(documents)
        except Exception as e:
            self.logger.error("Failed to Inaitalize the multidocIngestor", error=str(e))
            raise DocumentPortalException("Failed to Inaitalize the multidocIngestor", sys)
    def _create_retriver(self, documents):
        try:
            embedded_model = self.model_loader.load_embeddings()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            split_docs = text_splitter.split_documents(documents)
            vectorstore = FAISS.from_documents(documents=split_docs,embedding=embedded_model)
            vectorstore.save_local(str(self.faiss_dir))
            self.logger.info("FAISS index is saved locally",path= str(self.faiss_dir))
            retriver = vectorstore.as_retriever(search_type ="similarity", search_args={"k":5})
            return retriver
        except Exception as e:
            self.logger.error("Failed to Inaitalize the multidocIngestor", error=str(e))
            raise DocumentPortalException("Failed to Inaitalize the multidocIngestor", sys)
    