import mysql.connector
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Replace 'YOUR_TOKEN_HERE' with your actual bot token
TOKEN = '7514128984:AAFzpRzhjpFxLpj4E70QlBdPF7HGRfFhlww'

# Database configuration
DB_CONFIG = {
    'host': 'srv1509.hstgr.io',
    'user': 'u149555815_nextcoin',
    'password': 'Nextcoin2024',
    'database': 'u149555815_nextcoin'
}

def generate_balance(is_premium):
    if is_premium:
        return random.randint(8300, 12450)
    else:
        return random.randint(3500, 7200)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    username = user.username if user.username else user.first_name
    user_id = user.id

    # Connect to the database
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()

    try:
        # Check if user exists by user_id or username
        cursor.execute("SELECT * FROM users WHERE user_id = %s OR username = %s", (user_id, username))
        result = cursor.fetchone()

        if result is None:
            # Determine if the user is premium
            is_premium = 1 if user.is_premium else 0

            # Generate balance based on premium status
            balance = generate_balance(is_premium)

            # Insert the new user into the database
            cursor.execute("INSERT INTO users (username, user_id, balance, haspremium, referral_link) VALUES (%s, %s, %s, %s, %s)",
                           (username, user_id, balance, is_premium, ''))
            db.commit()

            # New user registration message
            welcome_message = f"Welcome, {username}! You have successfully registered."
        else:
            # User already exists, log them in
            welcome_message = f"Welcome back, {username}!"

        # Check if the user was referred by someone
        if context.args and result is None:  # Only process referral if it's a new registration
            inviter_id = int(context.args[0])
            inviter_username = (await context.bot.get_chat(inviter_id)).username

            # Update the referral count and balance for the inviter
            cursor.execute("UPDATE users SET referrals_count = referrals_count + 1 WHERE user_id = %s", (inviter_id,))
            cursor.execute("UPDATE users SET balance = balance + 1200 WHERE user_id = %s", (inviter_id,))
            
            # Update the balance for the newly invited user
            cursor.execute("UPDATE users SET balance = balance + 1200 WHERE user_id = %s", (user_id,))
            
            db.commit()

            # Notify the inviter
            await context.bot.send_message(
                chat_id=inviter_id,
                text="You Have A New Referral! You've earned 1200 $MASTER."
            )

            # Notify the invited user
            await update.message.reply_text(
                f"You Have Been Referred By {inviter_username}! You've earned 1200 $MASTER."
            )

        # Create the buttons
        keyboard = [
            [InlineKeyboardButton("Let's See", url='https://t.me/realmastercoin_bot/mastercoin')],
            [InlineKeyboardButton("Join Community", url='https://t.me/TheMasterCoinOfficial')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send the welcome message and buttons
        await update.message.reply_text(welcome_message)
        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=open('masterlion.png', 'rb'),  # Ensure 'masterlion.png' is in the same directory as this script
            caption=f"Hi {username}!\n\nYour Telegram Profile Decides Your Rewards!\nAre You Ready To See How Much You Can Earn Join Now.",
            reply_markup=reply_markup
        )
    except mysql.connector.Error as err:
        # Log or handle database errors
        print(f"Database error: {err}")
        await update.message.reply_text("An error occurred while processing your request.")
    finally:
        cursor.close()
        db.close()

async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    username = user.username if user.username else user.first_name
    user_id = user.id

    # Generate referral link
    referral_link = f"https://t.me/realmastercoin_bot?start={user_id}"

    # Connect to the database
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()

    try:
        # Get the total referrals count
        cursor.execute("SELECT referrals_count FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        referrals_count = result[0] if result else 0

        # Message with referral information
        referral_message = (
            f"Welcome To The Referral Master!\n"
            f"Below Your Referral Infos 👇\n\n"
            f"Total Referrals: {referrals_count}\n"
            f"Referral Link: {referral_link}\n\n"
            f"Share Your Referral Link And Earn 1200 $MASTER For Every Friend You Invite!"
        )
        # Send the referral message
        await update.message.reply_text(referral_message)
    except mysql.connector.Error as err:
        # Log or handle database errors
        print(f"Database error: {err}")
        await update.message.reply_text("An error occurred while fetching your referral information.")
    finally:
        cursor.close()
        db.close()

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('refer', refer))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
