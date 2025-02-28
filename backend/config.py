# config.py


# top k search
TOP_K = 3
SIMILARITY_TRESHOLD = 0.40

# llm model name/id
GEMINI_MODEL_NAME="gemini-2.0-flash"
LLAMA_MODEL_NAME = ""

# embedding model name
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# file path for RAG system
DATA_FILE_PATH = "data/datasets/CareerAdvisoryService.job_profiles_en_100_6thFeb.json"
INDEX_FILE_PATH = "data/indexes/index_job_profiles.index"

# csv file for storing latency data
LATENCY_FILE = "logs/latency_data.csv"

# csv files for storing questions answers and contexts
RESPONSES_FILE = "logs/rag_responses.csv"

# csv file for logs
LOG_FILE = "logs/main.log"

# questions answers and contextsresponse storage limit
MAX_RESPONSES = 100


