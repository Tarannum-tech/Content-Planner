import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.8-flash")

def generate_ideas(topic: str, count: int = 20):
    prompt = f"""Generate {count} unique content ideas for the topic: "{topic}".
For each idea provide:
- title (catchy)
- description (1 line)
- content_type (Blog/Video/Reel/Post)
- difficulty (Easy/Medium/Hard)

Return ONLY valid JSON in this exact format:
{{"ideas": [{{"title": "...", "description": "...", "content_type": "...", "difficulty": "..."}}]}}
"""
    response = model.generate_content(prompt)
    text = response.text.strip()

    # Clean markdown if any
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    return json.loads(text)
def generate_script(idea_title: str, content_type: str = "Blog", topic: str = ""):
    """Generate a full outline/script for a given idea."""
    prompt = f"""You are an expert content creator. Create a detailed {content_type} outline for:

Title: "{idea_title}"
Niche: "{topic}"

Format the response in markdown with these sections:
- **Hook** (opening line to grab attention)
- **Key Points** (3-5 bullet points)
- **Structure** (step-by-step breakdown)
- **CTA** (call to action at end)

Keep it practical and actionable. No fluff."""

    response = model.generate_content(prompt)
    return response.text