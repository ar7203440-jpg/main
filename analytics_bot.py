# performance track kare
import sqlite3
from datetime import datetime, timedelta

def get_daily_report():
    conn = sqlite3.connect('business.db')
    c = conn.cursor()
    
    # Aaj ki income
    c.execute("SELECT SUM(amount) FROM earnings WHERE date(date) = date('now')")
    today_income = c.fetchone()[0] or 0
    
    # Pichle 7 din ki income
    c.execute("SELECT SUM(amount) FROM earnings WHERE date >= date('now', '-7 days')")
    weekly_income = c.fetchone()[0] or 0
    
    # Best performing source
    c.execute("SELECT source, SUM(amount) FROM earnings GROUP BY source ORDER BY SUM(amount) DESC LIMIT 1")
    best_source = c.fetchone()
    
    conn.close()
    
    return {
        'today': today_income,
        'weekly': weekly_income,
        'best_source': best_source
    }