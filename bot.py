import os
import json
import random
from telegram import Update, InputFile, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATA_FILE = 'user_data.json'

# Initialize data storage
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'users': {}, 'total_dug': 0, 'total_sold': 0}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_data()
    
    if str(user.id) not in data['users']:
        data['users'][str(user.id)] = {
            'dug_count': 0,
            'sold_count': 0,
            'pills': 0,
            'username': user.username or user.first_name
        }
        save_data(data)
    
    keyboard = [
        ["Выкопать собаку", "Продать собаку"],
        ["Использовать таблетку", "Статистика"],
        ["Топ копателей", "DIBIL"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Привет я продавец бобожира",
        reply_markup=reply_markup
    )

async def show_dibil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_photo(
            photo=InputFile('DIBIL.jpg'),
            caption="Смотри какой DIBIL!"
        )
    except FileNotFoundError:
        await update.message.reply_text("DIBIL куда-то убежал...")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    data = load_data()
    user_id = str(user.id)
    
    if user_id not in data['users']:
        await start(update, context)
        return
    
    if text == "Выкопать собаку":
        data['users'][user_id]['dug_count'] += 1
        data['total_dug'] += 1
        save_data(data)
        await update.message.reply_text(f"Собака выкопана! 🐕 (Всего: {data['users'][user_id]['dug_count']})")
    
    elif text == "Продать собаку":
        if data['users'][user_id]['dug_count'] > 0:
            data['users'][user_id]['dug_count'] -= 1
            data['users'][user_id]['sold_count'] += 1
            data['total_sold'] += 1
            pills_gained = random.randint(3, 5)
            data['users'][user_id]['pills'] += pills_gained
            save_data(data)
            await update.message.reply_text(
                f"Собака продана! 💰 Получено {pills_gained} таблеток.\n"
                f"Таблеток: {data['users'][user_id]['pills']}\n"
                f"Собак осталось: {data['users'][user_id]['dug_count']}"
            )
        else:
            await update.message.reply_text("У вас нет собак для продажи!")
    
    elif text == "Использовать таблетку":
        if data['users'][user_id]['pills'] > 0:
            data['users'][user_id]['pills'] -= 1
            save_data(data)
            await update.message.reply_text(
                f"Таблетка использована! 💊\n"
                f"Осталось: {data['users'][user_id]['pills']}"
            )
        else:
            await update.message.reply_text("У вас нет таблеток!")
    
    elif text == "Статистика":
        stats_message = (
            f"📊 Ваша статистика:\n"
            f"Выкопали собак: {data['users'][user_id]['dug_count']}\n"
            f"Продано собак: {data['users'][user_id]['sold_count']}\n"
            f"Таблеток: {data['users'][user_id]['pills']}\n"
            f"Всего выкопано: {data['total_dug']}\n"
            f"Всего продано: {data['total_sold']}"
        )
        await update.message.reply_text(stats_message)
    
    elif text == "Топ копателей":
        sorted_diggers = sorted(
            data['users'].values(),
            key=lambda x: x['dug_count'],
            reverse=True
        )[:10]
        
        leaderboard = "🏆 Топ копателей:\n"
        for i, user in enumerate(sorted_diggers, 1):
            leaderboard += f"{i}. {user['username']}: {user['dug_count']} собак\n"
        await update.message.reply_text(leaderboard)
    
    elif text == "DIBIL":
        await show_dibil(update, context)

if __name__ == '__main__':
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not set!")
        exit(1)
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot starting...")
    application.run_polling()
