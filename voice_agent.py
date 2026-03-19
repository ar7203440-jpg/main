# voice_agent.py - Voice Command Assistant (Roman Urdu)
import speech_recognition as sr
import pyttsx3
import os
import subprocess
import sqlite3
from datetime import datetime
from google import genai
from config import GEMINI_API_KEY

# Text-to-Speech engine (bolne ke liye)
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Bolne ki speed
engine.setProperty('volume', 0.9)  # Awaaz ki volume

# Speech Recognition (sunne ke liye)
recognizer = sr.Recognizer()

# AI client
client = genai.Client(api_key=GEMINI_API_KEY)

def speak(text):
    """Roman Urdu mein bole"""
    print(f"🗣️ Bot: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Microphone se command sune"""
    with sr.Microphone() as source:
        print("\n🎤 Sun raha hoon... kuch bolo...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("✅ Sun liya, ab samajh raha hoon...")
            
            # Google Speech Recognition use karo
            text = recognizer.recognize_google(audio, language="ur-PK")  # Urdu/Pakistan
            print(f"👤 Aap ne kaha: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("معافی چاہتا ہوں، میں سمجھ نہیں پایا۔ دوبارہ کہیں۔")
            return None
        except sr.RequestError:
            speak("انٹرنیٹ کنیکشن چیک کریں۔")
            return None
        except sr.WaitTimeoutError:
            speak("کچھ بولا نہیں گیا۔")
            return None

def process_command(command):
    """Command ko samjhe aur action kare"""
    
    # 1. Content banao command
    if "content banao" in command or "پوسٹ بنا" in command:
        speak("کیا موضوع چاہیے؟")
        topic = listen()
        if topic:
            speak(f"{topic} پر content bana raha hoon...")
            # content_agent.py run karo ya direct function call
            os.system(f"python content_agent.py --topic '{topic}'")
            speak("content بن گیا۔")
    
    # 2. Posts dekho
    elif "posts dekho" in command or "پوسٹ دکھا" in command:
        speak("پوسٹس لا رہا ہوں...")
        os.system("python show_posts.py")
        speak("یہ رہیں پوسٹس۔")
    
    # 3. Income add karo
    elif "income add" in command or "آمدنی شامل" in command:
        speak("کتنی آمدنی ہوئی؟")
        amount = listen()
        if amount:
            # Extract numbers from speech (simplified)
            import re
            numbers = re.findall(r'\d+', amount)
            if numbers:
                amt = numbers[0]
                speak("کس ذریعے سے؟")
                source = listen()
                if source:
                    conn = sqlite3.connect('business.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO earnings (amount, source) VALUES (?, ?)", 
                              (float(amt), source))
                    conn.commit()
                    conn.close()
                    speak(f"روپے {amt} {source} سے شامل کر دیے۔")
    
    # 4. Total income
    elif "total income" in command or "کل آمدنی" in command:
        conn = sqlite3.connect('business.db')
        c = conn.cursor()
        c.execute("SELECT SUM(amount) FROM earnings")
        total = c.fetchone()[0] or 0
        conn.close()
        speak(f"کل آمدنی روپے {total} ہے۔")
    
    # 5. AI se baat karo
    elif "AI se poocho" in command or "سوال پوچھو" in command:
        speak("کیا پوچھنا ہے؟")
        question = listen()
        if question:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=f"Roman Urdu mein jawab do: {question}"
            )
            answer = response.text
            speak(answer)
    
    # 6. Help
    elif "help" in command or "مدد" in command:
        speak("میں یہ کام کر سکتا ہوں: content بنا سکتا ہوں، posts دکھا سکتا ہوں، income add کر سکتا ہوں، total income بتا سکتا ہوں، اور AI سے بات کر سکتا ہوں۔")
    
    # 7. Exit
    elif "exit" in command or "بند کرو" in command or "خدا حافظ" in command:
        speak("اللہ حافظ! پھر ملیں گے۔")
        return False
    
    else:
        speak("معاف کیجیے، یہ کام نہیں جانتا۔")
    
    return True

def main():
    speak("السلام علیکم! میں آپ کا وائس اسسٹنٹ ہوں۔")
    
    running = True
    while running:
        command = listen()
        if command:
            running = process_command(command)
        
        # Thoda wait karo agle command se pehle
        import time
        time.sleep(1)

if __name__ == "__main__":
    main()
    # content_agent.py mein yeh changes karo

import sys
import argparse

# Top par yeh add karo
def get_topic_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', type=str, default="motivation")
    args = parser.parse_args()
    return args.topic

# Aur function call mein topic pass karo
if __name__ == "__main__":
    topic = get_topic_from_args()
    create_content(topic, "voice_command")