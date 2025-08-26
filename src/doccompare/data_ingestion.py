import sys
from pathlib import Path
import fitz
from logger.custom_struct_logger import CustomStructLogger
from exception.custom_exception import DocumentPortalException

class DatainjectionComparator:
    def __init__(self,base_dir):
        self.logger= CustomStructLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True,exist_ok=True)
    
    def delete_existing_files(self):
        """delete the existing files
        """
        try:
            pass
        except Exception as e:
            self.logger.error("an error occured while deleting the PDF %s", str(e))
            raise DocumentPortalException("an error occured while deleting the PDF",e)
    
    def save_uploaded_files(self):
        """save uploaded files to a specific directory
        """
        try:
            pass
        except Exception as e:
            self.logger.error("an error occured while saving the PDF %s", str(e))
            raise DocumentPortalException("an error occured while saving the PDF",e)
    
    def read_pdf(self,pdf_path:Path):
        """read the pdf files
        """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"PDF is encrypted: {pdf_path}")
                all_text =[]
                for page_num in range(doc.page_count):
                    page= doc.load_page(page_num)
                    text = page.get_text()
                    
                    if text.strip():
                        all_text.append(f"\n --page {page_num+1} ---\n {text}")
                self.logger("pdf read sucessfully", file=str(pdf_path),pages =len(all_text))
                return "\n".join(all_text)
        except Exception as e:
            self.logger.error("an error occured while reading the PDF %s", str(e))
            raise DocumentPortalException("an error occured while reading the PDF",e)
    
    