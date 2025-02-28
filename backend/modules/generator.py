# generator.py

import os
from typing import Dict, Any, Optional

from typing import Tuple
import google.generativeai as genai

import log_helper 
from log_helper import logger
from modules.retrieval import retrieve_context
from log_helper import store_response

from config import GEMINI_MODEL_NAME
from modules.prompts import SYSTEM_PROMPT


from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def configure_genai() -> None:
    """Configures the Google Generative AI SDK with the API key."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    genai.configure(api_key=api_key)


# Initialize the API configuration
configure_genai()


def get_answer(
    user_query: str, 
    embedding_model: Any, 
    faiss_index: Any
) -> Dict[str, Any]:
    """
    Retrieves context for the user's query, generates a response, 
    and returns the result in a structured format.

    Args:
        user_query (str): The query entered by the user.
        embedding_model (Any): The embedding model used for vectorization.
        faiss_index (Any): The FAISS index for similarity search.

    Returns:
        Dict[str, Any]: A dictionary containing the response and retrieved context.
    """

    logger.info(f"Processing query: {user_query}")

    # Retrieve relevant context
    retrieved_context = retrieve_context(user_query, embedding_model, faiss_index)

    if not retrieved_context:
        logger.warning(f"No relevant data found for query: {user_query}")
        return {
            "status": "Success",
            "query": user_query,
            "response": "No relevant data found.",
            "retrieved_context": None
        }

    # Generate response based on retrieved context
    try:
        generated_answer, retrieved_context = generate_response(user_query, retrieved_context)
        logger.info(f"Generated response for query: {user_query}")
    except Exception as e:
        logger.error(f"Error generating response for query: {user_query} - {str(e)}")
        return {
            "status": "Error",
            "query": user_query,
            "response": "An error occurred while generating the response.",
            "retrieved_context": None
        }

    return {
        "status": "Success",
        "query": user_query,
        "response": generated_answer,
        "retrieved_context": retrieved_context
        }




@log_helper.log_execution_time
def generate_response(user_query: str, retrieved_context: str) -> Tuple[str, str]:
    """
    Generates a response from the Gemini model based on user query and retrieved context.
    
    Args:
        user_query (str): The user's input query.
        retrieved_context (str): Additional context retrieved for better response generation.
    
    Returns:
        Tuple[str, str]: The generated response and the retrieved context.
    """

    user_prompt = f"\nQuestion: {user_query} \nContext: {retrieved_context} \nAnswer:"
    
    gemini_response =  get_gemini_response(SYSTEM_PROMPT, user_prompt), retrieved_context

    return gemini_response


def get_gemini_response(system_prompt: str, user_prompt: str) -> str:
    """
    Interacts with the Gemini model to generate content based on prompts.
    
    Args:
        system_prompt (str): The system-level instruction for the model.
        user_prompt (str): The user query combined with contextual information.
    
    Returns:
        str: The generated response from the model.
    """
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL_NAME, 
        system_instruction=system_prompt
    )
    
    response = model.generate_content(
        user_prompt,
        generation_config=genai.GenerationConfig(
            max_output_tokens=8192,
            temperature=0,
            top_p=1, 
            top_k=32
        )
    )
    
    return response.text if response and hasattr(response, 'text') else ""
