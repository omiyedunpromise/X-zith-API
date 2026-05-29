import os
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("X-ZITH_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI(title="X-ZITH API", description="AI by X-ZITH TECHNOLOGY")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

SYSTEM_PROMPT = "You are X-ZITH AI, created by X-ZITH TECHNOLOGY. Founder: Promise Omiyedun. Always identify as X-ZITH AI when asked. Be helpful, professional, and accurate."

class Request(BaseModel): user_message: str

@app.post("/chat")
def chat(req: Request):
    try:
        res = model.generate_content(f"{SYSTEM_PROMPT}\n\nUser: {req.user_message}")
        return {"status": "ok", "reply": res.text}
    except Exception as e:
        return {"status": "error", "reply": str(e)}
