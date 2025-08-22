import sys
from src.logger import logging

def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    return f"Error in {file_name}, line {exc_tb.tb_lineno}: {str(error)}"

class CustomException(Exception):
    def _init_(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def _str_(self):
        return self.error_message

if __name__=="__main__":
    try:
        a=1/0
    except:
        logging.info("divide by zero error")
        raise CustomException

