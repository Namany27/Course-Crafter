import gradio as gr
import modal
import os
import tempfile

# 🔐 Modal auth
os.environ["MODAL_TOKEN_ID"] = "ak-QFZrcOywzIx2cPiTkQr6qp"
os.environ["MODAL_TOKEN_SECRET"] = "as-xd8FYk0A0LED2A74tbwwn0"
modal.config.token_id = os.environ["MODAL_TOKEN_ID"]
modal.config.token_secret = os.environ["MODAL_TOKEN_SECRET"]

# Load remote function
generate_course_plan = modal.Function.from_name("course-crafter", "generate_course_plan")

# AI generation
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
        return result
    except Exception as e:
        print("⚠️ Error:", e)
        return f"⚠️ Error: {str(e)}"

# TXT file creation + HTML auto-download
def create_txt_auto(course_text):
    if not course_text or course_text.startswith("⚠️ Error"):
        return "", ""

    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tmp:
        tmp.write(course_text)
        download_url = f"/file={os.path.basename(tmp.name)}"

    # Auto-download via JavaScript
    html = f"""
    <a id="download" href="{download_url}" download style="display:none;"></a>
    <script>document.getElementById("download").click();</script>
    <p>✅ File is being downloaded...</p>
    """
    return course_text, html

# UI
with gr.Blocks(css=".gr-box { border-radius: 12px; padding: 16px; box-shadow: 0 0 10px #eee; }") as ui:
    gr.Markdown("""
    # 🎓 **CourseCrafter**
    _AI-powered personalized course generator_

    Enter your details and **auto-download** your learning roadmap as a `.txt` file!
    """)

    with gr.Row():
        with gr.Column(scale=1):
            topic = gr.Textbox(label="📘 Topic")
            duration = gr.Textbox(label="⏱️ Duration")
            with gr.Row():
                budget = gr.Textbox(label="💰 Budget")
                currency = gr.Dropdown(["INR", "USD", "EUR", "GBP", "JPY"], value="INR", label="🌍 Currency")
            preferred_type = gr.Dropdown(["video", "text", "interactive", "any"], value="any", label="🎯 Preferred Content Type")
            submit_btn = gr.Button("🚀 Generate & Download")

        with gr.Column(scale=1):
            output_box = gr.Textbox(label="📦 AI Course Plan", lines=18, interactive=False, show_copy_button=True)
            auto_html = gr.HTML()

    submit_btn.click(
        fn=create_txt_auto,
        inputs=[topic, duration, budget, currency, preferred_type],
        outputs=[output_box, auto_html],
        preprocess=False
    )

# Run
if __name__ == "__main__":
    ui.launch(server_name="0.0.0.0", server_port=8080, share=True)