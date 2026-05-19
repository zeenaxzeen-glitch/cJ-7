import requests

API_KEY = "your API key"
MODEL_ID = "your AI model"

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": MODEL_ID,
    "messages": [{"role": "user", "content": "Hello, are you working?"}],
    "max_tokens": 100
}

try:
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    
    print("Status code:", response.status_code)
    print("Response content:", response.text)

    if response.status_code == 200 and response.text:
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        print("Gemini says:", answer)
    else:
        print("Error: API request did not return valid content")

except Exception as e:
    print("Exception:", e)
