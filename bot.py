import os
import logging
import sys
from typing import List
from dataclasses import dataclass

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    filters
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Bot Configuration
class BotConfig:
    # Get token from environment variable
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    # Webhook configuration for Render
    WEBHOOK_URL = os.environ.get('RENDER_EXTERNAL_URL', '')  # Render provides this
    PORT = int(os.environ.get('PORT', 8443))
    
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        sys.exit(1)

# Crypto Education Content
@dataclass
class CryptoTopic:
    title: str
    description: str
    icon: str

class CryptoEducation:
    def __init__(self):
        self.description = """
📚 **Crypto Education Bot**
*Your guide to understanding cryptocurrency and blockchain technology*

Welcome to a safe, educational space to learn about cryptocurrency fundamentals.
"""
        
        self.topics = [
            CryptoTopic("🔗 What is Blockchain?", 
                       "Blockchain is a decentralized, distributed ledger technology that records transactions across many computers. It ensures security, transparency, and immutability of data without central authority.", 
                       "🔗"),
            
            CryptoTopic("💰 What is Cryptocurrency?", 
                       "Cryptocurrency is digital money that uses cryptography for security. It operates independently of central banks and enables peer-to-peer transactions through blockchain technology.", 
                       "💰"),
            
            CryptoTopic("🔒 Crypto Security Basics", 
                       "Learn essential security practices: Use hardware wallets, enable 2FA, never share private keys, verify addresses, and beware of phishing scams. Your keys, your crypto!", 
                       "🔒"),
            
            CryptoTopic("🌱 Getting Started Safely", 
                       "Start with research, understand risks, begin with small amounts, use reputable exchanges, and never invest more than you can afford to lose. Education first!", 
                       "🌱")
        ]

