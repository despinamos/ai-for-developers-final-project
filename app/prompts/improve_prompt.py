IMPROVE_PROMPT = """
Based on the programming language and the user level, improve the code that follows.
Language: {language}
Level: {level}

The improved code must be:
- Similar in philosophy with the original one
- Do not add extra functionalities unless absolutely necessary
- Explain each change and improvement made thoroughly to the programmer
- Improve the code according to the user's level

Code to improve: {code}
"""