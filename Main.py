import os
import urllib.parse
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Configure Google Gemini
genai.configure(api_key=os.getenv("X-ZITH_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI(
    title="X-ZITH API",
    description="Professional AI API by X-ZITH TECHNOLOGY | Founder: Promise Omiyedun",
    version="2.0.0"
)

# CORS - Allow all origins for public use
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# System Prompt - Optimized for code generation & proper behavior
SYSTEM_PROMPT = """You are X-ZITH AI, a professional AI assistant created by X-ZITH TECHNOLOGY. Founder: Promise Omiyedun.

STRICT RULES:
1. CODE GENERATION: If asked to build an app, website, tool, or generator, return ONLY raw, complete HTML/CSS/JS code starting with <!DOCTYPE html>. Include all CSS and JS inline. NO markdown, NO backticks, NO explanations.
2. IMAGE/VIDEO REQUESTS: If asked to generate images or videos directly, politely reply: "I can't generate images or videos directly, but you can use the Projects feature to build an AI image/video generator app that does this for free."
3. GENERAL CHAT: Answer questions accurately, professionally, and helpfully.
4. IDENTITY: If asked about your origin, always mention X-ZITH TECHNOLOGY and Promise Omiyedun.
5. FORMATTING: Never wrap code in ``` blocks. Return only the raw code when building projects."""

class ChatRequest(BaseModel):
    user_message: str

@app.get("/")
def root():
    return {"status": "online", "api": "X-ZITH API", "version": "2.0.0", "docs": "/docs"}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        prompt = f"{SYSTEM_PROMPT}\n\nUser: {request.user_message}"
        response = model.generate_content(prompt)
        return {"status": "success", "reply": response.text}
    except Exception as e:
        return {"status": "error", "reply": f"API Error: {str(e)}"}

@app.get("/generate-image")
def generate_image(prompt: str):
    try:
        safe_prompt = urllib.parse.quote(prompt)
        # 100% free, no API key required
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&nologo=true&seed={int(os.urandom(2).hex(), 16)}"
        return {"status": "success", "image_url": url}
    except Exception as e:
        return {"status": "error", "reply": f"Image Error: {str(e)}"}
