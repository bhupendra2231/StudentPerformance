import sys
from src.logger import logging

def error_message_detail(error, error_detail: sys):
    """
    This function captures details of the error, including the filename, line number, and error message.
    
    Parameters:
    error (Exception): The caught exception.
    error_detail (sys): The sys module to extract exception information.
    
    Returns:
    str: Formatted error message string.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occurred in python script name [{file_name}] line number [{exc_tb.tb_lineno}] error message [{str(error)}]"
    return error_message

class CustomException(Exception):
    """
    Custom Exception class that extends the base Exception class.
    
    Attributes:
    error_message (str): Formatted error message.
    """
    def __init__(self, error_message, error_detail: sys):
        """
        Initializes CustomException with a detailed error message.
        
        Parameters:
        error_message (str): Initial error message.
        error_detail (sys): The sys module to extract exception information.
        """
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        """
        Returns the error message when the exception is printed.
        """
        return self.error_message

