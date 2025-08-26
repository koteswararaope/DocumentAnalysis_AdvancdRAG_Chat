import os
from utils.model_loader import Modelloader
from logger.custom_struct_logger import CustomStructLogger
from exception.custom_exception import DocumentPortalException

from langchain_groq import Chatgroq
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser


class DocumentAnalyzer:
    """Analyze the document using a pretrained LLM and log all the actions
    """
    
    def __init__(self):
        pass 
    
    def Analyze_doc(self, path:str):
        pass
    