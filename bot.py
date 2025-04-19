from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text("Bot is alive! 🚀")

BOT_TOKEN = os.getenv("8195681425:AAEB_otmC1cT_vw4FW9xKo8VuNqkPt95UBc")  # Get from Render env vars
updater = Updater(BOT_TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.start_polling()
updater.idle()