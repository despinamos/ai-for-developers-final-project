EXPLAIN_PROMPT = """
Based on the programming language and the user level, explain the code that follows.
Language: {language}
Level: {level}

While explaining code, make sure to follow these rules:
- ONLY explain the code in a clean and thorough way.
- Take into consideration the user's level. If the user is a beginner give them more details about basics, whereas if they are an advanced programmer, this may not be necessary.
- Explain the code in distinct steps.

Code to explain: {code}
"""