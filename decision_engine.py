# AI سے فیصلہ کرے کہ آج کیا کام بہتر رہے گا
from google import genai
from config import GEMINI_API_KEY
import sqlite3

client = genai.Client(api_key=GEMINI_API_KEY)

def get_best_tasks():
    # پچھلے 7 دنوں کی کارکردگی دیکھے
    conn = sqlite3.connect('business.db')
    c = conn.cursor()
    c.execute("SELECT source, SUM(amount) FROM earnings GROUP BY source ORDER BY SUM(amount) DESC LIMIT 3")
    top_sources = c.fetchall()
    conn.close()
    
    prompt = f"""
    Roman Urdu mein decision lo:
    Pichle hafte ki top income sources: {top_sources}
    
    Aaj ke liye 3 sabse important tasks batao:
    1. Content creation (kis topic par?)
    2. Affiliate marketing (kis product ko promote karna hai?)
    3. Freelance bidding (kis category mein?)
    
    Sirf tasks do, koi extra text nahi.
    """
    
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt
    )
    return response.text
    # decision_engine.py میں شامل کریں
def get_best_tasks():
    # ڈیٹابیس سے پچھلے 7 دنوں کا ڈیٹا لے کر AI سے مشورہ لیں
    import sqlite3
    conn = sqlite3.connect('business.db')
    c = conn.cursor()
    c.execute("SELECT source, SUM(amount) FROM earnings GROUP BY source ORDER BY SUM(amount) DESC LIMIT 3")
    top_sources = c.fetchall()
    conn.close()
    
    prompt = f"Roman Urdu mein aaj ke 3 best tasks batao jo freelancer kar sakta hai. Pichle hafte ki top income sources: {top_sources}"
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt
    )
    return response.text