import os
from typing import Tuple
import google.generativeai as genai

import log_helper 

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
    
    user_prompt = f"{user_query}\n\nContext:\n{retrieved_context}"

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
