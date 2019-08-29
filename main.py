# Let's make a dice bot
import random
import time
from telegram.ext import Updater,CommandHandler,MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram import Update,ParseMode
import logging
import os
import pandas as pd
import veg_processes as vp
from datetime import datetime

# Gemuesefunktionen
ledger = pd.read_csv("gemuese_de.csv",encoding = "utf-8", sep = ";")
def seasonal():
    current_month = datetime.today().month
    seasonal = ledger.query("Month == "+str(current_month)).query("Seasonal == True")["gemuese"].tolist()
    return seasonal

def in_list():
    master = ledger["gemuese"].tolist()
    return master

def suggestion():
    suggestion = random.choice(seasonal())
    return suggestion

def look_up(veggie):
    season_list = [x.lower() for x in seasonal()]
    approval = vp.matching(veggie.lower(),season_list)
    in_master = veggie.lower() in [x.lower() for x in in_list()]
    if approval > 0.7:
        approval = "Mmmmh, Saisonal...( ͡° ͜ʖ ͡°)"
    else:
        if in_master:
            approval = "Igitt, importiert ಠ_ಠ"
        else:
            approval = "Ich kann das Gemüse in meiner Liste nicht finden. Ist es richtig geschrieben und auch ein heimisches Gemüse? Obst, Exotische Gemüse oder Getreide (wie Kartoffeln) sind in meiner Liste nicht enthalten."
    return approval

# Toke functions
TELEGRAM_TOKEN = "957270511:AAH56Vpe-t8-w-R4essJZ5s7h0uLvrV3PEE"

PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

# start

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hallo Ich bin Gemüse Bot und ich empfehle dir saisonales Gemüse.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#Veggy function
LOOKUP = range(1)
def suggested_veggie(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Warum kochst Du nicht etwas mit "+suggestion())

veggie_handler = CommandHandler('empfehlung', suggested_veggie)
dispatcher.add_handler(veggie_handler)

def veggie_list(update, context):
    seasonal_list = ', '.join(seasonal())
    context.bot.send_message(chat_id=update.message.chat_id, text="Diese Gemüse sind gerade saisonal:")
    context.bot.send_message(chat_id=update.message.chat_id, text=seasonal_list)

veggieList_handler = CommandHandler('liste', veggie_list)
dispatcher.add_handler(veggieList_handler)

def recipe(update, context):
    seasonal_list = ','.join(random.sample(seasonal(),2))
    recipe = vp.getrecipe(seasonal_list)
    title = recipe['title']+':'
    summary = recipe['summary']
    context.bot.send_message(chat_id=update.message.chat_id, text=title)
    context.bot.send_message(chat_id=update.message.chat_id, text=summary, parse_mode=ParseMode.HTML)

recipe_handler = CommandHandler('rezept', recipe)
dispatcher.add_handler(recipe_handler)

def vrecipe(update, context):
    seasonal_list = ','.join(random.sample(seasonal(),2))
    recipe = vp.veggyrecipe(seasonal_list)
    title = recipe['label']
    summary = recipe['url']
    context.bot.send_message(chat_id=update.message.chat_id, text=title)
    context.bot.send_message(chat_id=update.message.chat_id, text=summary)

vrecipe_handler = CommandHandler('vrezept', vrecipe)
dispatcher.add_handler(vrecipe_handler)

def start_lookup(update,context):
    update.message.reply_text('Welches Gemüse oder Obst möchtest Du prüfen? (Antworte "cancel" zum abbrechen)')

    return LOOKUP

def cancel(update,context):
    update.message.reply_text('Tschüss bis zum nächsten mal.')
    return ConversationHandler.END

def veggie_lookup(update, context):
    test_veg = ''.join(update.message.text).strip()
    approval = look_up(test_veg)
    update.message.reply_text(approval)
    return ConversationHandler.END

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('suche', start_lookup)],
        states={LOOKUP: [MessageHandler(Filters.text, veggie_lookup)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )
dispatcher.add_handler(conv_handler)

#Unknown command handler
def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I am only here to role some tasty dice.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


#Start webhook
updater.start_webhook(listen="0.0.0.0",
                    port=PORT,
                    url_path=TELEGRAM_TOKEN)
updater.bot.set_webhook("https://gemuesebot.herokuapp.com/" + TELEGRAM_TOKEN)
updater.idle()
    
