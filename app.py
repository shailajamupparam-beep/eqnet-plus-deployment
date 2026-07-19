import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Ensure internal pathways resolve correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eqnet_plus.modules.preprocessor import clean_text

app = FastAPI(title="EQNet Plus API")

class TextPayload(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "EQNet Plus Pipeline Active"}

@app.post("/analyze")
def analyze(payload: TextPayload):
    # Handle the empty input requirement gracefully (Returns 422/400 validation error)
    if not payload.text.strip():
        raise HTTPException(status_code=422, detail="Input text cannot be empty")
        
    cleaned = clean_text(payload.text)
    return {
        "original_text": payload.text,
        "cleaned_text": cleaned,
        "status": "Success"
    }
