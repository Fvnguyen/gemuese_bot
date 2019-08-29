# import pandas as pd
# from datetime import datetime
# import random
import requests

# Lade Tabelle
# ledger = pd.read_csv("gemuese.csv",encoding = "utf-8", sep = ";")
# def seasonal():
#     current_month = datetime.today().month
#     seasonal = ledger.query("Month == "+str(current_month)).query("Seasonal == True")["gemuese"].tolist()
#     return seasonal

# def suggestion():
#     suggestion = random.choice(seasonal())
#     return suggestion

# def show_list():
#     seasonal_list = str(seasonal())
#     return seasonal_list

# def look_up(veggie):
#     approval = veggie in seasonal()
#     if approval:
#         approval = "Mmmmh, Saisonal...( ͡° ͜ʖ ͡°)"
#     else:
#         approval = "Igitt, importiert ಠ_ಠ"
#     return approval
api = "c4580f32420d491aa7cc0da3e49c5019 "

import requests

def getRecipeByIngredients(ingredients):
    payload = {
        'fillIngredients': False,
        'ingredients': ingredients,
        'limitLicense': False,
        'number': 5,
        'ranking': 1
    }

    api_key = api

    endpoint = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients"


    headers={
        "X-Mashape-Key": api_key,
        "X-Mashape-Host": "mashape host"
    }

    r = requests.get(endpoint, params=payload, headers=headers)
    results = r.json()
    title = results[0]['title']
    print(title)

getRecipeByIngredients('apple')