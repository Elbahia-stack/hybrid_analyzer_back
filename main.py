from database import Base, engine,get_db
import models
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import AnalyzeResponse, UserRegistre,AnalyzeRequest, UserLogin
from security import hash_password, verify_password 
from hagging_face import classify_text
from gemini_service import analyze_with_gemini
from auth import create_access_token, verify_token
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

Base.metadata.create_all(bind=engine)



app=FastAPI()
origins = [
     "http://localhost:3000",
    "http://172.26.112.1:3000",
   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
OAuth2_scheme=OAuth2PasswordBearer(tokenUrl="/login")

@app.post("/register")
def regester(user:UserRegistre,db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")
    hashed = hash_password(user.password)

    new_user = models.User(username=user.username, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
   
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Username ou password incorrect")

    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(data: AnalyzeRequest, validate_token=Depends(OAuth2_scheme)):
    verify_token(validate_token)
    text = data.text
    label , score= classify_text(text)
    gemini_result = analyze_with_gemini(text, label)

    return {
        "input_text": text,
        "hf_score": score,
        "hf_category":label,
        "gemini_analysis": gemini_result
    }












