import sys
import os
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from utils.model_loader import Modelloader
from exception.custom_exception import DocumentPortalException
from logger.custom_struct_logger import CustomStructLogger
from prompt.prompt_library import PROMPT_REGISTRY


class ConversationalRAG:
    def __init__(self, session_id:str, retriever):
        try:
            self.logger = CustomStructLogger().get_logger(__name__)
        except Exception as e:
            self.logger("ConversationalRAG Intialization has Failed", error =str(e))
            raise DocumentPortalException("ConversationalRAG Intialization has Failed",sys)
    
    def _load_llm(self):
        try:
            pass
        except Exception as e:
            self.logger("_load_llm  has Failed", error =str(e))
            raise DocumentPortalException("_load_llm  has Failed",sys)
        
    def _get_session_history(self,session_id:str):
        try:
            pass
        except Exception as e:
            self.logger("_get_session_history  has Failed", error =str(e))
            raise DocumentPortalException("_get_session_history has Failed",sys)
        
    def load_retriver_from_faiss(self):
        try:
            pass
        except Exception as e:
            self.logger("load_retriver_from_faiss  has Failed", error =str(e))
            raise DocumentPortalException("load_retriver_from_faiss has Failed",sys)
    
    def invoke(self):
        try:
            pass
        except Exception as e:
            self.logger("invoke  has Failed", error =str(e))
            raise DocumentPortalException("invoke has Failed",sys)