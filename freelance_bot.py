# freelance_bot.py - Fiverr/Upwork کے لیے خودکار proposal system
from google import genai
from config import GEMINI_API_KEY
import sqlite3
import datetime

# AI client
client = genai.Client(api_key=GEMINI_API_KEY)

# Database setup
conn = sqlite3.connect('business.db')
c = conn.cursor()

# Proposals table (اگر نہیں ہے تو بنا دے)
c.execute('''CREATE TABLE IF NOT EXISTS proposals
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              job_title TEXT,
              job_description TEXT,
              proposal_text TEXT,
              status TEXT DEFAULT 'draft',
              created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

def generate_proposal(job_title, job_description, budget=""):
    """
    AI se Roman Urdu mein proposal likhwaye
    """
    prompt = f"""
    Roman Urdu mein ek professional freelance proposal likho:
    
    Job Title: {job_title}
    Job Description: {job_description}
    Budget: {budget}
    
    Proposal mein yeh sab شامل ہو:
    1. Client کو greeting
    2. Apna experience (general)
    3. Job ke liye kyun best ho
    4. Timeline (3-5 din)
    5. Price (budget ke hisaab se)
    6. Call to action
    
    Sirf proposal do, koi extra text nahi.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Error generating proposal: {e}"

def save_proposal(job_title, job_desc, proposal):
    """
    Proposal ko database mein save kare
    """
    c.execute("INSERT INTO proposals (job_title, job_description, proposal_text, status) VALUES (?, ?, ?, ?)",
              (job_title, job_desc, proposal, 'draft'))
    conn.commit()
    print(f"✅ Proposal saved! ID: {c.lastrowid}")

def get_saved_proposals(limit=5):
    """
    Save kiye gaye proposals dekhe
    """
    c.execute("SELECT id, job_title, created_at, status FROM proposals ORDER BY created_at DESC LIMIT ?", (limit,))
    props = c.fetchall()
    
    if props:
        print("\n📋 Saved Proposals:")
        for p in props:
            print(f"ID: {p[0]}, Title: {p[1][:30]}..., Date: {p[2][:10]}, Status: {p[3]}")
    else:
        print("❌ Koi proposal nahi hai.")
    return props

def view_proposal_details(prop_id):
    """
    Kisi proposal ki details dekhe
    """
    c.execute("SELECT job_title, job_description, proposal_text FROM proposals WHERE id=?", (prop_id,))
    prop = c.fetchone()
    
    if prop:
        print("\n" + "="*50)
        print(f"📄 Job: {prop[0]}")
        print("="*50)
        print(f"Description: {prop[1]}")
        print("\n📝 Proposal:")
        print("-"*50)
        print(prop[2])
        print("-"*50)
    else:
        print("❌ Proposal nahi mila.")

def mark_as_sent(prop_id):
    """
    Proposal bhej diya gaya to status update kare
    """
    c.execute("UPDATE proposals SET status='sent' WHERE id=?", (prop_id,))
    conn.commit()
    print(f"✅ Proposal {prop_id} marked as sent!")

def main_menu():
    while True:
        print("\n" + "="*50)
        print("🤖 FREELANCE BOT MENU")
        print("="*50)
        print("1. نئی job کے لیے proposal بنائیں")
        print("2. Save kiye gaye proposals دیکھیں")
        print("3. Proposal کی details دیکھیں")
        print("4. Proposal کو 'sent' مارک کریں")
        print("5. Exit")
        
        choice = input("\nChoice (1-5): ")
        
        if choice == '1':
            title = input("Job title: ")
            desc = input("Job description: ")
            budget = input("Budget (optional): ")
            
            print("\n🤖 Proposal bana raha hoon...")
            proposal = generate_proposal(title, desc, budget)
            
            print("\n📝 Generated Proposal:")
            print("-"*40)
            print(proposal)
            print("-"*40)
            
            save = input("Save karna hai? (y/n): ")
            if save.lower() == 'y':
                save_proposal(title, desc, proposal)
        
        elif choice == '2':
            get_saved_proposals()
        
        elif choice == '3':
            try:
                pid = int(input("Proposal ID: "))
                view_proposal_details(pid)
            except:
                print("❌ Invalid ID")
        
        elif choice == '4':
            try:
                pid = int(input("Proposal ID: "))
                mark_as_sent(pid)
            except:
                print("❌ Invalid ID")
        
        elif choice == '5':
            print("Allah Hafiz!")
            break
        
        input("\nPress Enter to continue...")
    
    conn.close()

if __name__ == "__main__":
    main_menu()