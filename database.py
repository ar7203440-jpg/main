import sqlite3

# Database connection
conn = sqlite3.connect('business.db')
c = conn.cursor()

# Table for posts
c.execute('''CREATE TABLE IF NOT EXISTS posts
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              content TEXT,
              platform TEXT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

conn.commit()
conn.close()
print("✅ Database table ready!")