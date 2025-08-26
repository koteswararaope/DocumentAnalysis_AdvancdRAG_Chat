
import os
from pathlib import Path
from src.doc_analyzer.dataingestion import DocumentHandler
from src.doc_analyzer.dataanalaysis import DocumentAnalyzer
from exception.custom_exception import DocumentPortalException

pdf_path= r"C:\\Learning\\Python\\LLM_ops\\EndtoEnd\\DocumentAnalysis_AdvancdRAG_Chat\\data\\document_analysis\\NIPS-2017-attention-is-all-you-need-Paper.pdf"

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
    raise DocumentPortalException("can not save pdf")