import requests
import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = os.getenv("API_URL")

def classify_text(text: str):
    url = API_URL
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text, "parameters": {"candidate_labels": ["travel", "cooking", "sports", "science", "music", "technology", "health", "fashion", "education", "art", "history", "gaming", "movies", "literature", "photography", "fitness", "nature", "politics", "finance", "food", "diy", "animals", "relationships", "culture", "astronomy"]
}}

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=120)
        res.raise_for_status()
        result = res.json()
        if isinstance(result, list) and len(result) > 0:
           
            best_label = result[0]["label"]
            best_score=result[0]["score"]
            return best_label,best_score
        return "inconnu"
    except requests.Timeout:
        return "timeout"
    except requests.RequestException:
        return "erreur_api"
