# Let's make a dice bot
import random
import time
from telegram.ext import Updater,CommandHandler,MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram import Update
import logging
import os

TELEGRAM_TOKEN = "957270511:AAH56Vpe-t8-w-R4essJZ5s7h0uLvrV3PEE"

# states
ROLLDICE = range(1)

PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TELEGRAM_TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hello, I am dice bot and I will roll some tasty dice for you.")

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

def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I am only here to role some tasty dice.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_webhook(listen="0.0.0.0",
                    port=PORT,
                    url_path=TELEGRAM_TOKEN)
updater.bot.set_webhook("https://gemuesebot.herokuapp.com/" + TELEGRAM_TOKEN)
updater.idle()
    
