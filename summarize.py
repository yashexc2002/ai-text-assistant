# summarize.py

import requests
import gradio as gr

# Ollama API endpoint (direct)
OLLAMA_URL = "http://localhost:11434/api/generate"

# Category options and their corresponding prompt templates
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
    "💬 SQL & API - SQL Generator": "Generate an SQL query from this description:\n\n{text}",
    "📰 News - News Fetch + Summarize": "Summarize this news article into 3 bullet points:\n\n{text}",
    "💡 Edu/Research - Research Paper Summarizer": "Summarize this research paper clearly:\n\n{text}",
    "📦 Recommender - Product Recommendation": "Recommend products based on the following:\n\n{text}"
}

# List of categories for Gradio dropdown
CATEGORIES = list(CATEGORY_PROMPTS.keys())

def summarize_text(text, category):
    try:
        prompt_template = CATEGORY_PROMPTS.get(category, "Summarize:\n\n{text}")
        final_prompt = prompt_template.replace("{text}", text)

        payload = {
            "model": "gemma3:4b",  # Replace with another model if needed
            "prompt": final_prompt,
            "stream": False
        }

        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "No summary returned.")
    except requests.RequestException as e:
        return f"Request failed: {e}"

# Gradio interface
interface = gr.Interface(
    fn=summarize_text,
    inputs=[
        gr.Textbox(lines=10, placeholder="Enter your input text here", label="Input Text"),
        gr.Dropdown(choices=CATEGORIES, label="Choose a Category", value="📝 Content - Blog Writing")
    ],
    outputs=gr.Textbox(label="Result"),
    title="AI-Powered Text Assistant",
    description="Select a category and input your text. The assistant will respond accordingly.",
    examples=[
        ["I want to write a blog on how AI is changing the world.", "📝 Content - Blog Writing"],
        ["SELECT * FROM orders WHERE date > '2024-01-01';", "💬 SQL & API - SQL Generator"]
    ]
)

if __name__ == "__main__":
    interface.launch()
