# list_groq_models.py
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    models = client.models.list()
    print("Available Groq models:")
    for model in models.data:
        print(f"- {model.id}")
        print(f"  Created: {model.created}")
        print(f"  Owned by: {model.owned_by}")
        print()
except Exception as e:
    print(f"Error: {e}")