class CryptoEduBot:
    def __init__(self):
        self.config = BotConfig()
        self.education = CryptoEducation()
        logger.info("Crypto Education Bot initialized")
    
    async def start(self, update: Update, context: CallbackContext) -> None:
        """Handle /start command."""
        user = update.effective_user
        
        welcome_message = f"""
🎓 Welcome {user.first_name} to Crypto Education Bot! 🎓

{self.education.description}

📖 *Choose a topic to learn:*
1. What is Blockchain?
2. What is Cryptocurrency?
3. Crypto Security Basics
4. Getting Started Safely

📋 *Available Commands:*
/start - Welcome message
/topics - List all topics
/help - Show all commands
        """
        
        keyboard = [
            [InlineKeyboardButton("🔗 Blockchain", callback_data="blockchain"),
             InlineKeyboardButton("💰 Cryptocurrency", callback_data="crypto")],
            [InlineKeyboardButton("🔒 Security", callback_data="security"),
             InlineKeyboardButton("🌱 Getting Started", callback_data="started")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def topics(self, update: Update, context: CallbackContext) -> None:
        """Display all crypto topics."""
        message = "📚 **Available Crypto Education Topics**\n\n"
        
        for i, topic in enumerate(self.education.topics, 1):
            message += f"{topic.icon} **{i}. {topic.title}**\n"
            message += f"   {topic.description[:100]}...\n\n"
        
        await update.message.reply_markdown(message)
    
    async def help_command(self, update: Update, context: CallbackContext) -> None:
        """Show help message."""
        message = """
🤖 **Crypto Education Bot Commands**

/start - Welcome message with topic buttons
/topics - List all educational topics
/help - This help message

💡 Use the interactive buttons below to explore different crypto topics!
        """
        
        await update.message.reply_markdown(message)
    
    async def button_handler(self, update: Update, context: CallbackContext) -> None:
        """Handle button callbacks."""
        query = update.callback_query
        await query.answer()
        
        if query.data == "blockchain":
            topic = self.education.topics[0]
            message = f"**{topic.icon} {topic.title}**\n\n{topic.description}\n\n💡 *Key Takeaways:*\n• Decentralized ledger\n• Immutable records\n• No central authority\n• Transparent transactions"
            
        elif query.data == "crypto":
            topic = self.education.topics[1]
            message = f"**{topic.icon} {topic.title}**\n\n{topic.description}\n\n💡 *Key Takeaways:*\n• Digital currency\n• Peer-to-peer transactions\n• Cryptography for security\n• Limited supply"
            
        elif query.data == "security":
            topic = self.education.topics[2]
            message = f"**{topic.icon} {topic.title}**\n\n{topic.description}\n\n💡 *Key Takeaways:*\n• Hardware wallets recommended\n• Never share private keys\n• Enable 2FA\n• Verify all transactions"
            
        elif query.data == "started":
            topic = self.education.topics[3]
            message = f"**{topic.icon} {topic.title}**\n\n{topic.description}\n\n💡 *Key Takeaways:*\n• Research before investing\n• Start small\n• Use reputable platforms\n• Understand the risks"
        
        keyboard = [
            [InlineKeyboardButton("🔗 Blockchain", callback_data="blockchain"),
             InlineKeyboardButton("💰 Cryptocurrency", callback_data="crypto")],
            [InlineKeyboardButton("🔒 Security", callback_data="security"),
             InlineKeyboardButton("🌱 Getting Started", callback_data="started")],
            [InlineKeyboardButton("📚 All Topics", callback_data="all_topics")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def all_topics_handler(self, update: Update, context: CallbackContext) -> None:
        """Handle 'All Topics' button."""
        query = update.callback_query
        await query.answer()
        
        message = "📚 **Complete Crypto Education Topics**\n\n"
        
        for topic in self.education.topics:
            message += f"{topic.icon} **{topic.title}**\n"
            message += f"{topic.description}\n\n"
        
        keyboard = [
            [InlineKeyboardButton("🔗 Blockchain", callback_data="blockchain"),
             InlineKeyboardButton("💰 Cryptocurrency", callback_data="crypto")],
            [InlineKeyboardButton("🔒 Security", callback_data="security"),
             InlineKeyboardButton("🌱 Getting Started", callback_data="started")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    def setup_handlers(self, application: Application):
        """Setup all command handlers."""
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("topics", self.topics))
        application.add_handler(CommandHandler("help", self.help_command))
        
        # Button handlers
        application.add_handler(CallbackQueryHandler(self.button_handler, pattern="^(blockchain|crypto|security|started)$"))
        application.add_handler(CallbackQueryHandler(self.all_topics_handler, pattern="^all_topics$"))
        
        # Unknown command handler
        application.add_handler(MessageHandler(filters.COMMAND, self.unknown))
    
    async def unknown(self, update: Update, context: CallbackContext) -> None:
        """Handle unknown commands."""
        await update.message.reply_text("Sorry, I didn't understand that command. Try /help to see available commands.")
    
    async def set_webhook(self, application: Application):
        """Set webhook if WEBHOOK_URL is available."""
        if self.config.WEBHOOK_URL:
            webhook_url = f"{self.config.WEBHOOK_URL}/webhook"
            await application.bot.set_webhook(webhook_url)
            logger.info(f"Webhook set to: {webhook_url}")
        else:
            logger.info("Using polling mode (no webhook URL set)")
    
    def run_webhook(self):
        """Run bot with webhook (for Render)."""
        application = Application.builder().token(self.config.TOKEN).build()
        self.setup_handlers(application)
        
        # Set webhook on startup
        application.run_webhook(
            listen="0.0.0.0",
            port=self.config.PORT,
            secret_token='WEBHOOK_SECRET',
            webhook_url=f"{self.config.WEBHOOK_URL}/webhook" if self.config.WEBHOOK_URL else None
        )
    
    def run_polling(self):
        """Run bot with polling (for local development)."""
        application = Application.builder().token(self.config.TOKEN).build()
        self.setup_handlers(application)
        
        logger.info("Starting bot in polling mode...")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )

def main():
    """Main entry point."""
    try:
        bot = CryptoEduBot()
        
        # Check if we're on Render (has WEBHOOK_URL)
        config = BotConfig()
        
        if config.WEBHOOK_URL:
            logger.info("Running in webhook mode (Render)")
            bot.run_webhook()
        else:
            logger.info("Running in polling mode (Local)")
            bot.run_polling()
            
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
