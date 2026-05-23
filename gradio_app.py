import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000"


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

def call_ai(action, code, language, level, token):
    if not token:
        return "Not logged in... Please log in first."

    endpoints = {
        "Explain": "/ai/explain",
        "Review": "/ai/review",
        "Improve": "/ai/improve",
    }

    response = requests.post(
        f"{API_URL}{endpoints[action]}",
        json={
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
        action = gr.Radio(
            ["Explain", "Review", "Improve"],
            label="What do you want to do?",
            value="Explain"
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
            inputs=[action, code, language, level, token_state],
            outputs=output
        )


demo.launch()