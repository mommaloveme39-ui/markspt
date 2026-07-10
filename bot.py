import logging
from datetime import datetime
from typing import Dict, List

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

import config

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# User preferences storage
user_preferences = {}

# Sample news data
SAMPLE_NEWS = [
    {
        "title": "Mbappé, France dispatch Morocco with latest lethal performance",
        "source": "ESPN",
        "time": "02:09",
        "link": "https://www.espn.com/soccer/story/_/id/12345678",
        "summary": "France are favorites to win the World Cup for many reasons."
    },
    {
        "title": "Mbappé guides France past Morocco to WC semis",
        "source": "BBC Sport",
        "time": "02:09",
        "link": "https://www.bbc.com/sport/football/12345678",
        "summary": "Kylian Mbappé was at his devastating best as France edged past Morocco."
    },
    {
        "title": "Clippers-Raptors trade for Kawhi on hold amid probe",
        "source": "ESPN",
        "time": "01:45",
        "link": "https://www.espn.com/nba/story/_/id/12345678",
        "summary": "The NBA is investigating the circumstances surrounding the Kawhi Leonard trade."
    },
    {
        "title": "Stephen Curry acknowledges 'allure' of playing with LeBron",
        "source": "Sky Sports",
        "time": "01:30",
        "link": "https://www.skysports.com/nba/news/12345678",
        "summary": "Stephen Curry has admitted he finds the prospect of playing alongside LeBron James intriguing."
    },
    {
        "title": "Sources: Teams courting LeBron via voice memos",
        "source": "ESPN",
        "time": "01:15",
        "link": "https://www.espn.com/nba/story/_/id/12345678",
        "summary": "Several NBA teams are reportedly using voice memos to recruit LeBron James."
    },
    {
        "title": "Djokovic reaches Wimbledon final after epic semi-final",
        "source": "BBC Sport",
        "time": "02:00",
        "link": "https://www.bbc.com/sport/tennis/12345680",
        "summary": "Novak Djokovic reached his fifth consecutive Wimbledon final."
    }
]

# Category-specific news
CATEGORY_NEWS = {
    "football": [
        {
            "title": "Mbappé, France dispatch Morocco with latest lethal performance",
            "source": "ESPN",
            "time": "02:09",
            "link": "https://www.espn.com/soccer/story/_/id/12345678",
            "summary": "France are favorites to win the World Cup."
        },
        {
            "title": "Premier League: Man City extend lead at top",
            "source": "BBC Sport",
            "time": "01:50",
            "link": "https://www.bbc.com/sport/football/12345679",
            "summary": "Manchester City extended their lead at the top."
        }
    ],
    "basketball": [
        {
            "title": "Clippers-Raptors trade for Kawhi on hold amid probe",
            "source": "ESPN",
            "time": "01:45",
            "link": "https://www.espn.com/nba/story/_/id/12345678",
            "summary": "The NBA is investigating the trade."
        },
        {
            "title": "Stephen Curry acknowledges 'allure' of playing with LeBron",
            "source": "Sky Sports",
            "time": "01:30",
            "link": "https://www.skysports.com/nba/news/12345678",
            "summary": "Curry finds the prospect of playing with LeBron intriguing."
        }
    ],
    "tennis": [
        {
            "title": "Djokovic reaches Wimbledon final after epic semi-final",
            "source": "BBC Sport",
            "time": "02:00",
            "link": "https://www.bbc.com/sport/tennis/12345680",
            "summary": "Novak Djokovic reached his fifth consecutive Wimbledon final."
        },
        {
            "title": "Alcaraz: 'I'm ready to face Djokovic in final'",
            "source": "ESPN",
            "time": "01:40",
            "link": "https://www.espn.com/tennis/story/_/id/12345681",
            "summary": "Carlos Alcaraz says he is ready to face Djokovic."
        }
    ],
    "cricket": [
        {
            "title": "India wins T20 World Cup after thrilling final",
            "source": "BBC Sport",
            "time": "01:00",
            "link": "https://www.bbc.com/sport/cricket/12345682",
            "summary": "India clinched the T20 World Cup in a nail-biting final."
        }
    ],
    "nfl": [
        {
            "title": "Chiefs win Super Bowl in overtime thriller",
            "source": "ESPN",
            "time": "00:45",
            "link": "https://www.espn.com/nfl/story/_/id/12345683",
            "summary": "Kansas City Chiefs won their third Super Bowl in five years."
        }
    ],
    "baseball": [
        {
            "title": "Yankees sign Juan Soto to record contract",
            "source": "Sky Sports",
            "time": "00:30",
            "link": "https://www.skysports.com/baseball/12345684",
            "summary": "The New York Yankees signed Juan Soto to a historic deal."
        }
    ]
}

# ============ HELPER FUNCTIONS ============

def get_news(category: str = None, limit: int = 10) -> List[Dict]:
    """Fetch news based on category"""
    if category and category in CATEGORY_NEWS:
        return CATEGORY_NEWS[category][:limit]
    return SAMPLE_NEWS[:limit]

def format_news_message(news_list: List[Dict]) -> str:
    """Format news items for display"""
    if not news_list:
        return config.NO_NEWS_MESSAGE

    current_time = datetime.now().strftime("%H:%M")
    message = f"📰 *Latest Sports News*\n_{current_time}_\n\n"

    for i, item in enumerate(news_list, 1):
        message += f"*{i}. {item['title']}*\n"
        message += f"📌 *Source:* {item['source']} | 🕐 {item.get('time', current_time)}\n"
        if item.get('summary'):
            message += f"📝 {item['summary'][:100]}...\n"
        message += f"🔗 [Read More]({item['link']})\n\n"

    return message

