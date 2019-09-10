import re
import requests
import os
import random
import time
import os
import pandas as pd
from datetime import datetime
from functools import wraps
import pickle
import redis

r = redis.from_url(os.environ.get("REDIS_URL"))

# Function monitoring wrapper
def stat_counter(id,function):
    try:
        filename = 'bot_stats'
        data = pickle.loads(r.get(filename))
        print("loaded stats")
    except:
        print("did not load stats")
        data = []
    entry = [{'id':id,'function':function,'time': datetime.now()}]
    data.append(entry)
    new_data = pickle.dumps(data)
    r.set(filename,new_data)

def stats(func):
    @wraps(func)
    def function_wrapper(update, context,*args, **kwargs):
        stat_counter(update.effective_user.id,func.__name__)
        return func(update, context,*args, **kwargs)
    return function_wrapper


#Calculates the normalized Levenshtein distance of 2 strings
def levenshtein(s1, s2):
    l1 = len(s1)
    l2 = len(s2)
    matrix = [list(range(l1 + 1))] * (l2 + 1)
    for zz in list(range(l2 + 1)):
      matrix[zz] = list(range(zz,zz + l1 + 1))
    for zz in list(range(0,l2)):
      for sz in list(range(0,l1)):
        if s1[sz] == s2[zz]:
          matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
        else:
          matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
    distance = float(matrix[l2][l1])
    result = 1.0-distance/max(l1,l2)
    return result


#Untested matching function
def matching(text,master_list):
    result_list = [levenshtein(text, x) for x in master_list]
    result = max(result_list)
    return result

# recipe functions
def veggyrecipe():
    if r.exists("vgrecipe"):
        recipe = pickle.loads(r.get('vgrecipe'))
    else:
        ingredient_list = ','.join(random.sample(eng_seasonal(),2))
        uniseasonal = []
        for x in eng_unseasonal():
            uniseasonal.append('excluded='+x)
        uniseasonal = '&'.join(uniseasonal)
        appid = '&app_id='+os.environ['EDAMAM_app']
        appapi = '&app_key='+os.environ['EDAMAM_api']
        url = 'https://api.edamam.com/search?q='+ingredient_list+'&'+uniseasonal+appid+appapi+'&health=vegetarian'
        response = requests.request("GET", url)
        recipe = response.json()['hits'][0]['recipe']
        precipe = pickle.dumps(recipe)
        r.set('vgrecipe',precipe,ex = 20)
        link = re.sub('^drupal.{1}','',recipe['url'])
    summary = '['+recipe['label']+']'+'('+link+')'
    return 'Versuche es mal mit diesem leckeren Rezept',summary

def veganrecipe():
    if r.exists("vnrecipe"):
        recipe = pickle.loads(r.get('vnrecipe'))
    else:
        ingredient_list = ','.join(random.sample(eng_seasonal(),2))
        uniseasonal = []
        for x in eng_unseasonal():
            uniseasonal.append('excluded='+x)
        uniseasonal = '&'.join(uniseasonal)
        appid = '&app_id='+os.environ['EDAMAM_app']
        appapi = '&app_key='+os.environ['EDAMAM_api']
        url = 'https://api.edamam.com/search?q='+ingredient_list+'&'+uniseasonal+appid+appapi+'&health=vegan'
        response = requests.request("GET", url)
        recipe = response.json()['hits'][0]['recipe']
        precipe = pickle.dumps(recipe)
        r.set('vnrecipe',precipe,ex = 20)
        link = re.sub('^drupal.{1}','',recipe['url'])
    summary = '['+recipe['label']+']'+'('+link+')'
    return 'Versuche es mal mit diesem leckeren Rezept',summary

def getrecipe():
    if r.exists("recipe"):
        recipe = pickle.loads(r.get('recipe'))
    else:
        ingredient_list = ','.join(random.sample(eng_seasonal(),2))
        uniseasonal = []
        for x in eng_unseasonal():
            uniseasonal.append('excluded='+x)
        uniseasonal = '&'.join(uniseasonal)
        appid = '&app_id='+os.environ['EDAMAM_app']
        appapi = '&app_key='+os.environ['EDAMAM_api']
        url = 'https://api.edamam.com/search?q='+ingredient_list+'&'+uniseasonal+appid+appapi+'&health=vegetarian'
        response = requests.request("GET", url)
        recipe = response.json()['hits'][0]['recipe']
        precipe = pickle.dumps(recipe)
        r.set('recipe',precipe,ex = 20)
        link = re.sub('^drupal.{1}','',recipe['url'])
    summary = '['+recipe['label']+']'+'('+link+')'
    return 'Versuche es mal mit diesem leckeren Rezept',summary

# Gemuesefunktionen

def seasonal():
    ledger = pd.read_csv("gemuese_full.csv",encoding = "utf-8", sep = ",")
    current_month = datetime.today().month
    seasonal = ledger.query("Month == "+str(current_month)).query("Seasonal == True")["gemuese"].tolist()
    return 'Diese Gemüsesorten sind diesen Monat in Saison:',seasonal

def unseasonal():
    ledger = pd.read_csv("gemuese_full.csv",encoding = "utf-8", sep = ",")
    current_month = datetime.today().month
    unseasonal = ledger.query("Month == "+str(current_month)).query("Seasonal == False")["gemuese"].tolist()
    return 'Diese Gemüsesorten sind diesen Monat NICHT in Saison:',unseasonal

def eng_seasonal():
    ledger = pd.read_csv("gemuese_full.csv",encoding = "utf-8", sep = ",")
    current_month = datetime.today().month
    seasonal = ledger.query("Month == "+str(current_month)).query("Seasonal == True")["vegetable"].tolist()
    return seasonal

def eng_unseasonal():
    ledger = pd.read_csv("gemuese_full.csv",encoding = "utf-8", sep = ",")
    current_month = datetime.today().month
    unseasonal = ledger.query("Month == "+str(current_month)).query("Seasonal == False")["vegetable"].tolist()
    return unseasonal

def in_list():
    ledger = pd.read_csv("gemuese_full.csv",encoding = "utf-8", sep = ",")
    master = ledger["gemuese"].tolist()
    return master

def suggestion():
    suggestion = random.sample(seasonal()[1],1)
    return 'Warum kochst Du heute nicht etwas mit:',suggestion

def look_up(veggie):
    season_list = [x.lower() for x in seasonal()[1]]
    master = [x.lower() for x in in_list()]
    approval = matching(veggie.lower(),season_list)
    in_master = matching(veggie.lower(),master)
    if approval > 0.7:
        approval = "Mmmmh, Saisonal...( ͡° ͜ʖ ͡°)"
    else:
        if in_master > 0.7:
            approval = "Igitt, importiert ಠ_ಠ"
        else:
            approval = "Ich kann das Gemüse in meiner Liste nicht finden. Ist es richtig geschrieben und auch ein heimisches Gemüse? Obst, Exotische Gemüse oder Getreide (wie Kartoffeln) sind in meiner Liste nicht enthalten."
    return approval