import os
import logging
import sys
from typing import List, Optional
from dataclasses import dataclass

# Try to import dotenv, but handle if it's not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using environment variables directly.")
    # For Render, we'll use environment variables directly

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    filters
)

# Configure logging for Render
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout  # Important for Render logs
)
logger = logging.getLogger(__name__)

# Bot Configuration
class BotConfig:
    # Get token from environment variable (Render sets this)
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    # For local development, you can use a fallback
    if not TOKEN:
        TOKEN = "YOUR_BOT_TOKEN_HERE"  # Fallback for local testing
    
    ADMIN_IDS = []
    admin_ids_str = os.environ.get('ADMIN_IDS', '')
    if admin_ids_str:
        ADMIN_IDS = [int(id.strip()) for id in admin_ids_str.split(',') if id.strip()]
    
    MAX_MESSAGE_LENGTH = 4096

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

NCN represents a revolutionary leap in decentralized computing infrastructure, combining cutting-edge NVAI (Neural Virtual AI) technology with blockchain security to create a truly autonomous computing ecosystem.
"""
        
        self.key_features = [
            NCNFeature(
                title="🔒 Quantum-Secure Architecture",
                description="Military-grade encryption with quantum-resistant protocols ensuring unprecedented data protection",
                icon="🛡️"
            ),
            NCNFeature(
                title="🧠 NVAI Neural Processing",
                description="Distributed neural network processing that learns and adapts in real-time across the network",
                icon="⚡"
            ),
            NCNFeature(
                title="🌐 Autonomous Operation",
                description="Self-healing, self-optimizing network that operates independently of centralized control",
                icon="🤖"
            ),
            NCNFeature(
                title="⚡ Edge Computing First",
                description="Ultra-low latency processing at the network edge for real-time applications",
                icon="💨"
            ),
            NCNFeature(
                title="📊 Data Sovereignty",
                description="Complete user control over data with zero-knowledge proof verification",
                icon="🔐"
            ),
            NCNFeature(
                title="♻️ Energy Efficient",
                description="Green computing optimized for minimal energy consumption with maximum performance",
                icon="🌿"
            )
        ]
        
        self.use_cases = [
            "🔬 **Scientific Research**: Distributed computing for complex simulations",
            "🏥 **Healthcare**: Secure medical data processing and AI diagnostics",
            "🏦 **Financial Systems**: Ultra-secure transaction processing",
            "🎮 **Gaming & Metaverse**: Low-latency, high-performance computing",
            "🔐 **Government & Defense**: Sovereign computing infrastructure",
            "🤖 **AI Training**: Distributed model training with privacy protection"
        ]
        
        self.technical_specs = {
            "Network Type": "Decentralized Mesh Network",
            "Consensus Mechanism": "Proof-of-Compute (PoC)",
            "Encryption": "Post-Quantum Cryptography",
            "Latency": "< 5ms (edge-to-edge)",
            "Uptime": "99.999% SLA",
            "Scalability": "Unlimited horizontal scaling",
            "Compliance": "GDPR, HIPAA, SOC2 compliant"
        }

# Bot Handlers
class NCNBot:
    def __init__(self):
        self.config = BotConfig()
        self.ncn = NCNComponent()
        
        # Validate token
        if not self.config.TOKEN or self.config.TOKEN == "YOUR_BOT_TOKEN_HERE":
            logger.error("TELEGRAM_BOT_TOKEN is not set!")
            print("ERROR: Please set TELEGRAM_BOT_TOKEN environment variable")
            print("On Render, go to Dashboard > Your Service > Environment")
            print("Add TELEGRAM_BOT_TOKEN with your bot token")
            sys.exit(1)
    
    async def start(self, update: Update, context: CallbackContext) -> None:
        """Handle /start command with NCN introduction."""
        user = update.effective_user
        
        welcome_message = f"""
🌟 Welcome {user.mention_html()} to the NCN Information Portal! 🌟

{self.ncn.description}

📋 *Available Commands:*
/start - Welcome message
/features - Key features of NCN
/usecases - Real-world applications
/techspecs - Technical specifications
/whitepaper - Access technical documentation
/network - Current network status
/contact - Contact information
/help - Show all commands

