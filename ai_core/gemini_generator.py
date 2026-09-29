import os
import google.generativeai as genai


class GeminiDocumentGenerator:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def generate_document(self, document_type, parties, terms, dates):
        prompt = f"""
        Create a professional legal document.

        Document Type: {document_type}
        Parties: {parties}
        Terms: {terms}
        Effective Dates: {dates}

        Generate a clear, structured and professional document.
        """

        response = self.model.generate_content(prompt)

        return response.text
