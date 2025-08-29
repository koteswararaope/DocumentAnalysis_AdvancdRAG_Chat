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
from model.models import PromptType
import streamlit as st
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
load_dotenv()
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="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"
LANGCHAIN_PROJECT="rag-pipeline-debug"

class ConversationalRAG:
    def __init__(self, session_id:str, retriever):
        try:
            self.logger = CustomStructLogger().get_logger(__name__)
            self.session_id = session_id
            self.retriever= retriever
            self.llm = self._load_llm()
            self.context_prompt = PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.qa_prompt= PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
            self.history_aware_retriver = create_history_aware_retriever(
                self.llm, self.retriever, self.context_prompt
                )
            self.logger.info("Created history_aware_retriver")
            self.qa_chain = create_stuff_documents_chain(llm=self.llm,prompt=self.qa_prompt)
            self.rag_chain = create_retrieval_chain(self.history_aware_retriver,self.qa_chain)
            self.logger.info("Initialized Conversational RAG", session_id=self.session_id)
            self.chain= RunnableWithMessageHistory(
                self.rag_chain,
                self._get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer"
            )
            
        except Exception as e:
            self.logger.error("ConversationalRAG Intialization has Failed", error =str(e))
            raise DocumentPortalException("ConversationalRAG Intialization has Failed",sys)
    
    def _load_llm(self):
        try:
            llm = Modelloader().load_llm()
            self.logger.info("LLM loaded sucessfully", class_name= llm.__class__.__name__)
            return llm
        except Exception as e:
            self.logger.error("_load_llm  has Failed", error =str(e))
            raise DocumentPortalException("_load_llm  has Failed",sys)
        
    def _get_session_history(self,session_id:str)-> BaseChatMessageHistory:
        try:
            if "store" not in st.session_state:
                st.session_state.store = {}

            if session_id not in st.session_state.store:
                st.session_state.store[session_id] = ChatMessageHistory()
                self.logger.info("New chat session history created", session_id=session_id)
            history = st.session_state.store[session_id]
            return history #st.session_state.store[session_id]
        except Exception as e:
            self.logger.error("_get_session_history  has Failed", error =str(e))
            raise DocumentPortalException("_get_session_history has Failed",sys)
        
    def load_retriver_from_faiss(self,index_path :str):
        try:
            embeddings_model = Modelloader().load_embeddings()
            if not os.path.isdir(index_path):
                raise FileNotFoundError(f"Vector store is not found {index_path}")
            
            vector_store =FAISS.load_local(folder_path=index_path,embeddings=embeddings_model)
            self.logger.info("vector db is loaded sucessfully")
            return vector_store.as_retriever(search_type ="similarity",search_kwargs={"k":5})
            
        except Exception as e:
            self.logger.error("load_retriver_from_faiss  has Failed", error =str(e))
            raise DocumentPortalException("load_retriver_from_faiss has Failed",sys)
    
    def invoke(self,user_question:str) ->str:
        try:
            
            response= self.chain.invoke(
                {"input":user_question},
                config={"configurable":{"session_id":self.session_id}}
            )
            answer = response.get("answer","No answer")
            if not answer:
                self.logger.warnning("Empty answer recived", sessionid= self.session_id)
            self.logger.info("Chain invoked sucessfully", sessionid= self.session_id, user_input=user_question, answer_preview= answer[:150])
            return answer
        except Exception as e:
            self.logger.error("invoke  has Failed", error =str(e))
            raise DocumentPortalException("invoke has Failed",sys)

