import sys #provides various functions and variables used to manipulate different parts of the python runtime environments
import logging

def error_message_detail(error, error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename #tb_frame is a frame object that represents the current stack frame, and f_code is an attribute of the frame object that contains the code object being executed in that frame.
    error_message="Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error))
    return error_message #tb_lineno is an attribute of the traceback object that gives the line number in the source code where the exception occurred.
    

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message, error_detail=error_detail)
        #super().__init__(self.error_message) #This line calls the constructor of the parent class (Exception) with the error message as an argument, initializing the base Exception class with the custom error message.
        
    def __str__(self):
        return self.error_message
        #This method returns the string representation of the error message when the exception is printed or logged.
        #This is useful for debugging and understanding the context of the error.
        
