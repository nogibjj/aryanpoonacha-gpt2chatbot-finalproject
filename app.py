# app.py
from flask import Flask, render_template, request
from gpt2_chatbot import GPT2Chatbot

app = Flask(__name__)
chatbot = GPT2Chatbot()

@app.route("/", methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = chatbot.generate_response(prompt)
        return render_template("index.html", title="GPT2 Chatbot", response=response)
    return render_template("index.html", title="GPT2 Chatbot")
