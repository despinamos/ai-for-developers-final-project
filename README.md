The final project for AI for Developers Seminar (February 2026-May 2026). Project was developed in May-June 2026.

# Project Overview

AI Coding Tutor application developed with FastAPI. Users register on the app and may use it to have code they want explained, reviewed or improved, based on their choice.
The application also offers a Rag architecture where the user can upload files (.py, .md or .txt) and ask questions about them.
The user is able to view her/is history of interactions he has had on the app.
The application supports JWT Authentication.

# Tech Stack:

Python version 3.13.5 (Minimum version Python 3.11+)

# Installation:

## Clone Repository
Run in terminal
```
git clone https://github.com/despinamos/ai-for-developers-final-project.git
```

## Create Virtual Environment (venv) and activate it

```
python -m venv venv
```
```
venv\Scripts\activate
```

## Install requirements.txt

```
pip install -r requirements.txt
```

# Instructions for Deployment:

## Run backend
Run in terminal (runs on port 8000)
```
uvicorn app.main:app --reload
```

## Run UI
Open a second terminal and run UI on default port 7860
```
python gradio_app.py
```

# OpenAPI documentation
To view the full API documentation, visit:
```
http://127.0.0.1:8000/docs#/
```

# API Endpoints

## Login

```
POST /auth/login → validate credentials, return JWT access token.
```

## Users
```
POST /users/register → create a new user
GET  /users/me       → current user info (auth required)
GET  /users/admin    → admin-only endpoint
```

## AI
```
POST /ai/explain → explain user's code
POST /ai/review → review user's code
POST /ai/improve → improve user's code

POST /ai/explain/stream → explain user's code with stream response
POST /ai/review/stream → review user's code with stream response
POST /ai/improve/stream → improve user's code with stream response
```

## RAG Assistant

```
POST /rag/upload → upload new document
GET /rag/documents → get documents uploaded by current user
POST /rag/ask → ask a question to Rag Assistant and return simple answer
POST /rag/ask/stream → ask a question to Rag Assistant and return streaming response
```

## History
```
GET /history/ → return user's records
```

# GenAI Logic

The application offers basic GenAI logic in the form of an AI Coding Tutor. The application has two main functions:
- User inputs code and chooses to have the code either `explained`, `reviewed` or `improved` by the LLM.
- User uploads a file (`.txt`, `.py` or `.md`) which is then split in indexed chunks. S\he can then ask questions about the selected file to RAG Assistant, which only answers based on context from this document.