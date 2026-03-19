import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
SAMPLE_RATE = 16000

def speak(text):
    print(f"🗣️: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    print("🎤 بولیے...")
    audio = sd.rec(int(5 * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    
    r = sr.Recognizer()
    try:
        # audio ko text mein badlo
        text = r.recognize_google(audio, language="ur-PK")
        return text.lower()
    except:
        return None

# یہاں main program شروع ہوتا ہے
speak("کیا کہنا چاہتے ہیں؟")
command = listen()
if command:
    print(f"آپ نے کہا: {command}")
    speak(f"آپ نے کہا: {command}")
else:
    speak("سمجھ نہیں آیا")