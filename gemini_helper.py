import google.generativeai as genai

class GeminiHelper:
    """
    A helper class to manage all interactions with the Gemini API.
    """
    def __init__(self, api_key):
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            print("Gemini model initialized successfully.")
        except Exception as e:
            self.model = None
            print(f"Error initializing Gemini: {e}")

    def is_ready(self):
        """Checks if the model was initialized successfully."""
        return self.model is not None