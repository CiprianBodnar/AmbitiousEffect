from pymongo import  MongoClient
connection = MongoClient('localhost', 27017)
 
my_database = connection.AmbitiousEffect
data = my_database.data
questions = ["What is your name?", "What body weight do you have?", "How old are you?","Give me 3 best meals that you like."]

def insertProfileOption(question:str, answer:str):

    entry_data = {
        'question': question,
        'answer': answer
    }

    result = data.insert_one(entry_data)


def returnQuestion(index):
    if index<len(questions):
        return questions[index]
    return ""
