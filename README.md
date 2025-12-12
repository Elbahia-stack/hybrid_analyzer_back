# **Text Analyzer – Fullstack Project**

## 📝 **Description**

**Text Analyzer** est une application web fullstack permettant d’analyser des textes grâce à plusieurs services d’IA :

* 🎯 **Hugging Face** : classification Zero-Shot
* 🤖 **Gemini** : synthèse, enrichissement et analyse avancée
* 🔐 **JWT** : sécurisation complète du backend
* 🗄️ **PostgreSQL** : gestion des utilisateurs et logs

Le projet est composé de :
➡️ Un **backend FastAPI**
➡️ Un **frontend React / Next.js**

---

## ⚙️ **Architecture**

```
Frontend (React / Next.js)
          |
          v
Backend (FastAPI)
          |
          v
Hugging Face API + Gemini API
          |
          v
       PostgreSQL
```

---

# 🚀 **Backend**

## **Endpoints principaux**

* **POST /register** → créer un compte utilisateur
* **POST /login** → connexion + génération d’un JWT
* **POST /analyze** → analyser un texte (JWT requis)

## **Fonctionnalités**

* Classification via **Hugging Face (`facebook/bart-large-mnli`)**
* Synthèse et enrichissement via **Gemini**
* Détection de ton : **positif / neutre / négatif**
* Gestion des erreurs : timeouts, API down, scores faibles
* Système de logs complet

## **Base de données**

Table `users` :

* `id`
* `username`
* `passwordhash`
* `createdat`

---

# 🎨 **Frontend**

## **Pages principales**

* `/auth` → inscription / connexion
* `/analyze` → soumission du texte et affichage des résultats

## **Comportement**

* Stockage du **JWT** côté client
* Envoi automatique du token dans les requêtes protégées
* Affichage propre du résultat :

  * catégorie
  * ton
  * résumé
  * scores Hugging Face
  * réponse Gemini

---

# ⚡ **Installation rapide**

## **Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## **Frontend**

```bash
cd frontend
npm install
npm run dev
```

---

# 📡 **Endpoints Résumés**

### 🔐 Auth

* `POST /register` → `{ username, password }`
* `POST /login` → `{ username, password }`
  **Retour :** `{ token: "<JWT>" }`

### 🧠 Analyse

* `POST /analyze` → `{ text }`
  **Retour :**

```json
{
  "category": "science",
  "tone": "positif",
  "summary": "Résumé généré par Gemini",
  "huggingface_scores": {},
  "gemini_response": {}
}
```

---

