import google.genai as genai
import os
from pydantic import BaseModel, ValidationError

client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

class ResponseJson(BaseModel):
    resume: str
    ton: str
    categorie: str

def analyze_with_gemini(text, category):
    prompt = f"""
Tu es un assistant spécialisé en analyse de texte.
RENVOIE STRICTEMENT UN JSON.

TÂCHES :
1. Résumer le texte en 3 phrases maximum.
2. Détecter le ton : positif, neutre, négatif.
3. Catégorie = "{category}"

FORMAT ATTENDU :
{{
  "resume": "...",
  "ton": "...",
  "categorie": "{category}"
}}

TEXTE :
\"\"\"{text}\"\"\"
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": ResponseJson.model_json_schema()
        }
    )

    try:
        result = ResponseJson.model_validate_json(response.text)
        data = result.model_dump()

        # Convertir le ton en pourcentages proportionnels
        tone = data["ton"].lower()

        # Valeur par défaut pour chaque ton
        base = {"positive": 0, "neutral": 0, "negative": 0}

        if tone == "positif":
            base["positive"] = 70
            base["neutral"] = 20
            base["negative"] = 10
        elif tone == "neutre":
            base["positive"] = 20
            base["neutral"] = 60
            base["negative"] = 20
        elif tone == "négatif":
            base["positive"] = 10
            base["neutral"] = 20
            base["negative"] = 70

        # S'assurer que la somme = 100
        total = sum(base.values())
        for k in base:
            base[k] = round(base[k] * 100 / total)

        data.update(base)

        return data

    except ValidationError:
        return {"resume": "", "ton": "", "categorie": "", "positive": 0, "neutral": 0, "negative": 0}
