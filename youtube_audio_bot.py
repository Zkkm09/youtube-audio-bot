"""
Telegram Bot for YouTube Audio Downloads
Allows users to send YouTube links and receive audio files
Production-ready version with enhanced logging and error handling
"""

import os
import logging
from datetime import datetime
import telebot
from pytubefix import YouTube
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DOWNLOAD_DIR = "downloads"
LOG_DIR = "logs"

# Create necessary directories
for directory in [DOWNLOAD_DIR, LOG_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Configure logging
log_file = os.path.join(LOG_DIR, 'youtube_audio_bot.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Send a message when the command /start is issued."""
    user = message.from_user.first_name
    bot.reply_to(
        message,
        f"👋 Hi {user}!\n\n"
        "🎵 I'm a YouTube Audio Downloader Bot.\n\n"
        "📝 Just send me a YouTube link and I'll download the audio for you!\n\n"
        "Commands:\n"
        "/start - Show this message\n"
        "/help - Show help"
    )


@bot.message_handler(commands=['help'])
def send_help(message):
    """Send a message when the command /help is issued."""
    bot.reply_to(
        message,
        "📚 How to use:\n\n"
        "1. Send me any YouTube video link\n"
        "2. Wait while I download the audio\n"
        "3. Receive your audio file!\n\n"
        "Example:\n"
        "https://youtube.com/watch?v=...\n"
        "https://youtu.be/...\n\n"
        "⚠️ Note: Large files may take longer to process."
    )


@bot.message_handler(func=lambda message: True)
def download_youtube_audio(message):
    """Download audio from YouTube link sent by user."""
    url = message.text.strip()
    
    # Check if message contains a YouTube link
    if not ('youtube.com' in url or 'youtu.be' in url):
        bot.reply_to(
            message,
            "❌ This doesn't look like a YouTube link.\n"
            "Please send a valid YouTube URL."
        )
        return
    
    # Send initial status message
    status_msg = bot.reply_to(message, "📥 Processing your request...")
    
    try:
        # Fetch video information
        bot.edit_message_text(
            "🔍 Fetching video information...",
            chat_id=status_msg.chat.id,
            message_id=status_msg.message_id
        )
        
        # Try WEB client with automatic PO Token (requires nodejs)
        yt = YouTube(url, 'WEB')
        
        title = yt.title
        author = yt.author
        duration = yt.length
        
        bot.edit_message_text(
            f"📺 Video: {title}\n"
            f"👤 Author: {author}\n"
            f"⏱ Duration: {duration // 60}:{duration % 60:02d}\n\n"
            f"⬇️ Downloading audio...",
            chat_id=status_msg.chat.id,
            message_id=status_msg.message_id
        )
        
        # Get audio stream (itag=140: 128kbps mp4)
        audio_stream = yt.streams.get_by_itag(140)
        
        if not audio_stream:
            # Fallback to best audio
            audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        # Download audio
        audio_file = audio_stream.download(output_path=DOWNLOAD_DIR)
        file_size = os.path.getsize(audio_file) / (1024 * 1024)  # Convert to MB
        
        bot.edit_message_text(
            f"📺 {title}\n"
            f"📦 Size: {file_size:.2f} MB\n\n"
            f"📤 Uploading to Telegram...",
            chat_id=status_msg.chat.id,
            message_id=status_msg.message_id
        )
        
        # Send audio file to user
        with open(audio_file, 'rb') as audio:
            bot.send_audio(
                chat_id=message.chat.id,
                audio=audio,
                title=title,
                performer=author
            )
        
        # Delete status message and local file
        bot.delete_message(chat_id=status_msg.chat.id, message_id=status_msg.message_id)
        os.remove(audio_file)
        
        logger.info(f"Successfully sent audio: {title} to user {message.from_user.id}")
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error processing request: {error_msg}")
        
        try:
            bot.edit_message_text(
                f"❌ Error occurred:\n{error_msg}\n\n"
                "Please try again or send a different link.",
                chat_id=status_msg.chat.id,
                message_id=status_msg.message_id
            )
        except:
            bot.reply_to(
                message,
                f"❌ Error occurred:\n{error_msg}\n\n"
                "Please try again or send a different link."
            )
        
        # Clean up file if it exists
        try:
            if 'audio_file' in locals() and os.path.exists(audio_file):
                os.remove(audio_file)
        except:
            pass


def main():
    """Start the bot."""
    
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in .env file!")
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file!")
        return
    
    logger.info("="*60)
    logger.info("YouTube Audio Downloader Bot - Starting")
    logger.info("="*60)
    logger.info(f"Download directory: {DOWNLOAD_DIR}")
    logger.info(f"Log directory: {LOG_DIR}")
    
    print("🤖 YouTube Audio Downloader Bot")
    print("✅ Bot is running! Press Ctrl+C to stop.")
    
    try:
        # Start polling
        logger.info("Starting bot polling...")
        bot.infinity_polling()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print("\n👋 Bot stopped")
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)
        print(f"❌ Bot crashed: {e}")
        raise


if __name__ == '__main__':
    main()
