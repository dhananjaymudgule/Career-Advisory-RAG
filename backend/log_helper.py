# logger.py

import time
import logging



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(funcName)s: %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # logs to a file
        logging.StreamHandler()  # logs to console
    ]
)

# logger instance
logger = logging.getLogger(__name__)  




def log_execution_time(func):
    """Decorator to log the time a function takes to execute."""
    def wrapper(*args, **kwargs):
        start_time = time.time()  # record the start time
        result = func(*args, **kwargs)  # execute the function
        end_time = time.time()  # record the end time
        elapsed_time = end_time - start_time  # calculate elapsed time
        logging.info(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds")
        return result
    return wrapper
