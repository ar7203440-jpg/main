# khud ko improve kare
import sqlite3
import json

def analyze_performance():
    conn = sqlite3.connect('business.db')
    c = conn.cursor()
    
    # Kaunsi type ki posts zyada successful hui?
    c.execute("SELECT platform, COUNT(*) FROM posts GROUP BY platform")
    post_stats = c.fetchall()
    
    # Konsa income source best hai?
    c.execute("SELECT source, SUM(amount) FROM earnings GROUP BY source ORDER BY SUM(amount) DESC")
    income_stats = c.fetchall()
    
    conn.close()
    
    # Future decisions ke liye save karo
    insights = {
        'best_platform': post_stats[0][0] if post_stats else 'blog',
        'best_income_source': income_stats[0][0] if income_stats else 'affiliate',
        'total_posts': sum(p[1] for p in post_stats) if post_stats else 0,
        'total_income': sum(i[1] for i in income_stats) if income_stats else 0
    }
    
    return insights