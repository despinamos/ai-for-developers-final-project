import gradio as gr
import requests
import json
from pathlib import Path

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
        "✅ Logged in successfully",
        gr.update(visible=False), # auth_area
        gr.update(visible=True), # app_area
        f"## 🙂 Hello, {username}", # greeting
        "", # llm question textbox
        "", # llm assistant output
        "", # rag question textbox
        "", # rag assistant output 
        "No file uploaded yet.", # rag upload output
        "Click **Refresh History** to load your history.", # history message
        None # rag_document_id state
    )

def logout():
    """Logs current user out."""
    return (
        None,
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
        return f"❌ Error registering user: {response.text}"
    
    return "✅ Registered successfully. Please Log in using your credentials."

def upload_file(file, token):
    """Upload file for rag."""
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

    return (
        f"""
        ### File indexed successfully

        **Filename:** {data.get("filename")}

        **Chunks indexed:** {data.get("chunk_count") or data.get("chunks_stored")}

        **Preview:**
        ```text
        {data.get("preview", "")}

        """,
        data["document_id"]
    )

def ask_rag(question, top_k, token, document_id):
    """Ask RAG Assistant a question based on the file selected/uploaded."""
    if not token:
        return "Please log in first."

    response = requests.post(
        f"{API_URL}/rag/ask",
        json={
            "question": question,
             "document_id": document_id,
            "top_k": int(top_k),
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

def ask_rag_stream(question, top_k, token, document_id):
    """Ask RAG Assistant a question based on the file selected/uploaded and get streaming response."""
    if not token:
        return "Not logged in... Please log in first."

    response = requests.post(
        f"{API_URL}/rag/ask/stream",
        json={
            "question": question,
             "document_id": document_id,
            "top_k": int(top_k),
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
        stream=True
    )

    if response.status_code != 200:
        return f"RAG streaming question failed: {response.text}"

    output = ""

    for chunk in response.iter_content(
        chunk_size=1024,
        decode_unicode=True
    ):
        if chunk:
            output += chunk
            yield output

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

    html = ""

    for item in history:
        html += f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
            background: #6E6E6E;
        ">
            <h3>{item.get("action", "Unknown action")}</h3>

            <p><b>{item.get("created_at", "")}</b></p>

            <details>
                <summary><b>User Input</b></summary>
                <pre style="white-space: pre-wrap;">{item.get("input_text", "")}</pre>
            </details>

            <details>
                <summary><b>AI Response</b></summary>
                <div style="white-space: pre-wrap;">
                    {item.get("ai_response", "")}
                </div>
            </details>
        </div>

        """

    return html

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
        or data.get("improve")
        or str(data)
    )

def call_ai_stream(action, personality, code, language, level, token):
    if not token:
        return "Not logged in... Please log in first."
    
    endpoints = {
        "Explain": "/ai/explain/stream",
        "Review": "/ai/review/stream",
        "Improve": "/ai/improve/stream",
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
        headers={"Authorization": f"Bearer {token}"},
        stream=True
    )

    if response.status_code != 200:
        yield f"Calling ai streaming failed: {response.text}"
        return

    output = ""

    for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
        if chunk:
            output += chunk
            yield output

with gr.Blocks(title="AI Code Tutor") as demo:
    token_state = gr.State(value=None)
    rag_document_id_state = gr.State(value=None)

    gr.Markdown("# AI Code Tutor")
    greeting = gr.Markdown(label="Greeting")

    with gr.Group(visible=True) as auth_area:

        with gr.Tab("Login"):
            username = gr.Textbox(label="Username")
            password = gr.Textbox(label="Password", type="password")

            with gr.Row():
                with gr.Column(scale=2):
                    pass

                with gr.Column(scale=1):
                    login_btn = gr.Button(
                        "Login",
                        variant="primary",
                        min_width=150
                    )

                with gr.Column(scale=2):
                    pass

            login_status = gr.Markdown()

        with gr.Tab("Register"):
            reg_username = gr.Textbox(label="Username")
            reg_password = gr.Textbox(label="Password", type="password")

            with gr.Row():
                with gr.Column(scale=2):
                    pass

                with gr.Column(scale=1):
                    register_btn = gr.Button(
                        "Register",
                        variant="primary",
                        min_width=150
                    )

                with gr.Column(scale=2):
                    pass

            register_status = gr.Markdown()

            register_btn.click(
                register,
                inputs=[reg_username, reg_password],
                outputs=[register_status]
            )

    with gr.Group(visible=False) as app_area:
        
        # Top bar
        with gr.Row():
            with gr.Column(scale=4):
                gr.Markdown("")
            with gr.Column(scale=1):
                logout_btn = gr.Button(
                    "Logout",
                    variant="secondary",
                    min_width=120
                )

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

            with gr.Accordion("Personality Info", open=False):
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

            code = gr.Code(
                label="Paste your code",
                language="python",
                lines=12
            )

            with gr.Row():
                with gr.Column(scale=1):
                    language = gr.Textbox(
                        label="Language",
                        value="python"
                    )

                with gr.Column(scale=1):
                    level = gr.Dropdown(
                        ["beginner", "intermediate", "advanced"],
                        label="Level",
                        value="beginner"
                    )

            # Centered Run button
            with gr.Row():
                with gr.Column(scale=2):
                    pass

                with gr.Column(scale=1):
                    run_btn = gr.Button(
                        "Run",
                        variant="primary",
                        min_width=160
                    )

                with gr.Column(scale=2):
                    pass

            gr.Markdown("### AI Response")
            output = gr.Markdown()

            run_btn.click(
                call_ai_stream,
                inputs=[
                    action,
                    personality_dropdown,
                    code,
                    language,
                    level,
                    token_state
                ],
                outputs=output
            )

        with gr.Tab("RAG Assistant"):
            gr.Markdown("Upload a file, index it, then ask questions about its content.")

            with gr.Row():
                with gr.Column(scale=2):
                    rag_file = gr.File(
                        label="Upload .txt, .md, or .py file",
                        file_types=[".txt", ".md", ".py"]
                    )

                with gr.Column(scale=1):
                    gr.Markdown("### Upload Status")
                    upload_rag_status = gr.Markdown("No file uploaded yet.")

            # Centered upload button
            with gr.Row():
                with gr.Column(scale=2):
                    pass

                with gr.Column(scale=1):
                    upload_rag_btn = gr.Button(
                        "Upload and Index",
                        variant="primary",
                        min_width=180
                    )

                with gr.Column(scale=2):
                    pass

            upload_rag_btn.click(
                upload_file,
                inputs=[rag_file, token_state],
                outputs=[
                    upload_rag_status,
                    rag_document_id_state
                ]
            )

            gr.Markdown("---")
            gr.Markdown("## Ask a Question")

            rag_question = gr.Textbox(
                label="Question",
                placeholder="Example: How does authentication work?",
                lines=3
            )

            with gr.Row():
                with gr.Column(scale=1):
                    rag_top_k = gr.Slider(
                        minimum=1,
                        maximum=8,
                        value=4,
                        step=1,
                        label="Number of chunks to retrieve"
                    )

                with gr.Column(scale=1):
                    gr.Markdown(
                        "Retrieving more chunks gives the model more context, "
                        "but may include less relevant information."
                    )

            # Centered ask button
            with gr.Row():
                with gr.Column(scale=2):
                    pass

                with gr.Column(scale=1):
                    ask_rag_btn = gr.Button(
                        "Ask RAG",
                        variant="primary",
                        min_width=160
                    )

                with gr.Column(scale=2):
                    pass

            gr.Markdown("### RAG Answer")
            rag_answer = gr.Markdown()

            ask_rag_btn.click(
                ask_rag_stream,
                inputs=[rag_question, rag_top_k, token_state, rag_document_id_state],
                outputs=rag_answer
            )


        with gr.Tab("My History"):
            gr.Markdown("View previous requests you sent to the AI.")

            # Centered refresh button
            with gr.Row():
                with gr.Column(scale=2):
                    pass

                with gr.Column(scale=1):
                    refresh_history_btn = gr.Button(
                        "Refresh History",
                        variant="secondary",
                        min_width=170
                    )

                with gr.Column(scale=2):
                    pass

            gr.Markdown("### Previous Interactions")
            history_output = gr.HTML("Click **Refresh History** to load your history.")

            refresh_history_btn.click(
                get_history,
                inputs=[token_state],
                outputs=history_output
            )

        logout_btn.click(
            logout,
            outputs=[
                token_state, 
                rag_document_id_state, 
                login_status, auth_area, 
                app_area, 
                greeting
            ]
        )

        login_btn.click(
                login,
                inputs=[username, password],
                outputs=[
                    token_state, 
                    login_status, 
                    auth_area, 
                    app_area, 
                    greeting,
                    code,
                    output,
                    rag_question,
                    rag_answer,
                    upload_rag_status,
                    history_output,
                    rag_document_id_state
                ]
            )

demo.launch()