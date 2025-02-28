# log_helper.py

import time
import logging
import pandas as pd

from config import (LATENCY_FILE, RESPONSES_FILE, LOG_FILE, MAX_RESPONSES)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(funcName)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # logs to a file
        logging.StreamHandler()  # logs to console
    ]
)

# Logger instance
logger = logging.getLogger(__name__)



def store_latency(function_name, elapsed_time):
    """Stores latency data using Pandas and saves it to a CSV file."""

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    new_entry = pd.DataFrame({
        "Timestamp": [timestamp],
        "Function": [function_name],
        "Execution Time (s)": [elapsed_time]
    })

    try:
        df = pd.read_csv(LATENCY_FILE)
        df = pd.concat([df, new_entry], ignore_index=True)
    except FileNotFoundError:
        df = new_entry

    df.to_csv(LATENCY_FILE, index=False)


def store_response(question, answer, context):
    """Stores RAG system responses (question, answer, context) in a CSV file."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    new_entry = pd.DataFrame({
        "Timestamp": [timestamp],
        "Question": [question],
        "Answer": [answer],
        "Context": [context]
    })

    try:
        df = pd.read_csv(RESPONSES_FILE)
        df = pd.concat([df, new_entry], ignore_index=True)
    except FileNotFoundError:
        df = new_entry

    df.to_csv(RESPONSES_FILE, index=False)


def store_response_new(question, answer, context):
    """Stores RAG system responses (question, answer, context) in a CSV file, keeping only the last 100 entries."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    new_entry = pd.DataFrame({
        "Timestamp": [timestamp],
        "Question": [question],
        "Answer": [answer],
        "Context": [context]
    })

    try:
        df = pd.read_csv(RESPONSES_FILE)

        # Append new entry and keep only the last MAX_RESPONSES
        df = pd.concat([df, new_entry], ignore_index=True).tail(MAX_RESPONSES)
    except FileNotFoundError:
        df = new_entry  # If file doesn't exist, create a new one

    df.to_csv(RESPONSES_FILE, index=False)


def log_execution_time(func):
    """Decorator to log and store the execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time

        logger.info(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds")

        # store the latency for future reference 
        # store_latency(func.__name__, elapsed_time)

        return result
    return wrapper
