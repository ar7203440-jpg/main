from google import genai

# Yahan seedha API key paste karo (config ki zaroorat nahi)
API_KEY = "AIzaSyBcX..."  # apni nayi key yahan paste karo

client = genai.Client(api_key=API_KEY)
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents="Roman Urdu mein ek line likho"
)
print(response.text)