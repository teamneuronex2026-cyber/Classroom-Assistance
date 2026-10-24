import os
import speech_recognition as sr
from gtts import gTTS
from google import genai
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Initialize the Gemini Client
# The client automatically loads the GEMINI_API_KEY from your .env file via os.environ
client = genai.Client()
MODEL_ID = "gemini-2.5-flash"

def speak(text):
    print(f"[Assistant]: {text}")
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("response.mp3")
    # Play audio using mpg123
    subprocess.run(["mpg123", "-q", "response.mp3"])
    os.remove("response.mp3")

def listen_loop():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("\n[System] Calibrating for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("[System] Assistant is listening for your command...")

        while True:
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=10)
                print("[System] Processing speech...")
                
                # Convert speech to text using Google STT
                user_query = recognizer.recognize_google(audio)
                print(f"Teacher: {user_query}")

                if "exit" in user_query.lower() or "stop" in user_query.lower():
                    speak("Shutting down assistant. Goodbye!")
                    break

                # Query Google Gemini using the new SDK syntax
                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=user_query,
                )
                ai_reply = response.text
                
                speak(ai_reply)

            except sr.UnknownValueError:
                print("[!] Could not understand audio. Try speaking closer to the mic.")
            except sr.RequestError as e:
                print(f"[!] API Error: {e}")
            except KeyboardInterrupt:
                print("\nExiting application.")
                break

if __name__ == "__main__":
    speak("Classroom assistant online.")
    listen_loop()
