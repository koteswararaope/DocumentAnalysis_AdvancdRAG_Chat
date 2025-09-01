
import sys
import os
from dotenv import load_dotenv
from operator import itemgetter
from langchain_community.vectorstores import FAISS
from utils.model_loader import Modelloader
from exception.custom_exception import DocumentPortalException
from logger.custom_struct_logger import CustomStructLogger
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import PromptType
import streamlit as st
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()


class ConversationalRAG:
   
    def __init__(self, session_id:str, retriver=None):
        try:
            self.logger = CustomStructLogger(__name__)
            self.session_id = session_id
            self.llm = self._load_llm()
            self.context_propmpt: ChatPromptTemplate = PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.qa_prompt:ChatPromptTemplate = PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
            if retriver is None:
                raise ValueError("Retriver is empty")
            self.retriver = retriver
            self._build_lcel_chain()
            self.logger.info("ConversationalRAG is Intialized sucessfully")
            
        except Exception as e:
            self.logger.error("Failed to Inaitalize the ConversationalRAG", error = str(e))
            raise DocumentPortalException("Failed to Inaitalize the ConversationalRAG",sys)
        
    def load_retriever_faiss(self, index_path:str):
        """Load Fiass db and create a retriver
        """
        try:
            embeddings = Modelloader.load_embeddings()
            
            if not  os.path.isdir(index_path):
                raise FileNotFoundError("FAISS index directory not found", path= index_path)
            vector_store= FAISS.load_local(folder_path=index_path,embeddings=embeddings,allow_dangerous_deserialization=True)
            self.retriver = vector_store.as_retriever(search_type= "similarity", search_kwargs={"k":5})
            self.logger.info("retriver is cerated sucessfully")
            self._build_lcel_chain()
            return self.retriver
        except Exception as e:
            self.logger.error("Exception in load_retriever_faiss", error = str(e))
            raise DocumentPortalException("Exception in load_retriever_faiss",sys)
        
    def invoke(self):
        try:
            pass
            
        except Exception as e:
            self.logger.error("exception in invoke", error = str(e))
            raise DocumentPortalException("exception in invoke",sys)
    def _load_llm(self):
        try:
            llm = Modelloader.load_llm()
            if not llm:
                raise ValueError("LLM could not be loaded")
            return llm
            
        except Exception as e:
            self.logger.error("exception in _load_llm", error = str(e))
            raise DocumentPortalException("exception in _load_llm",sys)
    def _format_docs(self, docs):
        try:
            return "\n\n".join(d.page_content for d in docs)
            
        except Exception as e:
            self.logger.error("exception _format_docs", error = str(e))
            raise DocumentPortalException("exception in _format_docs",sys)
    def _build_lcel_chain(self):
        try:
            question_rewriter=(
                {"item":itemgetter("input"),"chat_history":itemgetter("chat_history")}
                |self.context_propmpt
                |self.llm
                |StrOutputParser()
            )
            retrive_docs=question_rewriter|self.retriver|self._format_docs
            self.chain= (
                    {
                        "context":retrive_docs,
                        "input":itemgetter("input"),
                        "chat_history":itemgetter("chat_history")
                    }
                    |self.qa_prompt
                    |self.llm|
                    StrOutputParser()
                    )
            self.logger.info("LCEL chain is created")
        except Exception as e:
            self.logger.error("exception in _build_lcel_chain", error = str(e))
            raise DocumentPortalException("exception in _build_lcel_chain",sys) 