from api.nutritionApi import nutrition_api, contain_vegetables_fruits, countCalories


def chatBootReplyer(chatbot, text, steps):
    print(text)
    reply = chatbot.get_response(text)
    aliments, vegetable_fruits_flag = contain_vegetables_fruits(text)
    if vegetable_fruits_flag:
        reply = str(countCalories(aliments)) + " calories"

    elif (text != 'byeta '):
        reply = chatbot.get_response(text).text

   # reply += " You've walked %d steps. Have a pizza!" % steps

    if (text == 'bye'):
        reply = 'Bye'
    return reply

