from flask import Flask, render_template, request, jsonify
import openai
import os
import json
from datetime import datetime

app = Flask(__name__)

# ✅ Fix path (use raw string or forward slashes)
BASE_DIR = r"D:\F_EDI\LM_Studio_Local_Server"
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# OpenAI local server
openai.api_base = "http://localhost:1234/v1"
openai.api_key = "not-needed"

# Load system prompt
with open(os.path.join(BASE_DIR, "system_message.txt"), "r", encoding="utf-8") as f:
    BASE_SYSTEM_MESSAGE = f.read().strip()


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    language = data.get("lang", "English")

    # Force bot to reply in chosen language
    system_message = f"{BASE_SYSTEM_MESSAGE}\nAlways reply in {language}."

    response = openai.ChatCompletion.create(
        model="local-model",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
    )

    reply = response.choices[0].message["content"].strip()

    # ✅ Save conversation in daily log
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(LOGS_DIR, f"{date_str}.json")

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_data = json.load(f)
    else:
        log_data = []

    log_data.append({"user": user_message, "bot": reply})

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

    return jsonify({"reply": reply})


@app.route("/dashboard")
def dashboard():
    """Show available daily logs"""
    files = os.listdir(LOGS_DIR)
    logs = sorted([f.replace(".json", "") for f in files if f.endswith(".json")])
    return render_template("dashboard.html", logs=logs)


@app.route("/log/<date>")
def view_log(date):
    """View specific day’s log"""
    log_path = os.path.join(LOGS_DIR, f"{date}.json")
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_data = json.load(f)
    else:
        log_data = []
    return render_template("log_view.html", date=date, log=log_data)


if __name__ == "__main__":
    app.run(debug=True)
