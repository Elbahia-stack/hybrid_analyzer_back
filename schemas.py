from pydantic import BaseModel



class UserRegistre(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
      username: str
      password: str

class AnalyzeRequest(BaseModel):
    text: str      
class AnalyzeResponse(BaseModel):
    input_text: str
    hf_category:str
    hf_score:float
    gemini_analysis: dict