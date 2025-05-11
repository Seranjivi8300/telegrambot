from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import os

# Set your Telegram Bot Token
TELEGRAM_TOKEN = '7445895634:AAG_t8jB_qnAft88E2PZX4BxYXm9AZZsPWQ'

# Helper function to download the file
def download_file_from_url(url, dest_folder='downloads'):
    os.makedirs(dest_folder, exist_ok=True)
    local_filename = url.split('/')[-1].split('?')[0]

    local_path = os.path.join(dest_folder, local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_path

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me a URL and I’ll upload the file to Telegram.")

# Message handler for URLs
async def handle_message(update: Update, context:
 ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("Please send a valid URL.")
        return

    try:
        await update.message.reply_text("Downloading file...")
        file_path = download_file_from_url(url)
        await update.message.reply_document(document=open(file_path, 'rb'))
        os.remove(file_path)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Main function
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    await app.run_polling()

# Run the bot
if _name_ == '_main_':
    import asyncio
    asyncio.run(main())
