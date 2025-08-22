import sys
import traceback

from logger.custom_logger import CustomLogger

logger = CustomLogger().get_logger(__file__)

class DocumentPortalException(Exception):
    def __init__(self, error_message, error_details:sys):
        _,_,err_details = error_details.exc_info()
        self.filename = err_details.tb_frame.f_code.co_filename
        self.lineno = err_details.tb_lineno
        self.error_message = str(error_message)
        self.traceback_str = ''.join(traceback.format_exception(*error_details.exc_info()))
    
    def __str__(self):
        return f""" 
            ERROR in [{self.filename}] at line [{self.lineno}]
            Message: {self.error_message}
            Traceback:
            {self.traceback_str}
            """
"""if __name__ == "__main__":
    try:
        a=1/0
        print(a)
    except Exception as e:
        _exception = DocumentPortalException(e,sys)
        logger.error(_exception)
        raise _exception"""