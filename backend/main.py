# main.py

from log_helper import logger
from fastapi import FastAPI, HTTPException
from modules.retrieval import (
    search_jobs,
    load_embedding_model,
    load_index,
    create_index
    )
from modules.generator import generate_response


# Initialize FastAPI app
app = FastAPI(title="JobMentor AI", description="AI-powered job mentoring API", version="1.0")


# Load model & FAISS index at startup
embedding_model = load_embedding_model()
faiss_index = load_index()


@app.get("/", tags=["test"])
def test_api():
    """
    test endpoint to verify API is working.
    """
    logger.info("api test requested.")
    return {"status": "running"}


@app.get("/query/", tags=["Job Search"])
def get_jobs(query: str):
    """
    Retrieve relevant jobs based on the user's query.
    
    Args:
        query (str): User's job-related query (skills, education, career interests).
    
    Returns:
        dict: API response with job recommendations.
    """
    logger.info(f"Received job query: {query}")

    try:
        relevant_jobs = search_jobs(query, embedding_model, faiss_index)

        if not relevant_jobs:
            logger.warning(f"No jobs found for query: {query}")
            return {"status": "Success", "query": query, "response": "No relevant jobs found."}

        response, retrieved_context = generate_response(query, relevant_jobs)
        logger.info(f"Generated response for query: {query}")

        return {"status": "Success", "query": query, "response": response, "retrieved_context":retrieved_context}

    except Exception as e:
        logger.error(f"Error processing query '{query}': {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@app.post("/update_index/")
def update_faiss_index():
    """
    API endpoint to update FAISS index when new job profiles are added.
    """
    create_index(embedding_model)
    return {"status": "Success", "message": "FAISS index updated successfully."}
