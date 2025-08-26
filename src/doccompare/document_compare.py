import sys
from dotenv import load_dotenv
import pandas as pd

from logger.custom_struct_logger import CustomStructLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import Modelloader
from model.models import SummaryResponse
from prompt.prompt_library import PROMPT_REGISTRY

from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentComparatorusingLLM:
    def __init__(self):
        load_dotenv()
        self.logger = CustomStructLogger().get_logger(__name__)
        self.loader = Modelloader()
        self.llm = self.loader.load_llm()
        self.parser =JsonOutputParser(pydantic_object=SummaryResponse)
        self.fixingparser = OutputFixingParser.from_llm(llm=self.llm,parser=self.parser)
        self.prompt= PROMPT_REGISTRY["document_comparison"]
        self.chain =self.prompt|self.llm|self.parser|self.fixingparser
        self.logger.info("DocumentComparatorusingLLM is intialized")
    
    def comapre_documnets(self):
        """Compare two documents and return the structured output
        """
        try:
            pass
        except Exception as e:
            self.logger.error("comapre_documnets has thrown an exception",str(e))
            raise DocumentPortalException("comapre_documnets has thrown an exception",e)
    
    def _format_reaponse(self):
        """format response from llm intoa structured format
        """
        try:
            pass
        except Exception as e:
            self.logger.error("_format_reaponse has thrown an exception",str(e))
            raise DocumentPortalException("_format_reaponse has thrown an exception",e)