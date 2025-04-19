import os
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATA_FILE = 'user_data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'users': {}, 'total_dug': 0}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_data()
    
    if str(user.id) not in data['users']:
        data['users'][str(user.id)] = {'dug_count': 0, 'username': user.username or user.first_name}
        save_data(data)
    
    keyboard = [["Выкопать собаку"], ["Статистика"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Привет я продавец бобожира",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    data = load_data()
    
    if text == "Выкопать собаку":
        if str(user.id) not in data['users']:
            data['users'][str(user.id)] = {'dug_count': 0, 'username': user.username or user.first_name}
        
        data['users'][str(user.id)]['dug_count'] += 1
        data['total_dug'] += 1
        save_data(data)
        await update.message.reply_text(f"Собака выкопана! 🐕 (Всего: {data['users'][str(user.id)]['dug_count']})")
    
    elif text == "Статистика":
        user_stats = data['users'].get(str(user.id), {'dug_count': 0})
        stats_message = (
            f"🐕 Ваша статистика:\n"
            f"Выкопали собак: {user_stats['dug_count']}\n"
            f"Всего выкопано: {data['total_dug']}"
        )
        await update.message.reply_text(stats_message)
    
    else:
        await update.message.reply_text("Используйте кнопки")

if __name__ == '__main__':
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not set!")
        exit(1)
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot starting...")
    application.run_polling()
