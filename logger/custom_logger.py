import logging
import os
from datetime import datetime

class CustomLogger:
    def __init__(self, log_dir="logs"):
        
        self.logs_dir = os.path.join(os.getcwd(),log_dir)
        os.makedirs("logs", exist_ok=True)
        log_file=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        logpath=os.path.join(self.logs_dir,log_file)
        logging.basicConfig(
            filename=logpath,
            format="[ %(asctime)s ] %(levelname)s %(name)s (line:%(lineno)d) -%(message)s",
            level=logging.INFO,
            force=True
        )
        
    def get_logger(self,name=__file__):
        return logging.getLogger(os.path.basename(name))

if __name__ =="__main__":
    loger = CustomLogger()
    logger = loger.get_logger(__file__)
    logger.info("custom logger is intialized")
    