import os
from telegram.ext import Application, CommandHandler

BOT_TOKEN = os.getenv('BOT_TOKEN')

async def start(update, context):
    await update.message.reply_text("Hello! I'm your bot!")

if __name__ == '__main__':
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not set in environment!")
        exit(1)
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("Bot starting...")
    application.run_polling()
