import requests
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn


def hypernym(word):
    '''extract hypernym of an word'''
    try:
        hyp1 = wn.synsets(word)[0].hypernyms()
        hyp2 = wn.synsets(word)[1].hypernyms()
        return hyp1 + hyp2
    except:
        return None


def has_digit(string):
    ok = 0
    for letter in string:
        if str.isdigit(letter):
            ok = 1
    if ok == 1:
        return True
    return False


def contain_vegetables_fruits(sentence):
    '''search if we have vegetables or fruits in sentence and put "1" if we don't have dimension before then'''
    new_sentence = ''
    foodList = ['apricot', 'bacon', 'beef', 'beer', 'biscuit', 'bread', ' butter', 'cabbage', 'cauliflower',
            'cereal', 'cheese', 'chicken', 'crisps', 'chocolate', 'cucumber', 'egg', 'eggs', 'fish', 'fruit-juice',
            'ham', 'hamburger', 'honey', 'hotdog', 'ice-cream', 'jam', 'lamb', 'lemonade', 'loaf', 'marmalade',
            'meat', 'milk', 'mussel', 'mushroom', 'onion', 'orange-juice', 'pancake', 'pasta', 'pear', 'peas', 'beer'
            'pork', 'pizza', 'potato', 'salad', 'sandwich', 'sausage',  'spaghetti', 'rice', 'toast', 'yoghurt', 'wine']
    flag = False
    count = 0
    for i in word_tokenize(sentence):
        if "vegetable" in str(hypernym(i)) or "fruit" in str(hypernym(i)) or "herb" in str(hypernym(i)) \
                or "vine" in str(hypernym(i)) or i in foodList:
            flag = True
            if count > 0:
                if (has_digit(word_tokenize(sentence)[count-1])) == True:
                    new_sentence = new_sentence + ' ' + word_tokenize(sentence)[count-1] + ' ' + i + ',\n'
                else:
                    new_sentence = new_sentence + ' 1 ' + i + ',\n'
            # if (has_digit(new_sentence.replace(" ", "")[-1:])) == False:
            #     new_sentence = new_sentence + ' ' + "1"
            # new_sentence = new_sentence + ' ' + i + ',\n'
        count = count + 1
    if new_sentence[-2:] == ',\n':
        new_sentence = new_sentence[:-2]
    # print(new_sentence)
    return new_sentence, flag

def hasNumber(inputString):
    if inputString[0].isdigit():
        return 1
    else:
        return 0


def nutrition_api(ingr):
    URL = "https://api.edamam.com/api/nutrition-data?app_id=02ab1cd6&app_key=02fc81c6585763eb1c80a86f5064c253"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'ingr': ingr}

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()

    calories = data['calories']
    if len(data['dietLabels']) > 0:
        fat_level = data['dietLabels'][0]
    else:
        fat_level = "Unknown"

    # print("Calories:%s\nFat Level:%s" % (calories, fat_level))
    return calories

def countCalories(ingredients):
    totalCalories = 0
    for ingr in ingredients.split(',\n'):
        # print(ingr + " "  + str(nutrition_api(ingr)))
        totalCalories = totalCalories + nutrition_api(ingr)
    return totalCalories


# nutrition_api("apple")
# nutrition_api("100g apple")
# nutrition_api("2 apple")
# nutrition_api("300g nuggets")
# nutrition_api("300g nuggets,\n 2 apple")
# nutrition_api('"1 apple",\n "1 banana",\n "1 avocado",\n "1 carrot"')


new_sentence, flag = contain_vegetables_fruits(sentence="how much calories has 100g apple 4 banana 200g avocado carrot  1 sausage  500g meat mama")
# countCalories(new_sentence)
