import gradio as gr
import requests
import json
from pathlib import Path

# TODO RAG, fix ui, admin page

API_URL = "http://127.0.0.1:8000"

def load_personalities():
    """Loads all personality JSON files"""
    personalities = {}
    personalities_dir = Path(__file__).parent / "system_personas"

    for file in personalities_dir.glob("*.json"):
        with open(file) as f:
            data = json.load(f)
            personalities[data["name"]] = data

    return personalities


PERSONALITIES = load_personalities()
print("Loaded personalities:", list(PERSONALITIES.keys()))

def get_greeting(personality: str):
    """Returns personality greeting (default if not specified otherwise)"""
    persona = PERSONALITIES.get(personality, PERSONALITIES["Default Coding Tutor"])
    return persona.get("greeting", "Hello!")

def login(username, password):
    """Login user."""
    response = requests.post(
        f"{API_URL}/auth/login",
        data={
            "username": username,
            "password": password
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    if response.status_code != 200:
        return None, f"Login failed: {response.text}"

    token = response.json()["access_token"]
    return (
        token, 
        "Logged in successfully",
        gr.update(visible=False), # auth_area
        gr.update(visible=True), # app_area
        f"## Hello, {username}", # greeting
    )

def logout():
    """Logs current user out."""
    return (
        None,
        "Logged out",
        gr.update(visible=True), # auth_area
        gr.update(visible=False), # app_area
        "", # greeting set to empty string
    )

def register(username, password):
    """Registers new user."""

    response = requests.post(
        f"{API_URL}/users/register",
        json={
            "username": username,
            "password": password
        },
    )

    if response.status_code != 201:
        return f"Error registering user: {response.text}"
    
    return "Registered successfully. Please Log in using your credentials."

def upload_file(file, token):
    if not token:
        return "Please log in first."
    
    if file is None:
        return "Please upload a file."
    
    with open(file.name, "rb") as f:
        response = requests.post(
            f"{API_URL}/rag/upload",
            files={
                "file": (
                    Path(file.name).name,
                    f,
                    "text/plain"
                )
            },
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
    if response.status_code != 200:
        return f"Upload failed: {response.text}"

    data = response.json()

    return f"""
    ### File indexed successfully

    **Filename:** {data.get("filename")}

    **Chunks indexed:** {data.get("chunk_count") or data.get("chunks_stored")}

    **Preview:**
    ```text
    {data.get("preview", "")}

    """

def ask_rag(question, top_k, token):
    if not token:
        return "Please log in first."

    response = requests.post(
        f"{API_URL}/rag/ask",
        json={
            "question": question,
            "top_k": int(top_k)
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if response.status_code != 200:
        return f"RAG question failed: {response.text}"

    data = response.json()

    sources = data.get("sources", [])

    sources_text = "\n\n".join(
        [f"### Source {i + 1}\n```text\n{source[:1000]}\n```" for i, source in enumerate(sources)]
    )

    return f"""
    Answer

    {data.get("answer", "")}

    Retrieved Sources

    {sources_text if sources_text else "No sources returned."}
    """

def get_history(token):
    if not token:
        return "Not logged in... Please log in first."
    
    response = requests.get(
        f"{API_URL}/history/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if response.status_code != 200:
        return f"Error loading history: {response.text}"
    
    history = response.json()

    if not history:
        return "No history yet."

    output = ""

    for item in history:
        output += f"""
        ### {item.get("action", "Unknown action")}

        **Date:** {item.get("created_at", "")}

        **Input:**
        ```python
        {item.get("input_text", "")}
        AI Response:
        {item.get("ai_response", "")}

        """

    return output

def call_ai(action, personality, code, language, level, token):
    if not token:
        return "Not logged in... Please log in first."

    endpoints = {
        "Explain": "/ai/explain",
        "Review": "/ai/review",
        "Improve": "/ai/improve",
    }

    persona = PERSONALITIES[personality]

    response = requests.post(
        f"{API_URL}{endpoints[action]}",
        json={
            "system_prompt":persona["system_prompt"],
            "code": code,
            "language": language,
            "level": level,
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if response.status_code != 200:
        return f"Error: {response.text}"

    data = response.json()

    return (
        data.get("explanation")
        or data.get("review")
        or data.get("improvement")
        or str(data)
    )

with gr.Blocks(title="AI Code Tutor") as demo:
    token_state = gr.State(value=None)

    gr.Markdown("# AI Code Tutor")
    greeting = gr.Markdown(label="Greeting")

    with gr.Group(visible=True) as auth_area:
        with gr.Tab("Login"):
            username = gr.Textbox(label="Username")
            password = gr.Textbox(label="Password", type="password")
            login_btn = gr.Button("Login")
            login_status = gr.Textbox(label="Status")
        
        with gr.Tab("Register"):
            reg_username = gr.Textbox(label="Username")
            reg_password = gr.Textbox(label="Password", type="password")
            register_btn = gr.Button("Register")
            register_status = gr.Textbox(label="Status")
        
            register_btn.click(
                register,
                inputs=[reg_username, reg_password],
                outputs=[register_status]

            )

    with gr.Group(visible=False) as app_area:

        logout_btn = gr.Button("Logout")

        with gr.Tab("Code Assistant"):

            with gr.Row():
                with gr.Column(scale=1):
                    action = gr.Radio(
                        ["Explain", "Review", "Improve"],
                        label="What do you want to do?",
                        value="Explain"
                    )
                with gr.Column(scale=1):
                    personality_dropdown = gr.Dropdown(
                        choices=list(PERSONALITIES.keys()),
                        value="Default Coding Tutor",
                        label="Select Personality",
                        info="Each personality has a unique system prompt"
                    )

                    gr.Markdown("### Personality Info")
                    personality_info = gr.Markdown("Select a personality to see details")

                    def update_info(personality):
                        persona = PERSONALITIES.get(personality, {})
                        prompt_preview = persona.get("system_prompt", "")[:200] + "..."
                        return f"""
                        **{persona.get('name', 'Unknown')}**

                        *Greeting:* {persona.get('greeting', 'Hello!')}

                        *System Prompt Preview:*
                        > {prompt_preview}
                        """
                    personality_dropdown.change(
                        update_info,
                        inputs=[personality_dropdown],
                        outputs=[personality_info]
                    )
            
            code = gr.Code(label="Paste your code", language="python")
            language = gr.Textbox(label="Language", value="python")
            level = gr.Dropdown(
                ["beginner", "intermediate", "advanced"],
                label="Level",
                value="beginner"
            )

            run_btn = gr.Button("Run")
            output = gr.Markdown(label="AI Response")

            run_btn.click(
                call_ai,
                inputs=[action, personality_dropdown, code, language, level, token_state],
                outputs=output
            )

        with gr.Tab("Rag Assistant"):
            gr.Markdown("## Upload a file and ask questions about it")
            rag_file = gr.File(
            label="Upload .txt, .md, or .py file",
            file_types=[".txt", ".md", ".py"]
            )

            upload_rag_btn = gr.Button("Upload and Index File")
            upload_rag_status = gr.Markdown()
            upload_rag_btn.click(
                upload_file,
                inputs=[rag_file, token_state],
                outputs=upload_rag_status
            )

            gr.Markdown("## Ask a question")

            rag_question = gr.Textbox(
                label="Question",
                placeholder="Example: How does authentication work?"
            )

            rag_top_k = gr.Slider(
                minimum=1,
                maximum=8,
                value=4,
                step=1,
                label="Number of chunks to retrieve"
            )

            ask_rag_btn = gr.Button("Ask RAG")
            rag_answer = gr.Markdown()

            ask_rag_btn.click(
                ask_rag,
                inputs=[rag_question, rag_top_k, token_state],
                outputs=rag_answer
            )


        with gr.Tab("History"):
            refresh_history_btn = gr.Button("Refresh History")
            history_output = gr.Markdown(label="Your History")

            refresh_history_btn.click(
            get_history,
            inputs=[token_state],
            outputs=history_output
            )

        logout_btn.click(
            logout,
            outputs=[token_state, login_status, auth_area, app_area, greeting]
        )

        login_btn.click(
                login,
                inputs=[username, password],
                outputs=[token_state, login_status, auth_area, app_area, greeting]
            )

demo.launch()