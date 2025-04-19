import os
import json
import random
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATA_FILE = 'user_data.json'

# Possible pill outcomes
PILL_RESULTS = [
    "КОПАЙ",
    "ЛИСИЧКА",
    "ТРУБА",
    "ПАХАЙ",
    "БОБОЖИР",
    "ШАНТРАПА",
    "ГАВНОЖИР"
]

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'users': {}, 'total_dug': 0, 'total_sold': 0, 'pills_used': 0}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_data()
    
    if str(user.id) not in data['users']:
        data['users'][str(user.id)] = {
            'dug_count': 0,
            'sold_count': 0,
            'pills': 0,
            'username': user.username or user.first_name,
            'pills_used': 0
        }
        save_data(data)
    
    help_text = (
        "🐕 Бобожир Бот 🐕\n"
        "Команды:\n"
        "/dig - Выкопать собаку\n"
        "/sell - Продать собаку (3-5 таблеток)\n"
        "/pill - Использовать таблетку (случайный эффект)\n"
        "/stats - Ваша статистика\n"
        "/top - Топ копателей\n"
        "/help - Помощь"
    )
    await update.message.reply_text(help_text)

async def use_pill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_data()
    user_id = str(user.id)
    
    if data['users'][user_id]['pills'] > 0:
        data['users'][user_id]['pills'] -= 1
        data['users'][user_id]['pills_used'] += 1
        data['pills_used'] += 1
        save_data(data)
        
        # Get random result
        result = random.choice(PILL_RESULTS)
        await update.message.reply_text(
            f"💊 Вам выпал: {result}\n"
            f"Осталось таблеток: {data['users'][user_id]['pills']}"
        )
    else:
        await update.message.reply_text("У вас нет таблеток!")

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_data()
    user_id = str(user.id)
    
    stats_message = (
        f"📊 Ваша статистика:\n"
        f"Выкопали собак: {data['users'][user_id]['dug_count']}\n"
        f"Продано собак: {data['users'][user_id]['sold_count']}\n"
        f"Таблеток: {data['users'][user_id]['pills']}\n"
        f"Использовано таблеток: {data['users'][user_id]['pills_used']}\n"
        f"Всего выкопано: {data['total_dug']}\n"
        f"Всего продано: {data['total_sold']}\n"
        f"Всего таблеток использовано: {data['pills_used']}"
    )
    await update.message.reply_text(stats_message)

# [Keep dig_dog(), sell_dog(), and show_top() functions unchanged from previous versions]

if __name__ == '__main__':
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not set!")
        exit(1)
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("dig", dig_dog))
    application.add_handler(CommandHandler("sell", sell_dog))
    application.add_handler(CommandHandler("pill", use_pill))
    application.add_handler(CommandHandler("stats", show_stats))
    application.add_handler(CommandHandler("top", show_top))
    
    print("Bot started with text-only pill system")
    application.run_polling()
