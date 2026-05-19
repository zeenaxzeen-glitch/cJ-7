# modules/voice.py

import speech_recognition as sr
import time
import modules.filter as filter_module   # 🔥 IMPORT MODULE, NOT VARIABLE

def listen():
    r = sr.Recognizer()

    # 🔥 Wait until speech finishes
    while filter_module.is_speaking:
        time.sleep(0.1)

    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)

        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text

    except sr.WaitTimeoutError:
        print("No input detected.")
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Speech API error: {e}")
    except Exception as e:
        print(f"Mic error: {e}")

    return None
