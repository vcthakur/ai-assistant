import requests

def ask_llm(prompt, url, headers):
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    try:
        return result["choices"][0]["message"]["content"]
    except:
        return str(result)