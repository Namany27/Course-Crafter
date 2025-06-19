import gradio as gr
import modal
import os
import tempfile

# 🔐 Set Modal Token for authentication
os.environ["MODAL_TOKEN_ID"] = "ak-QFZrcOywzIx2cPiTkQr6qp"
os.environ["MODAL_TOKEN_SECRET"] = "as-xd8FYk0A0LED2A74tbwwn0"
modal.config.token_id = os.environ["MODAL_TOKEN_ID"]
modal.config.token_secret = os.environ["MODAL_TOKEN_SECRET"]

# Load the remote Modal function
generate_course_plan = modal.Function.from_name("course-crafter", "generate_course_plan")

# Generate course plan using Modal function
def generate(topic, duration, budget, currency, preferred_type):
    context = {
        "topic": topic,
        "duration": duration,
        "budget": budget,
        "currency": currency,
        "preferred_content_type": preferred_type,
        "user_profile": {
            "learning_style": "visual",
            "time_per_day": "1 hour"
        }
    }

    try:
        result = generate_course_plan.remote(context)
        print("📦 AI Response:\n", result)
        return result, None
    except Exception as e:
        print("⚠️ Error:", e)
        return f"⚠️ Error: {str(e)}", None

# Generate .txt file from course plan
def create_txt(course_text):
    if not course_text or course_text.startswith("⚠️ Error"):
        print("⚠️ No content to create TXT file.")
        return None

    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tmp:
        tmp.write(course_text)
        print("✅ TXT file saved at:", tmp.name)
        return tmp.name

# Build the UI
with gr.Blocks(css=".gr-box { border-radius: 12px; padding: 16px; box-shadow: 0 0 10px #eee; }") as ui:
    gr.Markdown("""
    # 🎓 **CourseCrafter**
    _AI-powered personalized course generator_

    Enter your details and download your learning roadmap as a TXT file! ✨
    """)

    with gr.Row():
        with gr.Column(scale=1):
            topic = gr.Textbox(label="📘 Topic", placeholder="e.g. Python programming")
            duration = gr.Textbox(label="⏱️ Duration", placeholder="e.g. 4 weeks")

            with gr.Row():
                budget = gr.Textbox(label="💰 Budget", placeholder="e.g. 1000")
                currency = gr.Dropdown(
                    choices=["INR", "USD", "EUR", "GBP", "JPY"],
                    value="INR",
                    label="🌍 Currency"
                )

            preferred_type = gr.Dropdown(
                choices=["video", "text", "interactive", "any"],
                value="any",
                label="🎯 Preferred Content Type"
            )

            submit_btn = gr.Button("🚀 Generate Course Plan", variant="primary")
            download_btn = gr.Button("📥 Download as TXT")

        with gr.Column(scale=1):
            output_box = gr.Textbox(label="📦 AI-Generated Course Plan", lines=18, interactive=False, show_copy_button=True)
            txt_file = gr.File(label="📄TXT Generated", visible=false)

    submit_btn.click(
        fn=generate,
        inputs=[topic, duration, budget, currency, preferred_type],
        outputs=[output_box, txt_file]
    )

    download_btn.click(
        fn=create_txt,
        inputs=output_box,
        outputs=txt_file
    )

# Run app
if __name__ == "__main__":
    ui.launch(server_name="0.0.0.0", server_port=8080)