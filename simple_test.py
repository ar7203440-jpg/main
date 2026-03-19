from google import genai

API_KEY = "AIzaSy..."  # apni nayi key yahan paste karo

client = genai.Client(api_key=API_KEY)
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents="Hi"
)
print(response.text)