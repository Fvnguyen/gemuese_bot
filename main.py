# Let's make a bot that suggests seasonal vegetables
import random
import time
from telegram.ext import Updater,CommandHandler,MessageHandler, Filters, RegexHandler, ConversationHandler,  CallbackQueryHandler
from telegram import Update,ParseMode,InlineKeyboardButton, InlineKeyboardMarkup
import logging
import os
import pandas as pd
import veg_processes as vp
from datetime import datetime

# Toke functions
TELEGRAM_TOKEN = os.environ['gemuese_bot']

PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

# start

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hallo Ich bin der Gemüse Souffleur und ich empfehle dir gerne saisonales Gemüse.")
    context.bot.send_message(chat_id=update.message.chat_id, text="Probier mich einfach mal aus, z.B. mit /empfehlung oder /rezept.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#Veggy function
LOOKUP = range(1)
def suggested_veggie(update, context):
    suggestion = vp.suggestion()[0]+' '+str(vp.suggestion()[1])
    context.bot.send_message(chat_id=update.message.chat_id, text=suggestion)

veggie_handler = CommandHandler('empfehlung', suggested_veggie)
dispatcher.add_handler(veggie_handler)

def veggie_list(update, context):
    seasonal_list = ', '.join(vp.seasonal()[1])
    context.bot.send_message(chat_id=update.message.chat_id, text="Diese Gemüsesorten sind diesen Monat in Saison:")
    context.bot.send_message(chat_id=update.message.chat_id, text=seasonal_list)

veggieList_handler = CommandHandler('liste', veggie_list)
dispatcher.add_handler(veggieList_handler)

def start_lookup(update,context):
    update.message.reply_text('Welches Gemüse möchtest Du prüfen? (Antworte "cancel" zum abbrechen)')

    return LOOKUP

def cancel(update,context):
    update.message.reply_text('Tschüss bis zum nächsten mal.')
    return ConversationHandler.END

def veggie_lookup(update, context):
    test_veg = ''.join(update.message.text).strip()
    approval = vp.look_up(test_veg)
    update.message.reply_text(approval)
    return ConversationHandler.END

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('suche', start_lookup)],
        states={LOOKUP: [MessageHandler(Filters.text, veggie_lookup)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )
dispatcher.add_handler(conv_handler)

def recipe(update, context):
    keyboard = [[InlineKeyboardButton("Keine Einschränkung", callback_data='NONE'),
                 InlineKeyboardButton("Vegetarisch", callback_data='vegetarian')],

                [InlineKeyboardButton("Vegan", callback_data='vegan')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Soll ich ein Rezept mit Einschränkungen suchen?', reply_markup=reply_markup)

updater.dispatcher.add_handler(CommandHandler('rezept', recipe))

def diet(update, context):
    query = update.callback_query
    answer = str(update.callback_query.data)
    print(answer)
    if answer == 'NONE':
        recipe = vp.getrecipe()
        title = recipe[0]
        summary = recipe[1]
        query.edit_message_text(text=summary,parse_mode=ParseMode.MARKDOWN)
    elif answer == 'vegetarian':
        recipe = vp.veggyrecipe()
        title = recipe[0]
        summary = recipe[1]
        query.edit_message_text(text=summary,parse_mode=ParseMode.MARKDOWN)
    else:
        recipe = vp.veganrecipe()
        title = recipe[0]
        summary = recipe[1]
        query.edit_message_text(text=summary,parse_mode=ParseMode.MARKDOWN)
        

updater.dispatcher.add_handler(CallbackQueryHandler(diet))


#Unknown command handler
def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Tut mir Leid diesen Befehl kenne ich nicht.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


#Start webhook
updater.start_webhook(listen="0.0.0.0",
                    port=PORT,
                    url_path=TELEGRAM_TOKEN)
updater.bot.set_webhook("https://gemuesebot.herokuapp.com/" + TELEGRAM_TOKEN)
updater.idle()
    
