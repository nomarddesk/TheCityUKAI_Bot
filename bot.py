from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola",
    # ... (all your countries here)
    "Zambia", "Zimbabwe"
]

ITEMS_PER_PAGE = 20

async def start(update: Update, context: CallbackContext) -> None:
    """Send a paginated list of countries."""
    keyboard = [
        [InlineKeyboardButton("View Countries 🇺🇳", callback_data='page_0')],
        [InlineKeyboardButton("Count Countries 📊", callback_data='count')],
        [InlineKeyboardButton("Search 🔍", switch_inline_query_current_chat="")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to the Countries Bot! 🌍\n\n"
        "Click below to explore countries:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: CallbackContext) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == 'count':
        await query.edit_message_text(
            f"🌍 Total countries in the world: {len(COUNTRIES)}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("◀️ Back", callback_data='page_0')]
            ])
        )
    
    elif data.startswith('page_'):
        page = int(data.split('_')[1])
        start_idx = page * ITEMS_PER_PAGE
        end_idx = start_idx + ITEMS_PER_PAGE
        
        countries_page = COUNTRIES[start_idx:end_idx]
        
        message = f"🌍 Countries (Page {page + 1}/{(len(COUNTRIES) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE})\n\n"
        for i, country in enumerate(countries_page, start=start_idx + 1):
            message += f"{i}. {country}\n"
        
        # Create pagination buttons
        buttons = []
        if page > 0:
            buttons.append(InlineKeyboardButton("◀️ Previous", callback_data=f'page_{page-1}'))
        if end_idx < len(COUNTRIES):
            buttons.append(InlineKeyboardButton("Next ▶️", callback_data=f'page_{page+1}'))
        
        keyboard = [buttons] if buttons else []
        keyboard.append([InlineKeyboardButton("Back to Menu", callback_data='menu')])
        
        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif data == 'menu':
        keyboard = [
            [InlineKeyboardButton("View Countries 🇺🇳", callback_data='page_0')],
            [InlineKeyboardButton("Count Countries 📊", callback_data='count')]
        ]
        await query.edit_message_text(
            "Main Menu 🌍",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def main() -> None:
    TOKEN = "YOUR_BOT_TOKEN_HERE"
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
