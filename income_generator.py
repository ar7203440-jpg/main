# income_generator.py - Advanced Income Generation System
import sqlite3
import random
from datetime import datetime
from google import genai
from config import GEMINI_API_KEY

# AI setup
client = genai.Client(api_key=GEMINI_API_KEY)

# Database setup
conn = sqlite3.connect('business.db')
c = conn.cursor()

# Income sources table
c.execute('''CREATE TABLE IF NOT EXISTS income_sources
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              source_name TEXT,
              source_type TEXT,
              active INTEGER DEFAULT 1,
              earnings REAL DEFAULT 0,
              last_used DATETIME)''')

# Affiliate links table
c.execute('''CREATE TABLE IF NOT EXISTS affiliate_links
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              product_name TEXT,
              link TEXT,
              commission REAL,
              clicks INTEGER DEFAULT 0,
              sales INTEGER DEFAULT 0,
              earnings REAL DEFAULT 0)''')

# Tasks table for automatic income tasks
c.execute('''CREATE TABLE IF NOT EXISTS income_tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              task_name TEXT,
              schedule TEXT,
              last_run DATETIME,
              status TEXT)''')

conn.commit()

class IncomeGenerator:
    def __init__(self):
        self.income_sources = []
        self.load_sources()
    
    def load_sources(self):
        """Load active income sources from database"""
        c.execute("SELECT * FROM income_sources WHERE active=1")
        self.income_sources = c.fetchall()
        print(f"✅ Loaded {len(self.income_sources)} income sources")
    
    def add_income_source(self, name, source_type):
        """Add new income source"""
        c.execute("INSERT INTO income_sources (source_name, source_type, last_used) VALUES (?, ?, ?)",
                  (name, source_type, datetime.now()))
        conn.commit()
        print(f"✅ Income source '{name}' added!")
        self.load_sources()
    
    def add_affiliate_product(self, product, link, commission):
        """Add affiliate product"""
        c.execute("INSERT INTO affiliate_links (product_name, link, commission) VALUES (?, ?, ?)",
                  (product, link, commission))
        conn.commit()
        print(f"✅ Affiliate product '{product}' added!")
    
    def generate_affiliate_content(self, product_id):
        """AI se affiliate content banao"""
        c.execute("SELECT * FROM affiliate_links WHERE id=?", (product_id,))
        product = c.fetchone()
        if not product:
            print("❌ Product not found")
            return
        
        prompt = f"Roman Urdu mein ek persuasive post likho jo {product[1]} ko promote kare. Product link: {product[2]}. Commission: {product[3]}%. Logon ko buy karne ke liye motivate karo."
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        content = response.text
        
        # Save as post for social media
        conn2 = sqlite3.connect('business.db')
        c2 = conn2.cursor()
        c2.execute("INSERT INTO posts (content, platform) VALUES (?, ?)",
                   (content, "affiliate"))
        conn2.commit()
        conn2.close()
        
        print(f"✅ Affiliate post generated for {product[1]}")
        print("-"*40)
        print(content[:200] + "...")
        print("-"*40)
        return content
    
    def track_click(self, product_id):
        """Track affiliate link click"""
        c.execute("UPDATE affiliate_links SET clicks = clicks + 1 WHERE id=?", (product_id,))
        conn.commit()
        print(f"✅ Click tracked for product ID {product_id}")
    
    def track_sale(self, product_id, amount):
        """Track affiliate sale"""
        c.execute("UPDATE affiliate_links SET sales = sales + 1, earnings = earnings + ? WHERE id=?", (amount, product_id))
        conn.commit()
        
        # Also add to earnings
        c.execute("INSERT INTO earnings (amount, source) VALUES (?, ?)",
                  (amount, f"affiliate_product_{product_id}"))
        conn.commit()
        print(f"✅ Sale tracked: Rs.{amount}")
    
    def generate_daily_income_tasks(self):
        """AI se daily income tasks generate karo"""
        prompt = "Roman Urdu mein aaj ke 5 online income tasks batao jo koi freelancer kar sakta hai. Short bullet points mein."
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        tasks = response.text
        print("\n📋 Aaj ke income tasks:")
        print("-"*40)
        print(tasks)
        print("-"*40)
        
        # Save to database
        c.execute("INSERT INTO income_tasks (task_name, schedule, status) VALUES (?, ?, ?)",
                  ("Daily Tasks", "daily", "generated"))
        conn.commit()
        
        return tasks
    
    def generate_income_report(self):
        """Income report generate karo"""
        c.execute("SELECT SUM(earnings) FROM affiliate_links")
        affiliate_total = c.fetchone()[0] or 0
        
        c.execute("SELECT SUM(amount) FROM earnings")
        total_earnings = c.fetchone()[0] or 0
        
        c.execute("SELECT source_name, earnings FROM income_sources WHERE earnings > 0")
        sources = c.fetchall()
        
        print("\n💰 INCOME REPORT")
        print("="*50)
        print(f"Total Affiliate Earnings: Rs.{affiliate_total}")
        print(f"Total All Earnings: Rs.{total_earnings}")
        print("\n📊 Source-wise:")
        for source in sources:
            print(f"   {source[0]}: Rs.{source[1]}")
        
        c.execute("SELECT product_name, clicks, sales, earnings FROM affiliate_links WHERE clicks > 0 OR sales > 0")
        products = c.fetchall()
        if products:
            print("\n🛍️ Affiliate Performance:")
            for p in products:
                print(f"   {p[0]}: {p[1]} clicks, {p[2]} sales, Rs.{p[3]} earned")
        print("="*50)

