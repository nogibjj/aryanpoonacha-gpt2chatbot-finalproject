from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from gpt2_chatbot import GPT2Chatbot

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
db = SQLAlchemy(app)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String(500), nullable=False)
    response = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

chatbot = GPT2Chatbot()

@app.route("/", methods=['GET', 'POST'])
def chat():
    conversations = Conversation.query.order_by(Conversation.timestamp.desc()).limit(30).all()
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = chatbot.generate_response(prompt)
        # Save the conversation to the database
        conversation = Conversation(prompt=prompt, response=response)
        try:
            db.session.add(conversation)
            db.session.commit()
            # Add the new conversation to the list of recent conversations
            conversations.insert(0, conversation)
            # Ensure that the list of conversations doesn't exceed 30
            conversations = conversations[:30]
        except Exception as e:
            print("Failed to add conversation to database.")
            print(e)
            db.session.rollback()
        return render_template("index.html", title="GPT2 Chatbot", response=response, conversations=conversations)
    return render_template("index.html", title="GPT2 Chatbot", conversations=conversations)

with app.app_context():
    try:
        db.create_all()  # Create the database table
    except Exception as e:
        print("Failed to create database table.")
        print(e)

if __name__ == "__main__":
    app.run(debug=True)
