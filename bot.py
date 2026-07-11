import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

user_preferences = {}

SAMPLE_NEWS = [
    {"title": "Mbappé, France dispatch Morocco", "source": "ESPN", "link": "https://www.espn.com"},
    {"title": "Clippers-Raptors trade on hold", "source": "ESPN", "link": "https://www.espn.com"},
    {"title": "Curry acknowledges allure of playing with LeBron", "source": "Sky Sports", "link": "https://www.skysports.com"}
]

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📰 Latest News", callback_data="latest")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("❓ Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🏆 Welcome to markspt!\n\nGet real-time sports news.", reply_markup=reply_markup)

def latest(update: Update, context: CallbackContext):
    msg = "📰 *Latest Sports News*\n\n"
    for i, item in enumerate(SAMPLE_NEWS[:3], 1):
        msg += f"{i}. {item['title']}\n📌 {item['source']}\n🔗 [Read More]({item['link']})\n\n"
    update.callback_query.edit_message_text(msg, parse_mode="Markdown")

def about(update: Update, context: CallbackContext):
    update.callback_query.edit_message_text("📰 *About markspt*\n\nReal-time sports journalism from trusted networks.")

def help(update: Update, context: CallbackContext):
    update.callback_query.edit_message_text("❓ *Commands:*\n/start - Start\n/latest - News\n/about - About\n/help - Help")

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == "latest":
        latest(update, context)
    elif query.data == "about":
        about(update, context)
    elif query.data == "help":
        help(update, context)

def main():
    updater = Updater(config.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("latest", lambda u,c: latest(u,c) if u.callback_query else None))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
