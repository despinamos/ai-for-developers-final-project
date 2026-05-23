REVIEW_PROMPT = """
Based on the programming language and the user level, review the code that follows.
Language: {language}
Level: {level}

While reviewing code, make sure to follow these rules:
- ONLY review the code block
- Return the review in a clean and thorough way.
- Take into consideration the user's level. If the user is a beginner give them more details about basics, whereas if they are an advanced programmer, this may not be necessary.
- Review the code step by step
- If the code has errors, explain how the user can fix them according to their level (for example, don't propose something too complicated for a beginner)


Code to review: {code}
"""