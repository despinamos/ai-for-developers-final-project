from app.llm_client import LLMClient

from app.prompts.explain_prompt import EXPLAIN_PROMPT
from app.prompts.review_prompt import REVIEW_PROMPT
from app.prompts.improve_prompt import IMPROVE_PROMPT

class LLMService:

    @staticmethod
    def explain_code(code: str, language: str, level: str):
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": EXPLAIN_PROMPT.format(language=language, level=level, code=code)
            }
        ]

        return LLMClient.chat(messages)

    @staticmethod
    def review_code(code: str, language: str, level: str):
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": REVIEW_PROMPT.format(language=language, level=level, code=code)
            }
        ]

        return LLMClient.chat(messages)

    @staticmethod
    def improve_code(code: str, language: str, level: str):
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": IMPROVE_PROMPT.format(language=language, level=level, code=code)
            }
        ]

        return LLMClient.chat(messages)