# modules/assistant.py

from modules.memory import search_memory, save_memory
from modules.ai_bridge import ask_external_ai
from modules.filter import speak

def ask_cJ(question):

    answer = search_memory(question)

    if answer:
        print(f"cJ (memory): {answer}")
        speak(answer)
        return answer

    print("cJ: Thinking...")

    learned_answer = ask_external_ai(question)

    if not learned_answer:
        learned_answer = "Sorry, I couldn't process that."

    save_memory(question, learned_answer)

    print(f"cJ: {learned_answer}")
    speak(learned_answer)

    return learned_answer
