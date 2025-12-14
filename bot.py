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

# NCN Information
@dataclass
class NCNFeature:
    title: str
    description: str
    icon: str

class NCNComponent:
    def __init__(self):
        self.description = """
🚀 **NCN (NVAI Computing Network)**
*Secure, Independent Computing Network Powered by NVAI Technology*

NCN represents a revolutionary leap in decentralized computing infrastructure.
"""
        
        self.key_features = [
            NCNFeature("🔒 Quantum-Secure Architecture", "Military-grade encryption", "🛡️"),
            NCNFeature("🧠 NVAI Neural Processing", "Distributed neural network processing", "⚡"),
            NCNFeature("🌐 Autonomous Operation", "Self-healing network", "🤖"),
            NCNFeature("⚡ Edge Computing First", "Ultra-low latency processing", "💨"),
            NCNFeature("📊 Data Sovereignty", "Complete user control over data", "🔐"),
            NCNFeature("♻️ Energy Efficient", "Green computing optimized", "🌿")
        ]

class NCNBot:
    def __init__(self):
        self.config = BotConfig()
        self.ncn = NCNComponent()
        logger.info("NCN Bot initialized")
    
    async def start(self, update: Update, context: CallbackContext) -> None:
        """Handle /start command."""
        user = update.effective_user
        
        welcome_message = f"""
🌟 Welcome {user.first_name} to the NCN Information Portal! 🌟

{self.ncn.description}

📋 *Available Commands:*
/start - Welcome message
/features - Key features
/help - Show all commands
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Features", callback_data="features")],
            [InlineKeyboardButton("📞 Contact", callback_data="contact")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def features(self, update: Update, context: CallbackContext) -> None:
        """Display NCN features."""
        message = "🚀 **NCN Key Features**\n\n"
        
        for feature in self.ncn.key_features:
            message += f"{feature.icon} **{feature.title}**\n"
            message += f"   {feature.description}\n\n"
        
        await update.message.reply_markdown(message)
    
    async def help_command(self, update: Update, context: CallbackContext) -> None:
        """Show help message."""
        message = """
🤖 **NCN Bot Commands**

/start - Welcome message
/features - Key features of NCN
/help - This help message

💡 Use the interactive buttons for quick navigation!
        """
        
        await update.message.reply_markdown(message)
    
    async def contact(self, update: Update, context: CallbackContext) -> None:
        """Display contact information."""
        message = """
📞 **Contact NCN Team**

🌐 **Website:** https://ncn-network.io
📧 **Email:** contact@ncn-network.io

📍 **HQ:** Zurich, Switzerland
        """
        
        await update.message.reply_markdown(message)
    
    async def button_handler(self, update: Update, context: CallbackContext) -> None:
        """Handle button callbacks."""
        query = update.callback_query
        await query.answer()
        
        if query.data == "features":
            message = "🚀 **NCN Key Features**\n\n"
            for feature in self.ncn.key_features:
                message += f"{feature.icon} **{feature.title}**\n"
                message += f"   {feature.description}\n\n"
            
            await query.edit_message_text(
                message,
                parse_mode='Markdown'
            )
        elif query.data == "contact":
            await query.edit_message_text(
                "📞 **Contact NCN Team**\n\n🌐 Website: https://ncn-network.io\n📧 Email: contact@ncn-network.io",
                parse_mode='Markdown'
            )
    
    def setup_handlers(self, application: Application):
        """Setup all command handlers."""
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("features", self.features))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CallbackQueryHandler(self.button_handler))
        
        # Unknown command handler
        application.add_handler(MessageHandler(filters.COMMAND, self.unknown))
    
    async def unknown(self, update: Update, context: CallbackContext) -> None:
        """Handle unknown commands."""
        await update.message.reply_text("Sorry, I didn't understand that command. Try /help")
    
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
            drop_pending_updates=True  # IMPORTANT: Drops old updates to avoid conflicts
        )

def main():
    """Main entry point."""
    try:
        bot = NCNBot()
        
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
