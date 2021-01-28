from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer,ListTrainer
from api.nutritionApi import nutrition_api, contain_vegetables_fruits, countCalories
from constructProfiler import insertProfileOption
from constructProfiler import returnQuestion
import pyttsx3
import os
import keyboard
import speech_recognition as sr

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
trainer.train("chatterbot.corpus.english","chatterbot.corpus.english.conversations")

# Get a response to the input text 'I would like to book a flight.'

#speech
engine=pyttsx3.init()
engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')

def profileMaker():
    index = 0
    while returnQuestion(index) != "":
        q = returnQuestion(index)
        print(q)
        ans = input('You: ')
        insertProfileOption(q,ans)
        index = index + 1

print("Press 1 for text or 2 for speech:")
while True:
    if keyboard.read_key() == "1":
        profileMaker()
        while True:
            print("write anything: ")
            text = input('You: ')
            reply = chatbot.get_response(text)

            aliments, vegetable_fruits_flag = contain_vegetables_fruits(text)
            if vegetable_fruits_flag:
                reply = str(countCalories(aliments)) + " calories"

            elif (text != 'byeta '):
                reply = chatbot.get_response(text)

            if (text == 'bye'):
                print('Bot: Bye')
                engine.say('bye')
                engine.runAndWait()
                break

            print('Bot : ', reply)
            engine.say(reply)
            engine.runAndWait()
        break

    elif keyboard.read_key() == "2":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            while True:
                print("speak anything: ")
                audio = r.listen(source, timeout=20, phrase_time_limit=40)
                try:
                    text = r.recognize_google(audio, language='en-IN')
                except:
                    text = 'Sorry'
                print(text)
                reply = chatbot.get_response(text)

                aliments, vegetable_fruits_flag = contain_vegetables_fruits(text)
                if vegetable_fruits_flag:
                    reply = str(countCalories(aliments)) + " calories"
                    engine.say(reply)
                    engine.runAndWait()

                elif (text != 'bye'):
                    reply = chatbot.get_response(text)

                if (text == 'bye'):
                    print('Bot: Bye')
                    engine.say('bye')
                    engine.runAndWait()
                    break

                print('Bot : ', reply)
                engine.say(reply)
                engine.runAndWait()
        break