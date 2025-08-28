from enum import Enum
from pydantic import BaseModel, Field,RootModel
from typing import Optional,List,Dict,Any,Union

class DocMetadata(BaseModel):
    summary:List[str] =Field(default_factory=list,description="summary of the document")
    Title:str
    Author:str
    DateCreated:str
    LastModified:str
    Publisher:str
    Language:str
    Pagecount: Union[int,str]


class ChangeFormat(BaseModel):
    page:str
    change:str

class SummaryResponse(RootModel[list[ChangeFormat]]):
    pass

class PromptType(str, Enum):
    DOCUMENT_ANALYSIS = "document_analysis"
    DOCUMENT_COMPARISON = "document_comparison"
    CONTEXTUALIZE_QUESTION = "contextualize_question"
    CONTEXT_QA = "context_qa"