# config/config.py
import os

from dotenv import load_dotenv

load_dotenv()

def load_config():
    return {
        

        "llm_provider": os.getenv("LLM_PROVIDER", "groq"),
        "model_name": os.getenv("MODEL_NAME","llama-3.1-8b-instant")
    }
