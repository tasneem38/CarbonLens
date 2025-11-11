import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
print(f"API Key: {API_KEY}")

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("What is 2+2?")
        print("✅ SUCCESS! Gemini is working.")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ FAILED: {e}")
else:
    print("❌ No API key found in environment variables")
