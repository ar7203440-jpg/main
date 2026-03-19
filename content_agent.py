# content_agent.py
from google import genai
from config import GEMINI_API_KEY
import sqlite3
from datetime import datetime

# AI client
client = genai.Client(api_key=GEMINI_API_KEY)

# Database connection
conn = sqlite3.connect('business.db')
c = conn.cursor()

# Content banao
prompts = [
    ("motivation", "facebook"),
    ("business tips", "linkedin"),
    ("success story", "blog")
]

for topic, platform in prompts:
    print(f"\n✨ {platform} ke liye '{topic}' par content bana rahe hain...")
    
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=f"Roman Urdu mein {topic} par ek chhoti post likho, 50 words mein"
    )
    
    content = response.text
    
    # Database mein save karo
    c.execute(
        "INSERT INTO posts (content, platform) VALUES (?, ?)",
        (content, platform)
    )
    conn.commit()
    
    print(f"✅ Save ho gaya!")
    print("-"*40)
    print(content[:100] + "...")
    print("-"*40)

conn.close()
print("\n🎉 Saara content save ho gaya!")