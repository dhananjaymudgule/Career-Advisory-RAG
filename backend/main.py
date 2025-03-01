# main.py

from fastapi import FastAPI, HTTPException
from modules.retrieval import (
    retrieve_context,
    load_embedding_model,
    load_index,
    create_index
    )
from modules.generator import get_answer
from log_helper import logger



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


@app.get("/query/", tags=["Get Answers"])
def get_answers(query: str):
    """
    API endpoint to get answers from RAG AI
    """
    logger.info(f"Received query: {query}")

    try:
        
        response = get_answer(query, embedding_model, faiss_index)

        return response

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
