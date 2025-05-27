from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

# Predefined texts
region_texts = {
    "north": """–Північна Америка–

• 🇨🇦Канада - 🇬🇱Ґренландія
• 🇺🇸США - 🇦🇸Американське Самоа - 🇵🇷Пуерто-Рико
• 🇺🇸США - 🇧🇸Багамські острови
• 🇲🇽Мексика - 🇨🇷Коста-Рика 
• 🇭🇹Гаїті - 🇩🇴Домініканська Республіка""",

    "south": """–Південна Америка–

• 🇻🇪Венесуела - 🇨🇴Колумбія
• 🇵🇪Перу - 🇧🇴Болівія 
• 🇧🇷Бразилія - 🇺🇾Уругвай
  🇧🇷Бразилія - 🇵🇹Португалія
• 🇨🇱Чилі - 🇦🇷Аргентина""",

    "asia": """–Азія–

• 🇹🇷Туреччина - 🇦🇿Азербайджан
• 🇵🇸Палестина - 🇯🇴Йорданія 
• 🇰🇼Кувейт - 🇧🇭Бахрейн - 🇶🇦Катар
• 🇨🇳Китай - 🇭🇰Гонконг - 🇹🇼Тайвань
• 🇮🇳Індія - 🇳🇵Непал
  🇮🇳Індія - 🇲🇻Мальдіви 
  🇮🇳Індія - 🇧🇹Бутан 
• 🇵🇰Пакистан - 🇧🇩Бангладеш
• 🇲🇲М'янма - 🇹🇭Таїланд - 🇰🇭Камбоджа - 🇱🇦Лаос - 🇻🇳В'єтнам
• 🇲🇾Малайзія - 🇮🇩Індонезія
• 🇯🇵Японія - 🇹🇱Східний Тимор 
• 🇰🇷Південна Корея - 🇸🇬Сінгапур - 🇧🇳Бруней""",

    "europe": """–Європа–

• 🇬🇧Велика Британія - 🇮🇪Ірландія
  🇬🇧Велика Британія - 🇬🇬Гернсі
  🇬🇧Велика Британія - 🇬🇮Гібралтар
  🇬🇧Велика Британія - 🇲🇹 Мальта
• 🇪🇸Іспанія - 🇦🇩Андорра
  🇪🇸Іспанія - 🇮🇨Канарські острови
• 🇫🇷Франція - 🇲🇨Монако
  🇫🇷Франція - 🇱🇺Люксембург
• 🇳🇱Нідерланди - 🇧🇪Бельгія - 🇱🇺 Люксембург
• 🇬🇱Ґренландія - 🇩🇰Данія
• 🇩🇪Німеччина - 🇦🇹Австрія
  🇩🇪Німеччина - 🇱🇮Ліхтенштейн
• 🇦🇽Аландські острови - 🇸🇪Швеція
  🇦🇽Аландські острови - 🇫🇮 Фінляндія
• 🇪🇪Естонія - 🇱🇻Латвія - 🇱🇹Литва 
• 🇷🇴Румунія - 🇲🇩Молдова 
• 🇨🇿Чехія - 🇸🇰Словаччина
• 🇮🇹Італія - 🇸🇲Сан-Марино 
  🇮🇹Італія - 🇲🇹Мальта 
• 🇷🇸Сербія - 🇧🇦Боснія і Герцеговина
• 🇦🇱Албанія - 🇽🇰Косово
🇺🇦 Україна – 🇵🇱 Польща
• 🇬🇷Греція - 🇨🇾Кіпр"""
}

rules_text = """📜 **Правила**:

**1. Загальні умови**
1.1 ... (текст скорочено для прикладу)

**2. Вимоги до виконавця і пісні**
2.1 ...

**3. Система автофіналу**
3.1 ...
"""

# Menus
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ Лист обміну", callback_data="menu_exchange")],
        [InlineKeyboardButton("📜 Правила", callback_data="rules")]
    ])

def exchange_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌎 Північна Америка", callback_data="region_north")],
        [InlineKeyboardButton("🌍 Південна Америка", callback_data="region_south")],
        [InlineKeyboardButton("🌏 Азія та Океанія", callback_data="region_asia")],
        [InlineKeyboardButton("🌍 Європа", callback_data="region_europe")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ])

# Text Commands
async def cmd_north(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(region_texts["north"])

async def cmd_south(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(region_texts["south"])

async def cmd_europe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(region_texts["europe"])

async def cmd_asia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(region_texts["asia"])

async def cmd_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(rules_text)

async def cmd_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📋 *Список доступних команд:*\n\n"
        "🔹 /north — Показати обміни для Північної Америки\n"
        "🔹 /south — Показати обміни для Південної Америки\n"
        "🔹 /europe — Показати обміни для Європи\n"
        "🔹 /asia — Показати обміни для Азії та Океанії\n"
        "🔹 /rules — Показати правила конкурсу\n"
        "🔹 /commands — Показати цей список команд\n"
    )
    await update.message.reply_markdown(text)

# Start Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Лист обміну"], ["Правила"], ["Команди"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привіт! Обери опцію:", reply_markup=reply_markup)

# Button Callback Handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    match query.data:
        case "menu_exchange":
            await query.edit_message_text("Оберіть регіон:", reply_markup=exchange_menu())
        case "region_north":
            await query.edit_message_text(region_texts["north"], reply_markup=exchange_menu())
        case "region_south":
            await query.edit_message_text(region_texts["south"], reply_markup=exchange_menu())
        case "region_asia":
            await query.edit_message_text(region_texts["asia"], reply_markup=exchange_menu())
        case "region_europe":
            await query.edit_message_text(region_texts["europe"], reply_markup=exchange_menu())
        case "rules":
            await query.edit_message_text(rules_text, reply_markup=main_menu())
        case "back":
            await query.edit_message_text("Повернулись в головне меню:", reply_markup=main_menu())

# Text Listener for Reply Keyboard
async def text_listener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if text == "команди":
        await cmd_commands(update, context)
    elif text == "правила":
        await cmd_rules(update, context)
    elif text == "лист обміну":
        await update.message.reply_text("Оберіть регіон:", reply_markup=exchange_menu())
    else:
        await update.message.reply_text("Невідома команда. Спробуйте ще раз.")

# Run
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    handlers = [
        CommandHandler("start", start),
        CommandHandler("north", cmd_north),
        CommandHandler("south", cmd_south),
        CommandHandler("europe", cmd_europe),
        CommandHandler("asia", cmd_asia),
        CommandHandler("rules", cmd_rules),
        CommandHandler("commands", cmd_commands),
        CallbackQueryHandler(button_handler),
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_listener),
    ]

    for h in handlers:
        app.add_handler(h)

    print("✅ Bot is running...")
    app.run_polling()