# fill_database.py - Ek saath database mein data dalne ke liye
import sqlite3
import random
from datetime import datetime, timedelta

# Database connection
conn = sqlite3.connect('business.db')
c = conn.cursor()

# Pehle tables create karo (agar nahi hain)
c.execute('''CREATE TABLE IF NOT EXISTS posts
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              content TEXT,
              platform TEXT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

c.execute('''CREATE TABLE IF NOT EXISTS earnings
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              amount REAL,
              source TEXT,
              date DATETIME DEFAULT CURRENT_TIMESTAMP)''')

# Sample posts data
posts_data = [
    ("Mehnat karne walon ki kabhi haar nahi hoti. Kamyabi ek din zaroor milti hai.", "facebook"),
    ("Business mein sab se important cheez consistency hai. Roz ek step aage badho.", "linkedin"),
    ("Aaj ka inspirational quote: 'Kamyabi unki hoti hai jo haar maanne se pehle ek baar aur koshish karte hain.'", "blog"),
    ("Naye clients ke liye special discount! Aaj hi contact karein.", "facebook"),
    ("5 tips for successful freelancing: 1) Communication, 2) Quality work, 3) On-time delivery, 4) Reasonable rates, 5) Good reviews", "linkedin"),
    ("Dropshipping business kaise shuru karein? Aaj ki post mein seekhein.", "blog"),
    ("Affiliate marketing se ghar baitho paisa kamayein. Free course link in bio.", "facebook"),
    ("Roman Urdu mein content banana seekhein. Hamari AI agent aapki madad karega.", "linkedin"),
    ("Aaj ka thought: Paisa kamane se zyada important hai paisa save karna.", "blog"),
    ("Weekend special: 50% off on all digital products! Limited time offer.", "facebook")
]

# Sample earnings data
sources = ["fiverr", "upwork", "freelancer", "affiliate", "youtube", "blogging"]
earnings_data = []

# Last 30 days ke earnings generate karo
for i in range(30):
    date = datetime.now() - timedelta(days=i)
    for _ in range(random.randint(1, 3)):  # Har din 1-3 entries
        amount = round(random.uniform(100, 5000), 2)
        source = random.choice(sources)
        earnings_data.append((amount, source, date))

# Posts insert karo
c.executemany("INSERT INTO posts (content, platform) VALUES (?, ?)", posts_data)

# Earnings insert karo
c.executemany("INSERT INTO earnings (amount, source, date) VALUES (?, ?, ?)", earnings_data)

conn.commit()
conn.close()

print("✅ Database successfully filled with data!")
print(f"📝 {len(posts_data)} posts added")
print(f"💰 {len(earnings_data)} earnings entries added")