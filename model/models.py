from pydantic import BaseModel, Field
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
    