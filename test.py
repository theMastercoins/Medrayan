from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update

# Replace 'YOUR_TOKEN_HERE' with your actual bot token
TOKEN = '7514128984:AAFzpRzhjpFxLpj4E70QlBdPF7HGRfFhlww'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    username = user.username if user.username else user.first_name

    # Create the buttons
    keyboard = [
        [InlineKeyboardButton("Let's See", url='https://t.me/realmastercoin_bot/mastercoin')],
        [InlineKeyboardButton("Join Community", url='https://t.me/TheMasterCoinOfficial')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the photo with caption and buttons
    await context.bot.send_photo(
        chat_id=update.message.chat_id,
        photo=open('masterlion.png', 'rb'),  # Ensure 'masterlion.png' is in the same directory as this script
        caption=f"Hi {username}!\n\nYour Telegram Profile Decide Your Rewards!\nAre You Ready To See How Much You Can Earn Join Now.",
        reply_markup=reply_markup
    )

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler('start', start))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
