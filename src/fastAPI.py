from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src import translator_utils as Trans

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslationRequest(BaseModel):
    text: str
    output_language: str

@app.post("/translate")
async def translate_text(request: TranslationRequest):
    translated_text = Trans.translate(request.output_language, request.text)
    return {"translated_text": translated_text}

# ... existing code ...
