import sys 
import logging

def error_meassage_details(error: Exception,error_detail: sys) -> str:
    """
    Extracts detailed error information including file name,line number and the error message.

    params:
    - error: The exception that occured
    - error_detail: The sys module to get the traceback details
    - return: A formatted error message string
    """

    # extract traceback details (exception info)
    _,_,exc_tb = error_detail.exc_info()

    # get the file name where the exception occured
    file_name = exc_tb.tb_frame.f_code.co_filename

    # create a formatted error mesage string with file name,line number,and the actual error
    line_number = exc_tb.tb_lineno
    error_message = f"Error occured in python script : [{file_name}] at line number [{line_number}].The error is: {str(error)}"

    #log the error for better tarcking
    logging.error(error_message)

    return error_message

class MyException(Exception):
    """
    Custom exception class for handling errors
    """
    def __init__(self, error_message: str,error_detail: sys):
        """
        Initialse the Exception with a detailed error message

        params:
        - error_message: A string describing the error
        - error_detail: The sys module to access traceback details.
        """

        # call the base class constructor with the error message
        super().__init__(error_message)

        # format the detailed error message using the error_message_detail function
        self.error_message = error_meassage_details(error_message,error_detail)


    def __str__(self)->str:
        """
        Returns the string representation of the error message,
        overwrites the default __str__ method of Exception parent class.
        """
        return self.error_message