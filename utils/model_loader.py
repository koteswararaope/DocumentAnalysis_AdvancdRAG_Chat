import os
import sys
import json
from dotenv import load_dotenv
from utils.config_loader import load_config

from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

from logger.custom_struct_logger  import CustomStructLogger
from exception.custom_exception import DocumentPortalException

log = CustomStructLogger().get_logger(__name__)


class ApiKeyManager:
    REQUIRED_KEYS = ["GROQ_API_KEY", "GOOGLE_API_KEY"]

    def __init__(self):
        self.api_keys = {}
        raw = os.getenv("API_KEYS")

        if raw:
            try:
                parsed = json.loads(raw)
                if not isinstance(parsed, dict):
                    raise ValueError("API_KEYS is not a valid JSON object")
                self.api_keys = parsed
                log.info("Loaded API_KEYS from ECS secret")
            except Exception as e:
                log.warning("Failed to parse API_KEYS as JSON", error=str(e))

        # Fallback to individual env vars
        for key in self.REQUIRED_KEYS:
            if not self.api_keys.get(key):
                env_val = os.getenv(key)
                if env_val:
                    self.api_keys[key] = env_val
                    log.info(f"Loaded {key} from individual env var")

        # Final check
        missing = [k for k in self.REQUIRED_KEYS if not self.api_keys.get(k)]
        if missing:
            log.error("Missing required API keys", missing_keys=missing)
            raise DocumentPortalException("Missing API keys", sys)

        log.info("API keys loaded", keys={k: v[:6] + "..." for k, v in self.api_keys.items()})


    def get(self, key: str) -> str:
        val = self.api_keys.get(key)
        if not val:
            raise KeyError(f"API key for {key} is missing")
        return val


class Modelloader:
    """class to load the embeddings and llm
    """
    def __init__(self):
       
        if os.getenv("ENV", "local").lower() != "production":
            load_dotenv()
            self.validate_env()
            log.info("Running in LOCAL mode: .env loaded")
        else:
            log.info("Running in PRODUCTION mode")
            
        self.api_key_mgr = ApiKeyManager()
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
            embeddings=  GoogleGenerativeAIEmbeddings(model="models/embedding-001",
                                                      google_api_key=self.api_key_mgr.get("GOOGLE_API_KEY"))
            #embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            #test_vec = embeddings.embed_query("Hello world")
            #print(len(test_vec))
            return embeddings
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
            llm = ChatGroq(model_name=model_name,api_key=self.api_key_mgr.get("GROQ_API_KEY"),temperature=temprature,max_tokens=max_output_tokens)
            return llm
        
        except Exception as e:
            log.error("could not load llm", error =str(e))
            raise DocumentPortalException("could not load llm",sys)



"""ml = Modelloader()
ml.load_embeddings()
llm = ml.load_llm()
print(llm.invoke("where is hyderabad?"))"""