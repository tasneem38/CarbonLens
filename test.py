import os
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not API_KEY:
    print("❌ No API key found. Add HUGGINGFACE_API_KEY to your .env")
    exit()

# Correct new HF endpoint
API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "inputs": """
User carbon profile:
Energy = 220 kg
Travel = 180 kg
Food = 120 kg
Goods = 60 kg
Green Score = 65/100

Give one very specific carbon reduction recommendation under 40 words.
""",

    "parameters": {
        "max_new_tokens": 120,
        "temperature": 0.65
    }
}

print("\n=== RAW RESPONSE ===\n")

response = requests.post(API_URL, headers=headers, json=payload)

print(response.text)

print("\n=== AI RESPONSE ===\n")

try:
    data = response.json()
    if "generated_text" in data[0]:
        print(data[0]["generated_text"])
    else:
        print("No text returned:", data)
except Exception as e:
    print("Parsing error:", e)
