from dotenv import load_dotenv
import os

print("Testing dotenv...")
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print(f"API Key loaded: {api_key is not None}")
print(f"Key value: {api_key}")