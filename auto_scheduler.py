# auto_scheduler.py - Khud ba khud kaam karne wala system
import schedule
import time
import os
from datetime import datetime
import sqlite3

def job_content():
    """Har subah content banane wala kaam"""
    print(f"🕒 {datetime.now()} - Content ban raha hai...")
    os.system("python content_agent.py")
    print("✅ Content ban gaya!")

def job_affiliate():
    """Affiliate posts generate karo"""
    print(f"🕒 {datetime.now()} - Affiliate posts ban rahe hain...")
    try:
        # Agar income_generator.py mein function hai to use karo, nahi to direct run
        os.system("python income_generator.py --generate-affiliate")
    except:
        print("⚠️ Affiliate generation optional hai, continue...")
    print("✅ Affiliate posts check kiye!")

def job_report():
    """Roz report banao"""
    print(f"🕒 {datetime.now()} - Daily report bana rahe hain...")
    os.system("python show_posts.py")
    os.system("python earnings_tracker.py")
    print("✅ Report ready!")

def setup_scheduler():
    """Schedule set karo"""
    # Har subah 8 baje content
    schedule.every().day.at("08:00").do(job_content)
    
    # Har 6 ghante mein affiliate check
    schedule.every(6).hours.do(job_affiliate)
    
    # Roz shaam 6 baje report
    schedule.every().day.at("18:00").do(job_report)
    
    # Test ke liye (2 minute mein ek baar, baad mein hata dena)
    # schedule.every(2).minutes.do(job_content)

    print("\n" + "="*50)
    print("🤖 AUTO SCHEDULER START HO GAYA!")
    print("="*50)
    print("📅 Schedule:")
    print("   • Subah 8:00 - Content banega")
    print("   • Har 6 ghante - Affiliate posts")
    print("   • Shaam 6:00 - Daily report")
    print("="*50)
    print("🟢 Scheduler chalta rahega... (band karne ke liye Ctrl+C dabaao)")
    print("="*50)

def main():
    setup_scheduler()
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Har minute check karo
    except KeyboardInterrupt:
        print("\n🛑 Scheduler band kar diya. Allah Hafiz!")

if __name__ == "__main__":
    main()

# auto_scheduler_advanced.py
import schedule
import time
from decision_engine import get_best_tasks
from content_agent import create_content
from income_generator import generate_affiliate_post
import subprocess

def morning_tasks():
    tasks = get_best_tasks()
    print(f"📋 Aaj ke tasks:\n{tasks}")
    # Tasks ko parse kar ke execute karo
    if "content" in tasks.lower():
        create_content("automated", "blog")
    if "affiliate" in tasks.lower():
        generate_affiliate_post()

schedule.every().day.at("08:00").do(morning_tasks)
schedule.every(4).hours.do(check_performance)
# ... etc
from decision_engine import get_best_tasks

def morning_routine():
    tasks = get_best_tasks()
    print(f"🤖 آج کے tasks:\n{tasks}")
    # tasks کو parse کر کے relevant bots چلائیں
    if "content" in tasks:
        import content_agent
        content_agent.create_content("auto", "blog")
    if "affiliate" in tasks:
        import income_generator
        income_generator.generate_affiliate_post()