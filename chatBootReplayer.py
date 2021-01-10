from api.nutritionApi import nutrition_api, contain_vegetables_fruits, countCalories


def chatBootReplyer(chatbot, text):
    reply = chatbot.get_response(text)
    aliments, vegetable_fruits_flag = contain_vegetables_fruits(text)
    if vegetable_fruits_flag:
        reply = str(countCalories(aliments)) + " calories"

    elif (text != 'byeta '):
        reply = chatbot.get_response(text)

    if (text == 'bye'):
        print('Bot: Bye')
    return reply