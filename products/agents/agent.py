from functools import partial
import google.generativeai as genai
import logging
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class QueryException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Agent:
    def __init__(self, prompt_file_name: str):
        with open(f"products/agents/prompts/{prompt_file_name}.txt", "r") as f:
            self.base = f.read()
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.logger = logging.getLogger("agent")

    def query(self, **kwargs) -> str:
        response = self.model.generate_content(self.base.format(**kwargs)).candidates[0]
        if not hasattr(response, 'content'):
            raise QueryException('LLM response does not have content')
        text = response.content.parts[0].text
        self.logger.debug(f"Query response: {text}")
        return text
