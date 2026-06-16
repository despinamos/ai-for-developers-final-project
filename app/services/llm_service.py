from app.llm_client import LLMClient

from app.prompts.explain_prompt import EXPLAIN_PROMPT
from app.prompts.review_prompt import REVIEW_PROMPT
from app.prompts.improve_prompt import IMPROVE_PROMPT

class LLMService:

    @staticmethod
    def explain_code(system_prompt: str, code: str, language: str, level: str):
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": EXPLAIN_PROMPT.format(language=language, level=level, code=code)
            }
        ]

        return LLMClient.chat(messages)
    
    @staticmethod
    def explain_code_stream(system_prompt: str, code: str, language: str, level: str):
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": EXPLAIN_PROMPT.format(language=language, level=level, code=code)
            }
        ]

        return LLMClient.stream_chat(messages)

    @staticmethod
    def review_code(system_prompt: str, code: str, language: str, level: str):
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": REVIEW_PROMPT.format(language=language, level=level, code=code)
            }
        ]

        return LLMClient.chat(messages)
    
    @staticmethod
    def review_code_stream(system_prompt: str, code: str, language: str, level: str):
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": REVIEW_PROMPT.format(language=language, level=level, code=code)
            }
        ]

        return LLMClient.stream_chat(messages)

    @staticmethod
    def improve_code(system_prompt: str, code: str, language: str, level: str):
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": IMPROVE_PROMPT.format(language=language, level=level, code=code)
            }
        ]

        return LLMClient.chat(messages)
    
    @staticmethod
    def improve_code_stream(system_prompt: str, code: str, language: str, level: str):
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": IMPROVE_PROMPT.format(language=language, level=level, code=code)
            }
        ]

        return LLMClient.stream_chat(messages)