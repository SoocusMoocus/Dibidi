import os
import json
import random
from telegram import Update, InputFile
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATA_FILE = 'user_data.json'
PILL_IMAGE = 'DIBIL.png'  # Changed to PNG

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'users': {}, 'total_dug': 0, 'total_sold': 0}

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
            'username': user.username or user.first_name
        }
        save_data(data)
    
    help_text = (
        "🐕 Бобожир Бот 🐕\n"
        "Команды:\n"
        "/dig - Выкопать собаку\n"
        "/sell - Продать собаку (3-5 таблеток)\n"
        "/pill - Использовать таблетку (покажет DIBIL)\n"
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
        save_data(data)
        
        # PNG version with enhanced error handling
        try:
            if os.path.exists(PILL_IMAGE):
                await update.message.reply_photo(
                    photo=InputFile(PILL_IMAGE),
                    caption="💊 Таблетка активирована! Вот DIBIL:"
                )
            else:
                await update.message.reply_text(
                    f"Ошибка: {PILL_IMAGE} не найден в:\n{os.listdir()}"
                )
        except Exception as e:
            await update.message.reply_text(f"Ошибка отправки изображения: {str(e)}")
        
        await update.message.reply_text(
            f"Осталось таблеток: {data['users'][user_id]['pills']}"
        )
    else:
        await update.message.reply_text("У вас нет таблеток!")

# [Keep all other functions exactly the same as in previous version: dig_dog, sell_dog, show_stats, show_top]

if __name__ == '__main__':
    # PNG-specific verification
    print("Starting bot... Checking for PNG file:")
    if not os.path.exists(PILL_IMAGE):
        print(f"⚠️ Warning: {PILL_IMAGE} not found! Current files:")
        print(os.listdir())
    else:
        print(f"✅ {PILL_IMAGE} found! Size: {os.path.getsize(PILL_IMAGE)/1024:.1f} KB")

    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not set!")
        exit(1)
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # [Keep all handler registrations the same]
    
    application.run_polling()
