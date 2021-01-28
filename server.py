from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

from constructProfiler import insertProfileOption
from constructProfiler import returnQuestion

from chatBootReplayer import chatBootReplyer

import datetime
import stepcounter

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

@app.route("/chat/question/<user>", methods=["POST"])
def processQuestion(user):
    data = request.get_json()  # status code
    lastWeek = datetime.date.today() - datetime.timedelta(days=7)
  #  with stepcounter.DatabaseConnection(user) as db:
      #  steps = db.get_number_of_steps_after(lastWeek)
    jsonResponse = {}
    jsonResponse["question"] = data["question"]
    jsonResponse["answer"] = chatBootReplyer(chatbot, data["question"], steps)
    return jsonify(jsonResponse), 200

@app.route("/steps/<user>", methods=["POST"])
def steps(user):
    data = request.get_json()
    steps = data["steps"]
    with stepcounter.DatabaseConnection(user) as db:
        db.add_steps(steps, datetime.date.today())
    return "Steps uploaded successfully", 201


#...............
@app.route("/menu/breakfast",  methods=["GET"])
def getBreakFastMenu():

    resultJson = {}
    myLisy = []
    menuJson = {}

    menuJson["menu"] = "I propose some oak with banana and apple. Yes or no?"
    menuJson["points"] = 0
    myLisy.append(menuJson)
    menuJson["menu"] = "I propose some  milk and apple. Yes or no?"
    menuJson["points"] = 2
    myLisy.append(menuJson)
    resultJson["info"] = myLisy


    return resultJson

#..............

# Checks to see if the name of the package is the run as the main package.
if __name__ == "__main__":
    # Runs the Flask application only if the main.py file is being run.
    app.run(
        host="0.0.0.0",
        port=5000,
        )
