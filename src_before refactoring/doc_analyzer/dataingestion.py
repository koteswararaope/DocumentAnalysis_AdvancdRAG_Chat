import os
import fitz
import uuid
import sys
from datetime import datetime
from logger.custom_struct_logger import CustomStructLogger
from exception.custom_exception import DocumentPortalException

class DocumentHandler:
    """Handles PDF save and read operations and write logs for all actions
    """
    
    def __init__(self,data_dir=None, session_id=None):
        try:
            
            self.logger = CustomStructLogger().get_logger(__name__)
            self.data_dir = data_dir or os.getenv("DATA_STORAGE_PATH", 
                                                os.path.join(os.getcwd(),"data","document_analysis"))
            self.session_id = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            #create a folder to save the session data
            self.session_path= os.path.join(self.data_dir,self.session_id)
            os.makedirs(self.session_path,exist_ok=True)
            self.logger.info("Document handler intialized", sessionpath= self.session_path, sessionid=self.session_id)
        except Exception as e:
            self.logger.error("Data handler intialization failed")
            raise DocumentPortalException("Data handler intialization failed", e)
    
    def SavePdf(self,file):
        try:
            filename= os.path.basename(file.name)
            #if not filename.lower().endswith("*.pdf"):
                #raise DocumentPortalException("Invalid file type only pdfs are allowed")
            save_path= os.path.join(self.session_path,filename)
            with open(save_path,"wb") as f:
                f.write(file.getbuffer())
            self.logger.info("Document saved successfully", file =filename,path= save_path, session =self.session_id)
            return save_path
        except Exception as e:
            self.logger.error("Document could not be saved")
            raise DocumentPortalException("Document could not be saved",e)
    
    def ReadPdf(self, pdf_path):
        try:
            text_chunks =[]
            with fitz.open(pdf_path) as doc:
                for page_num, page in enumerate(doc, start=1):
                    text_chunks.append(f"\n--Page {page_num} ---\n{page.get_text()} ")
            text = "\n".join(text_chunks)
            self.logger.info("PDF is extracted sucessfully")
            return text
        except Exception as e:
            self.logger.error("Document could not be read")
            raise DocumentPortalException("Document could not be read",e)


if __name__ == "__main__":
    from pathlib import Path
    from io import BytesIO
    
    #handler = DocumentHandler()
    pdf_path= r"C:\\Learning\\Python\\LLM_ops\\EndtoEnd\\DocumentAnalysis_AdvancdRAG_Chat\\data\\document_analysis\\NIPS-2017-attention-is-all-you-need-Paper.pdf"
    
    
    class Dummyclass:
        def __init__(self, file_path):
            self.file_path= file_path
            self.name= Path(file_path).name
            print("filepath:", self.file_path)
        def getbuffer(self):
            return open(self.file_path,"rb").read()
    
    dummy_pdf = Dummyclass(pdf_path)
    handler = DocumentHandler(session_id="test_session")
    
    try:
        pdf_content = dummy_pdf.getbuffer()
        save_path= handler.SavePdf(dummy_pdf)
        content = handler.ReadPdf(save_path)
        print(content[:500])
    except Exception as e:
        raise DocumentPortalException("can not save pdf")
    