from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer,ListTrainer

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
trainer.train("chatterbot.corpus.english","chatterbot.corpus.english.conversations"1)

# Get a response to the input text 'I would like to book a flight.'

#speech
engine=pyttsx3.init()
engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')


print("Press 1 for text or 2 for speech:")
while True:
    if keyboard.read_key() == "1":
        while True:
            print("write anything: ")
            text = input('You: ')

            reply = chatbot.get_response(text)
            if (text != 'bye'):
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
                if (text != 'bye'):
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