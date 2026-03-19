# main.py - Master Controller
import os

def show_menu():
    print("\n" + "="*50)
    print("🤖 MY SMART BOT - MAIN MENU")
    print("="*50)
    print("1. AI se naya content banao (content_agent.py)")
    print("2. Saari posts dekho (show_posts.py)")
    print("3. Earnings tracker (earnings_tracker.py)")
    print("4. Database setup (database.py)")
    print("5. Exit")
    return input("\nChoice (1-5): ")

while True:
    choice = show_menu()
    if choice == '1':
        os.system("python content_agent.py")
    elif choice == '2':
        os.system("python show_posts.py")
    elif choice == '3':
        os.system("python earnings_tracker.py")
    elif choice == '4':
        os.system("python database.py")
    elif choice == '5':
        print("Allah Hafiz! 👋")
        break
    else:
        print("❌ Galat choice! Dobara try karo.")
    input("\nPress Enter to continue...")
    