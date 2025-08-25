import os
import sys
from dotenv import load_dotenv
from utils.config_loader import load_config

from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings


from logger.custom_struct_logger  import CustomStructLogger
from exception.custom_exception import DocumentPortalException

log = CustomStructLogger().get_logger(__name__)

class Modelloader:
    """class to load the embeddings and llm
    """
    def __init__(self):
        load_dotenv()
        self.validate_env()
        self.config = load_config()
        log.info("configuration :", config_keys=list(self.config.keys()))
        
        
    def validate_env(self):
        """ validate environemnt varibkes and API keys"""
        required_vars =["GOOGLE_API_KEY","GROQ_API_KEY"]
        self.api_keys = {key:os.getenv(key) for key in required_vars}
        missing = [k for k , v in self.api_keys.items() if not v]
        if missing:
            log.error("Missing environment varibles", missing_vars =missing)
            #raise DocumentPortalException("Missing environment varibles")
        
    def load_embeddings(self):
        """loading embedding model
        """
        log.info("loading embedding")
        try:
            
            embedded_model = self.config["embedding_model"]["model_name"]
            return GoogleGenerativeAIEmbeddings(model=embedded_model)
        except Exception as e:
            log.error("could not laod embedding model", error = str(e))
            raise DocumentPortalException("could not laod embedding model", sys)
    def load_llm(self):
        """loading LLM
        """
        log.info("loading llm")
        try:
            
            model_name = self.config["llm"]["groq"]["model_name"]
            temprature = self.config["llm"]["groq"]["temprature"]
            max_output_tokens = self.config["llm"]["groq"]["max_output_tokens"]
            return ChatGroq(model_name=model_name, temperature=temprature,max_tokens=max_output_tokens)
        
        except Exception as e:
            log.error("could not load llm", error =str(e))
            raise DocumentPortalException("could not load llm",sys)



"""ml = Modelloader()
ml.load_embeddings()
llm = ml.load_llm()
print(llm.invoke("where is hyderabad?"))"""