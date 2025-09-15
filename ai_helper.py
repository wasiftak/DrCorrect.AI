import google.generativeai as genai
import json
import re
import os

CACHE_FILE = 'ai_cache.json'

class AIHelper:
    """
    A helper class to manage all interactions with the Gemini API.
    """
    def __init__(self, api_key):
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
            self.cache = self._load_cache()
            print("Gemini model initialized successfully with 'gemini-1.5-flash-latest'.")
        except Exception as e:
            self.model = None
            self.cache = {}
            print(f"Error initializing Gemini: {e}")

    def _load_cache(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f: return json.load(f)
        return {}

    def _save_cache(self):
        with open(CACHE_FILE, 'w') as f: json.dump(self.cache, f, indent=2)

    def is_ready(self):
        return self.model is not None

    def analyze_text(self, selected_text):
        """Sends selected text to Gemini to be defined and distinguished."""
        if selected_text in self.cache:
            return self.cache[selected_text]

        if not self.is_ready():
            return "AI not available."

        print(f"Cache miss. Fetching analysis for '{selected_text}' from Gemini...")
        
        # --- FINAL PROMPT REFINEMENT ---
        # This prompt asks for a fluid, single-paragraph response.
        system_prompt = "You are an expert medical terminology assistant. The user will provide text containing medical terms. Your task is to respond with a single, concise paragraph that first defines each key term, and then explains how they are related or different."
        user_prompt = f"Please analyze the key medical terms in the following text: \"{selected_text}\""
        
        try:
            generation_config = genai.GenerationConfig(
                max_output_tokens=150,
                temperature=0.2 
            )

            response = self.model.generate_content(
                [system_prompt, user_prompt],
                generation_config=generation_config
            )

            result_text = response.text.strip()
            self.cache[selected_text] = result_text
            self._save_cache()
            return result_text
        except Exception as e:
            print(f"An API error occurred: {e}")
            return f"Error analyzing text: {e}"