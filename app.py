from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests

app = FastAPI()
OLLAMA_URL = "http://localhost:11434/api/generate"

# Prompt templates
CATEGORY_PROMPTS = {
    "📝 Content - Blog Writing": "Write a blog summary:\n\n{text}",
    "📝 Content - Email Writing": "Draft an email based on the following:\n\n{text}",
    "🤖 NLP Tools - Grammar Checker": "Check grammar and suggest corrections:\n\n{text}",
    "🤖 NLP Tools - Sentiment Analysis": "Analyze the sentiment of this text:\n\n{text}",
    "👩‍⚕️ Health - Symptom Analyzer": "Analyze the symptoms and give possible conditions:\n\n{text}",
    "💼 Career - Resume Generator": "Create a resume summary based on:\n\n{text}",
    "📄 PDF - Meeting Minutes": "Summarize this document into meeting minutes:\n\n{text}",
    "📊 Analytics - Financial Report Analyzer": "Summarize and analyze this financial report:\n\n{text}",
    "🔎 Code - Debugger": "Find and explain bugs in the following code:\n\n{text}",
    "💬 SQL & API - SQL Generator": "Generate SQL query from:\n\n{text}",
    "📰 News - News Fetch + Summarize": "Summarize this news article in bullet points:\n\n{text}",
    "💡 Edu/Research - Research Paper Summarizer": "Summarize this academic paper:\n\n{text}",
    "📦 Recommender - Product Recommendation": "Suggest products based on the following description:\n\n{text}"
}

@app.post("/summarize/")
def summarize_text(text: str, category: str = "📝 Content - Blog Writing"):
    template = CATEGORY_PROMPTS.get(category, "Summarize:\n\n{text}")
    prompt = template.replace("{text}", text)

    payload = {
        "model": "gemma3:4b",  # ✅ Use a valid Ollama model
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return {"summary": response.json().get("response", "No summary generated.")}
    except requests.RequestException as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/health")
def health_check():
    return {"status": "ok"}
