from google import genai
from config import GEMINI_API_KEY

print("🔍 Testing AI connection...")

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents="Roman Urdu mein ek line likho"
)

print("✅ AI jawab:")
print(response.text)