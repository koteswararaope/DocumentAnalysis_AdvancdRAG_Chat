import sys
from pathlib import Path
import fitz
from logger.custom_struct_logger import CustomStructLogger
from exception.custom_exception import DocumentPortalException

class DatainjectionComparator:
    def __init__(self,base_dir:str =r"data\document_compare"):
        self.logger= CustomStructLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True,exist_ok=True)
    
    def delete_existing_files(self, ):
        """delete the existing files
        """
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                        self.logger.info("file deleted :", path= str(file))
                self.logger.info("Directory is cleanned", directory=str(self.base_dir))
        except Exception as e:
            self.logger.error("an error occured while deleting the PDF %s", str(e))
            raise DocumentPortalException("an error occured while deleting the PDF",sys)
    
    def save_uploaded_files(self,reference_file,actual_file):
        """save uploaded files to a specific directory
        """
        try:
            self.delete_existing_files()
            
            ref_path=self.base_dir/reference_file.name
            act_path=self.base_dir/actual_file.name
            
            with open(ref_path,"wb") as f:
                f.write(reference_file.getbuffer())
            
            with open(act_path, "wb") as f:
                f.write(actual_file.getbuffer())
            
            self.logger.info("Files saved", reference=str(ref_path), actual=str(act_path))
            return ref_path,act_path
        except Exception as e:
            self.logger.error("an error occured while saving the PDF %s", str(e))
            raise DocumentPortalException("an error occured while saving the PDF",sys)
    
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
                #self.logger("pdf read sucessfully", file=str(pdf_path),pages =len(all_text))
                
                return "\n".join(all_text)
        except Exception as e:
            self.logger.error("an error occured while reading the PDF %s", str(e))
            raise DocumentPortalException("an error occured while reading the PDF",sys)
    
    def combined_documents(self ) ->str:
        try:
            content_dict ={}
            doc_parts=[]
            
            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix == ".pdf":
                    content_dict[filename.name]=self.read_pdf(filename)
            
            for filename, content in content_dict.items():
                doc_parts.append(f"Document: {filename}\n{content}")

            combined_text ="\n\n".join(doc_parts)
            self.logger.info("Documents combined", count= len(doc_parts))
            return combined_text
        
        except Exception as e:
            self.logger.error("error combining the documents %s", str(e))
            raise DocumentPortalException("an error occured while combining the documents",sys)