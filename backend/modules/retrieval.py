import os
import numpy as np
import faiss
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import log_helper 

from log_helper import logger

from modules.loader import get_text_job_profiles
from config import (EMBEDDING_MODEL_NAME, 
                    TOP_K, 
                    INDEX_FILE_PATH,
                    SIMILARITY_TRESHOLD)


# Global caching for performance
embedding_model = None
faiss_index = None


def load_embedding_model():
    """
    Loads the embedding model once and reuses it for all queries.
    
    Returns:
        HuggingFaceEmbeddings: Preloaded embedding model.
    """
    global embedding_model
    if embedding_model is None:
        embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        logger.info("Embedding model loaded into memory.")
    return embedding_model


def load_index():
    """Loads FAISS index and creates one if missing."""
    global faiss_index
    global embedding_model
    if faiss_index is None:
        if not os.path.exists(INDEX_FILE_PATH):
            logger.warning(f"FAISS index missing at {INDEX_FILE_PATH}. Generating new index...")
            create_index(embedding_model)
        
        faiss_index = faiss.read_index(INDEX_FILE_PATH)
        logger.info("FAISS index loaded into memory.")
    
    return faiss_index



def create_index(embedding_model):
    """
    Creates and saves a FAISS index for job profile embeddings.
    """
    logger.info("Creating FAISS index...")
    text_job_profiles = get_text_job_profiles()
    
    if not text_job_profiles:
        logger.error("No job profiles found. Index creation aborted.")
        return

    # Generate and normalize embeddings
    job_profiles_embeddings = embedding_model.embed_documents(text_job_profiles)
    # converted embeddings to numpy array
    emb_array = np.array(job_profiles_embeddings, dtype=np.float32)
    # normalized the embeddings
    emb_array /= np.linalg.norm(emb_array, axis=1, keepdims=True)

    # Create and save FAISS index
    index = faiss.IndexFlatIP(emb_array.shape[1])
    index.add(emb_array)
    faiss.write_index(index, INDEX_FILE_PATH)

    logger.info(f"FAISS index created successfully and saved at {INDEX_FILE_PATH}")



@log_helper.log_execution_time
def retrieve_context(user_query: str, embedding_model, faiss_index) -> str:
    """
    Searches the FAISS index for job profiles similar to the user's query and filters results based on a similarity threshold.
    
    Args:
        user_query (str): User's search query.
        model (HuggingFaceEmbeddings): Preloaded embedding model.
        index (faiss.Index): Preloaded FAISS index.

    Returns:
        str: Retrieved job profiles formatted as text.
    """
    logger.info(f"Searching for jobs related to: {user_query}")

    # Generate and normalize query embedding
    query_embedding = np.array(embedding_model.embed_query(user_query), dtype=np.float32).reshape(1, -1)
    query_embedding /= np.linalg.norm(query_embedding, axis=1, keepdims=True)

    # Perform search
    distances, indices = faiss_index.search(query_embedding, TOP_K)
    
    # Convert distances to similarity scores (cosine similarity, similarity = 1 - distance)
    similarity_scores = 1 - distances[0]
    
    # Filter results based on threshold
    valid_indices = [idx for idx, score in zip(indices[0], similarity_scores) if score >= SIMILARITY_TRESHOLD]
    
    if not valid_indices:
        logger.warning(f"No relevant info found above the threshold ({SIMILARITY_TRESHOLD}) for query: {user_query}")
        return "No relevant info found above the similarity threshold."

    text_job_profiles = get_text_job_profiles()
    retrieved_context = "\n\n".join([text_job_profiles[idx] for idx in valid_indices])
    
    logger.info(f"Retrieved {len(valid_indices)} job profiles for query: {user_query}")
    
    return retrieved_context




