import modal
from modal import Image
import requests
import json
from datetime import datetime
from utils.schedule import generate_schedule
from mcp_actions.send_reminder import send_reminder


# Define the Modal app and image
app = modal.App("course-crafter")
image = Image.debian_slim().pip_install("requests")

# Your deployed Mistral server endpoint
LLM_API_URL = "https://namany7927--course-crafter-mistral-server-fastapi-app.modal.run/v18/chat/completions"

def query_llm(messages):
    payload = {
        "messages": messages
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(LLM_API_URL, json=payload, headers=headers)
    
    print("📨 Sent payload to LLM:", payload)
    print("📥 Received response:", response.text)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"LLM request failed: {response.status_code}, {response.text}")


@app.function(schedule=modal.Period(days=1))
def daily_reminder():
    today = datetime.utcnow().strftime("%Y-%m-%d")

    # You could load this from DB, for now hardcoded:
    schedule = generate_schedule("2025-06-10", 5, "Machine Learning", "you@example.com", "email")

    for item in schedule:
        if item["date"] == today:
            send_reminder.remote(item)

@app.function(image=image)
def generate_course_plan(mcp_context):
    print("✅ Modal function 'generate_course_plan' is running!")

    if isinstance(mcp_context, str):
        mcp_context = json.loads(mcp_context)

    prompt = f"""
        I want to learn {mcp_context['topic']} but unable to find perfect plan and resourse.I only have  {mcp_context['duration']} and my budget is {mcp_context['budget']} {mcp_context['currency']}. I will  Prefer Content type to be {mcp_context['preferred_content_type']}. Can you help me craft a course with perfect resourse and well planed time table and also provide links for the resourse, links are mandatory.
    """
    

    print("🧠 Prompt constructed:", prompt)

    messages = [
        {"role": "system", "content": "You are a helpful assistant that generates learning roadmaps."},
        {"role": "user", "content": prompt}
    ]

    result = query_llm(messages)
    print("📤 Final result:", result)
    return result
