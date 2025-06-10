import gradio as gr
import modal
from reportlab.pdfgen import canvas
import tempfile
import os
from gradio_advancetextbox import AdvanceTextbox

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

# Generate PDF from course plan text
def create_pdf(course_text):
    if not course_text or course_text.startswith("⚠️ Error"):
        return None

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        c = canvas.Canvas(tmp.name)
        text_obj = c.beginText(40, 800)
        text_obj.setFont("Helvetica", 12)
        for line in course_text.split("\n"):
            text_obj.textLine(line)
        c.drawText(text_obj)
        c.save()
        return tmp.name

# Build the UI
with gr.Blocks(css=".gr-box { border-radius: 12px; padding: 16px; box-shadow: 0 0 10px #eee; }") as ui:
    gr.Markdown("""
    # 🎓 **CourseCrafter**
    _AI-powered personalized course generator_

    Enter your details and download your learning roadmap as a PDF! ✨
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
            download_btn = gr.Button("📥 Download as PDF")

        with gr.Column(scale=1):
            output_box = gr.Textbox(label="📦 AI-Generated Course Plan", lines=18, interactive=False, show_copy_button=True)
            pdf_file = gr.File(label="📄 Download your PDF", visible=False)

    submit_btn.click(
        fn=generate,
        inputs=[topic, duration, budget, currency, preferred_type],
        outputs=[output_box, pdf_file]
    )

    download_btn.click(
        fn=create_pdf,
        inputs=output_box,
        outputs=pdf_file
    )

# Run app
if __name__ == "__main__":
    ui.launch()