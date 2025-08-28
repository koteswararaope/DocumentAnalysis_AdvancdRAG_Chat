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
import uuid
from datetime import datetime

class Singledocingestor:
    def __init__(self, data_dir:str="data/single_doc_chat", faiss_dir:str ="faiss_index"):
        try:
            self.logger = CustomStructLogger().get_logger(__name__)
            self.data_dir = Path(data_dir)
            self.data_dir.mkdir(parents=True,exist_ok=True)
            
            self.faiss_dir = Path(faiss_dir)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)
            
            self.model_loader= Modelloader()
            self.logger.info("Singledocingestor is intialized", data_path=str(self.data_dir), faiss_path= str(self.faiss_dir) )
        except Exception as e:
            self.logger("Singledocingestor Intialization has Failed", error =str(e))
            raise DocumentPortalException("Singledocingestor Intialization has Failed",sys)
           
    def add_docs(self, files):
        try:
            documents =[]
            for file in files:
                unique_filename= f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.pdf"
                temp_path=self.data_dir/unique_filename
                
                with open(temp_path, "wb") as f:
                    f.write(file.read())
                self.logger.info("PDF saved for ingestion", file_name= file.name)
                loader =PyPDFLoader(str(temp_path))
                docs= loader.load()
                documents.extend(docs)
            self.log("PDF files loaded", count= len(documents))
            return self._create_retriver(documents)
        except Exception as e:
            self.logger("Exception occured in add_docs ", error =str(e))
            raise DocumentPortalException("Exception occured in add_docs",sys)
        
    def _create_retriver(self,documents):
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            docs_splits = text_splitter.split_documents(documents)
            self.logger.info("documents is splitted into chunks")
            embedded_model = self.model_loader.load_embeddings()
            vector_store= FAISS.from_documents(documents=docs_splits,embedding=embedded_model)
            vector_store.save_local(str(self.faiss_dir))
            self.logger("vector store ios saved locally ", saved_path= str(self.faiss_dir))
            
            retriver = vector_store.as_retriever(search_type ="similarity", search_kwargs={"k":5})
            self.logger("retriver is created for vector data base")
            return retriver
        
        except Exception as e:
            self.logger("exception in _get_retriver", error=str(e))
            raise DocumentPortalException("exception in _get_retriver",sys)