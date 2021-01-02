from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

from constructProfiler import insertProfileOption
from constructProfiler import returnQuestion

from chatBootReplayer import chatBootReplyer

chatbot = ChatBot(
    'Terminal',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///database.db'
)

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english", "chatterbot.corpus.english.conversations")

# Import the Flask module that has been installed.
from flask import Flask, jsonify, request

# Creating a new "app" by using the Flask constructor. Passes __name__ as a parameter.
app = Flask(__name__)
index = 0


@app.route("/profile", methods=["GET"])
def profileQuestionGenerator():
    global index
    jsonResponse = {}
    q = returnQuestion(index)
    jsonResponse["index"] = index
    jsonResponse["question"] = q
    jsonResponse["response"] = ""
    index = index + 1
    return jsonify(jsonResponse)


@app.route("/profile/answer", methods=["POST"])
def profileQuestionAnswer():
    data = request.get_json()  # status code
    insertProfileOption(data["question"]), data["response"]
    return jsonify(data), 200

@app.route("/chat/question", methods=["POST"])
def processQuestion():
    data = request.get_json()  # status code
    jsonResponse = {}
    jsonResponse["question"] = data["question"]
    jsonResponse["answer"] = chatBootReplyer(chatbot, data["question"])
    return jsonify(jsonResponse), 200

# Checks to see if the name of the package is the run as the main package.
if __name__ == "__main__":
    # Runs the Flask application only if the main.py file is being run.
    app.run()
