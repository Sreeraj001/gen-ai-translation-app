import os
from dotenv import load_dotenv
import google.generativeai as genai

# Function to translate text using Gemini API
def translate_text(text, target_language):  
    load_dotenv()

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-flash-latest') 
    response = model.generate_content(f"Translate '{text}' to {target_language}. just provide the translated text without any additional information.")

    return response.text


