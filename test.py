import pandas as pd
from datetime import datetime
import random

# Lade Tabelle
ledger = pd.read_csv("gemuese.csv",encoding = "utf-8", sep = ";")
def seasonal():
    current_month = datetime.today().month
    seasonal = ledger.query("Month == "+str(current_month)).query("Seasonal == True")["gemuese"].tolist()
    return seasonal

def suggestion():
    suggestion = random.choice(seasonal())
    return suggestion

def show_list():
    seasonal_list = str(seasonal())
    return seasonal_list

def look_up(veggie):
    approval = veggie in seasonal()
    if approval:
        approval = "Mmmmh, Saisonal...( ͡° ͜ʖ ͡°)"
    else:
        approval = "Igitt, importiert ಠ_ಠ"
    return approval