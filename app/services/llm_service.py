"""
LLM Service

Provides: 
  - explain_code(system_prompt, code, language, level) → calls LLM Client chat method
  - explain_code_stream(system_prompt, code, language, level) → calls LLM Client stream chat method
  - review_code(system_prompt, code, language, level) → calls LLM Client chat method
  - review_code_stream(system_prompt, code, language, level) → calls LLM Client stream chat method
  - improve_code(system_prompt, code, language, level) → calls LLM Client chat method
  - improve_code_stream(system_prompt, code, language, level) → calls LLM Client stream chat method
"""

from app.llm_client import LLMClient

from app.prompts.explain_prompt import EXPLAIN_PROMPT
from app.prompts.review_prompt import REVIEW_PROMPT
from app.prompts.improve_prompt import IMPROVE_PROMPT

class LLMService:

    @staticmethod
    def explain_code(system_prompt: str, code: str, language: str, level: str):
        """Explains code given by user with simple llm chat method."""
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
        """Explains code given by user with streaming llm method."""
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
        """Reviews code given by user with simple llm chat method."""
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
        """Reviews code given by user with streaming llm method."""
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
        """Improves code given by user with simple llm chat method."""
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
        """Improves code given by user with streaming llm method."""
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