import os
from utils.model_loader import Modelloader
from logger.custom_struct_logger import CustomStructLogger
from exception.custom_exception import DocumentPortalException

from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from model.models import DocMetadata
from prompt.prompt_library import *
class DocumentAnalyzer:
    """Analyze the document using a pretrained LLM and log all the actions
    """
    
    def __init__(self):
        self.logger = CustomStructLogger().get_logger(__name__)
        try:
            self.loader = Modelloader()
            self.llm = self.loader.load_llm()
            
            #parser
            self.parser = JsonOutputParser(pydantic_object=DocMetadata)
            self.fixing_parser = OutputFixingParser.from_llm(llm=self.llm,parser=self.parser)
            self.prompt = prompt
            
            self.logger.info("DocumentAnalyzer intialized sucessfully")
        except Exception as e:
            raise DocumentPortalException("error in intializing Document Analyzer",e)
    
    def Analyze_doc(self, document_text:str)->dict:
        """Analyze documnt text and extarct structured data and summary
        """
        try:
            chain = self.prompt|self.llm|self.fixing_parser
            response= chain.invoke({
               "format_instructions":self.parser.get_format_instructions(),
               "document_text" :document_text
            })
            self.logger.info("Meta Data extarction uscessfull", keys=list(response.keys()))
            return response
        except Exception as e:
            self.logger.error("could not analyze the document",error= str(e))
            raise DocumentPortalException("could not analyze the document", e)
    