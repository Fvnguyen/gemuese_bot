# Let's make a dice bot
import random
import time
from telegram.ext import Updater,CommandHandler,MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram import Update
import logging
import os
import pandas as pd
from datetime import datetime

# Gemuesefunktionen
ledger = pd.read_csv("gemuese.csv",encoding = "utf-8", sep = ";")
def seasonal():
    current_month = datetime.today().month
    seasonal = ledger.query("Month == "+str(current_month)).query("Seasonal == True")["gemuese"].tolist()
    return seasonal

def suggestion():
    suggestion = random.choice(seasonal())
    return suggestion

def look_up(veggie):
    approval = veggie in seasonal()
    if approval:
        approval = "Mmmmh, Saisonal...( ͡° ͜ʖ ͡°)"
    else:
        approval = "Igitt, importiert ಠ_ಠ"
    return approval

# Toke functions
TELEGRAM_TOKEN = "957270511:AAH56Vpe-t8-w-R4essJZ5s7h0uLvrV3PEE"

PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

# Dice rolling und start
ROLLDICE = range(1)

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hallo Ich bin Gemüse Bot und ich empfehle dir saisonales Gemüse.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def dice_roll(update,context):
    update.message.reply_text('Please enter the number of sides, the die should have')

    return ROLLDICE

def cancel(update,context):
    update.message.reply_text('Bye! I hope we can talk again some day.')
    return ConversationHandler.END

def rolldice(update, context):
    roll = random.randint(1, int(update.message.text))
    update.message.reply_text('You rolled: ' + str(roll))
    return ConversationHandler.END

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('rollDice', dice_roll)],
        states={ROLLDICE: [RegexHandler('^[0-9]+$', rolldice)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )
dispatcher.add_handler(conv_handler)


#Veggy function
def suggested_veggie(update, context):
    suggestion = "Warum kochst Du nicht etwas mit " + suggestion()
    context.bot.send_message(chat_id=update.message.chat_id, text=suggestion)

veggie_handler = CommandHandler('empfehlung', suggested_veggie)
dispatcher.add_handler(veggie_handler)

def veggie_list(update, context):
    seasonal_list = seasonal()
    context.bot.send_message(chat_id=update.message.chat_id, text="Diese Gemüse sind gerade saisonal:")
    context.bot.send_message(chat_id=update.message.chat_id, text=seasonal_list)

veggieList_handler = CommandHandler('liste', veggie_list)
dispatcher.add_handler(veggieList_handler)

def veggie_list(update, context):
    approval = look_up(context.args)
    context.bot.send_message(chat_id=update.message.chat_id, text=seasonal_list)

veggieList_handler = CommandHandler('suche', veggie_list)
dispatcher.add_handler(veggieList_handler)

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
    
