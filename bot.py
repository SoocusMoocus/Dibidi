import os
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Gets token from environment variables

def start(update, context):
    update.message.reply_text("Hello! I'm your bot!")

if __name__ == '__main__':
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not set in environment!")
        exit(1)
        
    updater = Updater(BOT_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    print("Bot starting...")
    updater.start_polling()
    updater.idle()