def get_category_keyboard() -> InlineKeyboardMarkup:
    """Create category selection keyboard"""
    keyboard = []
    row = []
    for i, (label, value) in enumerate(config.CATEGORIES.items()):
        row.append(InlineKeyboardButton(label, callback_data=f"cat_{value}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # Add action buttons
    keyboard.append([
        InlineKeyboardButton("📰 All News", callback_data="cat_all"),
        InlineKeyboardButton("✅ Done", callback_data="cat_done")
    ])

    return InlineKeyboardMarkup(keyboard)

def get_main_keyboard() -> InlineKeyboardMarkup:
    """Create main menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("📰 Latest News", callback_data="latest"),
            InlineKeyboardButton("🏆 Categories", callback_data="categories")
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============ COMMAND HANDLERS ============

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user

    # Initialize user preferences
    user_id = str(user.id)
    if user_id not in user_preferences:
        user_preferences[user_id] = {"categories": []}

    welcome_text = f"{config.WELCOME_MESSAGE}\n\n👋 *Welcome, {user.first_name}!*"

    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(),
        disable_web_page_preview=True
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    await update.message.reply_text(
        config.HELP_MESSAGE,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /about command"""
    await update.message.reply_text(
        config.ABOUT_MESSAGE,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def latest_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /latest command"""
    user_id = str(update.effective_user.id)
    categories = user_preferences.get(user_id, {}).get("categories", [])

    # Show fetching message
    status_msg = await update.message.reply_text(
        config.FETCHING_MESSAGE,
        parse_mode="Markdown"
    )

    # Fetch news based on preferences
    all_news = []
    if categories:
        for cat in categories:
            all_news.extend(get_news(cat, limit=3))
    else:
        all_news = get_news(limit=10)

    # Remove duplicates
    seen = set()
    unique_news = []
    for item in all_news:
        if item['title'] not in seen:
            seen.add(item['title'])
            unique_news.append(item)

    # Format and send
    news_message = format_news_message(unique_news[:10])

    await status_msg.edit_text(
        news_message,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(),
        disable_web_page_preview=True
    )

async def scores_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /scores command"""
    await update.message.reply_text(
        config.SCORES_MESSAGE,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    data = query.data

    # Initialize user preferences if not exists
    if user_id not in user_preferences:
        user_preferences[user_id] = {"categories": []}

    if data == "latest":
        # Show fetching message
        await query.edit_message_text(
            config.FETCHING_MESSAGE,
            parse_mode="Markdown"
        )

        # Fetch and display news
        categories = user_preferences[user_id].get("categories", [])
        all_news = []
        if categories:
            for cat in categories:
                all_news.extend(get_news(cat, limit=3))
        else:
            all_news = get_news(limit=10)

        news_message = format_news_message(all_news[:10])

        await query.edit_message_text(
            news_message,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard(),
            disable_web_page_preview=True
        )

    elif data == "categories":
        await query.edit_message_text(
            config.CATEGORY_SELECTION,
            parse_mode="Markdown",
            reply_markup=get_category_keyboard()
        )

    elif data == "about":
        await query.edit_message_text(
            config.ABOUT_MESSAGE,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )

    elif data == "help":
        await query.edit_message_text(
            config.HELP_MESSAGE,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )

    elif data.startswith("cat_"):
        category = data.replace("cat_", "")

        if category == "done":
            # Return to main menu
            await query.edit_message_text(
                "✅ *Categories updated!*\n\nUse 'Latest News' to see personalized updates.",
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
            return

        if category == "all":
            # Clear preferences and show all news
            user_preferences[user_id]["categories"] = []
            await query.edit_message_text(
                "📰 *Showing all news categories*\n\nYou'll see news from all sports.",
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
            return

        # Toggle category selection
        current_cats = user_preferences[user_id]["categories"]
        if category in current_cats:
            current_cats.remove(category)
        else:
            current_cats.append(category)

        # Show updated category selection
        selected_text = "\n".join([f"✅ {label}" for label, val in config.CATEGORIES.items() if val in current_cats])
        if not selected_text:
            selected_text = "No categories selected"

        message = f"{config.CATEGORY_SELECTION}\n\n*Your selections:*\n{selected_text}"
        await query.edit_message_text(
            message,
            parse_mode="Markdown",
            reply_markup=get_category_keyboard()
        )

# ============ ERROR HANDLING ============

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")

    if update and update.effective_message:
        await update.effective_message.reply_text(
            config.ERROR_MESSAGE,
            parse_mode="Markdown"
        )

async def post_init(application: Application) -> None:
    """Setup webhook after application starts"""
    logger.info("markspt_bot started successfully!")

# ============ MAIN FUNCTION ============

def main() -> None:
    """Start the bot"""
    # Create application
    application = Application.builder().token(config.BOT_TOKEN).post_init(post_init).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("latest", latest_command))
    application.add_handler(CommandHandler("scores", scores_command))

    # Callback query handler (for buttons)
    application.add_handler(CallbackQueryHandler(button_handler))

    # Error handler
    application.add_error_handler(error_handler)

    # Start webhook (for Render)
    if config.BOT_TOKEN:
        application.run_webhook(
            listen="0.0.0.0",
            port=config.PORT,
            url_path=config.BOT_TOKEN,
            webhook_url=f"https://markspt.onrender.com/{config.BOT_TOKEN}"
        )

if __name__ == "__main__":
    main()
