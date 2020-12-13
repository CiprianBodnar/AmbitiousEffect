import requests


def hasNumber(inputString):
    if inputString[0].isdigit():
        return 1
    else:
        return 0


def nutrition_api(ingr):
    URL = "https://api.edamam.com/api/nutrition-data?app_id=02ab1cd6&app_key=02fc81c6585763eb1c80a86f5064c253"

    # defining a params dict for the parameters to be sent to the API
    if hasNumber(ingr) == 0:
        ingr = "1 " + ingr

    PARAMS = {'ingr': ingr}

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()

    calories = data['calories']
    fat_level = data['dietLabels'][0]

    print("Calories:%s\nFat Level:%s" % (calories, fat_level))


# nutrition_api("2 apple")
# nutrition_api("100g apple")
nutrition_api("apple")
