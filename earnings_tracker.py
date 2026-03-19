# earnings_tracker.py - Income track karo
import sqlite3
from datetime import datetime

def add_earning():
    source = input("Source kya hai? (Fiverr/Upwork/Affiliate/etc): ")
    amount = float(input("Kitne paise mile? (Rs): "))
    
    conn = sqlite3.connect('business.db')
    c = conn.cursor()
    c.execute("INSERT INTO earnings (amount, source) VALUES (?, ?)", (amount, source))
    conn.commit()
    conn.close()
    print(f"✅ Rs.{amount} {source} se add kar diya!")

def show_earnings():
    conn = sqlite3.connect('business.db')
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM earnings")
    total = c.fetchone()[0] or 0
    
    c.execute("SELECT date, source, amount FROM earnings ORDER BY date DESC LIMIT 10")
    recent = c.fetchall()
    conn.close()
    
    print(f"\n💰 Total Earnings: Rs.{total}")
    print("📋 Recent Earnings:")
    for r in recent:
        print(f"   {r[0]} - {r[1]}: Rs.{r[2]}")

while True:
    print("\n1. Add Earning")
    print("2. Show Earnings")
    print("3. Exit")
    choice = input("Choice: ")
    if choice == '1':
        add_earning()
    elif choice == '2':
        show_earnings()
    elif choice == '3':
        break