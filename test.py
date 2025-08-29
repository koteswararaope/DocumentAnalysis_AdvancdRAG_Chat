
import os
from pathlib import Path
from src.doc_analyzer.dataingestion import DocumentHandler
from src.doc_analyzer.dataanalaysis import DocumentAnalyzer
from exception.custom_exception import DocumentPortalException

##tetsing for document analysis
"""pdf_path= r"C:\\Learning\\Python\\LLM_ops\\EndtoEnd\\DocumentAnalysis_AdvancdRAG_Chat\\data\\document_analysis\\NIPS-2017-attention-is-all-you-need-Paper.pdf"

class Dummyclass:
        def __init__(self, file_path):
            self.file_path= file_path
            self.name= Path(file_path).name
            print("filepath:", self.file_path)
        def getbuffer(self):
            return open(self.file_path,"rb").read()
    

dummy_pdf = Dummyclass(pdf_path)
handler = DocumentHandler(session_id="test_analysis_session")
    
try:
    pdf_content = dummy_pdf.getbuffer()
    save_path= handler.SavePdf(dummy_pdf)
    content = handler.ReadPdf(save_path)
    doc_analyzer = DocumentAnalyzer()
    response= doc_analyzer.Analyze_doc(content[:5000])
    print(response)
except Exception as e:
    raise DocumentPortalException("can not save pdf")"""
    
###testing for doc comparison
'''from src.doccompare.data_ingestion import DatainjectionComparator
from src.doccompare.document_compare import DocumentComparatorusingLLM
import io

def load_fake_upload_files(file_path:Path):
    """simulatig the loading files
    """
    return io.BytesIO(file_path.read_bytes())

def test_compare_document():
    ref_path=Path("C:\Learning\Python\LLM_ops\EndtoEnd\DocumentAnalysis_AdvancdRAG_Chat\data\document_compare\invoice_A.pdf")
    act_path=Path("C:\Learning\Python\LLM_ops\EndtoEnd\DocumentAnalysis_AdvancdRAG_Chat\data\document_compare\invoice_B.pdf")
    
    class fakeupload:
        def __init__(self, file_path:Path):
            self.name= file_path.name
            self._buffer = file_path.read_bytes()
        
        def getbuffer(self):
            return self._buffer
    
    datainjection= DatainjectionComparator()
    ref_upload= fakeupload(ref_path)
    act_upload = fakeupload(act_path)
    
    ref_file, act_file = datainjection.save_uploaded_files(ref_upload,act_upload)
    combined_text= datainjection.combined_documents()
    datainjection.clean_old_sessions(keep_latest=3)
    
    print("\n combined text 100 char \n")
    print(combined_text[:1000])
    
    llm_comparator= DocumentComparatorusingLLM()
    comparsion_df= llm_comparator.comapre_documnets(combined_text)
    print("\n====COMPARISON RESULT=======")
    print(comparsion_df)
    


if __name__ == "__main__":
    test_compare_document()'''
    
    

#single document chat

import sys
from pathlib import Path
from langchain_community.vectorstores import FAISS
from src.singledocchat.data_ingestion import Singledocingestor
from src.singledocchat.retrieval import ConversationalRAG
from utils.model_loader import Modelloader

FAISS_INDEX_PATH = Path("faiss_index")

def test_coversationalrag_pdf(pdf_path:str, user_question:str):
    try:
        module_loader= Modelloader()
        if FAISS_INDEX_PATH.exists():
            embeddings= module_loader.load_embeddings()
            vector_db = FAISS.load_local(folder_path=FAISS_INDEX_PATH,embeddings=embeddings)
            retriver = vector_db.as_retriever(search_type="similariy", search_kwargs={"k":5})
        else:
            with open(pdf_path, "rb") as f:
                upload_files= [f]
                docingector = Singledocingestor()
                retriver = docingector.add_docs(upload_files)
        
        session_id= "test_convresationl_rag"
        rag = ConversationalRAG(session_id=session_id,retriever=retriver)
        response = rag.invoke(user_question)
        print("response", response)
    except Exception as e:
        print(f"Test failed: {str(e)}")
        sys.exit(1)
    
if __name__ == "__main__":
    pdf_path = r"C:\Learning\Python\LLM_ops\EndtoEnd\DocumentAnalysis_AdvancdRAG_Chat\data\single_doc_chat\NIPS-2017-attention-is-all-you-need-Paper.pdf"
    question = "What is the significance of the attention mechanism? can you explain it in simple terms?"

    if not Path(pdf_path).exists():
        print(f"PDF file does not exist at: {pdf_path}")
        sys.exit(1)
    
# Run the test
    test_coversationalrag_pdf(pdf_path, question)