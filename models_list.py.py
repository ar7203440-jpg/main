# models_list.py - تمام ماڈل دکھانے کے لیے
from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

print("دستیاب ماڈلز:")
for model in client.models.list():
    print(f"- {model.name}")