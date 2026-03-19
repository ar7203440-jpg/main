import sounddevice as sd
import numpy as np
import wave
import speech_recognition as sr
import pyttsx3
import os
import io
from google import genai
from config import GEMINI_API_KEY
import time

# Text to speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# AI client
client = genai.Client(api_key=GEMINI_API_KEY)

WAKE_WORD = "جاڑوس"
SAMPLE_RATE = 16000

def speak(text):
    print(f"🗣️: {text}")
    engine.say(text)
    engine.runAndWait()

def record_audio(duration=4):
    """Microphone se audio record karo"""
    print("🎤 سن رہا ہوں...")
    recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    return recording

def audio_to_text(audio_data):
    """audio ko text mein badlo"""
    # audio data ko bytes mein convert karo
    bytes_io = io.BytesIO()
    with wave.open(bytes_io, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())
    bytes_io.seek(0)
    
    r = sr.Recognizer()
    with sr.AudioFile(bytes_io) as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio, language="ur-PK")
            return text.lower()
        except:
            return None

def main():
    speak("السلام علیکم! میں سننے کے لیے تیار ہوں۔")
    
    while True:
        # پہلے wake word سنیں
        audio = record_audio(3)
        text = audio_to_text(audio)
        
        if text and WAKE_WORD in text:
            speak("جی")
            
            # اب کمانڈ سنیں
            cmd_audio = record_audio(5)
            cmd_text = audio_to_text(cmd_audio)
            
            if cmd_text:
                print(f"کمانڈ: {cmd_text}")
                
                if "content" in cmd_text:
                    speak("کیا موضوع چاہیے؟")
                    topic_audio = record_audio(4)
                    topic = audio_to_text(topic_audio)
                    if topic:
                        os.system(f"python content_agent.py --topic '{topic}'")
                        speak("content بنا دیا")
                
                elif "خدا حافظ" in cmd_text:
                    speak("اللہ حافظ")
                    break
                
                else:
                    # AI se poocho
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=f"Roman Urdu mein chhota jawab do: {cmd_text}"
                    )
                    speak(response.text)
            else:
                speak("کچھ نہیں سنا")
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()