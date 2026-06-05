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
    return token, "Logged in successfully"

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

    with gr.Tab("Login"):
        username = gr.Textbox(label="Username")
        password = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        login_status = gr.Textbox(label="Status")

        login_btn.click(
            login,
            inputs=[username, password],
            outputs=[token_state, login_status]
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


demo.launch()