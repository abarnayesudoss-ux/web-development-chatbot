from flask import Flask, render_template, request, jsonify
import sqlite3, os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "chatbot.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

def get_response(message):
    msg = message.lower().strip()
    if not msg:
        return "Please enter a question."
    if "how" in msg or "help" in msg or "start" in msg:
        return "Sure! I can guide you step by step. Tell me the exact topic you want to learn about."
    return "For Web Development Assistant, I can provide simple step-by-step guidance, tips, examples, and checklists. Try asking: 'How do I get started?'"

@app.route("/")
def home():
    return render_template("index.html", title="Web Development Assistant")

@app.route("/chat", methods=["POST"])
def chat():
    data=request.get_json(silent=True) or {}
    message=data.get("message","")
    response=get_response(message)
    with sqlite3.connect(DB_PATH) as con:
        con.execute("INSERT INTO chat_history (user_message, bot_response) VALUES (?, ?)", (message,response))
    return jsonify({"response":response})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)), debug=True)
