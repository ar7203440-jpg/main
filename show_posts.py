# show_posts.py - Database se posts dekho
import sqlite3

conn = sqlite3.connect('business.db')
c = conn.cursor()

c.execute("SELECT id, platform, content, timestamp FROM posts ORDER BY timestamp DESC")
posts = c.fetchall()
conn.close()

if posts:
    print(f"\n📝 Total posts: {len(posts)}")
    print("="*60)
    for post in posts:
        print(f"\n🆔 ID: {post[0]}")
        print(f"📱 Platform: {post[1]}")
        print(f"📅 Time: {post[3]}")
        print(f"📄 Content: {post[2]}")
        print("-"*60)
else:
    print("❌ Database mein koi post nahi hai.")