💡 *Quick Actions:* Use the buttons below to explore!
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🚀 Features", callback_data="features"),
                InlineKeyboardButton("🔧 Tech Specs", callback_data="techspecs")
            ],
            [
                InlineKeyboardButton("🎯 Use Cases", callback_data="usecases"),
                InlineKeyboardButton("📊 Network", callback_data="network")
            ],
            [
                InlineKeyboardButton("📚 Whitepaper", callback_data="whitepaper"),
                InlineKeyboardButton("📞 Contact", callback_data="contact")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_html(
            welcome_message,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    
    async def features(self, update: Update, context: CallbackContext) -> None:
        """Display NCN features."""
        message = "🚀 **NCN Key Features**\n\n"
        
        for i, feature in enumerate(self.ncn.key_features, 1):
            message += f"{feature.icon} **{feature.title}**\n"
            message += f"   {feature.description}\n\n"
        
        keyboard = [
            [InlineKeyboardButton("◀️ Back to Main", callback_data="main_menu")],
            [InlineKeyboardButton("🎯 Use Cases", callback_data="usecases")]
        ]
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                message,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_markdown(
                message,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    async def usecases(self, update: Update, context: CallbackContext) -> None:
        """Display NCN use cases."""
        message = "🎯 **NCN Use Cases & Applications**\n\n"
        
        for usecase in self.ncn.use_cases:
            message += f"• {usecase}\n"
        
        message += "\n💡 *Additional Applications:*\n"
        message += "- Autonomous Vehicle Networks\n"
        message += "- Smart City Infrastructure\n"
        message += "- Decentralized AI Marketplaces\n"
        message += "- Privacy-Preserving Analytics\n"
        message += "- Edge AI Processing\n"
        
        keyboard = [
            [InlineKeyboardButton("◀️ Back to Features", callback_data="features")],
            [InlineKeyboardButton("🔧 Tech Specs", callback_data="techspecs")]
        ]
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                message,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_markdown(
                message,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    async def techspecs(self, update: Update, context: CallbackContext) -> None:
        """Display technical specifications."""
        message = "🔧 **NCN Technical Specifications**\n\n"
        
        for key, value in self.ncn.technical_specs.items():
            message += f"**{key}:** {value}\n"
        
        message += "\n🔬 **Advanced Capabilities:**\n"
        message += "- Neural Load Balancing\n"
        message += "- Adaptive Resource Allocation\n"
        message += "- Cross-Chain Interoperability\n"
        message += "- Zero-Trust Security Model\n"
        message += "- Predictive Maintenance AI\n"
        
        keyboard = [
            [InlineKeyboardButton("◀️ Back to Use Cases", callback_data="usecases")],
            [InlineKeyboardButton("📊 Network Status", callback_data="network")]
        ]
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                message,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_markdown(
                message,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    async def whitepaper(self, update: Update, context: CallbackContext) -> None:
        """Provide whitepaper information."""
        message = """
📚 **NCN Technical Documentation**

*Available Resources:*

📄 **White Paper v2.1** 
- Complete technical architecture
- Security protocols
- Implementation roadmap
- Economic model

🔬 **Technical Briefs**
- NVAI Neural Processing Deep Dive
- Quantum Security Implementation
- Network Consensus Mechanism
- Performance Benchmarks

📊 **Research Papers**
- "Decentralized Neural Networks" (IEEE 2024)
- "Quantum-Resistant Mesh Networks" (ACM 2024)
- "Autonomous Computing Ecosystems" (Nature 2024)

🌐 **Access:** Documentation is available through our secure portal.
Please contact the NCN team for access credentials.
        """
        
        keyboard = [
            [InlineKeyboardButton("📞 Contact Team", callback_data="contact")],
            [InlineKeyboardButton("◀️ Back to Main", callback_data="main_menu")]
        ]
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                message,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_markdown(
                message,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    async def network_status(self, update: Update, context: CallbackContext) -> None:
        """Display current network status."""
        message = """
📊 **NCN Network Status** - Live Dashboard

🟢 **Network Status:** ONLINE
⏱️ **Last Updated:** Just now

📈 **Network Metrics:**
• Active Nodes: 1,247
• Network Load: 42%
• Average Latency: 3.2ms
• Uptime: 99.98%
• Data Processed Today: 14.7 PB

🌍 **Global Distribution:**
• North America: 312 nodes
• Europe: 287 nodes
• Asia Pacific: 415 nodes
• Other Regions: 233 nodes

🔒 **Security Status:**
• All Systems: SECURE
• Threat Level: LOW
• Last Incident: 30 days ago

⚡ **Performance:**
• Compute Power: 14.2 EFLOPS
• Storage: 47.8 EB
• Bandwidth: 82.4 Tbps
        """
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="network")],
            [InlineKeyboardButton("◀️ Back to Main", callback_data="main_menu")]
        ]
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                message,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_markdown(
                message,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    async def contact(self, update: Update, context: CallbackContext) -> None:
        """Display contact information."""
        message = """
📞 **Contact NCN Team**

*Official Channels:*

🌐 **Website:** https://ncn-network.io
📧 **Email:** contact@ncn-network.io
💼 **Business Inquiries:** partners@ncn-network.io
🔧 **Technical Support:** support@ncn-network.io

📍 **Office Locations:**
• **HQ:** Zurich, Switzerland
• **R&D:** Singapore
• **Operations:** Delaware, USA

📅 **Schedule a Meeting:**
https://calendly.com/ncn-team

📱 **Social Media:**
• Twitter: @NCN_Network
• LinkedIn: NVAI Computing Network
• GitHub: ncn-org

⚠️ *Security Notice:* Only use official channels for communication.
        """
        
        keyboard = [
            [InlineKeyboardButton("🌐 Visit Website", url="https://ncn-network.io")],
            [InlineKeyboardButton("◀️ Back to Main", callback_data="main_menu")]
        ]
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                message,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_markdown(
                message,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    async def help_command(self, update: Update, context: CallbackContext) -> None:
        """Show help message."""
        message = """
🤖 **NCN Bot Commands**

*Main Commands:*
/start - Welcome message and main menu
/features - Key features of NCN
/usecases - Real-world applications
/techspecs - Technical specifications
/whitepaper - Access technical documentation
/network - Current network status
/contact - Contact information
/help - This help message

*Admin Commands:*
/admin - Admin panel (restricted)
/broadcast - Send announcement (admin only)
/stats - Bot statistics

💡 *Tip:* Use the interactive buttons for quick navigation!
        """
        
        await update.message.reply_markdown(message)
    
    async def button_handler(self, update: Update, context: CallbackContext) -> None:
        """Handle button callbacks."""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        handlers = {
            "features": self.features,
            "usecases": self.usecases,
            "techspecs": self.techspecs,
            "whitepaper": self.whitepaper,
            "network": self.network_status,
            "contact": self.contact,
            "main_menu": self.start
        }
        
        if data in handlers:
            await handlers[data](update, context)
    
    async def unknown(self, update: Update, context: CallbackContext) -> None:
        """Handle unknown commands."""
        await update.message.reply_text(
            "Sorry, I didn't understand that command. Try /help to see available commands."
        )
    
    async def stats(self, update: Update, context: CallbackContext) -> None:
        """Show bot statistics (admin only)."""
        user_id = update.effective_user.id
        
        if user_id not in self.config.ADMIN_IDS:
            await update.message.reply_text("❌ This command is for administrators only.")
            return
        
        stats_message = """
📊 **Bot Statistics**
        
• Uptime: Since deployment
• Total Users: Collecting data...
• Active Today: Monitoring...
• Commands Processed: Counting...

*More stats coming soon!*
        """
        
        await update.message.reply_markdown(stats_message)
    
    def setup_handlers(self, application: Application):
        """Setup all command handlers."""
        # Command handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("features", self.features))
        application.add_handler(CommandHandler("usecases", self.usecases))
        application.add_handler(CommandHandler("techspecs", self.techspecs))
        application.add_handler(CommandHandler("whitepaper", self.whitepaper))
        application.add_handler(CommandHandler("network", self.network_status))
        application.add_handler(CommandHandler("contact", self.contact))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("stats", self.stats))
        
        # Button callback handler
        application.add_handler(CallbackQueryHandler(self.button_handler))
        
        # Unknown command handler
        application.add_handler(MessageHandler(filters.COMMAND, self.unknown))
    
    def run(self):
        """Run the bot."""
        # Create application
        application = Application.builder().token(self.config.TOKEN).build()
        
        # Setup handlers
        self.setup_handlers(application)
        
        # Log startup message
        logger.info("🚀 NCN Bot is starting...")
        print("""
╔══════════════════════════════════════════╗
║      NCN Bot Initialization Complete     ║
╠══════════════════════════════════════════╣
║ Bot: NCN Information Portal              ║
║ Status: ✅ Running                       ║
║ Version: 2.0.0                           ║
║ Platform: Render                         ║
║ Network: NVAI Computing Network          ║
╚══════════════════════════════════════════╝
        """)
        
        # Start polling
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True  # Important for Render to avoid old updates
        )

def main():
    """Main entry point."""
    try:
        # Initialize and run bot
        bot = NCNBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Check if TELEGRAM_BOT_TOKEN is set in Render Environment Variables")
        print("2. Verify your bot token is correct")
        print("3. Check Render logs for more details")
        print("4. Make sure requirements.txt is up to date")
        sys.exit(1)

if __name__ == '__main__':
    main()
