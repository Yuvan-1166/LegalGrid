from groq import Groq
from app.core.config import settings
import json
from typing import Optional, List, Dict

class GroqClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.client = Groq(api_key=self.api_key)
        self.model = "openai/gpt-oss-120b"
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: Optional[int] = None
    ) -> str:
        """Send chat completion request to GROQ"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    def extract_json(self, text: str) -> dict:
        """Extract JSON from LLM response"""
        try:
            # Try direct parse
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON in text
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
            raise ValueError("No valid JSON found in response")

# Global LLM client
llm_client = GroqClient()
