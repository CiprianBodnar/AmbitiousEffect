import json
from chatterbot import ChatBot
from chatterbot.trainers import  ListTrainer

file1 = open('qa_Grocery_and_Gourmet_Food.json', 'r')
count = 0
train = []
chatbot = ChatBot('QA')
trainer = ListTrainer(chatbot)

while True:
    line = file1.readline()
    if not line:
        break
    line = line.replace('\'','"')
    try:
        d = json.loads(line)
        train.append(d['question'])
        train.append(d['answer'])
        print()
    except:
        print('wrong')

file1.close()

trainer.train(train)

while True:
    request = input('You: ')
    response = chatbot.get_response(request)
    print(response)