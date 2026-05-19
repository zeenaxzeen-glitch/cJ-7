# modules/memory.py

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(BASE_DIR, "..", "memory", "memory.json")

def load_memory():
    try:
        if not os.path.exists(MEMORY_FILE):
            return {}

        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_memory(question, answer):
    memory = load_memory()
    memory[question.lower()] = answer

    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4, ensure_ascii=False)

def search_memory(question):
    memory = load_memory()
    return memory.get(question.lower())
