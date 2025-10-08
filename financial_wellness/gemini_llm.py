# # backend/gemini_llm.py
# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# def query_gemini(prompt):
#     """
#     Query Gemini via OpenRouter API
#     """
#     url = "https://openrouter.ai/api/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "http://localhost",      # required by OpenRouter
#         "X-Title": "PolicyPal Insurance Advisor" # optional but good practice
#     }
#     payload = {
#     "model": "google/gemini-2.0-flash-exp:free",  # <-- replace with the exact name from /models
#     "messages": [
#         {"role": "system", "content": "You are a helpful insurance advisor."},
#         {"role": "user", "content": prompt}
#     ]
# }


#     response = requests.post(url, headers=headers, json=payload)

#     try:
#         response.raise_for_status()
#     except requests.exceptions.HTTPError as e:
#         print("Error Response:", response.text)
#         raise e

#     data = response.json()
#     return data["choices"][0]["message"]["content"]
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Use Gemini Pro for text generation
def query_gemini(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text