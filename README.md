# 📚 Course Crafter

🎯 *AI-powered Personalized Learning Roadmaps*

[![Demo Video](https://img.shields.io/badge/Watch-Demo-red?logo=youtube)](https://youtu.be/wfe3USWLW20?feature=shared)
[![Live App](https://img.shields.io/badge/Try-Live--Demo-brightgreen?logo=render)](https://course-crafter.onrender.com)
[![GitHub Repo](https://img.shields.io/badge/Source-Code-blue?logo=github)](https://github.com/Namany27/Course-Crafter)

---

## 🚀 Overview

**Course Crafter** is an AI-powered web app that generates **personalized self-learning roadmaps** based on:

- 🧠 Topic of interest  
- ⏱ Duration available  
- 💰 Budget constraints  
- 📦 Preferred content types

Whether you're diving into **Game Development**, **Machine Learning**, or any other topic, Course Crafter will tailor a curated learning path with resource links, schedules, and more — all based on your preferences.

---

## ✨ Features

- ⚡ Instant roadmap generation via **LLaMA 3**
- 🌐 Clean **Gradio-based UI**
- 🧩 Smart prompt engineering
- 📄 Exportable learning plans as **.txt** or **.pdf**
- ⏳ Personalized scheduling (via `.ics` calendar support)
- 🔔 Optional daily notifications via Twilio/Email *(Coming Soon)*
- 🔎 Dynamic resource fetching via YouTube, Reddit, arXiv *(WIP)*

---

## 📽 Demo

- 🔗 **Live App**: [course-crafter.onrender.com](https://course-crafter.onrender.com)  
- 📺 **Video Walkthrough**: [Watch Demo Video](https://youtu.be/wfe3USWLW20?feature=shared)

---

## 🛠 Tech Stack

- [Modal](https://modal.com/) — for serverless AI infrastructure  
- [Gradio](https://gradio.app/) — for frontend UI  
- [LLaMA 3](https://llama.meta.com/) — for powerful LLM generation  
- Python, FastAPI, FPDF, ICS, MCP (Model Context Protocol)

---

## 🧪 How It Works

1. User enters a topic, duration, budget, and preferred content types.
2. Request is sent to a Modal-deployed LLaMA 3 model via FastAPI.
3. AI generates a structured course plan with curated links and timelines.
4. Output is displayed via Gradio and downloadable/exportable.

---

## 🖥 Local Setup

```bash
git clone https://github.com/Namany27/Course-Crafter.git
cd Course-Crafter
pip install -r requirements.txt
python gradio_ui.py