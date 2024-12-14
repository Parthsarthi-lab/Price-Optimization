import logging
import sys
import os
from datetime import datetime

if not os.path.exists("training/logs"):
    os.makedirs("training/logs")


def setup_info_logger():
    """
    Sets up a logger that writes only INFO level logs to a dynamically named log file based on the current date and time.
    """
    # Define a dynamic filename with the current date and time for info logs
    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    
    # Create logs directory if it doesn't exist
    if not os.path.exists("training/logs/info_logs"):
        os.makedirs("training/logs/info_logs")
    
    # Full path for the log file
    log_filepath = os.path.join("training/logs/info_logs", log_filename)
    
    # Create a dedicated logger for info logs
    info_logger = logging.getLogger("info_logger")
    info_logger.setLevel(logging.INFO)  # Set level to INFO to capture info-level logs
    
    # File handler to write INFO level logs to file
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(logging.INFO)


    # Formatter
    formatter_info = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
    file_handler.setFormatter(formatter_info)
    
    # Add the handler to the logger
    info_logger.addHandler(file_handler)

    return info_logger

def setup_error_logger():
    # Define a dynamic filename with the current date and time for info logs
    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    
    # Create logs directory if it doesn't exist
    if not os.path.exists("training/logs/error_logs"):
        os.makedirs("training/logs/error_logs")
    
    # Full path for the log file
    log_filepath = os.path.join("training/logs/error_logs", log_filename)

    # Create the error logger
    error_logger = logging.getLogger("error_logger")


    # Set the levels
    error_logger.setLevel(logging.ERROR)

    # Handler for the error logger
    error_handler = logging.FileHandler(log_filepath)
    error_handler.setLevel(logging.ERROR)

    # Formatter for error logging
    formatter_error= logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s\n"
    )
    error_handler.setFormatter(formatter_error)
    
    # adding the handler
    error_logger.addHandler(error_handler)

    return error_logger


info_logger = setup_info_logger()
error_logger = setup_error_logger()

if __name__ == "__main__":
    info_logger.info("Hello, World!")
    error_logger.error("This is an error message")