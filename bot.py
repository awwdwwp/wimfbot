from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import ReplyKeyboardMarkup
import os
from dotenv import load_dotenv

load_dotenv()  # This loads .env variables

TOKEN = os.getenv("TOKEN")  # Use token from .env
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
1.1 До участі у сезоні допускаються будь-які країни світу, в тому числі частково визнані країни, або чітко визначені симулятором залежні території країн, таких як США або Великої Британії (Американське Самоа, Гібралтар і т.п.)

1.2 Для участі на конкурсі забороняється терористична держава росія

1.3 Обмін між країнами недоступний у разі, якщо ви берете виконавця за національними коріннями
(Наприклад: Ariana Grande має національні коріння з Італії, тож її неможливо брати від країн по обміну: Сан-Марино чи Мальта)

**2. Вимоги до виконавця і пісні**
2.1 Виконавець, обраної вами країни, повинен мати громадянство, ПМЖ (Постійне місце проживання) або ж мати національні коріння звідти

2.2 Виконавець, на період подачі пісень, має бути живим. Якщо це гурт — то у повному складі

2.3 Якщо гурт, на момент подачі пісні, у стані заморозки (група не розпалася, але не веде професійну діяльність) — дозволено

2.4 Пісня має бути авторською, забороняються народні пісні, кавери, ремікси і т.п.

2.5 Пісні, де більше 80% тексту написано російською мовою, заборонені ❌

2.6 Перегляди на платформі YouTube не мають перевищувати 70 млн

2.7 Пісня не має містити політичного підтексту

2.8 Пісня має бути випущеною після 1 січня 2015 року

2.9 Ліцензії не обмежені — приймаються пісні з будь-якими ліцензіями

2.10 Забороняються пісні з:
- Євробачення
- Нацвідборів на Євробачення (відкритих чи закритих)
- Дитячого Євробачення
- Американського аналогу
- Фестивалів, які прямо або опосередковано стосуються Євробачення

**3. Система автофіналу**
3.1 Куратор, який одержав перемогу у сезоні, автоматично стає фіналістом наступного сезону

3.2 Куратор країни, яка зайняла друге місце, може змінити країну на будь-яку іншу, залишаючи своє право автофіналіста

3.3 У разі відмови другого місця бути автофіналістом — це право переходить до наступного місця

3.4 Якщо сезон був лише з одним фіналом (з системою PQR або без), то:
- Перше і друге місце, а також автофіналісти — залишають це право
- Всі мають право змінити країну, окрім переможця

3.5 Делегації у сезоні дозволені, але не більше 2 учасників у делегації"""



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
async def cmd_north(update, context):
    await update.message.reply_text(region_texts["north"])

async def cmd_south(update, context):
    await update.message.reply_text(region_texts["south"])

async def cmd_europe(update, context):
    await update.message.reply_text(region_texts["europe"])

async def cmd_asia(update, context):
    await update.message.reply_text(region_texts["asia"])

async def cmd_rules(update, context):
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

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Лист обміну"],
        ["Правила"],
        ["Команди"]  # ← new button
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привіт! Обери опцію:", reply_markup=reply_markup)

# Button Handler (inline)
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

# ReplyKeyboard text handler
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
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("north", cmd_north))
    app.add_handler(CommandHandler("south", cmd_south))
    app.add_handler(CommandHandler("europe", cmd_europe))
    app.add_handler(CommandHandler("asia", cmd_asia))
    app.add_handler(CommandHandler("rules", cmd_rules))
    app.add_handler(CommandHandler("commands", cmd_commands))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_listener))

    print("✅ Bot is running...")
    app.run_polling()