from app.llm_client import LLMClient

class LLMService:

    @staticmethod
    def greeting(greet: str):
        messages = [
            {
                "role": "system",
                "content": "You are a social assistant."
            },
            {
                "role": "user",
                "content": f"{greet}"
            }
        ]

        return LLMClient.chat(messages)

    @staticmethod
    def explain_code(code: str, language: str, level: str):
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"""
                    Programming Language:
                    {language}

                    User Level:
                    {level}

                    Code:
                    {code}

                    Explain the code clearly.
                """
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
                "content": f"""
                    Programming Language:
                    {language}

                    User Level:
                    {level}

                    Code:
                    {code}

                    Review this code thoroughly.
                """
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
                "content": f"""
                    Programming Language:
                    {language}

                    User Level:
                    {level}

                    Code:
                    {code}

                    Show how you can improve this code block.
                """
            }
        ]

        return LLMClient.chat(messages)