def main_menu():
    income = IncomeGenerator()
    
    while True:
        print("\n" + "="*50)
        print("💰 ADVANCED INCOME GENERATOR")
        print("="*50)
        print("1. Add Income Source")
        print("2. Add Affiliate Product")
        print("3. Generate Affiliate Post")
        print("4. Track Click")
        print("5. Track Sale")
        print("6. Daily Income Tasks")
        print("7. Income Report")
        print("8. Show All Income Sources")
        print("9. Show Affiliate Products")
        print("10. Exit")
        
        choice = input("\nChoice (1-10): ")
        
        if choice == '1':
            name = input("Source name: ")
            stype = input("Source type (freelance/affiliate/product/etc): ")
            income.add_income_source(name, stype)
        
        elif choice == '2':
            product = input("Product name: ")
            link = input("Affiliate link: ")
            commission = float(input("Commission percentage: "))
            income.add_affiliate_product(product, link, commission)
        
        elif choice == '3':
            income.generate_affiliate_content(1)  # Simple version, you can add ID selection
        
        elif choice == '4':
            pid = int(input("Product ID: "))
            income.track_click(pid)
        
        elif choice == '5':
            pid = int(input("Product ID: "))
            amount = float(input("Sale amount: "))
            income.track_sale(pid, amount)
        
        elif choice == '6':
            income.generate_daily_income_tasks()
        
        elif choice == '7':
            income.generate_income_report()
        
        elif choice == '8':
            c.execute("SELECT * FROM income_sources")
            sources = c.fetchall()
            print("\n📋 Income Sources:")
            for s in sources:
                print(f"ID: {s[0]}, Name: {s[1]}, Type: {s[2]}, Active: {s[3]}, Earnings: Rs.{s[4]}")
        
        elif choice == '9':
            c.execute("SELECT * FROM affiliate_links")
            products = c.fetchall()
            print("\n📋 Affiliate Products:")
            for p in products:
                print(f"ID: {p[0]}, Product: {p[1]}, Commission: {p[3]}%, Clicks: {p[4]}, Sales: {p[5]}, Earnings: Rs.{p[6]}")
        
        elif choice == '10':
            print("Allah Hafiz! 👋")
            break
        
        input("\nPress Enter to continue...")
    
    conn.close()

if __name__ == "__main__":
    main_menu()