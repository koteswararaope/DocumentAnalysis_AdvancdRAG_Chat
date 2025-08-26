import sys
from dotenv import load_dotenv
import pandas as pd

from logger.custom_struct_logger import CustomStructLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import Modelloader

from prompt.prompt_library import PROMPT_REGISTRY

from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentComparatorusingLLM:
    def __init__(self):
        pass
    def comapre_documnets(self):
        """Compare two documents and return the structured output
        """
        pass
    def format_reaponse(self):
        """format response from llm intoa structured format
        """
        pass