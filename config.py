import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8080))

# Categories for user selection
CATEGORIES = {
    "⚽ Football": "football",
    "🏀 Basketball": "basketball",
    "🎾 Tennis": "tennis",
    "🏏 Cricket": "cricket",
    "🏈 NFL": "nfl",
    "⚾ Baseball": "baseball"
}

# Bot messages
WELCOME_MESSAGE = """🏆 *Welcome to markspt!*

Get instant, verified sports updates from trusted global networks like ESPN, BBC Sport, and Sky Sports.

*What you can do:*
📰 Get real-time sports headlines
🔗 Direct links to full articles
⚡ Breaking news alerts
📊 Live scores and updates

*How to use:*
1️⃣ Select your favorite sports below
2️⃣ Tap 'Latest News' for fresh updates
3️⃣ Use 'Help' anytime for assistance

*Start now by selecting a category below!* 👇"""

ABOUT_MESSAGE = """📰 *About markspt*

markspt provides real-time sports journalism, scores, and breaking news headlines from leading global sports networks.

*Features:*
✅ Verified news from trusted sources
✅ Direct article links for in-depth coverage
✅ Personalized sports categories
✅ Clean, ad-compliant content
✅ Instant updates

*Sources:*
• ESPN
• BBC Sport
• Sky Sports
• And more...

*Independent, clean, and ad-compliant journalism at your fingertips.*"""

HELP_MESSAGE = """❓ *How to Use markspt*

*Commands:*
/start - Restart the bot
/latest - Get latest news
/scores - Live scores
/about - About markspt
/help - Show this help message

*Menu Buttons:*
📰 *Latest News* - Refresh your news feed
🏆 *Categories* - Select your favorite sports
ℹ️ *About* - Learn about markspt
❓ *Help* - Get assistance

*Tips:*
• Select categories to personalize your feed
• Tap 'Latest News' anytime for fresh updates
• Click 'Read More' on any story for full article

*Need more help?* Contact support or check our channel."""

ERROR_MESSAGE = "⚠️ *Oops!* Something went wrong. Please try again later."

NO_NEWS_MESSAGE = "📭 *No news available at the moment.* Check back later!"

CATEGORY_SELECTION = """🏆 *Select Your Favorite Sports*

Choose categories below to personalize your news feed. You can select multiple sports!

Tap any category to toggle selection:"""

FETCHING_MESSAGE = "⏳ *Fetching the latest sports updates...* Please wait."

SCORES_MESSAGE = """📊 *Live Scores & Updates*

*Football:*
⚽ Liverpool 2 - 1 Manchester City
⚽ Real Madrid 3 - 0 Barcelona

*Basketball:*
🏀 Lakers 112 - 108 Warriors

*Tennis:*
🎾 Djokovic vs Alcaraz - In Progress

*Click 'Latest News' for more updates!*"""
