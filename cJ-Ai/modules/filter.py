# modules/filter.py

import pyttsx3
import re

is_speaking = False

def speak(text):
    global is_speaking
    is_speaking = True

    try:
        engine = pyttsx3.init()   # 🔥 create fresh engine each time
        engine.setProperty('rate', 180)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("Speech error:", e)

    is_speaking = False


def clean_text(text):
    text = re.sub(r"[*_#\[\]`>]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
