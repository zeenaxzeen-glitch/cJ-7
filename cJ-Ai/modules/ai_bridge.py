# modules/ai_bridge.py

import requests
from modules.filter import clean_text

API_KEY = "your API key"
MODEL_ID = "your AI model"

def ask_external_ai(question):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": question}],
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        # Proper error handling
        if response.status_code == 401:
            return "API Error: Invalid API Key."
        elif response.status_code == 429:
            return "API Error: Rate limit exceeded."
        elif response.status_code >= 500:
            return "Server Error from AI provider."

        response.raise_for_status()
        data = response.json()

        content = data["choices"][0]["message"]["content"]
        return clean_text(content)

    except requests.exceptions.Timeout:
        return "Error: AI request timed out."
    except requests.exceptions.RequestException as e:
        return f"Network Error: {str(e)}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"
